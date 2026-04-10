---
tags:
  - cyber-forensics
  - disk-imaging
  - evidence-acquisition
  - practical
  - pendrive
  - physical-drive
  - dd
  - dcfldd
  - write-blocker
aliases:
  - Physical Drive Imaging
  - Forensic Image Creation
  - Pendrive Imaging Guide
date: 2026-03-17
status: complete
difficulty: beginner
---

# 💾 Physical Drive Image Creation — Complete Guide

> [!abstract] What This Note Covers
> How to take a **real physical storage device** (pendrive, hard disk, SD card) and create a **forensically sound image** of it that can be used as evidence — step by step, with every command explained in plain language.

---

## 🧠 Before You Start — Understand What We Are Doing

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE GOLDEN RULE                              │
│                                                                 │
│   NEVER work on the original device.                           │
│   ALWAYS work on the image (the copy).                         │
│                                                                 │
│   Original pendrive → forensic image → all analysis on image   │
└─────────────────────────────────────────────────────────────────┘
```

> [!example] Real World Analogy
> Imagine a suspect hands over a USB drive at a police station. The detective does NOT open the USB and start clicking through files. Instead they:
> 1. Photograph it
> 2. Put the original in an evidence bag and lock it away
> 3. Make an exact copy (image)
> 4. Work on the copy forever after
>
> This is exactly what we do digitally.

---

## 🗂️ What You Need

| Item | Purpose |
|---|---|
| Physical pendrive / HDD / SSD / SD card | The evidence to image |
| Kali Linux machine | Where you run the commands |
| Enough free disk space | Image size = device size (32GB pendrive = 32GB image file) |
| A case folder | Organized place to save everything |
| `dcfldd` installed | Better than plain `dd` — hashes while copying |

---

## 📁 STEP 0 — Create Your Case Folder

Before touching the device, set up your organized workspace.

```bash
# Create a case directory (replace case001 with your case name/number)
mkdir -p ~/forensics-lab/cases/case001/{evidence,hashes,recovered,reports}

# Verify structure
tree ~/forensics-lab/cases/case001/
```

Expected output:
```
case001/
├── evidence/      ← image files go here
├── hashes/        ← all hash files go here
├── recovered/     ← recovered files go here
└── reports/       ← your documentation goes here
```

---

## 🔌 STEP 1 — Plug In and Identify the Device

Plug in your pendrive, then immediately run:

```bash
lsblk
```

Sample output:
```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0   500G  0 disk
├─sda1   8:1    0   499G  0 part /
└─sda2   8:2    0     1G  0 part [SWAP]
sdb      8:16   1    32G  0 disk          ← YOUR PENDRIVE
└─sdb1   8:17   1    32G  0 part /media/hexx/USB
```

> [!warning] Critical — Identify Correctly
> - `sda` = your Kali hard drive — **NEVER image this by mistake**
> - `sdb` = the newly plugged pendrive — **this is your target**
> - Always look at the **SIZE column** to confirm which is which
> - `RM=1` means removable — another indicator it is the pendrive

**If you are unsure, do this trick:**

```bash
# Step 1: Run lsblk WITHOUT the pendrive
lsblk > /tmp/before.txt

# Step 2: Plug in pendrive, wait 3 seconds, run again
lsblk > /tmp/after.txt

# Step 3: Compare — the new line is your pendrive
diff /tmp/before.txt /tmp/after.txt
```

**For even more detail:**

```bash
sudo fdisk -l
# Shows every device with exact size, partition type, and model name
# Look for "SanDisk", "Kingston", "Samsung" etc. — that is your pendrive
```

```bash
# Also useful — shows model name
sudo lsblk -o NAME,SIZE,MODEL,TRAN
# TRAN column: "usb" = USB device = your pendrive
```

---

## 🔒 STEP 2 — Unmount the Pendrive

Linux auto-mounts USB drives the moment you plug them in. If it is mounted, the OS can silently write to it — updating access timestamps, writing journal entries — which changes the evidence.

```bash
# Unmount the partition (sdb1)
sudo umount /dev/sdb1

