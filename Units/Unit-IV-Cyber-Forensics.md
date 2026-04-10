---
tags:
  - cyber-forensics
  - digital-forensics
  - unit-4
  - storage
  - data-recovery
  - evidence
  - deleted-files
  - file-systems
  - practical
  - kali-linux
aliases:
  - Cyber Forensics Unit 4
  - Digital Forensics Basics
date: 2026-03-17
status: complete
topic: Cyber Forensics
---

# 🔍 Unit IV: Fundamentals of Cyber Forensics
## Complete Theory + Step-by-Step Practicals (Kali Linux)

> [!abstract] Unit Overview
> This unit covers the **science of finding, preserving, and analyzing digital evidence** from computers and storage devices.
> Think of it as **CSI, but for computers.**
> Every topic includes a **real-world scenario** + **hands-on practical** you can run on Kali Linux.

---

## 🗺️ Topic Tree

```
Unit IV: Cyber Forensics
│
├── PART 1: Cyber Forensic Basics
│   ├── 1.1 Introduction to Cyber Forensics
│   ├── 1.2 Storage Fundamentals
│   ├── 1.3 File System Concepts
│   ├── 1.4 Data Recovery Concepts
│   └── 1.5 OS Software & Basic Terminology
│
└── PART 2: Data & Evidence Recovery
    ├── 2.1 Deleted File Recovery
    └── 2.2 Formatted Partition Recovery
```

---

# 📌 PART 1: Cyber Forensic Basics

---

## 1.1 Introduction to Cyber Forensics

### 🔎 What Is Cyber Forensics?

**Cyber Forensics** = The science of **identifying, preserving, analyzing, and presenting** digital evidence in a legally admissible way.

> [!example] 🌍 Real World Scenario
> **Case:** A bank employee is suspected of leaking customer data to a competitor.
>
> **What the forensic investigator does:**
> 1. Seizes the employee's laptop (with legal authorization / warrant)
> 2. Takes a **bit-for-bit forensic image** — never touching the original
> 3. Searches for sent emails, USB device history, clipboard logs
> 4. Recovers deleted Excel files containing customer account numbers
> 5. Builds a chronological timeline of the attack
> 6. Submits a court-admissible forensic report

---

### 🏛️ Branches of Cyber Forensics

| Branch | What It Covers | Real Example |
|---|---|---|
| **Disk Forensics** | HDDs, SSDs, USBs | Recovering deleted files from a suspect's laptop |
| **Network Forensics** | Packet captures, firewall logs | Tracing hacker's IP via PCAP analysis |
| **Memory Forensics** | RAM dumps | Finding encryption keys or malware in RAM |
| **Mobile Forensics** | Phones, tablets | Recovering deleted WhatsApp messages |
| **Email Forensics** | Headers, attachments | Tracing origin of a phishing email |
| **Malware Forensics** | Malware reverse engineering | Attributing ransomware to a threat actor |
| **Database Forensics** | DB logs, SQL queries | Detecting insider data theft in SQL Server |

---

### 📋 Standard Forensics Workflow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│          │    │          │    │          │    │          │
│ IDENTIFY │───▶│ PRESERVE │───▶│  ANALYZE │───▶│ PRESENT  │
│          │    │          │    │          │    │          │
│ What     │    │ Image it │    │ Dig into │    │ Report / │
│ evidence │    │ Hash it  │    │ the copy │    │ Testify  │
│ exists?  │    │ Log it   │    │ with     │    │ in court │
│          │    │          │    │ tools    │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

### 🔑 Core Principles

| Principle            | Meaning                               | Example                                   |
| -------------------- | ------------------------------------- | ----------------------------------------- |
| **Chain of Custody** | Track who touched evidence and when   | Evidence log sheet signed by each handler |
| **Integrity**        | Evidence not altered — proven by hash | MD5/SHA256 of image matches original      |
| **Admissibility**    | Collected legally                     | Search warrant or written consent         |
| **Authenticity**     | Prove where evidence came from        | Metadata, logs, witness statements        |

---

### 🧪 PRACTICAL 1.1 — Setting Up Forensics Lab on Kali

```bash
# Step 1: Install all core forensics tools
sudo apt update && sudo apt install -y \
  autopsy sleuthkit foremost scalpel testdisk \
  photorec dc3dd dcfldd ewf-tools hexedit xxd \
  binwalk exiftool volatility3 bulk-extractor \
  ntfs-3g extundelete

# Step 2: Verify installation
which autopsy fls foremost testdisk photorec bulk_extractor
echo "[+] All tools available!"

# Step 3: Create organized lab directory
mkdir -p ~/forensics-lab/{images,evidence,reports,recovered,tools}
cd ~/forensics-lab
echo "[+] Lab directory structure created"
tree ~/forensics-lab
```

---

### 🧪 PRACTICAL 1.2 — Creating & Verifying a Forensic Image

> [!info] Scenario
> You received a USB drive from a suspected insider threat. You must image it without modifying a single bit.

```bash
# Step 1: Identify the target device — DO NOT MOUNT
lsblk
fdisk -l /dev/sdb

# Step 2: Software write-protect
sudo blockdev --setro /dev/sdb
# Verify: blockdev --getro /dev/sdb  → should return 1

# Step 3: Hash the ORIGINAL before imaging
sudo md5sum /dev/sdb    | tee ~/forensics-lab/images/original_md5.txt
sudo sha256sum /dev/sdb | tee ~/forensics-lab/images/original_sha256.txt
echo "[+] Original hashes saved — chain of custody started"

# Step 4: Create forensic image with dc3dd
sudo dc3dd \
  if=/dev/sdb \
  of=~/forensics-lab/images/usb_evidence.img \
  hash=sha256 \
  log=~/forensics-lab/images/dc3dd_acquisition.log \
  bs=512 \
  verb=on

# Step 5: Hash the IMAGE
sha256sum ~/forensics-lab/images/usb_evidence.img \
  | tee ~/forensics-lab/images/image_sha256.txt

# Step 6: Compare — THEY MUST BE IDENTICAL
diff ~/forensics-lab/images/original_sha256.txt \
     ~/forensics-lab/images/image_sha256.txt

# No output = match = forensically sound image!
echo "[+] Image verified. Integrity confirmed."
```

> [!success] What This Proves
> Identical hashes = the image is a perfect, unmodified copy. This is what makes evidence **court-admissible**.

---

## 1.2 Storage Fundamentals

### 💾 How Storage Works

Data is stored as **binary (0s and 1s)** on physical media:
- **Magnetic polarity** — HDDs (North/South pole = 0 or 1)
- **Electrical charge in NAND cells** — SSDs (charge present/absent = 0 or 1)
- **Burned pits** — CDs/DVDs (pit/land = 0 or 1)

---

### 🧱 Storage Hierarchy

```
┌──────────────────────────────────────────────────────┐
│                  STORAGE HIERARCHY                   │
│                                          Speed       │
│  CPU Registers ────────────────────── ⚡ Fastest     │
│  L1/L2/L3 CPU Cache (KB-MB)                         │
│  RAM (Volatile — lost on power off) ── ⚡ Fast       │
│  NVMe SSD (fastest persistent storage)              │
│  SATA SSD                                           │
│  HDD (Spinning Magnetic Disk) ──────── 🐢 Slow      │
│  USB Flash Drive                                    │
│  Optical (CD/DVD/Blu-ray)                           │
│  Magnetic Tape Archive ─────────────── 🐢 Slowest   │
└──────────────────────────────────────────────────────┘
```

