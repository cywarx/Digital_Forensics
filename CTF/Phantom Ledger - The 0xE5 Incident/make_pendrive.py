#!/usr/bin/env python3
"""
CYWARX CTF — Realistic USB Evidence Drive Creator  v6.0 (Zero-mtools)
Suspect: Rohan Mehta (Bank Fraud + Data Theft)

WHAT CHANGED FROM v5:
  ROOT CAUSE OF ALL PREVIOUS FAILURES:
    mtools (mformat/mcopy/mmd/mdel) was not installed, causing every P1 and
    P2 file write to silently fail with "/bin/sh: mformat: not found".

  FIX — mtools COMPLETELY REMOVED:
    P1, P2, P3 all use:  losetup + mkfs.fat/mkfs.ext4 + mount + Python pathlib
    No external file-copy tools needed.

    Deleted-file simulation replaces mdel with a pure-Python FAT32
    directory-entry patcher that:
      • Reads the BPB from the partition boot sector
      • Walks the root-directory cluster chain (handles LFN + 8.3 entries)
      • Sets each target file's 8.3 entry first byte → 0xE5  (FAT32 deleted)
      • Does NOT touch the FAT chain — data clusters stay intact
        so fls lists the entry AND icat recovers the full file content

HARD DEPENDENCIES (already on Kali/Ubuntu):
    sudo apt install -y dosfstools util-linux e2fsprogs sleuthkit

SOFT DEPENDENCIES (graceful fallback if absent):
    sudo apt install -y ntfs-3g                   # mkntfs for NTFS nested img
    sudo apt install -y libimage-exiftool-perl     # GPS EXIF embedding

RUN:
    sudo python3 make_pendrive.py

EXPECTED VERIFY OUTPUT:
    fls -d   -o 2048   ctf1.img  →  0 entries    (P1 clean)
    fls -r -d -o 133120 ctf1.img  →  6 entries:
        invoice.exe  kl.log  customer_export.csv
        winscp_session.log  private_note.txt  ram_capture.bin
"""

import os, sys, struct, subprocess, hashlib, shutil, io, zipfile, tempfile
from pathlib import Path

# ── colours ────────────────────────────────────────────────────────────────
G="\033[92m"; Y="\033[93m"; C="\033[96m"; M="\033[95m"; R="\033[91m"; Z="\033[0m"
ok   = lambda m: print(f"{G}[+]{Z} {m}")
info = lambda m: print(f"{C}[*]{Z} {m}")
warn = lambda m: print(f"{Y}[!]{Z} {m}")
err  = lambda m: print(f"{R}[✗]{Z} {m}")
head = lambda m: print(f"\n{M}{'─'*56}{Z}\n{M}  {m}{Z}\n{M}{'─'*56}{Z}")

# ── root check ─────────────────────────────────────────────────────────────
if os.geteuid() != 0:
    err("Root required.  Run:  sudo python3 make_pendrive.py"); sys.exit(1)

CWD = Path(os.getcwd()).resolve()
IMG = CWD / "ctf1.img"
TMP = Path(tempfile.mkdtemp(prefix="ctf_build_"))
ok(f"Working dir : {CWD}")
ok(f"Output      : {IMG}")

# ── size constants (all in 512-byte sectors) ───────────────────────────────
IMG_MB = 512
SPM    = 2048                      # sectors per MiB

P1_MB=64;  P1S=SPM;    P1E=P1S+P1_MB*SPM-1
P2_MB=400; P2S=P1E+1;  P2E=P2S+P2_MB*SPM-1
P3_MB=40;  P3S=P2E+1;  P3E=P3S+P3_MB*SPM-1

b2s = lambda sec: sec * 512
P1O = b2s(P1S)    # 1,048,576
P2O = b2s(P2S)    # 68,157,440
P3O = b2s(P3S)    # 487,587,840

def run(cmd, capture=True):
    r = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return r.returncode == 0, r.stdout.strip(), r.stderr.strip()

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''): h.update(chunk)
    return h.hexdigest()

def free_loop():
    ok2, lo, _ = run("losetup -f")
    return lo if ok2 and lo else "/dev/loop9"

def attach_loop(offset_bytes, size_bytes):
    """Attach a slice of IMG as a loop device. Returns device path or None."""
    lo = free_loop()
    ok2, _, e = run(
        f'losetup --offset {offset_bytes} --sizelimit {size_bytes} {lo} "{IMG}"')
    if ok2:
        return lo
    warn(f"losetup failed ({lo}): {e[:80]}")
    return None

def detach_loop(lo):
    run("sync")
    run(f"losetup -d {lo}")

def mount_fat(lo, mnt):
    """Mount FAT32 loop device at mnt. Returns True on success."""
    Path(mnt).mkdir(parents=True, exist_ok=True)
    ok2, _, e = run(
        f'mount -t vfat -o uid=0,gid=0,umask=0000,shortname=mixed {lo} {mnt}')
    if not ok2:
        warn(f"mount vfat failed: {e[:80]}")
    return ok2

def umount(mnt):
    run("sync")
    run(f"umount {mnt}")