# If there are multiple partitions, unmount each one
sudo umount /dev/sdb1
sudo umount /dev/sdb2
```

> [!tip] "Not Mounted" is Fine
> If the command says `umount: /dev/sdb1: not mounted` — that is perfectly fine. Just continue to the next step.

**Verify nothing is mounted:**

```bash
mount | grep sdb
# Should return nothing — means it is fully unmounted
```

---

## 🛡️ STEP 3 — Write-Block the Device

A write blocker is a hardware device (like a Tableau T35u) that sits between the evidence drive and your computer, physically preventing any write commands from reaching the drive.

If you do not have hardware, use the software method:

```bash
# Set the device to read-only at the kernel level
sudo hdparm -r1 /dev/sdb
```

**Verify it worked:**

```bash
sudo hdparm -r /dev/sdb
```

Expected output:
```
/dev/sdb:
 readonly      =  1 (on)
```

> [!danger] Do NOT Skip This Step
> Without write-blocking, the moment dd opens the device for reading, the OS may write to it. This modifies the device, changes the hash, and makes the evidence legally compromised.
> If `hdparm` does not work on your device, use this alternative:
> ```bash
> sudo blockdev --setro /dev/sdb
> sudo blockdev --getro /dev/sdb   # should return: 1
> ```

---

## 🔐 STEP 4 — Hash the Original Device

This creates your **evidence seal** — the fingerprint of the original device before you do anything to it. This hash will be compared against the image hash after copying to prove the image is identical.

```bash
# SHA256 is the gold standard for forensics
sudo sha256sum /dev/sdb | tee ~/forensics-lab/cases/case001/hashes/original_sha256.txt

# Also compute MD5 as a secondary check
sudo md5sum /dev/sdb | tee ~/forensics-lab/cases/case001/hashes/original_md5.txt
```

> [!note] This Takes Time
> Hashing a 32GB pendrive takes 2–5 minutes depending on speed. Do not interrupt it.

Output example:
```
a1b2c3d4e5f6789abc0011223344556677889900aabbccddeeff0011  /dev/sdb
```

**Save this hash somewhere safe.** It is the proof that the original was untampered when you received it.

---

## 📸 STEP 5 — Create the Forensic Image

### Method A — `dcfldd` (Recommended)

`dcfldd` is the forensics-enhanced version of `dd`. It hashes the data live while copying, so you get hash verification built in automatically.

```bash
sudo dcfldd if=/dev/sdb \
            of=~/forensics-lab/cases/case001/evidence/pendrive.img \
            bs=512 \
            conv=noerror,sync \
            hash=sha256,md5 \
            hashlog=~/forensics-lab/cases/case001/hashes/dcfldd_hashlog.txt \
            status=on \
            sizeprobe=if
```

**Every argument explained:**

| Argument | Meaning | Why |
|---|---|---|
| `if=/dev/sdb` | Input = your pendrive | Read from here |
| `of=.../pendrive.img` | Output = image file | Write to here |
| `bs=512` | Block size = 512 bytes | Matches one physical disk sector exactly |
| `conv=noerror` | Don't stop on bad sectors | Keep going even if some sectors are damaged |
| `conv=sync` | Pad bad sectors with zeros | Keeps all sector offsets correct in the image |
| `hash=sha256,md5` | Hash both algorithms | Compute fingerprint while copying — no second pass needed |
| `hashlog=...txt` | Save hash to file | Written automatically when done |
| `status=on` | Show live progress | See speed, bytes copied, time remaining |
| `sizeprobe=if` | Detect source size | Calculates accurate progress percentage |

**What you see while it runs:**

```
31457280 bytes (30 MiB) copied, 3 s, 9.8 MB/s
```

**What you see when it finishes:**

```
62521344+0 records in
62521344+0 records out
SHA256: a1b2c3d4e5f6789abc0011223344556677889900...
MD5:    ff00ee11dd22cc33bb44aa5599887766...
```

---

### Method B — Plain `dd` (If dcfldd is not installed)

```bash
sudo dd if=/dev/sdb \
        of=~/forensics-lab/cases/case001/evidence/pendrive.img \
        bs=512 \
        conv=noerror,sync \
        status=progress
```

With plain `dd` you must hash separately after imaging (Step 6 below).

---

### Method C — `ddrescue` (For Damaged Drives)

If the pendrive has physical damage and many bad sectors, use `ddrescue` — it is smarter about retrying damaged areas and building a complete image from multiple passes.

```bash
sudo apt install gddrescue -y

# First pass — fast, skips unreadable areas
sudo ddrescue -d -r3 /dev/sdb \
              ~/forensics-lab/cases/case001/evidence/pendrive.img \
              ~/forensics-lab/cases/case001/evidence/pendrive.log