> [!warning] Volatile Memory in Forensics
> **RAM is lost when power is cut!** If a suspect's computer is running, you MUST do **live RAM acquisition FIRST** before pulling the plug. Encryption keys, running malware, network connections — all live in RAM.

---

### 🖴 HDD Anatomy

```
┌──────────────────────────────────────────────────────┐
│                   HDD STRUCTURE                      │
│                                                      │
│  Platter  ──► Spinning magnetic disk                 │
│  Track    ──► Concentric ring on platter             │
│  Sector   ──► Smallest addressable unit              │
│               Traditional = 512 bytes                │
│               Advanced Format = 4096 bytes           │
│  Cluster  ──► Group of sectors (OS allocation unit)  │
│  Cylinder ──► Same track across all platters         │
│                                                      │
│  ⭐ Slack Space = Unused bytes in last cluster       │
│     ← Old file data hides here! Forensic gold!       │
└──────────────────────────────────────────────────────┘
```

> [!example] 🌍 Slack Space Example
> You save a 3,000-byte file. Cluster size = 4,096 bytes.
> The last **1,096 bytes are slack space** — containing fragments from a PREVIOUS file stored in those clusters.
> Forensic tools can carve this for old passwords, document fragments, or chat messages.

---

### ⚡ SSD vs HDD — Forensics Perspective

| Feature               | HDD                  | SSD                         |
| --------------------- | -------------------- | --------------------------- |
| Recovery after delete | ✅ High (data intact) | ⚠️ Low (TRIM erases blocks) |
| Data carving          | ✅ Very effective     | ❌ Limited                   |
| Slack space           | ✅ Contains old data  | ❌ TRIM cleans it            |
| Recovery urgency      | Hours to days        | Minutes to seconds          |

> [!danger] SSD + TRIM = Evidence Destruction
> On SSDs with TRIM enabled, deleting sends an immediate erase command to NAND cells. Recovery window is **seconds to minutes**. Image SSDs IMMEDIATELY after seizure — every second counts.

---

### 🧪 PRACTICAL 1.3 — Exploring Storage at Block Level

```bash
# Step 1: Create a virtual practice disk (safe, no real hardware needed)
dd if=/dev/zero of=~/forensics-lab/practice_disk.img bs=1M count=100
echo "[+] 100MB virtual disk created"

# Step 2: Attach as loop device
sudo losetup /dev/loop10 ~/forensics-lab/practice_disk.img
sudo losetup -a   # Confirm loop10 is attached

# Step 3: Partition it
sudo parted /dev/loop10 --script \
  mklabel msdos \
  mkpart primary fat32 1MiB 100MiB
sudo mkfs.vfat -F 32 /dev/loop10p1 2>/dev/null || \
  sudo mkfs.vfat -F 32 /dev/loop10

# Step 4: View raw hex of first 512 bytes (Boot Sector)
sudo xxd /dev/loop10 | head -40
# Magic bytes: EB 58 90 = FAT32 jump instruction
# Last 2 bytes of sector: 55 AA = valid boot signature

# Step 5: Disk geometry info
sudo fdisk -l /dev/loop10
sudo blockdev --getss /dev/loop10   # Sector size (512 or 4096)
sudo blockdev --getsz /dev/loop10   # Total sectors

# Step 6: Cleanup
sudo losetup -d /dev/loop10
echo "[+] Block-level exploration done"
```

---

## 1.3 File System Concepts

### 📁 What Is a File System?

A **file system** = the organizational structure the OS uses to **store, name, and retrieve data** on disk.

> [!example] 🌍 Library Analogy
> - **Library building** = your hard drive
> - **Card catalog / index** = FAT table or MFT
> - **Books** = actual file data (in clusters)
> - **Shelf locations** = cluster addresses
>
> When you **delete a book**, you only **remove its catalog card** — the book stays on the shelf until someone puts a new book there (overwrites it).
> **This is exactly why deleted files are recoverable.**

---

### 🗂️ Common File Systems

| File System | OS               | Forensic Importance                    |
| ----------- | ---------------- | -------------------------------------- |
| **FAT32**   | USB, old Windows | Easy recovery — minimal metadata       |
| **exFAT**   | USB, SD, cameras | Common on camera cards                 |
| **NTFS**    | Modern Windows   | Most metadata-rich — MFT is a goldmine |
| **ext4**    | Linux            | Journaling helps recovery              |
| **APFS**    | macOS (2017+)    | Snapshots help, encryption hurts       |
| **HFS+**    | macOS (older)    | B-tree catalog                         |

---

### 🏗️ NTFS Deep Dive

```
┌──────────────────────────────────────────────────────────┐
│                  NTFS DISK LAYOUT                        │
│                                                          │
│  [VBR] [MFT Zone] [Data Area] [MFT Mirror] [Backup VBR] │
│                                                          │
│  $MFT      = File 0 — Master File Table (all metadata)   │
│  $MFTMirr  = File 1 — Backup of first 4 MFT entries      │
│  $LogFile  = File 2 — Transaction journal                │
│  $Bitmap   = File 6 — Used/free cluster map              │
│  $Recycle.Bin = Deleted file info ($I and $R files)      │
└──────────────────────────────────────────────────────────┘
```

#### MFT Entry (Per File/Folder)

```
┌───────────────────────────────────────────┐
│           MFT ENTRY (1024 bytes)          │
├───────────────────────────────────────────┤
│ $STANDARD_INFORMATION                     │
│  ├── Created, Modified, Accessed times    │
│  └── Owner, security permissions          │
├───────────────────────────────────────────┤
│ $FILE_NAME                                │
│  ├── Filename (also has its own MACE)     │
│  └── Parent directory reference           │
├───────────────────────────────────────────┤
│ $DATA                                     │
│  ├── Resident: small files stored HERE    │
│  └── Non-resident: pointer to clusters   │
└───────────────────────────────────────────┘
```

> [!tip] 🔑 MACE Timestamps — Key for Timeline Forensics
> | Letter | Meaning |
> |---|---|
> | **M** | Modified — content was changed |
> | **A** | Accessed — file was opened/read |
> | **C** | Changed — MFT metadata changed |
> | **E** | Entry Modified — $FILE_NAME attribute changed |
>
> **Timestomping Detection:** Attackers fake $STANDARD_INFORMATION timestamps but often forget $FILE_NAME timestamps. Comparing both reveals tampering!

---

#### Alternate Data Streams (ADS)

```bash
# ADS hides data inside NTFS files invisibly
# Attacker creates: legitimate.txt:hidden_malware
# Explorer shows:   legitimate.txt  (0 bytes visible)
# ADS contains:     full executable payload

# Detect ADS on Linux (with NTFS image mounted)
sudo mount -o ro,loop evidence.img /mnt/evidence
getfattr -n ntfs.streams.list /mnt/evidence/suspicious.txt

# Using TSK to read ADS
icat evidence.img <inode>:<stream_name>

# Windows detection:
# dir /r                      → shows all ADS
# Get-Item -Stream * file.txt → PowerShell
```

