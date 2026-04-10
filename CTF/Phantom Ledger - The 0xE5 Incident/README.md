# 🔍 CYWARX Digital Forensics CTF

**Operation: Phantom Ledger**

---

## 🧠 Overview

This Capture The Flag (CTF) challenge simulates a **real-world digital forensic investigation** involving:

* 💰 Bank fraud
* 📤 Data exfiltration
* 🕵️ Insider threat
* 💻 Malware (keylogger) activity

Participants must analyze a **USB forensic image (`ctf1.img`)** to uncover hidden artifacts, recover deleted evidence, and reconstruct the attacker’s actions.

---

## 👤 Suspect Profile

**Name:** Rohan Mehta
**Background:** Final-year student (B.Com)
**Allegation:**

* Unauthorized access to banking systems
* Theft of customer data (75,842 records)
* Exfiltration via remote server

---

## 🧪 Challenge Objective

Investigate the provided forensic image and:

* Identify **malicious activity**
* Recover **deleted files**
* Analyze **logs, metadata, and memory artifacts**
* Extract **hidden flags**
* Build a **timeline of events**

---

## 📦 Evidence Provided

| File             | Description                         |
| ---------------- | ----------------------------------- |
| `ctf1.img`       | Full USB disk image (512 MB)        |
| Multi-partitions | FAT32 + EXT4 structure              |
| Hidden data      | Unallocated space, EXIF, NTFS image |

---

## 🧱 Disk Structure

| Partition   | Type  | Purpose                  |
| ----------- | ----- | ------------------------ |
| P1          | FAT32 | Personal files (visible) |
| P2          | FAT32 | Evidence + deleted files |
| P3          | EXT4  | Hidden/private data      |
| Unallocated | Raw   | Carved artifacts         |

---

## 🧩 Key Challenges

### 🟢 CH-01: Hidden MBR Marker

* Location: Raw disk (offset `0x100`)
* Technique: Hex analysis

---

### 🟡 CH-02: EXIF Metadata

* File: `college_fest.jpg`
* Technique: Metadata extraction
* Tool: `exiftool`

---

### 🔴 CH-03: Keylogger Evidence

* File: `kl.log` (deleted)
* Contains:

  * Credentials
  * Activity logs

---

### 🟣 CH-04: Disguised Malware

* File: `invoice.exe`
* Hidden as normal file
* Identify via file signature (`MZ` header)

---

### 🔵 CH-05: NTFS Timestomping

* File: `ntfs_evidence.img`
* Compare:

  * `$STANDARD_INFORMATION`
  * `$FILE_NAME`

---

### 🟠 CH-06: Data Exfiltration Logs

* File: `winscp_session.log`
* Shows:

  * FTP server
  * Upload activity

---

### ⚫ CH-07: Insider Notes

* File: `private_note.txt`
* Contains full attack plan

---

### ⚡ CH-08: RAM Forensics

* File: `ram_capture.bin`
* Includes:

  * Running processes
  * Network connections
  * Memory artifacts

---

### 🧬 CH-09: Data Carving

* Location: Unallocated space
* Recover:

  * JPEG fragments
  * ZIP archive

---

## 🛠️ Recommended Tools

* `fls`, `icat`, `mmls` (Sleuth Kit)
* `Autopsy`
* `binwalk`
* `foremost` / `scalpel`
* `exiftool`
* `strings`
* `xxd`, `hexedit`

---

## 🚀 Getting Started

```bash
# View partition layout
mmls ctf1.img

# List deleted files (Partition 2)
fls -r -d -o 133120 ctf1.img

# Recover a file
icat -o 133120 ctf1.img <inode> > recovered_file
```

---

## 🎯 Learning Outcomes

* Disk forensics (FAT32, EXT4)
* File recovery techniques
* Metadata analysis
* Malware identification
* Timeline reconstruction
* Data carving

---

## ⚠️ Important Notes

* ❌ Do NOT modify the original image
* ✅ Work on a copy
* 🔍 Always verify findings with multiple tools

---

## 🧠 Author

**CYWARX / HeXx**
Cyber Security Analyst | DFIR Enthusiast

---

## 🏁 Final Words

> “Data never lies — it just waits to be discovered.”

Good luck, investigator 🕵️‍♂️

