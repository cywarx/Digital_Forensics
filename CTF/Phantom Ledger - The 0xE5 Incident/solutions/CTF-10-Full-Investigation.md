---
tags: [ctf, solution, unit4, forensics, full-investigation, chain-of-custody, all-flags]
challenge: "10 — Operation Phantom Ledger (Full Investigation)"
flag: "All 10 flags — complete case"
points: All 2025 points
difficulty: Expert
topic: Full Digital Forensics Investigation — Chain of Custody
image: ctf1.img (all partitions)
---

# 🕵️ Challenge 10 — Operation Phantom Ledger

> [!success] All Flags
> ```
> Cywarx{h3dd3n_m4rk3r}            01 — MBR hidden data
> Cywarx{3x1f_k1ll5_4n0nym1ty}     02 — EXIF GPS metadata
> Cywarx{s3ct0r_z3r0_n3v3r_li3s}   03 — Deleted kl.log
> Cywarx{MZ_exe_h1dd3n_4s_txt}      04 — Deleted invoice.exe
> Cywarx{t1m3st0mp_09}              05 — NTFS timestomping
> Cywarx{qu1ck_f0rm4t_15_n0t_w1p3} 06 — Deleted WinSCP log
> Cywarx{ph4nt0m_l3dg3r_cl0s3d}    07 — Deleted private_note.txt
> Cywarx{v0l4t1l3_k3y5_d1s4pp34r}  08 — RAM volatile key
> Cywarx{1102_ran_7_t1m3s}          08 — EventID 1102 + run count
> Cywarx{c4rv1ng_f1nd5_th3_truth}   09 — Data carving ZIP
> ```

> [!info] Real World Case — Combined: Enron + WannaCry + CAID + Twitter Hack
> This challenge simulates a real-world multi-stage forensic investigation combining all Unit IV techniques. Real investigations always involve multiple evidence sources, multiple tools, and strict chain of custody. A single broken step can make all evidence inadmissible.

---

## 📋 Case Briefing

```
CASE:     Operation Phantom Ledger
SUSPECT:  Rohan Mehta, B.Com student, former IndusInd Bank intern
CHARGES:  Data theft (IT Act 2000 s.43), Fraud (IPC 420), Criminal conspiracy (IPC 120B)
EVIDENCE: ctf1.img — USB drive seized from suspect's residence
```

---

## ⚖️ Phase 1 — Evidence Integrity (DO THIS FIRST)

> [!danger] Golden Rule
> **Never analyse original evidence.** Always verify hash first, then work on a verified copy. A modified hash = inadmissible evidence = case dismissed.

```bash
# Step 1: Compute and record hash of original image
sha256sum ctf1.img | tee case_evidence_hash.txt
```

**Output:**
```
[hash]  ctf1.img
```

```bash
# Step 2: Record in case notes
echo "Evidence received: $(date)" >> case_notes.txt
echo "SHA256: $(sha256sum ctf1.img | cut -d' ' -f1)" >> case_notes.txt
echo "Investigator: $(whoami)" >> case_notes.txt
echo "Workstation: $(hostname)" >> case_notes.txt
```

```bash
# Step 3: Work on a copy
cp ctf1.img ctf1_working_copy.img
# Or use write-blocked mount (read-only)
```

---

## 🗺️ Phase 2 — Partition Mapping

```bash
# See all partitions including hidden
mmls ctf1.img
```

**Output:**
```
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

     Slot    Start       End         Size        Description
000: Meta    0000000000  0000000000  0000000001  Primary Table (#0)
001: -----   0000000001  0000002047  0000002047  Unallocated
002: 000:000 0000002048  0000133119  0000131072  Win95 FAT32 (0x0B)
003: 000:001 0000133120  0000952319  0000819200  Win95 FAT32 (0x0B)
004: 000:002 0000952320  0001034239  0000081920  Linux (0x83)
005: -----   0001034240  0001048575  0000014336  Unallocated  ← TAIL SPACE
```

> [!important] What this reveals
> - P1 (offset 2048):   FAT32 personal files
> - P2 (offset 133120): FAT32 main drive
> - P3 (offset 952320): **Hidden ext4 partition** ← student must find this
> - Tail (offset 1034240): **Unallocated space** ← carving targets are here

---

## 🔍 Phase 3 — MBR Analysis (Flag 01)

```bash
python3 -c "
f = open('ctf1.img','rb')
f.seek(256)
print('Flag:', f.read(13).decode())
f.seek(510)
print('Boot sig:', f.read(2).hex())
"
```

**Output:**
```
Flag: h3dd3n_m4rk3r
Boot sig: 55aa
```

> [!success] `Cywarx{h3dd3n_m4rk3r}`

---

## 📁 Phase 4 — P1 Personal Files