---

### 🏗️ FAT32 Structure

```
┌──────────────────────────────────────────────────────┐
│                 FAT32 DISK LAYOUT                    │
│                                                      │
│  [MBR] [Reserved Sectors] [FAT1] [FAT2] [Data Area] │
│                                                      │
│  FAT Entry values:                                   │
│   0x00000000 = Free cluster                          │
│   0x0FFFFFFF = End of file chain                     │
│   0x0XXXXXXX = Next cluster in chain                 │
│                                                      │
│  DELETION:                                           │
│   ├── Filename[0] → 0xE5 (deleted marker)            │
│   ├── FAT chain entries → 0x00 (marked free)         │
│   └── Actual data → UNTOUCHED ← Still recoverable!   │
└──────────────────────────────────────────────────────┘
```

---

### 🧪 PRACTICAL 1.4 — File System Analysis with Sleuth Kit (TSK)

```bash
cd ~/forensics-lab

# ── SETUP: Build a test image with files to analyze ──

dd if=/dev/zero of=test_fat32.img bs=1M count=50
sudo losetup /dev/loop11 test_fat32.img
sudo mkfs.vfat -F 32 /dev/loop11
sudo mkdir -p /mnt/test_fat
sudo mount /dev/loop11 /mnt/test_fat

echo "CONFIDENTIAL: Project Cobra Financials — Transfer $2M" | \
  sudo tee /mnt/test_fat/secret.txt

echo "Normal boring file" | sudo tee /mnt/test_fat/readme.txt
sudo mkdir /mnt/test_fat/docs
echo "Bank account: CH56 0483 5012 3456 7800 9" | \
  sudo tee /mnt/test_fat/docs/accounts.txt

# Simulate suspect deleting evidence
sudo rm /mnt/test_fat/secret.txt
sudo umount /mnt/test_fat
sudo losetup -d /dev/loop11

echo "[+] Test image created with 1 deleted file"

# ── TSK ANALYSIS ──

# Step 1: Get image/partition info
mminfo test_fat32.img
mmls test_fat32.img

# Step 2: File system details (cluster size, FAT location, etc.)
fsstat test_fat32.img

# Step 3: LIST ALL FILES including deleted (marked with *)
fls -r test_fat32.img
# * prefix = deleted file

# Step 4: Show deleted files only
fls -r -d test_fat32.img

# Step 5: Show with full metadata (timestamps, size)
fls -r -l test_fat32.img

# Step 6: Find the inode of deleted secret.txt
fls -r -d test_fat32.img | grep "secret"
# Output: r/r * 3:   secret.txt   (inode = 3)

# Step 7: RECOVER the deleted file using its inode
icat test_fat32.img 3 > ~/forensics-lab/recovered_secret.txt
cat ~/forensics-lab/recovered_secret.txt
# Output: CONFIDENTIAL: Project Cobra Financials...

echo "[+] Deleted file recovered successfully!"

# Step 8: Generate MACE timeline
fls -r -m "/" test_fat32.img > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv
head -20 timeline.csv
echo "[+] Forensic timeline created!"
```

---

### 🧪 PRACTICAL 1.5 — Autopsy GUI (Full Walkthrough)

```bash
# Step 1: Launch Autopsy web interface
sudo autopsy &
# Navigate to: http://127.0.0.1:9999/autopsy in Firefox

# In Autopsy web UI:
# ─────────────────────────────────────────────────────
# 1. Click "New Case"
#    Case Name:    GED_Insider_Threat_2026
#    Description:  USB seized from suspect workstation
#    Investigator: HeXx
#
# 2. Add Host
#    Hostname:  SUSPECT-PC-01
#    OS:        Windows 10
#    Timezone:  Asia/Kolkata
#
# 3. Add Image File
#    Path:   /root/forensics-lab/test_fat32.img
#    Type:   Disk Image or VM File
#    Import: Symlink (fastest)
#
# 4. Run Analysis:
#    - File Analysis     → Browse all + deleted files
#    - Keyword Search    → Type: "password", "confidential"
#    - File Type Sort    → Find files by extension
#    - Hash Analysis     → Check against known-bad hashes
#    - Timeline          → Visual event timeline
# ─────────────────────────────────────────────────────

# Step 2: Use TSK tools alongside Autopsy for speed
# List files with deleted
fls -r ~/forensics-lab/test_fat32.img

# Get metadata of specific file/inode
istat ~/forensics-lab/test_fat32.img 3

# Get data blocks used by a file
ifind -n "readme.txt" ~/forensics-lab/test_fat32.img

echo "[+] Autopsy + TSK analysis complete"
```

---

## 1.4 Data Recovery Concepts

### 🗑️ What Really Happens When You Delete a File?

> [!info] The Biggest Myth in Tech
> Most people think "delete = gone." It doesn't. Here's the truth:

```
┌─────────────────────────────────────────────────────────────┐
│                WHAT DELETION ACTUALLY DOES                  │
│                                                             │
│  FAT32:                                                     │
│   ├── Filename byte 0 → 0xE5 (deleted marker)               │
│   ├── FAT cluster chain entries → 0x00 (marked free)        │
│   └── Actual data clusters → COMPLETELY UNTOUCHED           │
│                                                             │
│  NTFS:                                                      │
│   ├── MFT entry flag → "not in use"                         │
│   ├── $Bitmap bits for those clusters → 0 (free)            │
│   └── Actual data clusters → COMPLETELY UNTOUCHED           │
│                                                             │
│  SSD with TRIM:                                             │
│   ├── OS sends ATA TRIM command to drive                    │
│   └── NAND blocks → IMMEDIATELY ERASED                      │
│       Recovery is nearly impossible!                        │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔍 Data Carving — Recovering Without a File System

**Data carving** = Scan raw disk bytes for **file signature (magic bytes)** headers/footers — without needing the file system index.

#### Common File Magic Bytes

| File Type | Extension | Hex Signature | Notes |
|---|---|---|---|
| JPEG | .jpg | `FF D8 FF E0` | Most common image |
| PNG | .png | `89 50 4E 47` | Always starts with .PNG |
| PDF | .pdf | `25 50 44 46` | %PDF |
| ZIP | .zip | `50 4B 03 04` | Also: DOCX, XLSX, PPTX |
| EXE/DLL | .exe | `4D 5A` | "MZ" — DOS header |
| SQLite DB | .db | `53 51 4C 69 74 65` | "SQLite" |
| MP4 Video | .mp4 | `00 00 00 18 66 74 79 70` | ftyp |
| RAR | .rar | `52 61 72 21 1A 07` | "Rar!" |

> [!tip] How Carving Works Step by Step
> 1. Tool scans disk image byte-by-byte
> 2. Finds known **header** magic bytes (e.g., `FF D8 FF` = JPEG start)
> 3. Reads until known **footer** (e.g., `FF D9` = JPEG end)
> 4. Everything between = extracted as a recovered file
> 5. No file system needed — works even on completely formatted drives!

---

### 🧪 PRACTICAL 1.6 — Data Carving with Foremost, Scalpel & PhotoRec

```bash
cd ~/forensics-lab
mkdir -p carving_lab && cd carving_lab