# Second pass — retries only the bad areas from the log
sudo ddrescue -d -r3 --retry-passes=3 /dev/sdb \
              ~/forensics-lab/cases/case001/evidence/pendrive.img \
              ~/forensics-lab/cases/case001/evidence/pendrive.log
```

> [!tip] The `.log` file is your rescue map
> `ddrescue` tracks every sector it has and has not successfully copied in the `.log` file. If the drive fails mid-copy you can resume exactly where you left off. Never delete the log file until imaging is fully complete.

---

## ✅ STEP 6 — Verify Hash (Prove the Image is Identical)

This is the most critical step. You are proving that the image file is a perfect byte-for-byte copy of the original.

```bash
# Hash the image file
sudo sha256sum ~/forensics-lab/cases/case001/evidence/pendrive.img \
  | tee ~/forensics-lab/cases/case001/hashes/image_sha256.txt

# Compare original hash vs image hash
echo "=== ORIGINAL DEVICE HASH ===" 
cat ~/forensics-lab/cases/case001/hashes/original_sha256.txt

echo "=== IMAGE FILE HASH ==="
cat ~/forensics-lab/cases/case001/hashes/image_sha256.txt
```

**The long hash strings must be identical:**

```
# PASS — forensically sound ✓
a1b2c3d4e5f6789abc001122...  /dev/sdb
a1b2c3d4e5f6789abc001122...  pendrive.img

# FAIL — something went wrong ✗
a1b2c3d4e5f6789abc001122...  /dev/sdb
9999aaaa8888bbbb7777cccc...  pendrive.img
```

**Automated comparison:**

```bash
ORIG=$(awk '{print $1}' ~/forensics-lab/cases/case001/hashes/original_sha256.txt)
IMG=$(sha256sum ~/forensics-lab/cases/case001/evidence/pendrive.img | awk '{print $1}')

if [ "$ORIG" = "$IMG" ]; then
    echo "[✓] HASH MATCH — image is forensically sound"
    echo "    Evidence is admissible"
else
    echo "[✗] HASH MISMATCH — imaging failed or device was modified"
    echo "    Do NOT use this image as evidence"
fi
```

---

## 🔍 STEP 7 — Mount the Image Read-Only

Now you can safely browse the contents of the pendrive through the image file. The `-o ro` flag makes it impossible to accidentally modify.

```bash
# Create mount point
sudo mkdir -p /mnt/pendrive_evidence

# Mount the image — read-only, no access time updates
sudo mount -o ro,loop,noatime \
           ~/forensics-lab/cases/case001/evidence/pendrive.img \
           /mnt/pendrive_evidence

# Verify it is read-only
mount | grep pendrive_evidence
# Should contain: ro (confirms read-only)