```bash
# Mount P1
sudo losetup -P /dev/loop0 ctf1.img
sudo kpartx -av /dev/loop0
sudo mkdir -p /mnt/p1
sudo mount /dev/mapper/loop0p1 /mnt/p1
ls /mnt/p1/
```

**Output:**
```
contact.txt  DBMS_notes.txt  todo.txt  watchlist.txt  college_fest.jpg
```

```bash
# Check photos for EXIF
exiftool /mnt/p1/college_fest.jpg | grep -i "gps\|comment\|date"
```

**Output:**
```
GPS Latitude      : 26 deg 54' 44.64" N
GPS Longitude     : 75 deg 47' 14.28" E
Date/Time Original: 2024:03:17 14:32:11
User Comment      : 3x1f_k1ll5_4n0nym1ty  ← FLAG
```

> [!success] `Cywarx{3x1f_k1ll5_4n0nym1ty}`

---

## 📁 Phase 5 — P2 Visible Files

```bash
sudo mkdir -p /mnt/p2
sudo mount /dev/mapper/loop0p2 /mnt/p2
ls -la /mnt/p2/
ls -la /mnt/p2/Photos/
```

**Visible files:**
```
Resume_Rohan_Mehta.txt
bank_statement_Q1_2024.txt
Project_Banking_System/
Photos/agra_trip.jpg
Photos/fest_2024.jpg    ← also has EXIF flag
ntfs_evidence.img       ← NTFS timestamp challenge
```

```bash
# Bank statement shows suspicious deposit
grep "NEFT\|Unknown" /mnt/p2/bank_statement_Q1_2024.txt
```

**Output:**
```
17-Mar  NEFT Unknown        +50,000       61,900
```

> [!warning] Suspicious deposit
> Rs 50,000 received from unknown source the **same day** as the data theft. Potential payment for stolen data.

---

## 🔍 Phase 6 — P2 Deleted Files Recovery (Flags 03–07)

```bash
# List ALL deleted files on P2
fls -r -d -o 133120 ctf1.img
```

**Output:**
```
r/r * 7:   invoice.exe
r/r * 8:   kl.log
r/r * 9:   customer_export.csv
r/r * 10:  winscp_session.log
r/r * 11:  private_note.txt
r/r * 12:  ram_capture.bin
```

```bash
# Recover all at once
for inode in 7 8 9 10 11 12; do
    filename=$(fls -r -d -o 133120 ctf1.img | grep "^r/r \* ${inode}:" | awk '{print $3}')
    icat -o 133120 ctf1.img $inode > "recovered_${filename}"
    echo "Recovered: ${filename}"
done
```

**Output:**
```
Recovered: invoice.exe
Recovered: kl.log
Recovered: customer_export.csv
Recovered: winscp_session.log
Recovered: private_note.txt
Recovered: ram_capture.bin
```

```bash
# Extract all flags
echo "=== invoice.exe ===" && strings recovered_invoice.exe | grep Flag
echo "=== kl.log ===" && cat recovered_kl.log | grep Flag
echo "=== winscp_session.log ===" && cat recovered_winscp_session.log | grep Flag
echo "=== private_note.txt ===" && cat recovered_private_note.txt | grep Flag
echo "=== ram_capture.bin ===" && strings recovered_ram_capture.bin | grep "Flag\|key="
```

**Output:**
```
=== invoice.exe ===
Flag: MZ_exe_h1dd3n_4s_txt

=== kl.log ===
Flag: s3ct0r_z3r0_n3v3r_li3s

=== winscp_session.log ===
Flag: qu1ck_f0rm4t_15_n0t_w1p3

=== private_note.txt ===
Flag: ph4nt0m_l3dg3r_cl0s3d

=== ram_capture.bin ===
[CmdLine] keylogger.exe --key=v0l4t1l3_k3y5_d1s4pp34r
Flag: 1102_ran_7_t1m3s
```

> [!success] Flags 03–08 recovered!

---

## 🗂️ Phase 7 — NTFS Timestamp Analysis (Flag 05)

```bash
# Find deleted file in NTFS image
fls -r -d /mnt/p2/ntfs_evidence.img

# Get MFT entry
istat /mnt/p2/ntfs_evidence.img 4 | grep -A5 "STANDARD\|FILE_NAME"
```

**Output:**
```
$STANDARD_INFORMATION:
  Created:  2020-01-01 00:00:00  ← FAKE (timestomped)

$FILE_NAME:
  Created:  2024-03-17 09:22:41  ← REAL
```

> [!success] `Cywarx{t1m3st0mp_09}` (technique + real hour)

---

## 🪚 Phase 8 — Data Carving (Flag 09)

```bash
mkdir -p /tmp/carved
foremost -t jpg,zip -i ctf1.img -o /tmp/carved/ -q
unzip /tmp/carved/zip/00000000.zip -d /tmp/carved/extracted/
cat /tmp/carved/extracted/recovered_evidence.txt | grep Flag
```