# ── SETUP: Create image with "deleted" files ──

dd if=/dev/zero of=carving_test.img bs=1M count=80
sudo losetup /dev/loop12 carving_test.img
sudo mkfs.vfat -F 32 /dev/loop12
sudo mkdir -p /mnt/carving
sudo mount /dev/loop12 /mnt/carving

# Add files of various types
echo "SECRET: Bank PIN is 4829, Password: Cobra@2026" | \
  sudo tee /mnt/carving/sensitive.txt

# Create a minimal fake JPEG (correct magic bytes)
printf '\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01' | \
  sudo tee /mnt/carving/photo.jpg > /dev/null
echo "Photo evidence data here" | sudo tee -a /mnt/carving/photo.jpg

# Create a fake PDF
printf '\x25\x50\x44\x46\x2D\x31\x2E\x34\x0A' | \
  sudo tee /mnt/carving/document.pdf > /dev/null
echo "PDF content: Confidential Report" | sudo tee -a /mnt/carving/document.pdf

# DELETE EVERYTHING — suspect trying to cover tracks
sudo rm -rf /mnt/carving/*
echo "[!] All files deleted by suspect!"

sudo umount /mnt/carving
sudo losetup -d /dev/loop12
echo "[+] Carving test image ready"

# ══════════════════════════════════════════════
# METHOD 1: FOREMOST
# ══════════════════════════════════════════════
echo "===== FOREMOST CARVING ====="
mkdir -p foremost_output
foremost -t all -i carving_test.img -o foremost_output/ -v
# -t all = carve all known file types
# -v     = verbose output

echo "--- Audit log ---"
cat foremost_output/audit.txt

echo "--- Recovered files ---"
find foremost_output/ -type f | head -20

# ══════════════════════════════════════════════
# METHOD 2: SCALPEL (more configurable)
# ══════════════════════════════════════════════
echo "===== SCALPEL CARVING ====="
sudo cp /etc/scalpel/scalpel.conf ./custom_scalpel.conf

# Uncomment txt, jpg, pdf lines in config
sed -i 's/^#\(.*\.txt.*\)/\1/' custom_scalpel.conf
sed -i 's/^#\(.*jpg.*\)/\1/' custom_scalpel.conf

mkdir -p scalpel_output
scalpel -c custom_scalpel.conf carving_test.img -o scalpel_output/
ls scalpel_output/

# ══════════════════════════════════════════════
# METHOD 3: STRINGS (fastest text extraction)
# ══════════════════════════════════════════════
echo "===== STRING EXTRACTION ====="
strings carving_test.img | grep -i "password\|PIN\|secret\|cobra\|bank"
# Instantly reveals: "SECRET: Bank PIN is 4829, Password: Cobra@2026"

# ══════════════════════════════════════════════
# METHOD 4: BINWALK (firmware/embedded carving)
# ══════════════════════════════════════════════
echo "===== BINWALK SCAN ====="
binwalk carving_test.img
# Shows offsets of all detected file signatures

echo "[+] All carving methods complete!"
```

---

## 1.5 OS Software & Basic Terminology

### 📖 Complete Terms Cheatsheet

| Term | Definition | Forensic Relevance |
|---|---|---|
| **Sector** | Smallest disk unit (512/4096 bytes) | Physical storage cell |
| **Cluster** | Group of sectors (OS allocation unit) | Smallest unit OS uses |
| **Inode** | Linux file metadata structure | Stores timestamps, owner, size |
| **MFT Entry** | Windows equivalent of inode | Per-file metadata in NTFS |
| **Slack Space** | Unused bytes at end of last cluster | Contains old file fragments |
| **Unallocated Space** | Disk space marked as free | Best place to find deleted data |
| **Partition** | Logical division of a physical disk | C: drive, D: drive, /dev/sda1 |
| **Volume** | Formatted partition with file system | NTFS volume, ext4 volume |
| **Forensic Image** | Bit-for-bit copy of disk/partition | evidence.img, evidence.E01 |
| **Hash (MD5/SHA256)** | Cryptographic fingerprint of data | Proves evidence integrity |
| **Chain of Custody** | Evidence handling audit trail | Who touched it, when, why |
| **Write Blocker** | Hardware/software preventing writes | Tableau T8-R2, software hdparm |
| **Data Carving** | Finding files by magic bytes in raw disk | Foremost, Scalpel, PhotoRec |
| **Artifacts** | Digital traces left by user/OS activity | Browser history, prefetch files |
| **Metadata** | Data about data | File size, timestamps, owner |
| **Live Forensics** | Analysis while system is running | RAM capture, active processes |
| **Dead Forensics** | Analysis of powered-off system | Disk image analysis |
| **TRIM** | SSD command that erases deleted blocks | Kills forensic recovery on SSDs |
| **EnCase (.E01)** | Professional forensic image format | Compressed + metadata + hash |
| **Raw Image (.img)** | Simple bit-for-bit dump | No compression, most compatible |
| **Timestomping** | Faking file timestamps to hide activity | MACE timestamp manipulation |
| **Anti-Forensics** | Techniques to evade forensic analysis | Wiping, encryption, steganography |

---

### 📁 Critical Forensic Artifacts by OS

#### Windows Artifacts

```
C:\Windows\Prefetch\            → Recently executed programs (.pf files)
C:\Windows\System32\winevt\     → Event Logs (Security, System, Application)
C:\Users\%USER%\AppData\Local\  → Browser history, thumbnails, recent files
C:\$Recycle.Bin\                → $I files (metadata) + $R files (content)
C:\Windows\System32\config\     → Registry hives (SAM, SYSTEM, SOFTWARE)
NTUSER.DAT                      → Per-user registry hive
%TEMP%\                         → Temp files — often contain evidence fragments
*.LNK files                     → Shortcuts revealing recently opened files
Jump Lists                      → Recent files per-application
Shellbags                       → Folder browsing history (even deleted folders!)
$MFT                            → Complete file system metadata
$LogFile                        → NTFS transaction journal
```

#### Linux Artifacts

```
/var/log/auth.log          → SSH logins, sudo usage, failed auth
/var/log/syslog            → System events
/var/log/apache2/          → Web server access + error logs
~/.bash_history            → Command-line history
~/.zsh_history             → Zsh command history
/etc/passwd + /etc/shadow  → User accounts + password hashes
/tmp/                      → Temporary files — survive many reboots
~/.ssh/                    → SSH keys, known_hosts, authorized_keys
/proc/                     → Live kernel state (PIDs, network, memory maps)
Crontab entries            → Scheduled tasks — common persistence mechanism
/var/spool/mail/           → Local mail
```

---

### 🧪 PRACTICAL 1.7 — Extracting Windows Forensic Artifacts

```bash
# Assumes you have a Windows disk image mounted

# Step 1: Mount image read-only
sudo mkdir -p /mnt/win_evidence
sudo mount -t ntfs-3g \
  -o ro,loop,uid=$(id -u),gid=$(id -g),umask=022 \
  ~/forensics-lab/images/windows_disk.img \
  /mnt/win_evidence

echo "[+] Windows image mounted read-only"

# Step 2: Parse $MFT (Master File Table)
sudo cp /mnt/win_evidence/\$MFT ~/forensics-lab/MFT_backup

# Parse with analyzeMFT
pip3 install analyzeMFT --quiet
analyzeMFT.py -f ~/forensics-lab/MFT_backup \
  -o ~/forensics-lab/mft_parsed.csv 2>/dev/null
head -5 ~/forensics-lab/mft_parsed.csv

# Step 3: Recycle Bin artifacts
echo "=== Recycle Bin Contents ==="
ls /mnt/win_evidence/\$Recycle.Bin/ 2>/dev/null

# $I files = deletion metadata
for ifile in /mnt/win_evidence/\$Recycle.Bin/S-*/\$I*; do
  echo "--- $ifile ---"
  xxd "$ifile" 2>/dev/null | head -3
  # Bytes 8-16 = original file size
  # Bytes 16-24 = deletion timestamp
  # Bytes 24+  = original file path (UTF-16)