# Browse files safely
ls -la /mnt/pendrive_evidence/
file /mnt/pendrive_evidence/*

# Prove you cannot modify it (expected: error)
touch /mnt/pendrive_evidence/test.txt
# Output: touch: cannot touch: Read-only file system ← GOOD
```

**If the image has multiple partitions, mount by offset:**

```bash
# First see the partition layout
mmls ~/forensics-lab/cases/case001/evidence/pendrive.img

# Output shows partition start sectors, e.g.:
# 002: 000:000  2048  ...  NTFS
# Offset = sector_start × 512 = 2048 × 512 = 1048576

sudo mount -o ro,loop,noatime,offset=1048576 \
           ~/forensics-lab/cases/case001/evidence/pendrive.img \
           /mnt/pendrive_evidence
```

---

## 🕵️ STEP 8 — Run Forensic Analysis

With the image mounted and verified, begin analysis — all on the copy, never the original.

### List all files including deleted ones

```bash
# The * (asterisk) marks deleted files
fls -r ~/forensics-lab/cases/case001/evidence/pendrive.img

# Show only deleted files
fls -r -d ~/forensics-lab/cases/case001/evidence/pendrive.img
```

### Recover a deleted file

```bash
# Get inode number from fls output (e.g.: r/r * 42-128-1: secret.txt)
icat ~/forensics-lab/cases/case001/evidence/pendrive.img 42 \
  > ~/forensics-lab/cases/case001/recovered/secret.txt

cat ~/forensics-lab/cases/case001/recovered/secret.txt
```

### Get file metadata and timestamps

```bash
# Full metadata for any file by inode number
istat ~/forensics-lab/cases/case001/evidence/pendrive.img 42
# Shows: created, modified, accessed, MFT changed timestamps
```

### Carve files from raw bytes

```bash
foremost -t jpg,pdf,docx,zip,png \
         -i ~/forensics-lab/cases/case001/evidence/pendrive.img \
         -o ~/forensics-lab/cases/case001/recovered/carved/
```

### Search for keywords in raw bytes

```bash
# Find text evidence even in deleted/unallocated space
strings ~/forensics-lab/cases/case001/evidence/pendrive.img \
  | grep -iE "password|secret|account|transfer|bitcoin"
```

### Open in Autopsy GUI

```bash
autopsy
# Browser opens at http://localhost:9999/autopsy
# New Case → Add Host → Add Image → point to pendrive.img
# All-in-one: browse files, recover deleted, keyword search, timeline
```

---

## 📄 STEP 9 — Document Everything (Chain of Custody)

Every action you took must be documented. This is what makes evidence legally admissible.

```bash
cat > ~/forensics-lab/cases/case001/reports/chain_of_custody.txt << EOF
════════════════════════════════════════════════════
       CHAIN OF CUSTODY — EVIDENCE LOG
════════════════════════════════════════════════════
Case Number    : CASE-001-2026
Date           : $(date)
Investigator   : HeXx
Organization   : Security Team

── EVIDENCE DETAILS ─────────────────────────────
Item Number    : E001
Device Type    : USB Pendrive
Make/Model     : $(sudo lsblk -o MODEL /dev/sdb | tail -1)
Capacity       : $(sudo lsblk -o SIZE /dev/sdb | tail -1)
Device Path    : /dev/sdb

── HASH VALUES ──────────────────────────────────
Original SHA256: $(cat ~/forensics-lab/cases/case001/hashes/original_sha256.txt | awk '{print $1}')
Image SHA256   : $(sha256sum ~/forensics-lab/cases/case001/evidence/pendrive.img | awk '{print $1}')
Hash Match     : YES

── IMAGE FILE ───────────────────────────────────
Image Path     : ~/forensics-lab/cases/case001/evidence/pendrive.img
Image Size     : $(du -h ~/forensics-lab/cases/case001/evidence/pendrive.img | awk '{print $1}')
Tool Used      : dcfldd

── HANDLING LOG ─────────────────────────────────
$(date "+%Y-%m-%d %H:%M")  HeXx  Device received and photographed
$(date "+%Y-%m-%d %H:%M")  HeXx  Device unmounted (sudo umount)
$(date "+%Y-%m-%d %H:%M")  HeXx  Write-blocked (hdparm -r1)
$(date "+%Y-%m-%d %H:%M")  HeXx  Original hashed (SHA256 + MD5)
$(date "+%Y-%m-%d %H:%M")  HeXx  Image created with dcfldd
$(date "+%Y-%m-%d %H:%M")  HeXx  Image hash verified — MATCH
$(date "+%Y-%m-%d %H:%M")  HeXx  Image mounted read-only
$(date "+%Y-%m-%d %H:%M")  HeXx  Analysis begun on image only

── NOTES ────────────────────────────────────────
Original device sealed in evidence bag #E001
All analysis performed on forensic copy only
Original device stored in evidence locker
════════════════════════════════════════════════════
EOF

cat ~/forensics-lab/cases/case001/reports/chain_of_custody.txt
```

---

## 🧹 STEP 10 — Unmount When Done

```bash
sudo umount /mnt/pendrive_evidence
```

The image file remains intact. You can remount it any time later for further analysis.

---

## ⚠️ Common Mistakes — What NOT to Do

> [!danger] Mistake 1 — Working on the Original Device
> Running `fls /dev/sdb` or opening files from the mounted original device modifies timestamps and may write journal entries.
> Always image first, analyze the image.

> [!danger] Mistake 2 — Forgetting to Unmount Before Imaging
> If the OS has the pendrive mounted during `dd`/`dcfldd`, the OS may write to it mid-copy. Your hash will not match and the image is contaminated.

> [!danger] Mistake 3 — Imaging `sda` Instead of `sdb`
> `if=/dev/sda` would try to image your entire Kali Linux hard drive. Always double-check with `lsblk` and confirm sizes before running.

> [!danger] Mistake 4 — No Hash Verification
> Creating an image without hashing before and after means you have no proof the image matches the original. It is not legally usable as evidence.

> [!danger] Mistake 5 — Mounting as Read-Write
> `mount -o loop image.img /mnt/point` without the `ro` flag mounts as read-write by default. Every file you open updates its `atime` timestamp — you are modifying the evidence.

---

## 🔄 Quick Reference — All Commands in Order

```bash
# 0. Create case folder
mkdir -p ~/forensics-lab/cases/case001/{evidence,hashes,recovered,reports}

# 1. Identify the device
lsblk
sudo lsblk -o NAME,SIZE,MODEL,TRAN

# 2. Unmount
sudo umount /dev/sdb1

# 3. Write-block
sudo hdparm -r1 /dev/sdb
sudo hdparm -r /dev/sdb          # verify: readonly = 1

# 4. Hash original
sudo sha256sum /dev/sdb | tee ~/forensics-lab/cases/case001/hashes/original_sha256.txt

# 5. Create image
sudo dcfldd if=/dev/sdb \
            of=~/forensics-lab/cases/case001/evidence/pendrive.img \
            bs=512 conv=noerror,sync \
            hash=sha256 \
            hashlog=~/forensics-lab/cases/case001/hashes/dcfldd_hashlog.txt \
            status=on

# 6. Verify hash
sudo sha256sum ~/forensics-lab/cases/case001/evidence/pendrive.img \
  | tee ~/forensics-lab/cases/case001/hashes/image_sha256.txt
diff ~/forensics-lab/cases/case001/hashes/original_sha256.txt \
     ~/forensics-lab/cases/case001/hashes/image_sha256.txt

# 7. Mount read-only
sudo mkdir -p /mnt/pendrive_evidence
sudo mount -o ro,loop,noatime \
           ~/forensics-lab/cases/case001/evidence/pendrive.img \
           /mnt/pendrive_evidence

# 8. Analyze (examples)
fls -r -d ~/forensics-lab/cases/case001/evidence/pendrive.img
foremost -t all -i ~/forensics-lab/cases/case001/evidence/pendrive.img \
         -o ~/forensics-lab/cases/case001/recovered/

# 9. Document chain of custody (see Step 9 above)

# 10. Unmount when done
sudo umount /mnt/pendrive_evidence
```

---

## 📊 Tool Comparison

| Tool | Best For | Hash Built-In | Bad Sector Handling |
|---|---|---|---|
| `dcfldd` | Standard forensic imaging | Yes — live | noerror+sync |
| `dd` | Simple copies, scripting | No — manual | noerror+sync |
| `ddrescue` | Damaged/failing drives | No — manual | Intelligent retry |
| FTK Imager | Windows, GUI, .E01 format | Yes | Yes |
| `Guymager` | GUI on Linux, .E01/.AFF | Yes | Yes |

---

## 📐 Storage Size Reference

| Device | Approximate Image Size | Rough Imaging Time |
|---|---|---|
| 4 GB SD card | 4 GB | ~1 min at 50 MB/s |
| 32 GB pendrive | 32 GB | ~10 min at 50 MB/s |
| 64 GB pendrive | 64 GB | ~20 min at 50 MB/s |
| 500 GB HDD | 500 GB | ~2–3 hours at 50 MB/s |
| 1 TB SSD | 1 TB | ~4–5 hours at 50 MB/s |

> [!tip] Speed Tip
> For large drives, you can increase block size to speed things up once you know the drive is healthy:
> `bs=4M` instead of `bs=512` — roughly 8× faster, but if a bad sector hits, you lose 4MB per bad block instead of 512 bytes. Use `bs=512` for evidence drives with unknown health.

---

## 🔗 Related Notes

- [[Unit-IV-Cyber-Forensics-Complete]]
- [[Cyber-Forensics-Keywords-Glossary#Acquisition]]
- [[Cyber-Forensics-Keywords-Glossary#Bit-for-Bit Forensic Image]]
- [[Cyber-Forensics-Keywords-Glossary#Chain of Custody]]
- [[Cyber-Forensics-Keywords-Glossary#Write Blocker]]
- [[Cyber-Forensics-Keywords-Glossary#Hash (MD5 / SHA256)]]
- [[Task-01-Forensic-Imaging-Hashing]]
- [[Task-02-Disk-Storage-Analysis]]