**Output:**
```
Flag: c4rv1ng_f1nd5_th3_truth
```

> [!success] `Cywarx{c4rv1ng_f1nd5_th3_truth}`

---

## 🔒 Phase 9 — Hidden Partition (P3)

```bash
sudo mkdir -p /mnt/p3
sudo mount /dev/mapper/loop0p3 /mnt/p3
cat /mnt/p3/private.txt
```

**Output:**
```
Hidden ext4 partition found!
Visible only with: mmls ctf1.img or fdisk -l ctf1.img

FTP:       rohan_upload / Upl04d!99  @  185.44.21.9
Secondary: admin / S3cr3t@123  @  10.0.0.55
```

---

## 📊 Phase 10 — Timeline Reconstruction

```
DATE/TIME            EVENT                              EVIDENCE SOURCE
────────────────     ──────────────────────             ─────────────────────
2024-03-15 ???       Keylogger installed on bank PC     private_note.txt (Phase 1)
2024-03-17 09:15:22  Keylogger starts capturing         kl.log timestamp
2024-03-17 09:15:48  Admin credentials captured         kl.log: S3cr3t@123
2024-03-17 09:22:11  75842 records selected for export  kl.log clipboard entry
2024-03-17 09:22:41  invoice.exe (keylogger) last used  ntfs_evidence.img $FN
2024-03-17 09:28:55  WinSCP FTP session opened          winscp_session.log
2024-03-17 09:31:44  Upload complete (76.4MB)           winscp_session.log
2024-03-17 14:22:33  keylogger.exe ran (run 7)          ram_capture.bin Prefetch
2024-03-17 14:25:03  Security Event Log CLEARED         ram_capture.bin EventID 1102
2024-03-17 14:32:11  Photo taken near bank              fest_2024.jpg EXIF GPS
2024-03-17 ???       All USB files deleted              fls shows 6 deleted inodes
```

---

## 📝 Case Report Summary

```
DIGITAL FORENSIC INVESTIGATION REPORT
Case: Operation Phantom Ledger
Investigator: [Your Name]
Date: [Date]
Evidence: ctf1.img (SHA256: [hash])

FINDINGS:

1. INTEGRITY: Image verified untampered (hash match)

2. IDENTITY: Suspect confirmed as Rohan Mehta
   - Contact.txt, Resume, student ID on drive
   - EXIF metadata on photos confirms device ownership

3. LOCATION: GPS places suspect at crime scene
   - fest_2024.jpg: Jaipur bank area (26.9124N 75.7873E)
   - DateTimeOriginal: 2024:03:17 14:32:11 (day of theft)

4. PREMEDITATION: Planning document recovered
   - private_note.txt: 5-phase operation plan with completion marks
   - Proves deliberate, organised theft (not accidental)

5. CREDENTIAL THEFT: Keylogger evidence
   - invoice.exe: Windows keylogger (MZ magic bytes confirmed)
   - kl.log: Captured admin:S3cr3t@123 at 09:15:48

6. DATA EXFILTRATION: FTP transfer evidence
   - winscp_session.log: Connected 185.44.21.9:22
   - Transferred customer_export.csv (76,418,048 bytes)
   - 75842 customer records confirmed stolen

7. ANTI-FORENSICS ATTEMPTS:
   - 6 files deleted from FAT32 partition (0xE5 markers)
   - Timestamps faked on keylogger EXE (timestomping)
   - Windows Security Event Log cleared (EventID 1102)
   - All attempts defeated by forensic analysis

8. RECOVERED EVIDENCE:
   - 6 deleted files recovered via fls/icat
   - 3 JPEGs + 1 ZIP recovered via foremost carving
   - Hidden partition discovered via mmls
   - MBR hidden data extracted via raw read

CONCLUSION:
Digital evidence conclusively proves premeditated data theft,
credential harvesting, and exfiltration of 75,842 bank records.
All evidence obtained from verified, untampered image.
Chain of custody maintained throughout investigation.
```

---

## 🧹 Cleanup

```bash
sudo umount /mnt/p1 /mnt/p2 /mnt/p3 2>/dev/null
sudo kpartx -dv /dev/loop0
sudo losetup -d /dev/loop0
```

---

## 🔗 All Challenge Solutions

- [[CTF-01-MBR-Hidden-Marker]]
- [[CTF-02-EXIF-Metadata]]
- [[CTF-03-Deleted-kl-log]]
- [[CTF-04-Deleted-invoice-exe]]
- [[CTF-05-NTFS-Timestomping]]
- [[CTF-06-WinSCP-FTP-Log]]
- [[CTF-07-Private-Note]]
- [[CTF-08-RAM-Volatile-Data]]
- [[CTF-09-Data-Carving]]
- You are here: [[CTF-10-Full-Investigation]]