done

# Step 4: Prefetch analysis (recently run programs)
ls /mnt/win_evidence/Windows/Prefetch/*.pf 2>/dev/null | head -15
# Filenames reveal: PROGRAM.EXE-XXXXXXXX.pf
# Inside: executable path + up to 8 volumes accessed + timestamps

# Step 5: Browser history (Chrome)
CHROME_HIST=$(find /mnt/win_evidence/Users/ \
  -name "History" \
  -path "*/Chrome/User Data/Default/*" 2>/dev/null | head -1)

if [ ! -z "$CHROME_HIST" ]; then
  cp "$CHROME_HIST" ~/forensics-lab/chrome_history.db
  sqlite3 ~/forensics-lab/chrome_history.db \
    "SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch') as visit_time,
            url, title, visit_count
     FROM urls
     ORDER BY last_visit_time DESC LIMIT 20;"
fi

# Step 6: Event log analysis
find /mnt/win_evidence/Windows/System32/winevt/ \
  -name "*.evtx" 2>/dev/null | head -10

# Parse event logs
pip3 install python-evtx --quiet
python3 -c "
import Evtx.Evtx as evtx
import Evtx.Views as e_views
import glob

for evtx_file in glob.glob('/mnt/win_evidence/Windows/System32/winevt/Logs/Security.evtx'):
    with evtx.Evtx(evtx_file) as log:
        for record in list(log.records())[-10:]:  # Last 10 events
            print(record.xml()[:300])
            print('---')
" 2>/dev/null | head -50

sudo umount /mnt/win_evidence
echo "[+] Windows artifact extraction complete"
```

---

# 📌 PART 2: Data & Evidence Recovery

---

## 2.1 Deleted File Recovery

### 🗑️ Deletion Deep Dive

> [!example] 🌍 Real World Scenario
> **Case:** A corporate spy deletes all files from a USB before surrendering it to investigators. HR needs to know what data was taken.

#### FAT32 — Before and After Deletion

```
BEFORE DELETION:
├── Directory Entry: "COBRA_P~1.TXT" → Start cluster: 45
├── FAT[45] = 46   (next cluster)
├── FAT[46] = 47   (next cluster)
├── FAT[47] = 0xFFFFFFFF  (end of file)
└── Clusters 45-47 data: "Project Cobra: Transfer $500,000..."

AFTER rm/delete:
├── Directory Entry: 0xE5OBRA_P~1.TXT  ← 0xE5 = deleted!
├── FAT[45] = 0x00  (marked free)
├── FAT[46] = 0x00  (marked free)
├── FAT[47] = 0x00  (marked free)
└── Clusters 45-47: "Project Cobra: Transfer $500,000..." ← STILL HERE!

AFTER NEW FILE OVERWRITES SAME CLUSTERS:
└── Clusters 45-47: "AAAAAAAAAAAAAAAAAAAAAAAAA..."  ← GONE FOREVER
```

#### NTFS — Before and After Deletion

```
BEFORE DELETION:
├── MFT Entry #48: [IN USE] | filename: secret.txt | clusters: 1024-1028
├── $Bitmap bits 1024-1028: 1 (used)
└── Clusters 1024-1028: "Secret financial data..."

AFTER DELETION:
├── MFT Entry #48: [NOT IN USE] | clusters: 1024-1028
├── $Bitmap bits 1024-1028: 0 (free)
└── Clusters 1024-1028: "Secret financial data..." ← STILL HERE!
```

---

### 🛠️ Recovery Tools Reference

| Tool | Platform | Type | Best For |
|---|---|---|---|
| **fls + icat** (TSK) | Linux | CLI | Precise inode-based recovery |
| **PhotoRec** | Cross-platform | CLI | Any file type, formatted disks |
| **TestDisk** | Cross-platform | CLI | Partition + directory recovery |
| **Foremost** | Linux | CLI | File carving by signature |
| **Scalpel** | Linux | CLI | Advanced, configurable carving |
| **ntfsundelete** | Linux | CLI | NTFS-specific recovery |
| **extundelete** | Linux | CLI | ext3/ext4 specific recovery |
| **Autopsy** | Cross-platform | GUI | Full forensic suite |
| **Recuva** | Windows | GUI | User-friendly quick recovery |
| **R-Studio** | Windows/Mac | GUI | Commercial, deepest recovery |

---

### 🧪 PRACTICAL 2.1 — Complete Deleted File Recovery Lab

```bash
cd ~/forensics-lab
mkdir -p recovery_lab && cd recovery_lab

# ══════════════════════════════════════════════
# SETUP: Build the crime scene
# ══════════════════════════════════════════════

# Step 1: Create a USB simulation image
dd if=/dev/zero of=suspect_usb.img bs=1M count=100
sudo losetup /dev/loop13 suspect_usb.img
sudo mkfs.vfat -F 32 /dev/loop13 -n "SUSPECT_USB"
sudo mkdir -p /mnt/suspect_usb
sudo mount /dev/loop13 /mnt/suspect_usb

# Step 2: Add incriminating files
echo "Project Cobra: Transfer \$500,000 to Account XY-9876" | \
  sudo tee /mnt/suspect_usb/financial_plan.txt

echo "Compromised accounts:" | sudo tee /mnt/suspect_usb/targets.txt
echo "admin@company.com : Admin@2024" | sudo tee -a /mnt/suspect_usb/targets.txt
echo "ceo@company.com : CEO#Secure99" | sudo tee -a /mnt/suspect_usb/targets.txt

sudo mkdir /mnt/suspect_usb/exfil
echo "Customer DB: 50,000 records exported on 2026-03-15" | \
  sudo tee /mnt/suspect_usb/exfil/export_log.txt

# Step 3: Suspect deletes everything!
sudo rm -rf /mnt/suspect_usb/*
echo "[!] Suspect deleted all files!"
ls /mnt/suspect_usb   # Empty

sudo umount /mnt/suspect_usb
sudo losetup -d /dev/loop13

# ══════════════════════════════════════════════
# EVIDENCE ACQUISITION — ALWAYS DO THIS FIRST
# ══════════════════════════════════════════════

# Hash the image BEFORE doing anything
md5sum suspect_usb.img    | tee suspect_usb_md5.txt
sha256sum suspect_usb.img | tee suspect_usb_sha256.txt
echo "[+] Chain of custody hash recorded"

# ══════════════════════════════════════════════
# RECOVERY METHOD 1: TSK (fls + icat) — PRECISE
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 1: Sleuth Kit Recovery"
echo "==============================="

# List ALL entries including deleted
echo "--- All files (deleted marked with *) ---"
fls -r -d suspect_usb.img

# Create output directory
mkdir -p tsk_recovered

# Recover each deleted file
fls -r -d suspect_usb.img | while read entry; do
  # Check for deleted files (* prefix)
  if echo "$entry" | grep -q '^\*\|r/r \*\|d/d \*'; then
    inode=$(echo "$entry" | grep -oP '\d+(?=:)')
    fname=$(echo "$entry" | sed 's/.*:\s*//' | tr '/' '_')
    if [ ! -z "$inode" ] && [ ! -z "$fname" ]; then
      echo "[+] Recovering inode $inode → $fname"
      icat suspect_usb.img "$inode" > "tsk_recovered/${fname}" 2>/dev/null
    fi
  fi
