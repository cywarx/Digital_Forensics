---
tags:
  - cyber-forensics
  - keywords
  - glossary
  - definitions
  - unit-4
aliases:
  - Forensics Keywords
  - Forensics Glossary
  - Cyber Forensics Terms
date: 2026-03-17
status: complete
---

# 🔑 Cyber Forensics — Keywords & Glossary
> [!abstract] About This File
> Every important keyword from Unit IV explained in the **simplest possible way** with **real-world analogies** so you never forget what they mean.
> Arranged alphabetically with examples, forensic context, and related terms.

---

## 🗂️ Quick Index

| #   | Keyword                                | One-Line Summary                                   |
| --- | -------------------------------------- | -------------------------------------------------- |
| 1   | [[#Acquisition]]                       | First step — grabbing the evidence safely          |
| 2   | [[#Allocated Space]]                   | Space actively used by files                       |
| 3   | [[#Alternate Data Stream (ADS)]]       | NTFS's secret hiding place inside files            |
| 4   | [[#Artifact]]                          | Digital breadcrumb left by user or system          |
| 5   | [[#Bitmap Bits]]                       | The "available seats" chart of your disk           |
| 6   | [[#Bit-for-Bit Forensic Image]]        | A perfect clone of storage, byte by byte           |
| 7   | [[#Chain of Custody]]                  | The evidence diary — who touched what and when     |
| 8   | [[#Chronological Timeline]]            | Plotting all events in time order                  |
| 9   | [[#Cluster]]                           | The smallest chunk the OS can allocate             |
| 10  | [[#Data Carving]]                      | Finding files in raw bytes without a file system   |
| 11  | [[#Dead Forensics]]                    | Analyzing a powered-OFF device                     |
| 12  | [[#Deleted File]]                      | A file marked "gone" but still physically present  |
| 13  | [[#Evidence Integrity]]                | Proof the evidence was never modified              |
| 14  | [[#FAT Table (File Allocation Table)]] | FAT32's linked-list index of file locations        |
| 15  | [[#File Signature (Magic Bytes)]]      | A file's secret identity tag at byte 0             |
| 16  | [[#File Slack]]                        | Wasted space between file end and cluster end      |
| 17  | [[#Forensic Image]]                    | See Bit-for-Bit Forensic Image                     |
| 18  | [[#Hash (MD5 / SHA256)]]               | A digital fingerprint for files and disks          |
| 19  | [[#Inode]]                             | Linux/ext4's per-file identity card                |
| 20  | [[#Live Forensics]]                    | Analyzing a powered-ON running device              |
| 21  | [[#Logical Copy]]                      | Copy of just the files (NOT a forensic image)      |
| 22  | [[#Magnetic Polarity]]                 | How HDDs physically store 0s and 1s                |
| 23  | [[#MFT (Master File Table)]]           | NTFS's complete file directory — the spine         |
| 24  | [[#Mount]]                             | Attaching a disk/image so the OS can read it       |
| 25  | [[#Partition]]                         | A logical section of a physical disk               |
| 26  | [[#Seizure]]                           | The legal act of taking evidence                   |
| 27  | [[#Sector]]                            | Smallest physical unit on a disk (512B or 4KB)     |
| 28  | [[#Slack Space]]                       | All unused hidden space on a disk                  |
| 29  | [[#Steganography]]                     | Hiding secret data inside innocent files           |
| 30  | [[#Timestomping]]                      | Attacker faking file timestamps                    |
| 31  | [[#TRIM]]                              | SSD's self-cleaning command that destroys evidence |
| 32  | [[#TSK (The Sleuth Kit)]]              | The most important forensics CLI toolkit           |
| 33  | [[#Unallocated Space]]                 | "Free" disk space — graveyard of deleted files     |
| 34  | [[#Volatile Data]]                     | Data that disappears when power is cut             |
| 35  | [[#Volume Shadow Copy (VSS)]]          | Windows' automatic snapshots of files              |
| 36  | [[#Write Blocker]]                     | Hardware/software that prevents evidence tampering |

---

---

## A

---

### Acquisition

> [!tip] Simple Definition
> **Acquisition** = The process of making a safe, verified copy of a storage device to use as evidence — without touching or changing the original.

**Real World Example:**
Imagine a suspect's phone is found at a crime scene. A detective doesn't scroll through the phone directly — they use a **forensic tool to make an exact copy** of the phone's storage onto an evidence drive. That copy is the **acquired image**. The original phone goes into an evidence bag, sealed.

**In Practice (Kali Linux):**
```bash
# Acquire a USB drive to an image file
dcfldd if=/dev/sdb \
       of=/cases/evidence.img \
       hash=sha256 \
       hashlog=/cases/hash.log

# 'if' = input (the suspect device)
# 'of' = output (the image file)
# hash = live verification during copy
```

**Why It Matters:**
- Any analysis must be done on the **acquired copy**, never the original
- Acquisition must be done with a **write blocker** to prevent contamination
- The moment acquisition is done, you hash it — that hash is your **evidence seal**

**Related:** [[#Write Blocker]], [[#Hash (MD5 / SHA256)]], [[#Bit-for-Bit Forensic Image]]

---

### Allocated Space

> [!tip] Simple Definition
> **Allocated Space** = Disk space that is currently in use by an active file. The OS has "reserved" these clusters for the file.

**Real World Example:**
Think of a hotel. **Allocated space** = rooms that are currently booked by guests. The room is occupied, the booking exists, and you can't give it to someone else.

```
Disk visualization:
┌────────────────────────────────────────────────┐
│  [FILE A]  [FILE B]  [FREE]  [FILE C]  [FREE]  │
│ allocated  allocated  unalloc  allocated  unalloc│
└────────────────────────────────────────────────┘
```

**Forensic Note:**
- Active files live in allocated space
- **Unallocated space** is where deleted files hide
- Allocated + Unallocated = Total disk capacity

**Related:** [[#Unallocated Space]], [[#Cluster]]

---

### Alternate Data Stream (ADS)

> [!tip] Simple Definition
> **ADS** = A hidden extra data channel that NTFS allows to be attached to any file. The main file looks normal, but extra secret data is hidden in a parallel "stream."

**Real World Example:**
Imagine a letter (the main file). Inside the envelope there's a secret compartment (ADS) where you can hide another note. Anyone who just reads the letter sees nothing unusual — but the hidden note is still there.

**Attacker's Use:**
```bash
# Hide a malware payload inside a normal text file
echo "MALWARE_CODE_HERE" > invoice.txt:malware.exe

# Normal view:
ls -la invoice.txt      # Shows: 0 bytes (!!!)
cat invoice.txt         # Shows: original content only

# Forensic detection:
dir /r invoice.txt      # Windows — shows ALL streams
fls image.img | grep ":"  # Kali — shows ADS entries
```

**What to look for:**
```
Normal:    invoice.txt
Suspicious: invoice.txt:Zone.Identifier    ← normal (download marker)
Very Sus:   invoice.txt:payload.exe        ← MALWARE hiding here!
            invoice.txt:config             ← C2 config hidden here!
```

> [!warning] Forensic Red Flag
> Any ADS stream with a `.exe`, `.dll`, `.bat`, `.ps1`, or `.vbs` name is a serious red flag. Real malware (like APT groups) regularly uses ADS to hide payloads on victim machines.

**Related:** [[#MFT (Master File Table)]], [[#TSK (The Sleuth Kit)]]

---

### Artifact

> [!tip] Simple Definition
> **Artifact** = Any digital trace left behind by a user's activity or the operating system. Like a footprint in the sand — you didn't mean to leave it, but it's there.

**Real World Example:**
When you walk through sand at a beach, you leave **footprints** — you didn't mean to create evidence, but they tell the story of where you walked. Digital artifacts work the same way.

**Common Windows Artifacts:**
| Artifact | Location | What It Reveals |
|---|---|---|
| Prefetch files | `C:\Windows\Prefetch\` | Which programs ran & when |
| Event Logs | `C:\Windows\System32\winevt\` | Logins, errors, new services |
| Browser History | `AppData\...\History` | What websites were visited |
| LNK Files | `C:\Users\...\Recent\` | Which files were recently opened |
| Jump Lists | `AppData\...\AutomaticDestinations` | Files per-application recently used |
| USB History | `HKLM\SYSTEM\...\USBSTOR` | Every USB ever plugged in |
| `$Recycle.Bin` | `C:\$Recycle.Bin\` | Deleted files + exact deletion time |

**Related:** [[#Chronological Timeline]], [[#MFT (Master File Table)]]

---

## B

---

### Bitmap Bits

> [!tip] Simple Definition
> **Bitmap** = A map of every cluster on the disk, where each bit says either **"1 = in use"** or **"0 = free."** The OS checks this before writing anything new.

**Real World Example:**
Think of a **cinema seating chart**. Every seat has a status:
- 🟢 = Empty (available) → `0` in the bitmap
- 🔴 = Occupied (in use) → `1` in the bitmap

When you buy a ticket, the system flips your seat from `0` → `1`. When you leave, it flips back to `0`. Same thing happens on a disk.

```
Bitmap visualization (each bit = one cluster):

Cluster:  1  2  3  4  5  6  7  8  9  10
Bitmap:   1  1  1  0  0  1  0  0  1  1
           ↑  ↑  ↑        ↑        ↑  ↑
         FILE A        FILE B    FILE C

Clusters 4, 5, 7, 8 = FREE → This is where deleted file data lives!
```

**When a File is Deleted:**
1. OS flips the file's cluster bits from `1` → `0`
2. Clusters now appear "free" in the bitmap
3. BUT the actual data in those clusters is **untouched**
4. This is why deleted files are recoverable!

**NTFS Bitmap file:** `$Bitmap` (a special MFT entry)
**FAT32 equivalent:** The FAT table entries (0x00 = free)

```bash
# View bitmap status with Sleuth Kit
fsstat image.img | grep -i "bitmap\|free"
```

**Related:** [[#FAT Table (File Allocation Table)]], [[#MFT (Master File Table)]], [[#Unallocated Space]]

---

### Bit-for-Bit Forensic Image

> [!tip] Simple Definition
> **Bit-for-bit forensic image** = An exact byte-perfect copy of an entire storage device — including empty space, deleted files, hidden sectors, and everything else. Not just the files, but **every single bit** on the disk.

**Real World Example:**
Normal file copy = Photocopying only the text on a page.
Bit-for-bit image = A **complete replication of the entire paper** — including the invisible ink, the watermark, the paper texture, the blank margins, and the pencil marks that were erased.

**Normal copy vs Forensic Image:**
```
┌──────────────────────────────────────────────────────┐
│              NORMAL COPY (xcopy/cp)                  │
│  Copies: Active files and folders only               │
│  Misses: Deleted files, slack space, MFT entries,   │
│          unallocated space, bad sectors, metadata    │
├──────────────────────────────────────────────────────┤
│           BIT-FOR-BIT FORENSIC IMAGE (dd/dcfldd)    │
│  Copies: Sector 0 to last sector — EVERYTHING        │
│  Includes: Deleted files, slack space, MFT, bad     │
│            sectors (padded with 0s), all metadata    │
└──────────────────────────────────────────────────────┘
```

**Creating one on Kali:**
```bash
# dd = basic bit-for-bit
dd if=/dev/sdb of=evidence.img bs=512 conv=noerror,sync

# dcfldd = dd + live hashing (preferred in forensics)
dcfldd if=/dev/sdb of=evidence.img \
       hash=sha256 \
       hashlog=hash.log \
       bs=4096 \
       conv=noerror,sync

# Verify — both hashes MUST match
sha256sum /dev/sdb > original.hash
sha256sum evidence.img > image.hash
diff original.hash image.hash   # No output = perfect match
```

**Common Image Formats:**
| Format | Extension | Notes |
|---|---|---|
| Raw/DD | `.img`, `.raw`, `.dd` | Simplest, no compression |
| EnCase | `.E01` | Industry standard, compressed, includes metadata |
| AFF | `.aff` | Open source, compressed |

**Related:** [[#Acquisition]], [[#Hash (MD5 / SHA256)]], [[#Write Blocker]]

---

## C

---

### Chain of Custody

> [!tip] Simple Definition
> **Chain of Custody** = A complete, unbroken written record of **who handled the evidence, when they handled it, what they did with it, and where it was stored** — from the moment of seizure to the courtroom.

**Real World Example:**
Think of a **blood sample** taken at a crime scene. A chain of custody log tracks:
- Nurse A collected it at 2:00 PM
- Officer B transported it at 2:30 PM
- Lab Tech C received it at 3:15 PM
- Analyst D ran tests at 4:00 PM

If this chain breaks (e.g., the sample sat unattended for 2 hours with no log), a defense lawyer can argue: **"Anyone could have tampered with it."** The evidence becomes inadmissible.

**Digital Chain of Custody Document:**
```
════════════════════════════════════════
    CHAIN OF CUSTODY FORM
════════════════════════════════════════
Case Number    : CASE-2026-001
Evidence Item  : USB Drive — Kingston 32GB
Seized From    : John Smith's desk drawer
Seized By      : Investigator HeXx
Date/Time      : 2026-03-17  10:30 AM
Hash (SHA256)  : a1b2c3d4e5f6...

HANDLING LOG:
─────────────────────────────────────────
10:30 AM  HeXx        Seized from scene
10:45 AM  HeXx        Photographed, bagged, sealed
11:00 AM  HeXx        Transported to forensics lab
11:30 AM  HeXx        Imaged with dcfldd
11:45 AM  HeXx        Verified hash — MATCH
12:00 PM  HeXx        Placed in evidence locker #7
─────────────────────────────────────────
```

> [!warning] Break the Chain = Lose the Case
> If chain of custody is broken — even slightly — the defense can claim evidence was **planted, modified, or contaminated**. The evidence is thrown out. The case collapses.

**Related:** [[#Acquisition]], [[#Seizure]], [[#Hash (MD5 / SHA256)]]

---

### Chronological Timeline

> [!tip] Simple Definition
> **Chronological Timeline** = Arranging all digital events (file created, file accessed, file deleted, user logged in, USB plugged in, program executed) in **time order** to reconstruct exactly what happened and when.

**Real World Example:**
You're investigating a bank fraud. Instead of random clues, you build a **timeline**:
```
Timeline — Suspect's Laptop:
─────────────────────────────────────────────────────
08:45 AM  Login event (Event ID 4624)
09:02 AM  USB drive connected (USBSTOR registry key)
09:05 AM  customer_db.csv — ACCESSED (atime updated)
09:07 AM  WinSCP.exe — EXECUTED (Prefetch file)
09:09 AM  ftp_log.txt — CREATED (shows upload started)
09:22 AM  customer_db.csv — DELETED
09:24 AM  USB drive removed
09:25 AM  cmd.exe — EXECUTED (Prefetch)
09:26 AM  ftp_log.txt — DELETED
09:30 AM  Event Log CLEARED (Event ID 1102) ← Anti-forensics!
─────────────────────────────────────────────────────
```
This timeline **tells the complete story** of the crime, in order.

**Building a timeline on Kali:**
```bash
# mactime (Sleuth Kit) — generates timeline from file system
fls -r -m / image.img > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv

# Sort by date/time
sort timeline.csv | head -50

# Output format: Date | Size | Type | UID | Filename
# 2026-03-17 09:05 | 204800 | .a.. | 0 | customer_db.csv
# (dots = M.A.C.E — which timestamps changed)
```

**MACE in Timeline:**
```
M... = Only Modified time changed
.A.. = Only Accessed time changed (file was read!)
..C. = MFT entry was changed
...E = Entry modified (rename, move, delete)
MA.. = File was both modified and accessed
MACE = All 4 timestamps changed (new file created)
```

**Related:** [[#Artifact]], [[#MFT (Master File Table)]], [[#Timestomping]]

---

### Cluster

> [!tip] Simple Definition
> **Cluster** = The **minimum amount of disk space** the operating system allocates to any file, no matter how small the file is. It's made up of one or more sectors.

**Real World Example:**
Imagine hotel rooms are all suites (big rooms). You only need to stay for one night and just need a bed — but you're given the entire suite. Even if you don't use the sitting room or the extra bathroom, **you're paying for the whole suite**. That wasted space in the suite = **file slack**.

```
Cluster Size = 4096 bytes (4KB) — common on Windows NTFS

A file that is 100 bytes:
┌──────────────────────────────────────────────────┐
│  100 bytes of actual data │ 3996 bytes of SLACK  │
│  (the file content)       │ (wasted/old data!)   │
└──────────────────────────────────────────────────┘
         ← ── ── One cluster (4096 bytes) ── ── →
```

**Cluster sizes by file system:**
| File System | Default Cluster | Max Cluster |
|---|---|---|
| FAT32 | 4KB–32KB (varies) | 32KB |
| NTFS | 4KB | 2MB |
| ext4 | 4KB | 64KB |

```bash
# Check cluster size
fsstat image.img | grep -i "cluster\|block size"
# Cluster Size: 4096
```

**Related:** [[#Sector]], [[#Slack Space]], [[#File Slack]]

---

## D

---

### Data Carving

> [!tip] Simple Definition
> **Data Carving** = Scanning raw disk bytes looking for **known file headers and footers (magic bytes)** to reconstruct files — **completely ignoring the file system**. No directory listing needed.

**Real World Example:**
Imagine a shredded newspaper. Each piece is a sector of the disk. Data carving is like scanning all the pieces looking for ones that start with "**SPORTS SECTION**" (= file header) and end with "**END OF SPORTS**" (= file footer), then grabbing everything in between to reconstruct the sports section — without needing the original table of contents.

**How it works:**
```
Raw disk bytes:
...FF D8 FF E0 [JPEG DATA HERE] FF D9...FF D8 FF...
    ↑                            ↑
  JPEG HEADER                 JPEG FOOTER
  (FF D8 FF)                  (FF D9)

Carver extracts: everything between header and footer → saves as photo.jpg
```

**Common File Headers (Magic Bytes):**
```
JPEG:   FF D8 FF         footer: FF D9
PDF:    25 50 44 46      footer: 25 25 45 4F 46 (%PDF ... %%EOF)
PNG:    89 50 4E 47      footer: 49 45 4E 44 AE 42 60 82
ZIP:    50 4B 03 04      footer: 50 4B 05 06
EXE:    4D 5A (MZ)       no footer — uses max size limit
SQLite: 53 51 4C 69      no footer
```

**Tools:**
```bash
# foremost — classic carver
foremost -t jpg,pdf,zip -i disk.img -o /output/

# scalpel — faster, configurable
scalpel disk.img -o /output/

# photorec — GUI-based, very effective
photorec disk.img

# binwalk — great for firmware
binwalk -e disk.img
```

> [!warning] Key Limitation
> Carving fails on **fragmented files** because it assumes data is stored contiguously. It also **loses original filenames** — you get `file0001.jpg` instead of `vacation_photo.jpg`.

**Related:** [[#File Signature (Magic Bytes)]], [[#Unallocated Space]], [[#Slack Space]]

---

### Dead Forensics

> [!tip] Simple Definition
> **Dead Forensics** = Analyzing a device that is **powered OFF**. You image the disk and analyze the image — the system is not running.

**Real World Example:**
A suspect's laptop is seized and powered off. Investigators bring it to the lab, image the hard drive, and analyze the image file. The laptop itself is never turned on. This is **dead forensics**.

**Advantages:**
- Evidence is stable — nothing is changing
- RAM has already been lost (acceptable trade-off)
- File system is in a consistent state
- Most common type of forensics

**Disadvantages:**
- Volatile data (RAM contents) is gone forever
- Encrypted drives may be locked — no key in memory

**Contrast with [[#Live Forensics]]**

---

### Deleted File

> [!tip] Simple Definition
> A **deleted file** is a file where the OS has removed the "pointer" (directory entry or MFT record) and marked the clusters as "available" — but the actual data bytes are **still physically on the disk**.

**Real World Example:**
Imagine a whiteboard with a list of library books. A "deleted" book = you erase the book's name from the list, but the actual book is **still on the shelf**. Anyone who knows where to look can still find it. Only when a new book takes that shelf space is the old one truly gone.

**Lifecycle of a deleted file:**
```
Step 1: File exists
        MFT entry: "IN USE"  |  FAT: clusters assigned  |  Data: on disk

Step 2: User presses DELETE
        MFT entry: "NOT IN USE"  |  FAT: clusters = 0x00 (free)  |  Data: STILL ON DISK

Step 3: Recovery window (most important time!)
        File data = recoverable with fls, icat, PhotoRec etc.

Step 4: New file written to same clusters
        Data OVERWRITTEN → Recovery becomes impossible or partial

Step 5: Secure wipe
        Data overwritten multiple times → Not recoverable
```

```bash
# Find deleted files
fls -r -d image.img
# * = deleted (the asterisk is the key!)

# Extract a deleted file by inode
icat image.img 42 > recovered_file.jpg
```

**Related:** [[#Unallocated Space]], [[#Bitmap Bits]], [[#MFT (Master File Table)]]

---

## E

---

### Evidence Integrity

> [!tip] Simple Definition
> **Evidence Integrity** = Proof that digital evidence has **not been modified** since it was collected. Verified using cryptographic hash values (MD5/SHA256).

**Real World Example:**
Imagine you seal a bag of flour and put a **wax seal** with your fingerprint on it. Later, if the wax seal is unbroken and matches your fingerprint, you know no one tampered with the bag. A **hash value** is the digital equivalent of that wax seal.

**How hash verification works:**
```bash
# Step 1: Hash the original BEFORE imaging
sha256sum /dev/sdb
# Output: a1b2c3d4... /dev/sdb   ← THE SEAL

# Step 2: Image the drive
dcfldd if=/dev/sdb of=evidence.img hash=sha256

# Step 3: Hash the image
sha256sum evidence.img
# Output: a1b2c3d4... evidence.img   ← SAME HASH = UNTAMPERED

# Step 4: Six months later in court — re-verify
sha256sum evidence.img
# Must STILL be: a1b2c3d4...
# If different: evidence was tampered with → case dismissed!
```

> [!danger] Hash Mismatch = Game Over
> If the hash of the image doesn't match the hash of the original, the evidence is inadmissible. The entire case can collapse. This is why hash verification is **step 1 and final step** of every forensic investigation.

**Related:** [[#Hash (MD5 / SHA256)]], [[#Chain of Custody]], [[#Bit-for-Bit Forensic Image]]

---

## F

---

### FAT Table (File Allocation Table)

> [!tip] Simple Definition
> **FAT (File Allocation Table)** = FAT32's index that tracks **which clusters belong to which file** and whether clusters are free or in use. It works like a chain — each cluster points to the next one in the file.

**Real World Example:**
Imagine a **treasure map** where each location has a note: *"The next piece of treasure is at location X."* The FAT table is exactly this — a chain of "next cluster" pointers.

```
File: photo.jpg occupies clusters 5, 6, 9, 12

FAT Table:
Cluster 1:  0xFFFFFFFF (EOF — end of another file)
Cluster 2:  0x00000000 (FREE)
Cluster 3:  0x00000004 (points to cluster 4)
Cluster 4:  0xFFFFFFFF (EOF)
Cluster 5:  0x00000006 → points to cluster 6 ← photo.jpg starts here
Cluster 6:  0x00000009 → points to cluster 9
Cluster 7:  0x00000000 (FREE)
Cluster 8:  0x00000000 (FREE)
Cluster 9:  0x0000000C → points to cluster 12
Cluster 12: 0xFFFFFFFF (EOF) ← photo.jpg ends here
```

**FAT32 Deletion Process:**
```
Before delete:
  FAT[5] = 6, FAT[6] = 9, FAT[9] = 12, FAT[12] = EOF

After delete:
  FAT[5] = 0  (free!)
  FAT[6] = 0  (free!)
  FAT[9] = 0  (free!)
  FAT[12] = 0 (free!)
  Directory entry: first byte → 0xE5 (deleted marker)

Data clusters 5, 6, 9, 12: UNTOUCHED → recoverable!
```

**FAT vs NTFS:**
| | FAT32 | NTFS |
|---|---|---|
| Index type | FAT table (linked list) | MFT (database entries) |
| Metadata | Minimal | Rich (timestamps, permissions, ADS) |
| Recovery ease | Moderate | High (MFT entries preserved) |
| Max file size | 4GB | 16EB |

**Related:** [[#MFT (Master File Table)]], [[#Bitmap Bits]], [[#Deleted File]]

---

### File Signature (Magic Bytes)

> [!tip] Simple Definition
> **File Signature** = A specific sequence of bytes at the very beginning (and sometimes end) of every file that acts as its **identity badge** — telling you what type of file it is, regardless of the file extension.

**Real World Example:**
A **national ID card** starts with a standardized format — even if someone changes their name on it, the underlying card structure reveals what country issued it. Similarly, a JPEG file always starts with `FF D8 FF` — even if you rename it to `tax_document.txt`, the first bytes still scream "I'm a JPEG!"

**This is how investigators catch liars:**
```bash
# Suspect renames malware to look like a text file:
# "invoice.txt" — but let's check the real signature

xxd invoice.txt | head -2
# Output: 0000000: 4d5a 9000 0300 0000...
#         MZ = Windows executable!
# This is a .EXE disguised as .txt!

# Correct identification:
file invoice.txt
# Output: invoice.txt: PE32 executable (GUI) Intel 80386, for MS Windows
```

**Master Signature Table:**
```
Extension | Magic Bytes (Hex)              | ASCII
──────────────────────────────────────────────────
.jpg      | FF D8 FF                       | ÿØÿ
.png      | 89 50 4E 47 0D 0A 1A 0A       | .PNG....
.pdf      | 25 50 44 46 2D                 | %PDF-
.zip      | 50 4B 03 04                    | PK..
.exe/.dll | 4D 5A                          | MZ
.gif      | 47 49 46 38                    | GIF8
.doc      | D0 CF 11 E0                    | ÐÏ..
.docx     | 50 4B 03 04 (= ZIP internally) | PK..
.sqlite   | 53 51 4C 69 74 65 33 00       | SQLite3.
.mp4      | 00 00 00 xx 66 74 79 70       | ....ftyp
.rar      | 52 61 72 21                    | Rar!
.7z       | 37 7A BC AF 27 1C             | 7z¼¯'.
```

**Related:** [[#Data Carving]], [[#Unallocated Space]]

---

### File Slack

> [!tip] Simple Definition
> **File Slack** = The **unused space between the end of a file's actual content and the end of the last cluster** the file occupies. This gap often contains fragments of previously deleted files.

**Real World Example:**
You have a room (cluster = 4096 sq ft). You only use 800 sq ft of it (your file content). The remaining 3296 sq ft is **file slack** — and it still has the **furniture from the previous tenant** (old deleted file fragments)!

```
Visual breakdown:
┌──────────────────────────────────────────────────────────────┐
│                   ONE CLUSTER (4096 bytes)                   │
├──────────────────────────────────┬───────────────────────────┤
│   ACTUAL FILE DATA (800 bytes)   │   FILE SLACK (3296 bytes) │
│   "Hello World!"                 │   [old deleted data here] │
└──────────────────────────────────┴───────────────────────────┘
```

**Two Types of Slack:**

| Type | What it is | Forensic value |
|---|---|---|
| **File Slack** | Space after EOF to end of last sector | May contain RAM residue (RAM slack) |
| **Volume Slack** | Space after last partition | Can hide data intentionally |

**Formula:**
```
File Slack = (Clusters Used × Cluster Size) − File Size
Example:
  File size = 1500 bytes
  Cluster size = 4096 bytes
  Clusters used = 1 (ceiling of 1500/4096)
  File Slack = (1 × 4096) - 1500 = 2596 bytes of potentially recoverable old data
```

```bash
# Visualize slack with Sleuth Kit
blkcat image.img [cluster_number] | xxd
# You'll see file content in first N bytes, then old data after it!
```

**Related:** [[#Cluster]], [[#Slack Space]], [[#Unallocated Space]]

---

## H

---

### Hash (MD5 / SHA256)

> [!tip] Simple Definition
> **Hash** = A fixed-length digital fingerprint of any data. Change even **one bit** of the data and the hash completely changes. It's mathematically impossible to reverse — you can't get the original data from the hash.

**Real World Example:**
Imagine a magical stamp machine. You feed it any document — 1 page or 10,000 pages — and it gives you a unique 64-character code (for SHA256). Feed the same document again — exact same code. Change even one comma in the document — completely different code.

**Hash in action:**
```bash
echo "Hello World" | sha256sum
# a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e

echo "Hello world" | sha256sum   # lowercase 'w'
# 64ec88ca00b268e5ba1a35678a1b5316d212f4f366b2477232534a8aeca37f3c
# ← COMPLETELY DIFFERENT!  One letter change = totally different hash

# Real forensics use:
sha256sum evidence.img
# a1b2c3d4e5f6789... evidence.img

# This 64-char string is your SEAL — it never changes unless data changes
```

**MD5 vs SHA256:**
| | MD5 | SHA256 |
|---|---|---|
| Output length | 128-bit (32 hex chars) | 256-bit (64 hex chars) |
| Speed | Faster | Slower |
| Security | Collision possible | Much stronger |
| Forensics use | Secondary check | Primary — court standard |
| Command | `md5sum file` | `sha256sum file` |

> [!tip] Use Both
> Professional forensicators compute **both MD5 and SHA256** — MD5 for quick verification during work, SHA256 for court-level evidence.

**Related:** [[#Evidence Integrity]], [[#Chain of Custody]], [[#Bit-for-Bit Forensic Image]]

---

## I

---

### Inode

> [!tip] Simple Definition
> **Inode** = Linux/ext4's **identity card for every file**. It stores all the metadata about a file — size, owner, timestamps, permissions, and pointers to where the data blocks are — but NOT the filename.

**Real World Example:**
In a library, every book has a **catalog card** in the card catalog:
- Book title is NOT on the card
- The card has: Author, Size (pages), Location on shelf (block pointers), Date added, Who can borrow it (permissions)
- The directory is what maps "book title" → "catalog card number"

Same in ext4:
- **Inode** = catalog card (no filename)
- **Directory entry** = maps filename → inode number

**Inode Contents:**
```
Inode #42:
  File type:   Regular file
  Size:        24,576 bytes
  Owner:       UID 1000 (hexx)
  Group:       GID 1000
  Permissions: rw-r--r--  (644)
  atime:       2026-03-17 09:05  ← Last accessed
  mtime:       2026-03-15 14:22  ← Last modified
  ctime:       2026-03-17 09:05  ← Status changed
  nlink:       1   ← Number of hard links (0 = deleted!)
  Blocks:      [3832, 3833, 3834, 3835, 3836, 3837]
```

**Forensic Note:**
```bash
# Get inode details
istat -f ext4 image.img 42

# When nlink = 0 → file is deleted but data may still be there!
# ext4 may zero block pointers on deletion — use journal recovery
extundelete image.img --restore-inode 42
```

**NTFS Equivalent:** MFT Entry (but stores filename too)

**Related:** [[#MFT (Master File Table)]], [[#Deleted File]], [[#FAT Table (File Allocation Table)]]

---

## L

---

### Live Forensics

> [!tip] Simple Definition
> **Live Forensics** = Analyzing a device that is **powered ON and running**. You collect volatile data (RAM, network connections, running processes) before it's lost.

**Real World Example:**
You arrive at a suspect's house and their computer is **on and logged in**. You have a choice:
- Pull the plug → lose everything in RAM (encryption keys, running processes, open network connections)
- Do live forensics → capture RAM first, then image the disk

**What live forensics captures:**
```bash
# On live Windows system:
# 1. Capture RAM
winpmem.exe -o ram.dump

# On live Linux system:
sudo avml /tmp/ram.lime

# Then analyze with Volatility3:
python3 vol.py -f ram.dump windows.pslist     # Running processes
python3 vol.py -f ram.dump windows.netscan    # Active connections
python3 vol.py -f ram.dump windows.cmdline    # Command history
python3 vol.py -f ram.dump windows.hashdump   # Password hashes!
```

**Live vs Dead:**
| | Live Forensics | Dead Forensics |
|---|---|---|
| System state | Powered ON | Powered OFF |
| RAM data | Captured! | Lost forever |
| Risk | OS may alter disk during analysis | Safe — nothing changes |
| Encryption | May be unlocked in RAM | Drive may be locked |

**Related:** [[#Volatile Data]], [[#Dead Forensics]]

---

### Logical Copy

> [!tip] Simple Definition
> **Logical Copy** = Copying only the **visible files and folders** — like a normal file copy. Does NOT include deleted files, slack space, unallocated space, or MFT metadata.

**Real World Example:**
Logical copy = Using Ctrl+C → Ctrl+V to copy files.
Forensic image = Using a specialized machine that duplicates every atom of the original disk.

```
Logical Copy gets:
  ✓ Active files
  ✓ Folder structure
  ✗ Deleted files
  ✗ Slack space
  ✗ MFT metadata
  ✗ Unallocated space

Forensic Image gets:
  ✓ Everything above PLUS all of below:
  ✓ Deleted files
  ✓ Slack space
  ✓ All metadata
  ✓ Unallocated space
  ✓ Hidden partitions
  ✓ Bad sectors (padded with 0s)
```

**When to use logical copy:**
- When you only need to analyze active documents (not a full forensic case)
- Mobile device triage (when physical imaging isn't possible)
- Cloud storage (you can only get logical access)

**Related:** [[#Bit-for-Bit Forensic Image]], [[#Acquisition]]

---

## M

---

### Magnetic Polarity

> [!tip] Simple Definition
> **Magnetic Polarity** = The physical mechanism by which a Hard Disk Drive (HDD) stores data. Tiny magnetic domains on the spinning platter are oriented in one of two directions — **North or South** — representing **1 or 0**.

**Real World Example:**
Think of millions of **tiny bar magnets** embedded in the HDD platter. A read/write head can:
- **Flip a magnet north** → stores a `1`
- **Flip a magnet south** → stores a `0`

When reading, the head detects which way each magnet points → interprets it as 1 or 0.

```
HDD Platter Surface (magnified):
┌─────────────────────────────────────────────────┐
│  N→  S→  N→  N→  S→  S→  N→  S→  N→  S→       │
│  1   0   1   1   0   0   1   0   1   0          │
│                                                  │
│  N = North pole facing read head = bit 1         │
│  S = South pole facing read head = bit 0         │
└─────────────────────────────────────────────────┘
```

**Why it matters for forensics:**
Even after "deletion," the magnetic polarities representing old data remain on the platter until overwritten. Old-school forensics labs (government level) could use **Magnetic Force Microscopy (MFM)** to read faint residual polarity from previously overwritten sectors. This is why DoD secure wiping requires multiple passes.

**SSD Difference:**
SSDs use **flash memory cells** (electrons trapped in floating gate transistors) instead of magnetic polarity. No magnetic fields — completely different storage physics.

**Related:** [[#Bit-for-Bit Forensic Image]], [[#TRIM]]

---

### MFT (Master File Table)

> [!tip] Simple Definition
> **MFT (Master File Table)** = NTFS's **master database** where every single file and folder on the volume has its own 1KB entry. It contains timestamps, permissions, filename, file size, and either the file content itself (if tiny) or pointers to where the content is stored.

**Real World Example:**
MFT = A **massive Excel spreadsheet** where:
- Each **row** = one file or folder (1KB per row)
- Each **column** = a property (filename, size, created, modified, owner, location on disk...)
- The spreadsheet is always stored as the first file on an NTFS volume

```
MFT Entry #42 (for document.txt):
┌────────────────────────────────────────────────────┐
│  MFT Entry Header                                  │
│  Signature: FILE                                   │
│  Status: IN USE (or NOT IN USE if deleted)         │
├────────────────────────────────────────────────────┤
│  $STANDARD_INFORMATION attribute:                  │
│    Created:  2026-03-15 10:00:00                   │
│    Modified: 2026-03-17 09:05:00                   │
│    Accessed: 2026-03-17 09:05:00                   │
│    MFT Mod:  2026-03-17 09:22:00                   │
├────────────────────────────────────────────────────┤
│  $FILE_NAME attribute:                             │
│    Name: document.txt                              │
│    Parent: MFT Entry 5 (root directory)            │
│    Size: 4096 bytes                                │
├────────────────────────────────────────────────────┤
│  $DATA attribute:                                  │
│    Data runs: [Cluster 1024 → 1025 → 1026]        │
│    (or inline data if file < ~700 bytes)           │
└────────────────────────────────────────────────────┘
```

**Special MFT Files (system metadata):**
| MFT Entry | Name | Purpose |
|---|---|---|
| 0 | `$MFT` | The MFT itself |
| 1 | `$MFTMirr` | First 4 MFT entries backup |
| 2 | `$LogFile` | Transaction journal |
| 3 | `$Volume` | Volume name, NTFS version |
| 6 | `$Bitmap` | Cluster allocation bitmap |
| 8 | `$BadClus` | Bad sector map |

**Forensic goldmine:**
```bash
# Extract MFT from mounted image
cp /mnt/evidence/\$MFT ./MFT_raw

# Parse ALL MFT entries (including deleted)
analyzeMFT.py -f MFT_raw -o mft_analysis.csv

# Grep for interesting files
grep -i "password\|wallet\|payload" mft_analysis.csv
grep "True" mft_analysis.csv   # Active=True entries
```

> [!tip] Key Forensic Fact
> Even after a file is deleted, its **MFT entry is NOT immediately overwritten**. Windows keeps it around and only reuses old MFT entries when all new allocation space is exhausted. This is why NTFS deleted file recovery is so reliable!

**Related:** [[#FAT Table (File Allocation Table)]], [[#Inode]], [[#Chronological Timeline]]

---

### Mount

> [!tip] Simple Definition
> **Mount** = Telling the operating system: *"Attach this disk (or image file) and let me browse its contents through a folder."* The disk is **not copied** — the OS just creates an access point to it.

**Real World Example:**
**Mount** = Plugging in a USB drive. The moment you plug it in, Windows gives it a drive letter (E:, F:, etc.) and you can browse files. You didn't copy the USB — you just **attached it** so the OS could access it.

**Unmount** = Safely removing the USB. The OS detaches access.

**In Forensics — ALWAYS mount READ-ONLY:**
```bash
# Create mount point (folder to access through)
sudo mkdir /mnt/evidence

# Mount image file read-only:
# -o ro = read-only (CANNOT modify evidence!)
# -o loop = treat file as a block device
# -o noatime = don't update access timestamps!
sudo mount -o ro,loop,noatime evidence.img /mnt/evidence

# Now browse freely — you cannot accidentally modify it!
ls /mnt/evidence/
cat /mnt/evidence/Documents/secret.txt

# Verify it's truly read-only:
echo "test" > /mnt/evidence/test.txt
# Error: Read-only file system   ← GOOD!

# Mount specific partition by offset
# (partition starts at sector 2048, sector size = 512)
OFFSET=$((2048 * 512))   # = 1,048,576 bytes
sudo mount -o ro,loop,offset=$OFFSET,noatime evidence.img /mnt/evidence
```

**Different mount types:**
| Mount Type | When to use |
|---|---|
| `ro` (read-only) | **Always** in forensics! |
| `loop` | When mounting an image file (not real device) |
| `noatime` | Prevents updating access timestamps when reading |
| `offset=N` | When mounting a specific partition from a full disk image |

> [!danger] NEVER mount as read-write in forensics
> Mounting as read-write modifies `atime` (access timestamp) on every file you open. This changes evidence and breaks the hash. Always use `-o ro,noatime`.

**Related:** [[#Bit-for-Bit Forensic Image]], [[#Acquisition]], [[#Write Blocker]]

---

## P

---

### Partition

> [!tip] Simple Definition
> **Partition** = A logically separate section of a physical disk. One physical 1TB hard drive can have 3 partitions — each acting like a completely separate disk with its own file system.

**Real World Example:**
Think of a **large warehouse** (the physical disk). A partition is like building **walls inside the warehouse** to create separate rooms (C:, D:, E:). Each room has its own key and filing system, but they're all in the same building.

```
Physical Disk (1TB):
┌─────────────────────────────────────────────────────────────┐
│ MBR/GPT │ Partition 1 (C:) │ Partition 2 (D:) │ Free Space │
│  512B   │  500GB NTFS      │  400GB NTFS      │  100GB     │
└─────────────────────────────────────────────────────────────┘

In sectors (mmls output):
000: Meta  0     0      1     Primary Table
001: ----  0     2047   2048  Unallocated
002: 000:0 2048  1026047 1024000  NTFS (C:)
003: 000:1 1026048 1874943 848896  NTFS (D:)
```

**MBR vs GPT Partitioning:**
| | MBR | GPT |
|---|---|---|
| Max partitions | 4 primary | 128 |
| Max disk size | 2TB | 9.4 ZB |
| Backup table | None | YES — at end of disk! |
| Forensics tip | Check sector 0 | Check backup at last sectors |

**Related:** [[#Bitmap Bits]], [[#FAT Table (File Allocation Table)]], [[#MFT (Master File Table)]]

---

## S

---

### Seizure

> [!tip] Simple Definition
> **Seizure** = The **legal act** of taking possession of a device or storage media as evidence. Must be done with proper legal authority (warrant, consent, or exigent circumstances). Everything after seizure depends on how well seizure was done.

**Real World Example:**
Police arrive at a suspect's office with a **search warrant**. They physically take:
- The laptop
- The USB drives on the desk
- The external hard drives
- Even the mobile phone

Every item is **photographed in place**, **labeled**, **bagged**, and **sealed**. This entire process = **seizure**. If done wrong, the evidence is thrown out.

**Seizure Best Practices:**
```
Before Touching Anything:
  1. Photograph everything in place (devices, cables, screen)
  2. Note the state (on/off, logged in, connected drives)
  3. If powered ON → consider live forensics first
  4. If powered OFF → leave it OFF (don't turn on!)

During Seizure:
  5. Use anti-static bags for storage
  6. Write-block all seized drives immediately
  7. Label every item with unique evidence number
  8. Seal bags with tamper-evident seals
  9. Document in seizure report: what, where, when, who

If Computer is ON:
  10. Photograph screen (note current user, open programs)
  11. Capture RAM if possible before shutdown
  12. Then safely shut down
```

> [!warning] Pulling the Plug Debate
> - **Old school:** Pull the plug immediately (clean shutdown may overwrite evidence)
> - **Modern approach:** Safely capture RAM first, then pull plug
> - **For encrypted drives:** If it's running and unlocked — RAM may have the key!

**Related:** [[#Chain of Custody]], [[#Live Forensics]], [[#Write Blocker]]

---

### Sector

> [!tip] Simple Definition
> **Sector** = The **smallest physical unit** of storage on a disk. Traditionally 512 bytes, modern drives use 4096 bytes (4KB = Advanced Format). Everything on a disk is measured in sectors.

**Real World Example:**
A sector is like one **brick in a wall** — it's the smallest unit used to build storage. Files are made of many bricks, but the bricks themselves are always the same size.

```
Disk = Millions of sectors laid end-to-end:
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│  S0  │  S1  │  S2  │  S3  │  S4  │  S5  │  S6  │ ...
│ MBR  │ GPT  │      │      │      │      │      │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘
  512B   512B   512B   512B   512B   512B   512B

Sector 0 = Always the MBR (if MBR disk)
Sector 1 = GPT header (if GPT disk)
```

**Sector vs Cluster:**
- **Sector** = Hardware level — defined by the drive manufacturer (512B or 4KB)
- **Cluster** = OS level — defined by the file system (4KB, 8KB, 32KB etc. = multiple sectors)

```bash
# Read specific sector (e.g., MBR = sector 0)
dd if=image.img bs=512 count=1 skip=0 | xxd

# Read sector 2048 (common partition start)
dd if=image.img bs=512 count=1 skip=2048 | xxd
```

**Related:** [[#Cluster]], [[#Magnetic Polarity]], [[#Partition]]

---

### Slack Space

> [!tip] Simple Definition
> **Slack Space** = The collective term for ALL the "wasted" or unused space on a disk that can contain forensic evidence — including file slack, volume slack, and partition slack.

**Real World Example:**
Think of moving into a new apartment. The previous tenant's stuff is technically gone (directory entries deleted), but they left things **in corners, under carpets, and in closets** that the cleaning crew didn't touch. Slack space is those hidden leftovers.

**Types of Slack Space:**

```
┌─────────────────────────────────────────────────────────────┐
│  FILE SLACK                                                 │
│  Space between end of file content and end of last cluster  │
│  May contain: fragments of old deleted files (RAM slack)    │
├─────────────────────────────────────────────────────────────┤
│  VOLUME SLACK                                               │
│  Space after the last partition on a disk                   │
│  Often used by attackers to HIDE data (anti-forensics!)     │
├─────────────────────────────────────────────────────────────┤
│  PARTITION SLACK                                            │
│  Space between end of one partition and start of the next   │
│  Another hiding spot for malicious data                     │
├─────────────────────────────────────────────────────────────┤
│  UNALLOCATED SPACE                                          │
│  All clusters marked as "free" — where deleted files live   │
└─────────────────────────────────────────────────────────────┘
```

**Forensic value:**
```bash
# Extract file slack with bulk_extractor
bulk_extractor -o output/ image.img
# It automatically finds strings in slack space!

# Manual slack inspection
# Get cluster number from istat
istat image.img 42   # See which clusters file uses
# Then read the full cluster(s) — file content + slack
blkcat image.img 1024 | xxd
# Bytes after file EOF = the slack!
```

> [!tip] Hidden Files in Volume Slack
> Attackers and intelligence agencies sometimes hide entire files in volume slack — after the last partition. Tools like `dcfldd` and `dd` capture it automatically since they copy the entire disk. A logical copy would completely miss it.

**Related:** [[#File Slack]], [[#Unallocated Space]], [[#Cluster]]

---

### Steganography

> [!tip] Simple Definition
> **Steganography** = The art of **hiding secret data inside an innocent-looking file** (image, audio, video) so that no one knows the hidden data even exists.

**Real World Example:**
Imagine a criminal sends a family vacation photo to an accomplice. It looks completely normal — mountains, smiles, sunshine. But hidden inside the pixel values is an encoded message: **"Meet at warehouse at 3AM."** This is steganography.

**How it works (in JPEG):**
```
JPEG stores color values per pixel (R, G, B — 0-255 each)
Pixel: R=200, G=145, B=89

LSB (Least Significant Bit) steganography:
  Original R value: 11001000  (= 200)
  Hidden bit inserted in last bit:
  Modified R value: 11001001  (= 201) → nearly invisible change!

  Do this across thousands of pixels → hide kilobytes of data
  The image looks identical to human eye!
```

**Detection tools:**
```bash
# StegDetect — statistical analysis
stegdetect -t jiow image.jpg

# Zsteg — for PNG/BMP
zsteg image.png -a

# Steghide — extract hidden data
steghide extract -sf image.jpg
# (if no password, try empty password)

# ExifTool — check for anomalous metadata
exiftool image.jpg
# Look for unusual comment fields or large metadata blocks

# Binwalk — check for embedded files
binwalk image.jpg
# May show hidden ZIP/RAR inside the JPEG!
```

**Related:** [[#Alternate Data Stream (ADS)]], [[#Data Carving]]

---

## T

---

### Timestomping

> [!tip] Simple Definition
> **Timestomping** = An **anti-forensics technique** where an attacker deliberately modifies the timestamps of a file (Created, Modified, Accessed, MFT-Changed) to **hide when the malware was installed** or when evidence was created.

**Real World Example:**
A criminal breaks into your house and steals something, but before leaving, they **move the hands of your wall clock back to yesterday** so security footage timestamps look wrong. Timestomping is the digital version.

**Attacker uses:**
```bash
# Metasploit timestomp module
meterpreter > timestomp malware.exe -f C:/Windows/System32/notepad.exe
# Copies notepad.exe's timestamps onto malware.exe
# Now malware looks like it's been there since Windows was installed!

# PowerShell method
(Get-Item "malware.exe").CreationTime = "2020-01-01 00:00:00"
(Get-Item "malware.exe").LastWriteTime = "2020-01-01 00:00:00"

# Linux touch command
touch -t 202001010000.00 malware.sh
```

**Forensic Detection:**
```bash
# NTFS has TWO sets of timestamps per file:
# 1. $STANDARD_INFORMATION — user-visible, easily changed
# 2. $FILE_NAME — in directory index, harder to change

# If these don't match → TIMESTOMPING!
istat image.img 42
# Look for $STANDARD_INFORMATION vs $FILE_NAME timestamp mismatch!

# Another clue: $MFT entry has ctime ($STANDARD_INFORMATION)
# If ctime > mtime → something changed metadata AFTER the file was modified
# That's suspicious!
```

**Related:** [[#Chronological Timeline]], [[#MFT (Master File Table)]], [[#Artifact]]

---

### TRIM

> [!tip] Simple Definition
> **TRIM** = An ATA command that SSDs use to **immediately erase** the data blocks of deleted files, so those blocks are ready for new data quickly. This destroys forensic evidence much faster than HDDs.

**Real World Example:**
HDD = Hotel where the cleaning crew comes **only when a new guest books the room**. Until then, old guest's belongings might still be there.

SSD with TRIM = Hotel where the cleaning crew **arrives the instant you check out** and sanitizes everything immediately. By the time the next guest comes, the room is spotless — nothing left of the previous guest.

**How TRIM works:**
```
Step 1: User deletes file on SSD
Step 2: OS updates NTFS — clusters marked free
Step 3: OS sends TRIM command to SSD controller
Step 4: SSD controller immediately erases those NAND blocks
Step 5: Forensic investigator tries to recover → EMPTY BLOCKS!
                                               ← Evidence is gone!
```

**Why TRIM exists:**
SSDs can't overwrite data in place — they must **erase an entire block** (128KB–512KB) before writing. TRIM lets the SSD erase blocks proactively so writes are fast. Without TRIM, SSDs would slow down dramatically over time.

**Forensic Impact:**
| Situation | Recovery Chance |
|---|---|
| HDD — recently deleted | High (>80%) |
| SSD + TRIM enabled — deleted | Very Low (<10%) |
| SSD + TRIM disabled | Moderate |
| SSD — deleted from USB (no TRIM) | Higher |

**Check if TRIM is enabled:**
```bash
# Linux
cat /sys/block/sda/queue/discard_max_bytes
# Non-zero = TRIM capable

# Windows
fsutil behavior query DisableDeleteNotify
# 0 = TRIM enabled, 1 = TRIM disabled
```

**Related:** [[#Magnetic Polarity]], [[#Unallocated Space]], [[#Deleted File]]

---

### TSK (The Sleuth Kit)

> [!tip] Simple Definition
> **TSK (The Sleuth Kit)** = The most important open-source **command-line forensics toolkit**. It contains tools to analyze disk images, list files (including deleted), extract file content by inode/MFT number, and build file system timelines.

**Real World Example:**
TSK is the **Swiss Army knife of disk forensics**. Just like a Swiss Army knife has a blade, scissors, screwdriver, and more — TSK has a tool for every file system task.

**Core TSK Commands:**

```bash
# ── DISK & PARTITION TOOLS ──────────────────────────────
mmls image.img          # Map out all partitions
mmstat image.img        # Partition table type (MBR/GPT)

# ── FILE SYSTEM TOOLS ───────────────────────────────────
fsstat image.img        # File system statistics (cluster size, etc.)
fsstat -o 2048 image.img  # Stats for partition at sector offset 2048

# ── FILE LISTING ────────────────────────────────────────
fls image.img           # List root directory files
fls -r image.img        # Recursive — all files
fls -r -d image.img     # DELETED files only (the key forensic command!)
fls -r -m / image.img   # Bodyfile format (for timeline)

# ── FILE EXTRACTION ─────────────────────────────────────
icat image.img 42       # Extract file by inode/MFT number
icat image.img 42 > evidence.jpg  # Save to file

# ── FILE METADATA ───────────────────────────────────────
istat image.img 42      # All metadata for inode 42 (timestamps, blocks)

# ── BLOCK/CLUSTER TOOLS ─────────────────────────────────
blkcat image.img 1024   # Read cluster #1024 raw bytes
blkls image.img         # List unallocated blocks (deleted file space!)
blkls image.img | xxd   # View raw unallocated bytes

# ── TIMELINE ────────────────────────────────────────────
fls -r -m / image.img > bodyfile.txt    # Create bodyfile
mactime -b bodyfile.txt -d > timeline.csv  # Generate sorted timeline
```

**TSK Name Meanings:**
| Tool | Stands For | Purpose |
|---|---|---|
| `mmls` | Media Management List | Partition layout |
| `fls` | File Listing | List files (+ deleted) |
| `icat` | Inode Concatenate | Extract file content |
| `istat` | Inode Statistics | File metadata |
| `fsstat` | File System Statistics | FS-level info |
| `blkcat` | Block Concatenate | Read raw blocks |
| `blkls` | Block Listing | List data units |
| `mactime` | MAC Time | Timeline generation |

**Autopsy = TSK with a GUI:**
```bash
# Autopsy is basically a web-based GUI for TSK
autopsy
# Opens at: http://localhost:9999/autopsy
```

**Related:** [[#MFT (Master File Table)]], [[#Inode]], [[#Chronological Timeline]]

---

## U

---

### Unallocated Space

> [!tip] Simple Definition
> **Unallocated Space** = All the clusters on a disk that are currently marked as "free" — whether they were never used, or previously held deleted files. **This is the primary hunting ground for forensic investigators.**

**Real World Example:**
Think of an apartment building where **vacant apartments** exist in two types:
1. Apartments that were **never occupied** (empty from the start)
2. Apartments where the **previous tenant moved out** but their belongings (furniture, notes, belongings) are still inside

Type 2 = deleted file data still sitting in "free" clusters.

```
Disk map:
┌────────────────────────────────────────────────────────────┐
│ [FILE A] [FILE B] [    FREE    ] [FILE C] [    FREE    ]  │
│  used     used    ← unalloc →    used    ← unalloc →      │
│                       ↑                      ↑             │
│              Deleted file data      Never-used space       │
│              might be here!         (less interesting)     │
└────────────────────────────────────────────────────────────┘
```

**Extracting and analyzing unallocated space:**
```bash
# Extract ALL unallocated space from image
blkls image.img > unallocated_space.raw

# Run data carving on the unallocated space
foremost -t jpg,pdf,zip -i unallocated_space.raw -o /output/

# Search for keywords in unallocated space
strings unallocated_space.raw | grep -i "password\|bitcoin\|account"

# Autopsy automatically highlights unallocated space
# and lets you carve from it with a few clicks
```

**Related:** [[#Allocated Space]], [[#Data Carving]], [[#Bitmap Bits]], [[#Deleted File]]

---

## V

---

### Volatile Data

> [!tip] Simple Definition
> **Volatile Data** = Information stored in **RAM (memory)** that **disappears permanently the moment the power is cut**. This includes running processes, network connections, encryption keys, and logged-in user sessions.

**Real World Example:**
Volatile data is like writing on a **whiteboard with a UV pen** — visible only when the UV light (power) is on. The moment you turn off the UV light (cut power), everything on the board is invisible — gone forever. The whiteboard itself (disk) remains, but that UV-written content is lost.

**What's lost when you pull the plug:**
```
Volatile Data (LOST):
  ✗ Running processes
  ✗ Open network connections
  ✗ Logged-in user sessions
  ✗ Encryption keys in memory (TrueCrypt/Veracrypt keys!)
  ✗ Command history (unsaved)
  ✗ Clipboard contents
  ✗ Unsaved documents
  ✗ Malware running only in RAM (fileless malware!)

Non-Volatile Data (PRESERVED):
  ✓ Files on disk
  ✓ Registry (saved to disk)
  ✓ Browser history (saved)
  ✓ Logs (written to disk)
```

> [!warning] Fileless Malware
> Modern malware (like PowerShell-based attacks) runs **entirely in RAM** with nothing written to disk. If you pull the plug without capturing RAM, the malware evidence is **gone forever**. This is why live forensics and RAM acquisition are critical.

```bash
# Capture RAM on Windows (live system)
winpmem.exe -o ram.dump

# Capture RAM on Linux
sudo avml /tmp/ram.lime

# Analyze with Volatility3
python3 vol.py -f ram.dump windows.pslist
python3 vol.py -f ram.dump windows.malfind   # Suspicious injected code!
```

**Related:** [[#Live Forensics]], [[#Dead Forensics]]

---

### Volume Shadow Copy (VSS)

> [!tip] Simple Definition
> **VSS (Volume Shadow Copy Service)** = Windows' built-in automatic snapshot system. Windows periodically creates **point-in-time copies** of the file system. Even if an attacker deletes files, older VSS snapshots may still have them.

**Real World Example:**
VSS is like a **time machine** built into Windows. At 8AM, Windows takes a photograph of all your files. At 10AM, an attacker deletes everything. But the 8AM photograph still exists — you can open it and see the files as they were at 8AM.

**Why ransomware deletes shadow copies:**
Most ransomware (WannaCry, REvil, LockBit) runs this command first:
```cmd
vssadmin delete shadows /all /quiet
```
They know forensicators will check shadow copies for pre-encryption files!

**Forensic Access:**
```bash
# List shadow copies on live Windows
vssadmin list shadows

# Browse shadow copy (run as admin)
mklink /d C:\ShadowCopy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\

# On mounted image (with libvshadow):
sudo apt install libvshadow-utils
vshadowmount image.img /mnt/vss
ls /mnt/vss/  # Shows vss1, vss2, etc.
sudo mount -o ro /mnt/vss/vss1 /mnt/shadow_files
ls /mnt/shadow_files/  # Old versions of files!
```

**Related:** [[#Artifact]], [[#Chronological Timeline]]

---

## W

---

### Write Blocker

> [!tip] Simple Definition
> **Write Blocker** = A device (hardware) or software setting that **physically prevents any write commands from reaching the evidence drive** — ensuring you can only READ from it, never accidentally modify it.

**Real World Example:**
Imagine a **one-way mirror** at a museum — you can look at the art, but you absolutely cannot touch it. A write blocker is that one-way barrier between you and the evidence drive.

**Without write blocker — disaster:**
```
You plug USB evidence drive into your Kali PC.
Linux automatically tries to mount it.
Linux writes to the drive:
  - Updates access timestamps on every file you view
  - Writes journal entries
  - May swap data to it
  - Hash of drive NOW DIFFERS from original
  → Evidence contaminated → Case dismissed
```

**Hardware Write Blockers (best):**
- Tableau T8u (USB)
- Tableau T35u (SATA/IDE)
- WiebeTech USB WriteBlocker
- These go between the evidence drive and your computer

**Software Write Blockers (Kali Linux):**
```bash
# Method 1: hdparm (for physical drives)
sudo hdparm -r1 /dev/sdb   # Set read-only flag
hdparm -r /dev/sdb          # Verify: readonly = 1

# Method 2: Mount with strict read-only
sudo mount -o ro,noatime,noload /dev/sdb1 /mnt/evidence

# Method 3: blockdev
sudo blockdev --setro /dev/sdb

# Verify it's truly read-only
sudo blockdev --getro /dev/sdb
# Output: 1 = read-only, 0 = read-write
```

> [!danger] Cardinal Rule
> **Never connect evidence storage to a working computer without a write blocker.** This is the #1 mistake that gets forensic investigators fired and cases thrown out of court.

**Related:** [[#Acquisition]], [[#Chain of Custody]], [[#Seizure]]

---

## 📊 Visual Summary — All Keywords at a Glance

```
FORENSICS KEYWORD MIND MAP
═══════════════════════════════════════════════════════════════

              ┌─────────────────────────────┐
              │     CYBER FORENSICS         │
              └──────────────┬──────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
  EVIDENCE              FILE SYSTEM           RECOVERY
  COLLECTION            CONCEPTS              TECHNIQUES
  ─────────             ────────              ──────────
  • Seizure             • MFT                 • Data Carving
  • Acquisition         • Inode               • Unallocated Space
  • Write Blocker       • FAT Table           • Slack Space
  • Bit-for-bit Image   • Bitmap Bits         • File Slack
  • Chain of Custody    • Cluster             • TRIM impact
  • Hash (MD5/SHA)      • Sector              • TSK tools
  • Evidence Integrity  • ADS                 • Mount (read-only)
  • Volatile Data       • Magnetic Polarity   • Deleted File
  • Live Forensics      • File Signature      • Partition Recovery
  • Dead Forensics      • Slack Space

       ▼                     ▼                     ▼
  ANALYSIS              ANTI-FORENSICS        ARTIFACTS
  TOOLS                 DETECTION             & TIMELINE
  ─────────             ──────────            ──────────
  • TSK/Sleuth Kit      • Timestomping        • Chronological TL
  • Autopsy             • Steganography       • Artifact
  • Volatility3         • ADS hiding          • VSS
  • analyzeMFT          • TRIM effects        • Prefetch
  • mactime/timeline    • Log clearing        • Event Logs
  • foremost/scalpel    • Secure wipe         • Registry
```

---

## 🧪 Quick Test Yourself

> [!question] Quiz Questions
> 1. What byte value replaces the first character of a FAT32 deleted filename?
> 2. Why should you NEVER mount evidence as read-write?
> 3. What is the difference between file slack and unallocated space?
> 4. Why does TRIM make SSD forensics harder than HDD forensics?
> 5. Name 3 commands from The Sleuth Kit and what each does.
> 6. An attacker changes file timestamps. What comparison reveals this?
> 7. Where does Windows store a record of every USB device ever connected?
> 8. What is the MBR signature in hex and at what offset?
> 9. Why is hiberfil.sys valuable for forensics?
> 10. What does `fls -r -d image.img` do?

> [!success] Answers
> 1. `0xE5`
> 2. It updates access timestamps and may write journal entries, breaking the hash verification and contaminating evidence
> 3. File slack = unused space inside an allocated cluster (within a file's last cluster). Unallocated space = clusters completely free (not assigned to any file)
> 4. TRIM immediately erases deleted file blocks on SSDs; HDDs leave data untouched until overwritten by new data
> 5. `fls` (list files + deleted), `icat` (extract file by inode), `istat` (file metadata/timestamps)
> 6. Compare `$STANDARD_INFORMATION` timestamps vs `$FILE_NAME` timestamps in NTFS — they should match; a mismatch = timestomping
> 7. `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR`
> 8. `0x55 0xAA` at byte offset 510–511
> 9. hiberfil.sys is a compressed RAM dump written to disk when Windows hibernates — it contains running processes, open files, network connections, and possibly encryption keys
> 10. Recursively lists only DELETED files in the image (the `-d` flag = deleted only, `*` in output marks deleted entries)

---

## 🔗 Related Notes

- [[Unit-IV-Cyber-Forensics-Complete]]
- [[00-Lab-Setup]]
- [[Task-01-Forensic-Imaging-Hashing]]
- [[Task-03-File-System-Investigation]]
- [[Task-07-08-Carving-Formatted-Recovery]]