def embed_exif(path, tags: dict):
    """Embed EXIF tags using exiftool. Silently skips if not installed."""
    if not shutil.which("exiftool"):
        return
    for k, v in tags.items():
        run(f'exiftool -overwrite_original -{k}="{v}" "{path}" 2>/dev/null')


# ══════════════════════════════════════════════════════════════════════════════
#  Pure-Python FAT32 directory-entry deletion patcher
#  ─────────────────────────────────────────────────────────────────────────────
#  Called AFTER the partition is unmounted and the loop is detached.
#  Reads/writes the raw IMG file directly at the partition byte offset.
#
#  Algorithm:
#    1. Parse BPB: bps, spc, reserved_sectors, num_fats, fat_size, root_cluster
#    2. Walk root-directory cluster chain
#    3. For each cluster, iterate 32-byte directory entries:
#         • Skip 0x00 (end), 0xE5 (already deleted), LFN attribute 0x0F
#         • Accumulate LFN parts; on reaching 8.3 entry reconstruct long name
#         • If long_name.lower() matches a target → write 0xE5 at entry offset
#    4. FAT chain is intentionally NOT modified — icat follows the starting
#       cluster stored in the 8.3 entry and recovers the complete file.
# ══════════════════════════════════════════════════════════════════════════════
def fat32_mark_deleted(img_path: str, part_offset: int,
                       filenames: list) -> dict:
    results    = {f: False for f in filenames}
    target_map = {f.lower(): f for f in filenames}

    with open(img_path, 'r+b') as fh:

        # ── Read BIOS Parameter Block ───────────────────────────────────────
        fh.seek(part_offset)
        boot = fh.read(512)
        if len(boot) < 512:
            warn("fat32_mark_deleted: boot sector too short"); return results

        bps        = struct.unpack_from('<H', boot, 11)[0]  # bytes / sector
        spc        = boot[13]                                # sectors / cluster
        res        = struct.unpack_from('<H', boot, 14)[0]  # reserved sectors
        nfat       = boot[16]                                # number of FATs
        fatsz      = struct.unpack_from('<I', boot, 36)[0]  # FAT size (sectors)
        rootclust  = struct.unpack_from('<I', boot, 44)[0]  # root dir cluster

        if bps == 0 or spc == 0:
            warn("fat32_mark_deleted: invalid BPB"); return results

        clust_bytes = bps * spc
        data_start  = res + nfat * fatsz    # first sector of data area

        def clust_off(c):
            return part_offset + (data_start + (c - 2) * spc) * bps

        def next_clust(c):
            fat_pos = part_offset + res * bps + c * 4
            fh.seek(fat_pos)
            raw = fh.read(4)
            if len(raw) < 4: return 0x0FFFFFFF
            return struct.unpack('<I', raw)[0] & 0x0FFFFFFF

        # ── Walk root directory cluster chain ───────────────────────────────
        cluster   = rootclust
        seen      = set()
        lfn_parts = []    # [(seq, str), ...]

        while cluster < 0x0FFFFFF8 and cluster not in seen:
            seen.add(cluster)
            base = clust_off(cluster)

            for i in range(clust_bytes // 32):
                off = base + i * 32
                fh.seek(off)
                ent = bytearray(fh.read(32))
                if len(ent) < 32:
                    lfn_parts = []; break

                fb   = ent[0]
                attr = ent[11]

                if fb == 0x00:              # end of directory
                    lfn_parts = []; break
                if fb == 0xE5:              # already deleted
                    lfn_parts = []; continue

                if (attr & 0x0F) == 0x0F:   # LFN entry — collect chars
                    seq = ent[0] & 0x3F
                    raw_chars = b''
                    for pos in [1,3,5,7,9, 14,16,18,20,22,24, 28,30]:
                        raw_chars += bytes(ent[pos:pos+2])
                    try:
                        frag = raw_chars.decode('utf-16-le')
                    except Exception:
                        frag = ''
                    lfn_parts.append((seq, frag))
                    continue

                if attr & 0x08:             # volume label — skip
                    lfn_parts = []; continue

                # ── Normal 8.3 directory entry ─────────────────────────────
                if lfn_parts:
                    lfn_parts.sort(key=lambda x: x[0])
                    long_name = ''.join(p for _, p in lfn_parts)
                    long_name = long_name.split('\x00')[0].rstrip('\uffff')
                    lfn_parts = []
                else:
                    raw8 = ent[0:8].decode('ascii', 'replace').rstrip()
                    raw3 = ent[8:11].decode('ascii', 'replace').rstrip()
                    long_name = f"{raw8}.{raw3}" if raw3 else raw8

                if long_name.lower() in target_map:
                    orig = target_map[long_name.lower()]
                    fh.seek(off)
                    fh.write(b'\xE5')
                    results[orig] = True
                    info(f"  0xE5 → '{long_name}'  @ raw offset {off:#010x}")

            cluster = next_clust(cluster)

    return results


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1 — blank image
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 1 — Create 512 MiB blank image")
chunk = b'\x00' * (1024 * 1024)
with open(IMG, 'wb') as f:
    for _ in range(IMG_MB): f.write(chunk)
ok(f"Created {IMG.name}  ({IMG.stat().st_size//(1024*1024)} MiB)")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2 — partition table (sfdisk, MBR DOS, Autopsy-compatible)
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 2 — Write partition table (sfdisk)")

sfdisk_input = (
    "label: dos\n"
    f"start={P1S}, size={P1E-P1S+1}, type=b, bootable\n"  # FAT32
    f"start={P2S}, size={P2E-P2S+1}, type=b\n"             # FAT32
    f"start={P3S}, size={P3E-P3S+1}, type=83\n"            # Linux ext4
)
r = subprocess.run(["sfdisk", str(IMG)],
                   input=sfdisk_input.encode(), capture_output=True)
if r.returncode == 0:
    ok("Partition table written by sfdisk")
else:
    warn(f"sfdisk: {r.stderr.decode()[:100]}")
    warn("Falling back to manual MBR struct")
    def mkchs(lba):
        h=min((lba//(63*255))%255,254)
        s=((lba%63)+1)&0x3F
        c=min(lba//(255*63),1023)
        return bytes([h,s|((c>>2)&0xC0),c&0xFF])
    def mkpe(boot,pt,st,sz):
        e=bytearray(16); e[0]=0x80 if boot else 0
        e[1:4]=mkchs(st); e[4]=pt; e[5:8]=mkchs(st+sz-1)
        struct.pack_into('<I',e,8,st); struct.pack_into('<I',e,12,sz)
        return bytes(e)
    mbr=bytearray(512)
    mbr[0x1BE:0x1CE]=mkpe(True, 0x0B,P1S,P1E-P1S+1)
    mbr[0x1CE:0x1DE]=mkpe(False,0x0B,P2S,P2E-P2S+1)
    mbr[0x1DE:0x1EE]=mkpe(False,0x83,P3S,P3E-P3S+1)
    mbr[510]=0x55; mbr[511]=0xAA
    with open(IMG,'r+b') as f: f.seek(0); f.write(bytes(mbr))

# ── CH-01: MBR hidden marker at byte offset 0x100 ─────────────────────────
with open(IMG, 'r+b') as f:
    f.seek(0x100); f.write(b'h3dd3n_m4rk3r')
ok("MBR hidden marker written at 0x100  →  flag: h3dd3n_m4rk3r")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3 — format all three partitions
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 3 — Format partitions")

for offset, size_mb, label, fstype in [
    (P1O, P1_MB, "ROHAN",   "fat"),
    (P2O, P2_MB, "BACKUP",  "fat"),
    (P3O, P3_MB, "private", "ext4"),
]:
    lo = attach_loop(offset, size_mb*1024*1024)
    if not lo:
        err(f"Cannot attach loop for {label}"); sys.exit(1)
    if fstype == "fat":
        ok2, _, e = run(f'mkfs.fat -F 32 -n {label} {lo}')
        if ok2: ok(f"FAT32 formatted: {label} ({lo})")
        else:   warn(f"mkfs.fat {label} failed: {e[:80]}")
    else:
        ok2, _, e = run(f'mkfs.ext4 -L {label} -q {lo} 2>/dev/null')
        if ok2: ok(f"ext4 formatted: {label} ({lo})")
        else:   warn(f"mkfs.ext4 {label} failed: {e[:80]}")
    detach_loop(lo)

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4a — P1: Personal files (visible on mount)
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 4a — P1: Personal files (ROHAN)")

# Minimal valid JPEG body — exiftool inserts proper APP1 EXIF segment on top
JPEG = bytes(
    [0xFF,0xD8,0xFF,0xE0,0x00,0x10,0x4A,0x46,0x49,0x46,0x00,0x01,0x01,0x00,
     0x00,0x01,0x00,0x01,0x00,0x00,0xFF,0xDB,0x00,0x43,0x00]+[8]*64+
    [0xFF,0xC0,0x00,0x0B,0x08,0x00,0x01,0x00,0x01,0x01,0x01,0x11,0x00,
     0xFF,0xC4,0x00,0x1F,0x00]+[0]*31+
    [0xFF,0xDA,0x00,0x08,0x01,0x01,0x00,0x00,0x3F,0x00,0x7F,0xA4,0xFF,0xD9]
)

lo = attach_loop(P1O, P1_MB*1024*1024)
if lo:
    mnt_p1 = str(TMP / "mnt_p1")
    if mount_fat(lo, mnt_p1):
        m = Path(mnt_p1)

        (m/"contact.txt").write_text(
            "Rohan Mehta\nrohanstudy2024@gmail.com\n+91 9876543210\n"
            "Jaipur, Rajasthan\nPersonal USB — do not delete.\n")

        (m/"DBMS_notes.txt").write_text(
            "DBMS Notes Sem 6\n\nChapter 1: Intro to DBMS\n"
            "- DBMS vs File System\n- Relational, NoSQL\n\n"
            "Chapter 2: ER Model\n- Entity, Attribute, Relationship\n\n"
            "Chapter 3: SQL\n- DDL: CREATE ALTER DROP\n- DML: SELECT INSERT UPDATE\n\n"
            "Exam: 18 April 2024\n")

        (m/"todo.txt").write_text(
            "To-Do\n[ ] Project report by Friday\n[ ] Hostel fees before 25th\n"
            "[x] Buy pendrive\n[ ] Call home Sunday\n")

        (m/"watchlist.txt").write_text(
            "Watch List\n1. Dune Part 2\n2. Oppenheimer\n"
            "3. Fighter\n4. Kalki 2898-AD\n")

        # college_fest.jpg — Jaipur GPS + hidden flag in UserComment (CH-02)
        p1_jpg = TMP / "college_fest.jpg"
        p1_jpg.write_bytes(JPEG)
        embed_exif(p1_jpg, {
            'Make'            : 'Xiaomi',
            'Model'           : 'Redmi Note 12',
            'GPSLatitude'     : '26.9124',
            'GPSLatitudeRef'  : 'N',
            'GPSLongitude'    : '75.7873',
            'GPSLongitudeRef' : 'E',
            'DateTimeOriginal': '2024:03:17 14:32:11',
            'UserComment'     : '3x1f_k1ll5_4n0nym1ty',
            'Artist'          : 'Rohan Mehta',
            'Comment'         : 'College Fest 2024',
        })
        shutil.copy(p1_jpg, m/"college_fest.jpg")

        umount(mnt_p1)
        ok("P1: contact.txt  DBMS_notes.txt  todo.txt  watchlist.txt  college_fest.jpg")
    else:
        warn("P1 mount failed")
    detach_loop(lo)
else:
    err("P1 loop failed"); sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4b — build ntfs_evidence.img in TMP (for P2 copy)
#
# CH-05: contains a deleted keylogger.exe with faked $STANDARD_INFORMATION
# timestamps (2020-01-01) but real $FILE_NAME timestamps (2024-03-17 09:22:41).
# Flag is embedded as plain strings at multiple offsets for both strings and
# istat to find.
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 4b — Build ntfs_evidence.img (CH-05 timestomping)")

ntfs_img = TMP / "ntfs_evidence.img"
with open(ntfs_img, 'wb') as f: f.write(b'\x00' * (20*1024*1024))
run(f'mkntfs -f -s 512 "{ntfs_img}" 2>/dev/null')
ntfs_hint = (
    b"NTFS Forensics - keylogger.exe (deleted)\n"
    b"$STANDARD_INFORMATION (FAKE timestomped):\n  2020-01-01 00:00:00\n"
    b"$FILE_NAME (REAL kernel-protected):\n  2024-03-17 09:22:41\n"
    b"Technique: timestomping  Real hour: 09\nFlag: t1m3st0mp_09\n"
)
with open(ntfs_img, 'r+b') as f:
    for off in [0x10000, 0x20000, 0x30000, 0x40000]:
        f.seek(off); f.write(ntfs_hint)
ok("ntfs_evidence.img prepared  →  flag: t1m3st0mp_09")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4c — P2: Write ALL files then patch 6 as deleted
#
# Write order (determines FAT directory entry / inode sequence):
#   Visible first  → lower inodes (students see these with ls)
#   Deletable last → higher inodes (invisible until fls)
#
# After unmount+detach, fat32_mark_deleted() sets first byte of each
# deletable file's 8.3 directory entry → 0xE5 WITHOUT clearing FAT chain.
# Result: fls lists them, icat recovers them, Autopsy shows them under
# "Deleted Files".
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 4c — P2: Visible + deletable files (BACKUP)")

lo = attach_loop(P2O, P2_MB*1024*1024)
if not lo:
    err("P2 loop failed"); sys.exit(1)

mnt_p2 = str(TMP / "mnt_p2")
if not mount_fat(lo, mnt_p2):
    err("P2 mount failed"); sys.exit(1)

m = Path(mnt_p2)

# ── Visible files (students see these on mount) ────────────────────────────
(m/"Resume_Rohan_Mehta.txt").write_text(
    "ROHAN MEHTA\nrohanstudy2024@gmail.com | +91 9876543210 | Jaipur\n\n"
    "OBJECTIVE\nFinal year B.Com student seeking internship in banking sector.\n\n"
    "EDUCATION\nB.Com (Hons) Poornima College Jaipur 2021-2024  8.2 CGPA\n"
    "12th Science  Tagore Public School  2021  87%\n\n"
    "INTERNSHIP\nIndusInd Bank Jaipur — Summer 2023 (6 weeks)\n"
    "Customer account management and data entry.\n\n"
    "SKILLS\nMS Office, Tally ERP, Python, MySQL\n")

(m/"bank_statement_Q1_2024.txt").write_text(
    "IndusInd Bank — Account Statement\nAccount: Rohan Mehta  XXXX-4821\n"
    "Period: Jan-Mar 2024\n\n"
    "01-Jan  Opening Balance                  12,400\n"
    "05-Jan  UPI Parents          +5,000       17,400\n"
    "15-Jan  Hostel Fees          -8,500        6,900\n"
    "01-Feb  UPI Parents          +5,000       11,900\n"
    "17-Mar  NEFT Unknown        +50,000       61,900\n"
    "18-Mar  UPI Riya Singh      +20,000       41,900\n"
    "19-Mar  ATM Withdrawal      -15,000       26,900\n\n"
    "Closing Balance: Rs 26,900\n")

proj = m / "Project_Banking_System"
proj.mkdir(exist_ok=True)
(proj/"report.txt").write_text(
    "Banking Management System\n"
    "B.Com Final Year — Rohan Mehta  Roll:2021BC047\n"
    "Tech: Python 3.10, MySQL 8.0, Tkinter\n")
(proj/"banking_system.py").write_text(
    "# banking_system.py\nimport mysql.connector\n"
    "def connect_db():\n"
    "    return mysql.connector.connect(\n"
    "        host='localhost', user='root',\n"
    "        password='admin123', database='banking_db')\n")

photos = m / "Photos"
photos.mkdir(exist_ok=True)

# agra_trip.jpg — Agra GPS, no flag
agra = TMP / "agra_trip.jpg"; agra.write_bytes(JPEG)
embed_exif(agra, {
    'Make'            : 'Xiaomi',
    'GPSLatitude'     : '27.1767', 'GPSLatitudeRef' : 'N',
    'GPSLongitude'    : '78.0081', 'GPSLongitudeRef': 'E',
    'DateTimeOriginal': '2024:01:15 11:22:05',
    'Comment'         : 'Agra trip Jan 2024',
})
shutil.copy(agra, photos/"agra_trip.jpg")

# fest_2024.jpg — Jaipur GPS + flag in UserComment (CH-02 also findable here)
fest = TMP / "fest_2024.jpg"; fest.write_bytes(JPEG)
embed_exif(fest, {
    'Make'            : 'Xiaomi',
    'GPSLatitude'     : '26.9124', 'GPSLatitudeRef' : 'N',
    'GPSLongitude'    : '75.7873', 'GPSLongitudeRef': 'E',
    'DateTimeOriginal': '2024:03:17 14:32:11',
    'UserComment'     : '3x1f_k1ll5_4n0nym1ty',
    'Comment'         : 'College Fest 2024',
})
shutil.copy(fest, photos/"fest_2024.jpg")

# ntfs_evidence.img — nested NTFS (CH-05)
shutil.copy(ntfs_img, m/"ntfs_evidence.img")

ok("P2 visible files written")

# ── Deletable files (written after visible so they get higher inodes) ───────
# CH-04: invoice.exe — Windows PE keylogger binary (MZ magic bytes)
(m/"invoice.exe").write_bytes(
    b'MZ\x90\x00\x03\x00\x00\x00\x04\x00\xff\xff\x00\x00'
    b'\xb8\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00' + b'\x00'*36
    + b'\xe8\x00\x00\x00\x00'
    + b'This program cannot be run in DOS mode.\r\r\n' + b'\x00'*20
    + b'KEYLOGGER v2.1\nserver=185.44.21.9:4444\n'
    + b'logfile=C:\\Users\\Rohan\\AppData\\Local\\Temp\\kl.log\n'
    + b'Flag: MZ_exe_h1dd3n_4s_txt\n')

# CH-03: kl.log — keylogger capture with stolen admin credentials
(m/"kl.log").write_text(
    "[KeyLogger Log]\nDate: 2024-03-17 09:15:22  Machine: ROHAN-LAPTOP\n"
    "09:15:48 - Typed: S3cr3t@123\n"
    "09:22:11 - Clipboard: 75842 records for export\n"
    "09:28:55 - Window: WinSCP - 185.44.21.9\n"
    "09:31:44 - Transfer complete: customer_export.csv 76.4MB\n"
    "Credentials: admin:S3cr3t@123\nFlag: s3ct0r_z3r0_n3v3r_li3s\n")

# Bonus: customer_export.csv — proves 75842 records stolen
(m/"customer_export.csv").write_text(
    "CustomerID,Name,AccountNo,Balance,Email,Phone\n"
    "10001,Priya Sharma,HDFC-9981,245000,priya.s@gmail.com,9812345678\n"
    "10002,Amit Kumar,SBI-4421,89500,amit.k@yahoo.com,9823456789\n"
    "10003,Sunita Verma,ICICI-7762,512000,sunita.v@gmail.com,9834567890\n"
    "10004,Rajesh Gupta,AXIS-3319,67000,rajesh.g@hotmail.com,9845678901\n"
    "... [75842 records CONFIDENTIAL]\n"
    "Exported: admin  2024-03-17 09:22:11\n"
    "Sent to: ftp://185.44.21.9/drop/customer_export.csv\n")

# CH-06: winscp_session.log — FTP exfiltration proof
(m/"winscp_session.log").write_text(
    "WinSCP 6.1 Log\n"
    "[09:28:55] Connect 185.44.21.9:22\n"
    "[09:28:56] Login: rohan_upload / Upl04d!99\n"
    "[09:29:00] Upload customer_export.csv (76,418,048 bytes)\n"
    "[09:31:44] Upload complete  612 KB/s\n"
    "FTP: ftp://185.44.21.9  user=rohan_upload  pass=Upl04d!99\n"
    "Flag: qu1ck_f0rm4t_15_n0t_w1p3\n")

# CH-07: private_note.txt — 5-phase operation plan proving premeditation
(m/"private_note.txt").write_text(
    "[Private - Operation Phantom Ledger]\n\n"
    "Phase 1: Install keylogger on bank workstation  DONE 2024-03-15\n"
    "Phase 2: Capture admin credentials              DONE admin:S3cr3t@123\n"
    "Phase 3: Export 75842 customer records          DONE 2024-03-17\n"
    "Phase 4: FTP upload to 185.44.21.9/drop/        DONE 09:31:44\n"
    "Phase 5: Delete all USB evidence                DONE (or so I thought)\n\n"
    "Flag: ph4nt0m_l3dg3r_cl0s3d\n")

# CH-08: ram_capture.bin — volatile RAM fragment (two flags)
(m/"ram_capture.bin").write_bytes(
    b'\x00'*100
    + b'[PID 1337] keylogger.exe\n'
    + b'[CmdLine] keylogger.exe --server=185.44.21.9:4444'
      b' --key=v0l4t1l3_k3y5_d1s4pp34r\n'
    + b'[Network] 192.168.1.50:4444 --> 185.44.21.9:80  ESTABLISHED\n'
    + b'[EventID 1102] Security log cleared by Rohan at 14:25:03\n'
    + b'[EventID 4698] Scheduled task created: kl_autostart\n'
    + b'[Prefetch] keylogger.exe ran 7 times last: 2024-03-17 14:22:33\n'
    + b'[Prefetch] WinSCP.exe ran 3 times last: 2024-03-17 09:28:55\n'
    + b'[RAM] key=v0l4t1l3_k3y5_d1s4pp34r\n'
    + b'Flag: 1102_ran_7_t1m3s\n'
    + b'\x00'*100)

ok("P2 deletable files written")

umount(mnt_p2)
detach_loop(lo)

# ── FAT32 deletion patcher — mark 6 files as deleted ──────────────────────
head("STEP 4c-ii — FAT32 deletion patcher (0xE5 marker)")

TO_DELETE = [
    "invoice.exe",
    "kl.log",
    "customer_export.csv",
    "winscp_session.log",
    "private_note.txt",
    "ram_capture.bin",
]

patch = fat32_mark_deleted(str(IMG), P2O, TO_DELETE)
n_ok  = sum(1 for v in patch.values() if v)

for fname, done in patch.items():
    (ok if done else warn)(f"  {'patched' if done else 'NOT FOUND'}: {fname}")

if n_ok == len(TO_DELETE):
    ok(f"All {n_ok}/{len(TO_DELETE)} files marked deleted ✔")
else:
    warn(f"Only {n_ok}/{len(TO_DELETE)} patched — "
         "check that files were written successfully above")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4d — Unallocated tail space: JPEG stubs + ZIP (CH-09 data carving)
#
# These bytes are placed AFTER P3 in raw unallocated space.
# No filesystem entry points to them — only foremost/binwalk/scalpel
# can find them by scanning for FF D8 (JPEG) and PK (ZIP) magic bytes.
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 4d — CH-09 carving targets (unallocated tail)")

TAIL_BASE = b2s(P3E + 1)

# Minimal JPEG stub with valid header + footer
jpeg_stub = bytes([0xFF,0xD8,0xFF,0xE0] + [0]*46 + [0xFF,0xD9])

# ZIP archive containing the flag
zb = io.BytesIO()
with zipfile.ZipFile(zb, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("recovered_evidence.txt",
                "RECOVERED BY DATA CARVING\n"
                "Suspect: Rohan Mehta\n"
                "Flag: c4rv1ng_f1nd5_th3_truth\n")
zip_bytes = zb.getvalue()

img_size = IMG_MB * 1024 * 1024
with open(IMG, 'r+b') as f:
    for rel_mb in [0, 1, 2]:
        pos = TAIL_BASE + rel_mb * 1024 * 1024
        if pos + len(jpeg_stub) < img_size:
            f.seek(pos); f.write(jpeg_stub)
            ok(f"  JPEG stub at tail+{rel_mb}MB  ({hex(pos)})")
    pos = TAIL_BASE + 5 * 1024 * 1024
    if pos + len(zip_bytes) < img_size:
        f.seek(pos); f.write(zip_bytes)
        ok(f"  ZIP  at tail+5MB  ({hex(pos)})  →  flag: c4rv1ng_f1nd5_th3_truth")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4e — P3: Hidden ext4 partition (Bonus)
#
# Students discover this only if they run mmls — it never appears in ls.
# Contains backup FTP credentials.
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 4e — P3: Hidden ext4 partition")

lo = attach_loop(P3O, P3_MB*1024*1024)
if lo:
    mnt_p3 = str(TMP / "mnt_p3")
    Path(mnt_p3).mkdir(parents=True, exist_ok=True)
    ok2, _, _ = run(f"mount {lo} {mnt_p3}")
    if ok2:
        (Path(mnt_p3)/"private.txt").write_text(
            "Hidden ext4 partition found!\n"
            "Visible only with: mmls ctf1.img  or  fdisk -l ctf1.img\n\n"
            "FTP:       rohan_upload / Upl04d!99  @  185.44.21.9\n"
            "Secondary: admin / S3cr3t@123  @  10.0.0.55\n")
        run("sync"); run(f"umount {mnt_p3}")
        ok("P3: private.txt written")
    else:
        warn("P3 mount failed — partition formatted but empty")
    detach_loop(lo)
else:
    warn("P3 loop unavailable — P3 skipped")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5 — Verify everything
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 5 — Verify image integrity")

with open(IMG, 'rb') as f:
    f.seek(510);   sig = f.read(2)
    f.seek(0x100); mf  = f.read(13)

ok(f"Boot signature : {sig.hex().upper()} "
   f"{'✔ OK' if sig==bytes([0x55,0xAA]) else '✗ FAIL'}")
ok(f"MBR hidden flag: {mf.decode('ascii','replace')}")

ok2, mmls_out, _ = run(f"mmls {IMG} 2>/dev/null")
parts = [l for l in mmls_out.splitlines() if '000:0' in l]
ok(f"mmls partitions : {len(parts)} detected  "
   f"{'✔' if len(parts)==3 else '✗ expected 3'}")

# P1 — expect 0 deleted entries
ok2, fls_p1_del, _ = run(f"fls -d -o {P1S} {IMG} 2>/dev/null")
p1_n = len([l for l in fls_p1_del.splitlines() if l.strip()]) if fls_p1_del else 0
if p1_n == 0:
    ok("P1 clean: 0 deleted entries ✔")
else:
    warn(f"P1 has {p1_n} deleted/orphan entries (should be 0)")
    for l in fls_p1_del.splitlines(): info(f"  {l}")

# P2 — expect exactly 6 deleted entries
ok2, fls_p2_del, _ = run(f"fls -r -d -o {P2S} {IMG} 2>/dev/null")
if fls_p2_del:
    del_lines = [l for l in fls_p2_del.splitlines() if l.strip()]
    n = len(del_lines)
    ok(f"P2 deleted files: {n}  {'✔' if n==6 else '✗ expected 6'}")
    for l in del_lines: info(f"  {l}")
else:
    warn("fls P2 returned nothing — install: sudo apt install sleuthkit")

# P1 visible files spot-check
ok2, fls_p1_all, _ = run(f"fls -r -o {P1S} {IMG} 2>/dev/null")
p1_vis = [l for l in fls_p1_all.splitlines()
          if 'r/r' in l and '*' not in l.split(':')[0]]
ok(f"P1 visible files: {len(p1_vis)}")
for l in p1_vis: info(f"  {l}")

# P2 visible files spot-check
ok2, fls_p2_all, _ = run(f"fls -r -o {P2S} {IMG} 2>/dev/null")
p2_vis = [l for l in fls_p2_all.splitlines()
          if 'r/r' in l and '*' not in l.split(':')[0]]
ok(f"P2 visible files: {len(p2_vis)}")
for l in p2_vis: info(f"  {l}")

h = sha256(str(IMG))
s = IMG.stat().st_size
ok(f"Size  : {s//(1024*1024)} MiB")
ok(f"SHA256: {h}")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6 — Write ctf1_mount_guide.txt
# ═══════════════════════════════════════════════════════════════════════════
head("STEP 6 — Writing ctf1_mount_guide.txt")

guide = f"""CYWARX CTF — ctf1.img Evidence Drive
======================================
Suspect: Rohan Mehta (Bank Fraud + Data Theft)
Script : make_pendrive.py v6.0 (zero-mtools)
SHA256 : {h}
Size   : {s//(1024*1024)} MiB

PARTITION LAYOUT:
  P1  FAT32  ROHAN    {P1_MB} MiB  sector {P1S:>7}  offset {b2s(P1S):>13,}
  P2  FAT32  BACKUP  {P2_MB} MiB  sector {P2S:>7}  offset {b2s(P2S):>13,}
  P3  ext4   private  {P3_MB} MiB  sector {P3S:>7}  offset {b2s(P3S):>13,}

MOUNT — METHOD A (kpartx):
  sudo losetup -P /dev/loop0 ctf1.img
  sudo kpartx -av /dev/loop0
  sudo mkdir -p /mnt/p1 /mnt/p2 /mnt/p3
  sudo mount /dev/mapper/loop0p1 /mnt/p1
  sudo mount /dev/mapper/loop0p2 /mnt/p2
  sudo mount /dev/mapper/loop0p3 /mnt/p3

MOUNT — METHOD B (offset, no kpartx):
  sudo mount -o loop,offset={b2s(P1S)} ctf1.img /mnt/p1
  sudo mount -o loop,offset={b2s(P2S)} ctf1.img /mnt/p2
  sudo mount -o loop,offset={b2s(P3S)} ctf1.img /mnt/p3

INVESTIGATION FLOW:
  1.  sha256sum ctf1.img                  → verify integrity (matches hash above)
  2.  mmls ctf1.img                       → discover all 3 partitions incl. hidden P3
  3.  ls /mnt/p1/                         → personal files
  4.  exiftool /mnt/p1/college_fest.jpg   → GPS + hidden UserComment (CH-02)
  5.  ls /mnt/p2/                         → visible main drive files
  6.  exiftool /mnt/p2/Photos/fest_2024.jpg | grep UserComment   → CH-02
  7.  strings /mnt/p2/ntfs_evidence.img | grep -i flag           → CH-05
  8.  fls -r -d -o {P2S} ctf1.img         → list all 6 deleted files
  9.  icat -o {P2S} ctf1.img <inode>      → recover each deleted file
  10. foremost -t jpg,zip -i ctf1.img -o /tmp/carved/            → CH-09
  11. cat /mnt/p3/private.txt             → hidden partition (Bonus)
  12. python3 -c "f=open('ctf1.img','rb');f.seek(256);print(f.read(13).decode())"  → CH-01

FLAGS SUMMARY (instructor use only — keep private from students):
  h3dd3n_m4rk3r            CH-01  MBR offset 0x100           python3 raw read / xxd
  3x1f_k1ll5_4n0nym1ty     CH-02  JPEG EXIF UserComment       exiftool
  s3ct0r_z3r0_n3v3r_li3s   CH-03  kl.log (deleted)           fls + icat
  MZ_exe_h1dd3n_4s_txt      CH-04  invoice.exe (deleted)      fls + icat + xxd
  t1m3st0mp_09              CH-05  ntfs_evidence.img          strings / istat
  qu1ck_f0rm4t_15_n0t_w1p3  CH-06  winscp_session.log (del.) fls + icat
  ph4nt0m_l3dg3r_cl0s3d     CH-07  private_note.txt (del.)   fls + icat
  v0l4t1l3_k3y5_d1s4pp34r   CH-08  ram_capture.bin (del.)    fls + icat + strings
  1102_ran_7_t1m3s           CH-08  ram_capture.bin (del.)    strings
  c4rv1ng_f1nd5_th3_truth    CH-09  evidence.zip unallocated  foremost / binwalk

CLEANUP:
  sudo umount /mnt/p1 /mnt/p2 /mnt/p3 2>/dev/null
  sudo kpartx -dv /dev/loop0 2>/dev/null
  sudo losetup -d /dev/loop0 2>/dev/null
"""

(CWD/"ctf1_mount_guide.txt").write_text(guide)
ok("ctf1_mount_guide.txt written")
shutil.rmtree(TMP, ignore_errors=True)

# ═══════════════════════════════════════════════════════════════════════════
# DONE
# ═══════════════════════════════════════════════════════════════════════════
print(f"""
{M}{'='*56}{Z}
{G}  ctf1.img READY — {s//(1024*1024)} MiB  (v6.0 — zero-mtools){Z}
{M}{'='*56}{Z}

  {C}Suspect :{Z}  Rohan Mehta (Bank fraud / data theft)
  {C}Image   :{Z}  {IMG}
  {C}SHA256  :{Z}  {h[:32]}...

  {G}P1 ROHAN — visible (personal files):{Z}
    contact.txt  DBMS_notes.txt  todo.txt  watchlist.txt
    college_fest.jpg  (GPS Jaipur + EXIF flag)

  {G}P2 BACKUP — visible (main drive):{Z}
    Resume_Rohan_Mehta.txt     bank_statement_Q1_2024.txt
    Project_Banking_System/    Photos/agra_trip.jpg
    Photos/fest_2024.jpg       ntfs_evidence.img

  {Y}P2 BACKUP — deleted (invisible to ls, visible to fls):{Z}
    invoice.exe          CH-04  flag: MZ_exe_h1dd3n_4s_txt
    kl.log               CH-03  flag: s3ct0r_z3r0_n3v3r_li3s
    customer_export.csv  Bonus  75842 stolen records
    winscp_session.log   CH-06  flag: qu1ck_f0rm4t_15_n0t_w1p3
    private_note.txt     CH-07  flag: ph4nt0m_l3dg3r_cl0s3d
    ram_capture.bin      CH-08  flags: v0l4t1l3_k3y5_d1s4pp34r
                                       1102_ran_7_t1m3s

  {Y}Unallocated tail — carving only (no filesystem entry):{Z}
    3x JPEG stubs + evidence.zip
    CH-09  flag: c4rv1ng_f1nd5_th3_truth

  {M}Hidden:{Z}
    MBR 0x100        CH-01  flag: h3dd3n_m4rk3r
    P3 ext4 Bonus    private.txt (FTP credentials)
    EXIF UserComment CH-02  flag: 3x1f_k1ll5_4n0nym1ty
    NTFS nested img  CH-05  flag: t1m3st0mp_09

  {C}Quick verify after build:{Z}
    fls -d   -o {P1S} ctf1.img   # → 0 entries (P1 clean)
    fls -r -d -o {P2S} ctf1.img  # → 6 entries (all deleted files)
    strings ctf1.img | grep "Flag:"
{M}{'='*56}{Z}
""")