done

echo "--- Recovered files ---"
ls -la tsk_recovered/
echo "--- Content of financial_plan.txt ---"
cat tsk_recovered/financial_plan.txt 2>/dev/null
echo "--- Content of targets.txt ---"
cat tsk_recovered/targets.txt 2>/dev/null

# ══════════════════════════════════════════════
# RECOVERY METHOD 2: PhotoRec — CARVING
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 2: PhotoRec Carving"
echo "==============================="

mkdir -p photorec_output

# Interactive mode (recommended):
# photorec suspect_usb.img
# → Select: No partition
# → Select: FAT32
# → Search

# Scripted/CLI mode:
photorec /log \
  /d photorec_output/ \
  /cmd suspect_usb.img \
  partition_none,fileopt,enable,txt,search 2>/dev/null || \
echo "[!] Run: photorec suspect_usb.img  (interactive)"

echo "--- PhotoRec output ---"
find photorec_output/ -type f 2>/dev/null | head -10

# ══════════════════════════════════════════════
# RECOVERY METHOD 3: strings — INSTANT TEXT
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 3: String Extraction"
echo "==============================="

echo "--- Sensitive strings found in image ---"
strings suspect_usb.img | grep -iE \
  "password|cobra|project|transfer|account|company|export|confidential"

# ══════════════════════════════════════════════
# RECOVERY METHOD 4: Foremost — CARVING
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 4: Foremost Carving"
echo "==============================="

mkdir -p foremost_output
foremost -t all -i suspect_usb.img -o foremost_output/ -q
echo "--- Foremost audit ---"
cat foremost_output/audit.txt 2>/dev/null

echo ""
echo "[+] ALL RECOVERY METHODS COMPLETE"
echo "[+] Suspect data is NOT gone — evidence recovered!"
```

---

### 🧪 PRACTICAL 2.2 — NTFS Deleted File Recovery

```bash
cd ~/forensics-lab/recovery_lab

# ── SETUP ──
dd if=/dev/zero of=ntfs_evidence.img bs=1M count=100
sudo losetup /dev/loop14 ntfs_evidence.img
sudo mkfs.ntfs -Q /dev/loop14
sudo mkdir -p /mnt/ntfs_lab
sudo mount -t ntfs-3g /dev/loop14 /mnt/ntfs_lab

echo "NTFS Secret: Merger target = CompanyXYZ" | \
  sudo tee /mnt/ntfs_lab/merger_memo.txt
echo "Credentials: admin:MergerPass#2026" | \
  sudo tee /mnt/ntfs_lab/creds.txt

# Delete files
sudo rm /mnt/ntfs_lab/merger_memo.txt /mnt/ntfs_lab/creds.txt

sudo umount /mnt/ntfs_lab
sudo losetup -d /dev/loop14
echo "[+] NTFS evidence image ready"

# ── NTFS RECOVERY ──

# Method 1: ntfsundelete — NTFS-specific
echo "=== ntfsundelete scan ==="
ntfsundelete ntfs_evidence.img --scan
# Shows files with % recoverability

echo "=== Recovering all deleted files ==="
mkdir -p ntfs_recovered
ntfsundelete ntfs_evidence.img \
  --undelete \
  --match '*' \
  --destination ntfs_recovered/

ls -la ntfs_recovered/
cat ntfs_recovered/merger_memo.txt 2>/dev/null
cat ntfs_recovered/creds.txt 2>/dev/null

# Method 2: TSK on NTFS
echo "=== TSK on NTFS ==="
fls -r -d -f ntfs ntfs_evidence.img

# Get inode of deleted file and recover
INODE=$(fls -r -d -f ntfs ntfs_evidence.img | grep "creds" | grep -oP '\d+(?=:)')
[ ! -z "$INODE" ] && icat -f ntfs ntfs_evidence.img $INODE > tsk_creds.txt
cat tsk_creds.txt 2>/dev/null

echo "[+] NTFS recovery complete!"
```

---

## 2.2 Formatted Partition Recovery

### 💽 Types of Formatting — What Gets Destroyed?

> [!example] 🌍 Real World Scenario
> **Case:** A disgruntled employee quick-formats the company laptop before returning it, believing all evidence of data theft is gone.

```
┌─────────────────────────────────────────────────────────────┐
│                  WHAT FORMATTING DESTROYS                   │
├──────────────────────────┬──────────────────────────────────┤
│ FORMAT TYPE              │ WHAT SURVIVES                    │
├──────────────────────────┼──────────────────────────────────┤
│ Quick Format             │ ALL DATA in clusters survives    │
│ (Windows default)        │ Only FAT/MFT rewritten           │
│                          │ Recovery: 80-100% possible       │
├──────────────────────────┼──────────────────────────────────┤
│ Full Format (Vista+)     │ Data overwritten with zeros      │
│                          │ Recovery: Very difficult         │
├──────────────────────────┼──────────────────────────────────┤
│ dd if=/dev/zero          │ Complete zero fill               │
│ (Zero wipe)              │ Recovery: Impossible             │
├──────────────────────────┼──────────────────────────────────┤
│ DoD 5220.22-M            │ 7-pass overwrite                 │
│ (Secure wipe)            │ Recovery: Impossible             │
└──────────────────────────┴──────────────────────────────────┘
```

---

### 🔄 How Recovery Works on Formatted Drive

```
QUICK-FORMATTED DISK STATE:
├── Partition Table:    EXISTS (usually intact)
├── FAT/MFT:            CLEARED (new blank tables)
├── Data clusters:      COMPLETELY INTACT
└── Recovery strategy:
    ├── Method 1: Find backup partition structures
    ├── Method 2: Scan raw disk for directory signatures
    └── Method 3: Carve by magic bytes (no file system needed)
```

---

### 🧪 PRACTICAL 2.3 — Formatted Disk Recovery with TestDisk

```bash
cd ~/forensics-lab/recovery_lab

# ══════════════════════════════════════════════
# SETUP: Create and quick-format a disk
# ══════════════════════════════════════════════

# Step 1: Create disk with valuable data
dd if=/dev/zero of=formatted_disk.img bs=1M count=150
sudo losetup -P /dev/loop15 formatted_disk.img

sudo parted /dev/loop15 --script \
  mklabel msdos \
  mkpart primary fat32 1MiB 75MiB \
  mkpart primary fat32 75MiB 150MiB

sudo mkfs.vfat -F 32 /dev/loop15p1 -n "EVIDENCE1"
sudo mkfs.vfat -F 32 /dev/loop15p2 -n "EVIDENCE2"

sudo mkdir -p /mnt/evid1 /mnt/evid2
sudo mount /dev/loop15p1 /mnt/evid1
sudo mount /dev/loop15p2 /mnt/evid2

# Add evidence files
echo "MERGER DOCS: CompanyABC acquisition price = \$2.5 billion" | \
  sudo tee /mnt/evid1/merger_confidential.txt
echo "Wire transfer: Account CH56-0483-5012-3456 | \$500,000" | \
  sudo tee /mnt/evid1/wire_transfer.txt

for i in {1..5}; do
  echo "Exfiltrated document $i — Customer PII data" | \
    sudo tee /mnt/evid2/exfil_doc_$i.txt
done

echo "Recorded on 2026-03-15 at 14:32 IST" | \
  sudo tee /mnt/evid2/access_log.txt

sudo umount /mnt/evid1 /mnt/evid2

# Step 2: Simulate employee QUICK-FORMATTING the drive
echo "[!] Employee quick-formatting drive to hide evidence..."
sudo mkfs.vfat -F 32 /dev/loop15p1 -n "BLANK_DISK"
echo "[!] Format complete — employee thinks data is gone!"

sudo losetup -d /dev/loop15
echo "[+] Formatted evidence image ready"

# ══════════════════════════════════════════════
# HASH THE IMAGE (Chain of Custody)
# ══════════════════════════════════════════════
sha256sum formatted_disk.img | tee formatted_disk_sha256.txt
echo "[+] Image hash recorded"

# ══════════════════════════════════════════════
# RECOVERY METHOD 1: TestDisk (Interactive)
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 1: TestDisk"
echo "==============================="
echo ""
echo "TestDisk walkthrough (run interactively):"
echo "  testdisk formatted_disk.img"
echo ""
echo "  Navigation:"
echo "  1. No Log"
echo "  2. Select: [formatted_disk.img]"
echo "  3. Partition Table: [Intel] (MBR)"
echo "  4. [Analyse]"
echo "  5. [Quick Search]"
echo "  6. Found partitions listed — press P to list files"
echo "  7. Navigate to files, press C to copy"
echo "  8. Select destination: ~/forensics-lab/recovery_lab/testdisk_output/"
echo ""

mkdir -p testdisk_output
# Run TestDisk (semi-automated log mode):
echo "testdisk /log formatted_disk.img" > run_testdisk.sh
chmod +x run_testdisk.sh
echo "[+] Run: sudo testdisk formatted_disk.img"

# ══════════════════════════════════════════════
# RECOVERY METHOD 2: PhotoRec (most reliable)
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 2: PhotoRec on Formatted"
echo "==============================="

mkdir -p photorec_formatted

# PhotoRec doesn't care about file system — pure carving
photorec /log \
  /d photorec_formatted/ \
  /cmd formatted_disk.img \
  partition_none,fileopt,enable,txt,search 2>/dev/null || \
echo "[!] Run: photorec formatted_disk.img  (interactive)"

echo "--- Files recovered after format ---"
find photorec_formatted/ -type f 2>/dev/null | head -20

# Verify content survived formatting
grep -r "MERGER\|merger\|wire transfer\|exfil\|CompanyABC" \
  photorec_formatted/ 2>/dev/null | head -10

# ══════════════════════════════════════════════
# RECOVERY METHOD 3: Foremost Carving
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 3: Foremost on Formatted"
echo "==============================="

mkdir -p foremost_formatted
foremost -t txt,pdf,jpg,png \
  -i formatted_disk.img \
  -o foremost_formatted/ -q

cat foremost_formatted/audit.txt 2>/dev/null

# ══════════════════════════════════════════════
# RECOVERY METHOD 4: Strings — Quick Win
# ══════════════════════════════════════════════
echo ""
echo "==============================="
echo "METHOD 4: String Extraction"
echo "==============================="
strings formatted_disk.img | grep -iE \
  "merger|wire|transfer|exfil|account|confidential|billion|customer"

echo ""
echo "[+] Formatted disk recovery complete!"
echo "[+] Quick-format does NOT destroy data!"
```

---

### 🧪 PRACTICAL 2.4 — Lost Partition Recovery

```bash
cd ~/forensics-lab/recovery_lab

# ── SCENARIO: Corrupted/Deleted Partition Table ──

dd if=/dev/zero of=lost_partition.img bs=1M count=150
sudo losetup -P /dev/loop16 lost_partition.img

sudo parted /dev/loop16 --script \
  mklabel msdos \
  mkpart primary ntfs 1MiB 150MiB

sudo mkfs.ntfs -Q /dev/loop16p1
sudo mkdir -p /mnt/lost_ntfs
sudo mount -t ntfs-3g /dev/loop16p1 /mnt/lost_ntfs

echo "Critical Witness Statement" | sudo tee /mnt/lost_ntfs/witness.txt
echo "Transaction IDs: TX-001, TX-002, TX-003" | sudo tee /mnt/lost_ntfs/txids.txt

sudo umount /mnt/lost_ntfs

# CORRUPT partition table (simulate attack or accidental damage)
sudo dd if=/dev/zero of=/dev/loop16 bs=512 count=1
echo "[!] Partition table CORRUPTED — disk appears empty!"

sudo fdisk -l /dev/loop16  # Should show: unrecognized partition

sudo losetup -d /dev/loop16
echo "[+] Corrupted image ready"

# ── RECOVERY WITH TESTDISK ──
echo ""
echo "=== TestDisk Partition Recovery ==="
echo ""
echo "Steps to run interactively:"
echo "  sudo testdisk lost_partition.img"
echo ""
echo "  1. Create log → No Log"
echo "  2. Disk → Select lost_partition.img"
echo "  3. Partition type → [Intel] MBR"
echo "  4. [Analyse]"
echo "  5. [Quick Search]"
echo "     → TestDisk finds: P NTFS 1-19 start=2048 size=..."
echo "  6. Press ENTER to confirm found partition"
echo "  7. [Write] → Confirm Y → Enter"
echo "  8. Partition table reconstructed!"
echo ""

# After TestDisk rewrites partition table, remount:
sudo losetup -P /dev/loop17 lost_partition.img
sudo mount -t ntfs-3g -o ro /dev/loop17p1 /mnt/recovered_part 2>/dev/null

if [ $? -eq 0 ]; then
  echo "=== Files recovered after partition reconstruction ==="
  ls /mnt/recovered_part/
  cat /mnt/recovered_part/witness.txt 2>/dev/null
  sudo umount /mnt/recovered_part
fi

sudo losetup -d /dev/loop17 2>/dev/null
echo "[+] Partition recovery complete!"
```

---

### 🧪 PRACTICAL 2.5 — Bulk Extractor (Deep Artifact Mining)

```bash
cd ~/forensics-lab

# Bulk Extractor scans raw disk images and extracts:
# - Email addresses
# - URLs and domains
# - Credit card numbers
# - Phone numbers
# - GPS coordinates
# - Encryption artifacts
# - Browser history fragments

mkdir -p bulk_output

# Run bulk_extractor on any forensic image
bulk_extractor \
  -o bulk_output/ \
  -E email \
  -E url \
  -E domain \
  -E ccn \
  -E telephone \
  -E find \
  recovery_lab/suspect_usb.img

# Review extracted artifacts
echo "=== Email addresses found ==="
cat bulk_output/email.txt 2>/dev/null | grep -v "^#" | head -15

echo "=== URLs found ==="
cat bulk_output/url.txt 2>/dev/null | grep -v "^#" | head -15

echo "=== Domain names ==="
cat bulk_output/domain.txt 2>/dev/null | grep -v "^#" | head -15

echo "=== Phone numbers ==="
cat bulk_output/telephone.txt 2>/dev/null | grep -v "^#" | head -10

echo "=== Histogram (most-seen domains) ==="
cat bulk_output/url_histogram.txt 2>/dev/null | head -10

echo "[+] Bulk extraction complete!"
```

---

### 🧪 PRACTICAL 2.6 — Memory Forensics with Volatility 3

```bash
# ── LIVE RAM CAPTURE (on running suspect machine) ──

# Method 1: avml (Microsoft Memory Acquisition)
wget -q https://github.com/microsoft/avml/releases/download/v0.11.2/avml -O /tmp/avml
chmod +x /tmp/avml
sudo /tmp/avml ~/forensics-lab/ram_dump.lime
echo "[+] RAM captured"

# Method 2: /dev/mem (limited on modern kernels with CONFIG_STRICT_DEVMEM)
sudo dd if=/dev/mem of=~/forensics-lab/ram_dump.img bs=1M 2>/dev/null

# ── ANALYSIS WITH VOLATILITY 3 ──

RAM=~/forensics-lab/ram_dump.lime

# Step 1: Identify OS
vol3 -f $RAM windows.info 2>/dev/null
vol3 -f $RAM linux.bash 2>/dev/null

# Step 2: Running processes
vol3 -f $RAM windows.pslist     # Process list
vol3 -f $RAM windows.pstree     # Process tree (shows parent-child)
vol3 -f $RAM windows.psscan     # Hidden process scan (rootkit detection!)

# Step 3: Network connections at capture time
vol3 -f $RAM windows.netstat

# Step 4: Command line history of all processes
vol3 -f $RAM windows.cmdline

# Step 5: Find injected DLLs / hollowed processes
vol3 -f $RAM windows.malfind

# Step 6: Dump suspicious process (e.g., PID 1234)
mkdir -p ~/forensics-lab/process_dumps
vol3 -f $RAM windows.dumpfiles --pid 1234 \
  --dump-dir ~/forensics-lab/process_dumps/

# Step 7: Extract credentials from memory
vol3 -f $RAM windows.cachedump   # Cached domain credentials
vol3 -f $RAM windows.lsadump     # LSA secrets
vol3 -f $RAM windows.hashdump    # SAM database hashes

# Step 8: Quick string search in RAM
strings $RAM | grep -iE "password|login|secret|apikey|token" | head -20

echo "[+] Memory forensics complete!"
```

---

## 📊 Complete Forensics Toolkit Reference

```
┌──────────────────────────────────────────────────────────────┐
│                  FORENSICS TOOL MATRIX                       │
├───────────────────────┬──────────────────────────────────────┤
│ TASK                  │ TOOL(S)                              │
├───────────────────────┼──────────────────────────────────────┤
│ Disk Imaging          │ dc3dd, dcfldd, dd, FTK Imager        │
│ Hash Verification     │ md5sum, sha256sum, hashdeep           │
│ Partition Analysis    │ mmls, fdisk -l, parted               │
│ File System Info      │ fsstat, mminfo, blkid                │
│ List + Deleted Files  │ fls (TSK), Autopsy                   │
│ Recover by Inode      │ icat (TSK)                           │
│ File Carving          │ foremost, scalpel, photorec          │
│ Partition Recovery    │ testdisk                             │
│ NTFS Recovery         │ ntfsundelete, Autopsy                │
│ ext4 Recovery         │ extundelete, PhotoRec                │
│ Artifact Mining       │ bulk_extractor                       │
│ Memory Analysis       │ volatility3, strings                 │
│ Timeline Creation     │ mactime (TSK), log2timeline          │
│ Hex Analysis          │ xxd, hexedit, hexdump, 010 Editor    │
│ Metadata Extraction   │ exiftool, mediainfo                  │
│ Full GUI Suite        │ Autopsy, Sleuth Kit                  │
│ String Searching      │ strings, grep, bulk_extractor        │
│ Steganography         │ steghide, binwalk, stegsolve         │
│ Event Log Parsing     │ python-evtx, chainsaw, hayabusa      │
└───────────────────────┴──────────────────────────────────────┘
```

---

## 🎯 Quick Revision — Key Points for Exam

> [!summary] 🔑 Must-Remember Points
>
> **Fundamentals:**
> 1. Cyber Forensics = Identify → Preserve → Analyze → Present
> 2. Chain of Custody = audit trail of who handled evidence
> 3. Always hash BEFORE and AFTER imaging (MD5/SHA256)
> 4. NEVER work on original — always use forensic image copy
> 5. Volatile evidence (RAM) must be captured BEFORE disk imaging
>
> **Storage:**
> 6. Sector = smallest physical unit (512 or 4096 bytes)
> 7. Cluster = group of sectors (smallest OS allocation unit)
> 8. Slack Space = unused bytes in last cluster — contains old file fragments
> 9. SSD + TRIM = near-instant destruction of deleted data
>
> **File Systems:**
> 10. FAT32 deletion → first byte of filename becomes `0xE5`, FAT entries → `0x00`
> 11. NTFS deletion → MFT entry "not in use", $Bitmap bits cleared
> 12. Data clusters UNTOUCHED in both cases — **deletion ≠ destruction**
> 13. MACE timestamps = Modified, Accessed, Changed, Entry Modified
> 14. ADS = Alternate Data Streams — hidden data in NTFS files
>
> **Recovery:**
> 15. Quick format = only FAT/MFT rewritten — ALL data recoverable
> 16. Full format (Vista+) = zeros written — very hard to recover
> 17. Data carving = find files by magic bytes (no file system needed)
> 18. PhotoRec, Foremost, Scalpel = file carving tools
> 19. TestDisk = partition table reconstruction
> 20. `strings` = fastest way to extract readable text from raw images

---

## 🔗 Related Notes

- [[Active Directory Forensics]]
- [[Network Traffic Analysis with Wireshark]]
- [[Malware Analysis Basics]]
- [[VAPT Methodology]]
- [[Incident Response Playbook]]
- [[Memory Forensics — Volatility Cheatsheet]]

---

*Notes by: HeXx | Last Updated: 2026-03-17 | Status: Complete with Practicals*
