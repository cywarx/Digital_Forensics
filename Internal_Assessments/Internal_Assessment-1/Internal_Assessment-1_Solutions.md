# Digital Forensics — Internal Assessment 1
## The Devid Case · Complete Solution Notes

**Course:** Digital Forensics  
**Total Marks:** 10  
**Evidence File:** `Devid_evidence.img` (200 MB · MBR · FAT32)

---

## 🛠️ Pre-Analysis Setup — Creating the Evidence Image

Before starting the assessment, the forensic image must be created using the provided script.

```bash
# Make the script executable and run as root
chmod +x create_devid_evidence.sh
sudo bash create_devid_evidence.sh
```

**Expected terminal output:**

```
============================================================
  FORENSIC IMAGE CREATOR - THE Devid CASE (200MB)
============================================================
[*] Creating 200MB empty image...
200+0 records in
200+0 records out
209715200 bytes (210 MB, 200 MiB) copied, 1.234 s, 170 MB/s

[*] Creating MBR partition table...
[*] Setting up loop device...
Loop device: /dev/loop0

[*] Formatting partition as FAT32 with label 'Devid_USB'...
[*] Mounting partition...
[*] Creating normal user content...
[*] Downloading nature/waterfall image...
[*] Embedding GPS metadata into vacation_photo.jpg...
    ✓ GPS: 19.0760 N, 72.8777 E (Lonavala/Mumbai region)
    ✓ Date/Time: 2024:03:15 14:23:45
    ✓ Device: Apple iPhone 14 Pro
    ✓ Description: Weekend getaway near Lonavala waterfall
    ✓ Comment: Met with V.S. at the waterfall. Deal confirmed for March 25.
[*] Creating files to be deleted...
[*] Deleting suspicious files (traces remain for recovery)...

[*] Visible files on drive:
total 144
drwxr-xr-x  2 user user   512 Apr  9 14:30 .
drwxr-xr-x 18 root root  4096 Apr  9 14:29 ..
-rwxr-xr-x  1 user user   312 Apr  9 14:30 personal.txt
-rwxr-xr-x  1 user user 125952 Apr  9 14:30 vacation_photo.jpg
-rwxr-xr-x  1 user user   418 Apr  9 14:30 wifi_info.txt
-rwxr-xr-x  1 user user   387 Apr  9 14:30 work_notes.txt

[*] Generating hash values...

============================================================
  [✓] FORENSIC IMAGE CREATED SUCCESSFULLY!
============================================================

Filename: Devid_evidence.img
Size: 200MB  |  Volume Label: Devid_USB
Partition: MBR, FAT32 (Offset: 2048 sectors)

--- HASH VALUES ---
ddeeeb30bd85ec8f9b776ff366c9f432  Devid_evidence.img
ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f  Devid_evidence.img

--- FILES PRESENT (Visible) ---
  - work_notes.txt
  - personal.txt
  - wifi_info.txt
  - vacation_photo.jpg

--- FILES DELETED (Recoverable) ---
  - btc_transfer_record.txt
  - project_nightfall.txt
  - passwords_secure.txt
  - offshore_ledger.txt
```

> **What the script does:** Creates a 200 MB blank image → partitions it with MBR/FAT32 → mounts it → writes both visible and "suspicious" files → deletes the suspicious files (FAT32 directory entries marked free, data still on disk) → embeds forensic GPS metadata into the photo → generates hash files.

---

---

# Question 1 — Create Copy and Verify Hash `[4 Marks]`

---

## Q1(a) — Command to Create a Working Copy `[2 Mark]`

> **Rule #1 of forensics:** Never work on the original evidence. Always analyse a verified copy.

### ✅ Best Answer — dc3dd (Forensic-Grade, Recommended)

```bash
dc3dd if=Devid_evidence.img of=Devid_working.img hash=sha256 hof=Devid_working.hash log=acquisition.log
```

**Terminal Output:**

```
dc3dd 7.2.646 started at 2026-04-09 23:41:31 +0530
compiled options:
command line dc3dd if=Devid_evidence.img of=Devid_working.img hash=sha256 hof=Devid_working.hash log=acquisition.log
sector size: 512 bytes (assumed)
   209715200 bytes ( 200 M ) copied ( 100% ),    2 s, 117 M/s                 
   209715200 bytes ( 200 M ) hashed ( 100% ),    1 s, 285 M/s                 

input results for file `Devid_evidence.img':
   409600 sectors in
   4ec013c17ddf4d5acff3351d2086da76231d7532b3a0cf51b71a5683311f10c3 (sha256)

output results for file `Devid_working.img':
   409600 sectors out

output results for file `Devid_working.hash':
   409600 sectors out
   [ok] 4ec013c17ddf4d5acff3351d2086da76231d7532b3a0cf51b71a5683311f10c3 (sha256)

dc3dd completed at 2026-04-09 23:41:32 +0530
```

**Why dc3dd?** It copies AND hashes in one pass, generates a machine-readable hash output file (`hof`) and a human-readable acquisition log — all required for court-admissible forensic acquisition.

---

### Method 2 — dd (Standard Linux)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ dd if=Devid_evidence.img of=Devid_working.img bs=4M conv=sync,noerror status=progress
```

**Terminal Output:**

```
198180864 bytes (198 MB, 189 MiB) copied, 0 s, 1.6 GB/s
209715200 bytes (210 MB, 200 MiB) copied, 0.131 s, 1.6 GB/s
409600+0 records in
409600+0 records out
209715200 bytes (210 MB, 200 MiB) copied, 0.134 s, 1.6 GB/s
```

| Flag | Purpose |
|------|---------|
| `bs=4M` | Block size 4 MB — faster than default 512 bytes |
| `conv=sync` | Pads short blocks to maintain sector alignment |
| `conv=noerror` | Continues past read errors (important for damaged media) |
| `status=progress` | Shows live progress |

---

### Method 3 — ddrescue (For Damaged/Failing Media)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ ddrescue Devid_evidence.img Devid_working.img rescue.log
```

**Terminal Output:**

```
GNU ddrescue 1.27
Press Ctrl-C to interrupt
     ipos:  209715200 B,   errors:       0,   average rate:   209 MB/s
     opos:  209715200 B,    time from last successful read:       0 s
Finished                                
```

> **When to use ddrescue:** When the source media has bad sectors. The `rescue.log` allows you to resume if interrupted. Run it twice — second pass recovers data from bad sectors that the first pass skipped.

---

### Method 4 — dd with Inline Hash (Single Pipeline Command)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ dd if=Devid_evidence.img bs=4M conv=sync,noerror | tee Devid_working.img | sha256sum > Devid_working.sha256
```

**Terminal Output:**

```
409600+0 records in
409600+0 records out
209715200 bytes (210 MB, 200 MiB) copied, 0.134 s, 1.6 GB/s
```

---

### Method 5 — cat (Simple Copy, Not Forensic-Grade)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat Devid_evidence.img > Devid_working.img
```

> ⚠️ **Warning:** `cat` produces a valid bit-for-bit copy but generates no hash or log. Acceptable for a classroom lab, **not** for real casework.

---

### Method Comparison Table

| Method | Forensic Log | Auto Hash | Handles Bad Sectors | Speed |
|--------|-------------|-----------|-------------------|-------|
| `dc3dd` | ✅ Yes | ✅ Yes | ✅ Yes | Fast |
| `dd` | ❌ No | ❌ No | With `noerror` | Fast |
| `ddrescue` | ✅ Yes | ❌ No | ✅ Best | Slower |
| `dd + tee` | ❌ No | ✅ Yes | Partial | Fast |
| `cat` | ❌ No | ❌ No | ❌ No | Fast |

---

## Q1(b) — Generate MD5 and SHA-256 Hash Values `[1 Marks]`

### ✅ Best Answer — md5sum + sha256sum

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ md5sum Devid_evidence.img > Devid_evidence.md5.txt
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sha256sum Devid_evidence.img > Devid_evidence.sha256.txt
```

**Terminal Output (verify the saved files):**

```
┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat Devid_evidence.md5.txt
ddeeeb30bd85ec8f9b776ff366c9f432  Devid_evidence.img

┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat Devid_evidence.sha256.txt
ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f  Devid_evidence.img
```

---

### Method 2 — Combined Single Command (Both Hashes at Once)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ md5sum Devid_evidence.img | tee Devid_evidence.md5.txt && sha256sum Devid_evidence.img | tee Devid_evidence.sha256.txt
```

**Terminal Output:**

```
ddeeeb30bd85ec8f9b776ff366c9f432  Devid_evidence.img
ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f  Devid_evidence.img
```

---

### Method 3 — shasum with Algorithm Specification

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ shasum -a 256 Devid_evidence.img > Devid_evidence.sha256.txt
┌──(hexx㉿hexx)-[~/IA-1]
└─$ shasum -a 512 Devid_evidence.img > Devid_evidence.sha512.txt
```

---

### Method 4 — OpenSSL

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ openssl md5 Devid_evidence.img
┌──(hexx㉿hexx)-[~/IA-1]
└─$ openssl sha256 Devid_evidence.img
```

**Terminal Output:**

```
MD5(Devid_evidence.img)= ddeeeb30bd85ec8f9b776ff366c9f432
SHA2-256(Devid_evidence.img)= ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f
```

---

### Method 5 — hashdeep (Multiple Algorithms Simultaneously)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ hashdeep -c md5,sha256 Devid_evidence.img > Devid_evidence.hashes
┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat Devid_evidence.hashes
```

**Terminal Output:**

```
%%%% HASHDEEP-1.0
%%%% size,md5,sha256,filename
## Invoked from: /home/hexx/IA-1
## $ hashdeep -c md5,sha256 Devid_evidence.img
##
209715200,ddeeeb30bd85ec8f9b776ff366c9f432,ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f,Devid_evidence.img
```

---

### Generated Hash Values (Reference)

| Algorithm | Hash Value |
|-----------|-----------|
| MD5 | `ddeeeb30bd85ec8f9b776ff366c9f432` |
| SHA-256 | `ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f` |

> **MD5 vs SHA-256:** MD5 is fast and widely used in legacy tools, but is cryptographically broken (collision attacks possible). SHA-256 is the current standard. Always generate both for interoperability.

---

### Verifying the Working Copy Against Original Hash

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sha256sum -c Devid_evidence.sha256
```

**Terminal Output (Success):**

```
Devid_evidence.img: OK
```

**Terminal Output (Failure — evidence of tampering):**

```
Devid_evidence.img: FAILED
sha256sum: WARNING: 1 computed checksum did NOT match
```

---

## Q1(c) — Why Hash Verification is Critical `[1 Mark]`

Hash verification is the **cornerstone of digital forensic integrity**. It answers the fundamental question: *"Is what we are analysing exactly what was seized?"*

| Reason | Explanation |
|--------|------------|
| **Data Integrity** | Cryptographic hashes provide mathematical proof the file is unaltered. Even a single flipped bit produces a completely different hash — it is computationally infeasible to create a modified file with the same hash. |
| **Chain of Custody** | Hash values create an auditable record linking the analysed copy back to the original seized media at every transfer point (seizure → lab → analyst → court). |
| **Court Admissibility** | Courts require proof that digital evidence is authentic and unaltered. Hash verification meets both Daubert and Frye standards as a scientifically accepted methodology. |
| **Error Detection** | Media corruption or copying errors during transfer change the hash, alerting the investigator to problems *before* analysis produces unreliable results. |
| **Reproducibility** | Any party (prosecution, defence, independent experts) can verify they are working with bit-for-bit identical evidence, ensuring scientific transparency. |
| **Tamper Detection** | If evidence is maliciously modified after seizure, the hash will no longer match — making tampering immediately detectable. |

**In this case specifically:** The script generates `Devid_evidence.md5.txt` and `Devid_evidence.sha256.txt` at creation time. Any forensic examiner who later runs `sha256sum -c Devid_evidence.sha256` and sees `OK` can prove to a court that the image they analysed is identical to the image that was created from Devid's USB drive.

---

---

# Question 2 — Analyse Partition and Recover Deleted Files `[4 Marks]`

---

## Q2(a) — Partition Structure and Starting Sector Offset `[1 Mark]`

### ✅ Best Answer — mmls (The Sleuth Kit)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ mmls Devid_evidence.img
```

**Terminal Output:**

```
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000401407   0000399360   Win95 FAT32 (0x0b)
003:  -------   0000401408   0000409599   0000008192   Unallocated
```

**Answer:** The starting sector offset is **2048**.

This is why all Sleuth Kit commands use `-o 2048` — it tells the tool to skip the first 2048 × 512 = 1,048,576 bytes (1 MB MBR area) before reading the FAT32 filesystem.

---

### Method 2 — fdisk

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ fdisk -l Devid_evidence.img
```

**Terminal Output:**

```
Disk Devid_evidence.img: 200 MiB, 209715200 bytes, 409600 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xf298c5d6

Device              Boot  Start    End  Sectors  Size Id Type
Devid_evidence.img1        2048 401407   399360  195M  b W95 FAT32
```

---

### Method 3 — parted

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ parted Devid_evidence.img print
```

**Terminal Output:**

```
Model:  (file)
Disk /home/hexx/IA-1/Devid_evidence.img: 210MB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  206MB   205MB   primary  fat32        lba
```

---

### Method 4 — sfdisk

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sfdisk -l Devid_evidence.img
```

**Terminal Output:**

```
Disk Devid_evidence.img: 200 MiB, 209715200 bytes, 409600 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512/512 bytes
I/O size (minimum/optimal): 512/512 bytes
Disklabel type: dos
Disk identifier: 0xf298c5d6

Device              Boot Start    End Sectors  Size Id Type
Devid_evidence.img1      2048  401407  399360  195M  b W95 FAT32
```

---

### Partition Layout Summary

| Field | Value |
|-------|-------|
| Partition table type | MBR (DOS) |
| Disk identifier | 0xf298c5d6 |
| Starting sector offset | **2048** |
| End sector | 401407 |
| Partition length | 399,360 sectors |
| Partition size | 195 MB |
| Filesystem | Win95 FAT32 (type code 0x0b) |
| Byte offset formula | 2048 × 512 = **1,048,576 bytes** |
| Unallocated before (MBR area) | 2048 sectors (1 MB) |
| Unallocated after (tail) | 8192 sectors (4 MB) |

---

## Q2(b) — List All Deleted Files `[1 Mark]`

In FAT32, deleting a file marks its directory entry with `0xE5` as the first byte of the filename. The data clusters are marked free in the FAT table but are **not zeroed**. The Sleuth Kit's `fls` tool reads these directory entries directly.

### ✅ Best Answer — fls with -d and -r flags

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ fls -o 2048 -rd Devid_evidence.img
```

**Terminal Output:**

```
r/r 3:   Devid_USB   (Volume Label Entry)
r/r 4:   $FAT1
r/r 6:   $FAT2
r/r * 7:   btc_transfer_record.txt
r/r * 8:   project_nightfall.txt
r/r * 9:   passwords_secure.txt
r/r * 10:  offshore_ledger.txt
r/r 11:  work_notes.txt
r/r 12:  personal.txt
r/r 13:  wifi_info.txt
r/r 14:  vacation_photo.jpg
v/v 15:  $MBR
v/v 16:  $FAT1
v/v 17:  $FAT2
V/V 18:  $OrphanFiles
```

**Reading the output:** The asterisk (`*`) before the inode number means the file's directory entry is marked deleted (first byte = `0xE5`). Files without an asterisk are present and accessible normally.

---

### Deleted Files Identified

| Inode | Filename | Forensic Significance |
|-------|----------|-----------------------|
| 7 | `btc_transfer_record.txt` | Cryptocurrency transaction record |
| 8 | `project_nightfall.txt` | Hostile corporate takeover plan |
| 9 | `passwords_secure.txt` | Bank credentials, crypto seed, SSH keys |
| 10 | `offshore_ledger.txt` | Cayman Islands offshore account ledger |

---

### Method 2 — fls with -d flag only (Deleted Only, Cleaner Output)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ fls -o 2048 -d Devid_evidence.img
```

**Terminal Output:**

```
r/r * 7:   btc_transfer_record.txt
r/r * 8:   project_nightfall.txt
r/r * 9:   passwords_secure.txt
r/r * 10:  offshore_ledger.txt
```

---

### Method 3 — fls with Timeline Export

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ fls -o 2048 -rd -m / Devid_evidence.img > timeline.csv
┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat timeline.csv
```

**Terminal Output (mactime format):**

```
0|/btc_transfer_record.txt (deleted)|7|r/rrwxrwxrwx|0|0|482|1710059722|1710059722|1710059722|0
0|/project_nightfall.txt (deleted)|8|r/rrwxrwxrwx|0|0|412|1710059722|1710059722|1710059722|0
0|/passwords_secure.txt (deleted)|9|r/rrwxrwxrwx|0|0|528|1710059722|1710059722|1710059722|0
0|/offshore_ledger.txt (deleted)|10|r/rrwxrwxrwx|0|0|631|1710059722|1710059722|1710059722|0
0|/work_notes.txt|11|r/rrwxrwxrwx|0|0|387|1710059722|1710059722|1710059722|0
```

> This CSV can be imported into Autopsy, log2timeline, or Excel for a full activity timeline.

---

### Method 4 — tsk_recover (Bulk Recovery with List)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ mkdir recovered_all
┌──(hexx㉿hexx)-[~/IA-1]
└─$ tsk_recover -o 2048 -a Devid_evidence.img recovered_all/
┌──(hexx㉿hexx)-[~/IA-1]
└─$ ls -la recovered_all/
```

**Terminal Output:**

```
Files Recovered: 8
total 184
drwxr-xr-x 2 hexx hexx  4096 Apr  9 14:35 .
drwxr-xr-x 5 hexx hexx  4096 Apr  9 14:35 ..
-rw-r--r-- 1 hexx hexx   482 Apr  9 14:35 btc_transfer_record.txt
-rw-r--r-- 1 hexx hexx   412 Apr  9 14:35 offshore_ledger.txt
-rw-r--r-- 1 hexx hexx   312 Apr  9 14:35 personal.txt
-rw-r--r-- 1 hexx hexx   412 Apr  9 14:35 project_nightfall.txt
-rw-r--r-- 1 hexx hexx   528 Apr  9 14:35 passwords_secure.txt
-rw-r--r-- 1 hexx hexx 125952 Apr  9 14:35 vacation_photo.jpg
-rw-r--r-- 1 hexx hexx   418 Apr  9 14:35 wifi_info.txt
-rw-r--r-- 1 hexx hexx   387 Apr  9 14:35 work_notes.txt
```

---

## Q2(c) — Recover One Deleted File and Summarise Contents `[2 Marks]`

### ✅ Best Answer — icat (Inode-Based Single File Recovery)

`icat` reads data directly from the disk using the inode number, bypassing the filesystem's "deleted" marker.

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ icat -o 2048 Devid_evidence.img 7
```

**Terminal Output — btc_transfer_record.txt:**

```
==========================================
BITCOIN TRANSFER CONFIRMATION
==========================================
From: Devid
To: Binance Exchange (Crypto Wallet)
Amount: 2.5 BTC
Transaction ID: a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
Date: 2024-03-10 09:15:22 UTC
Wallet Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
Status: COMPLETED
IP Address: 185.243.112.87
==========================================
```

**Save recovered file to disk:**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ icat -o 2048 Devid_evidence.img 7 > recovered_btc_transfer.txt
┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat recovered_btc_transfer.txt
```

---

### Summary of btc_transfer_record.txt

| Field | Value | Forensic Significance |
|-------|-------|-----------------------|
| Sender | Devid | Links suspect directly to transaction |
| Recipient | Binance Exchange | Crypto exchange used for fund movement |
| Amount | 2.5 BTC | ~$150,000 USD at March 2024 rates |
| Transaction ID | `a7b8c9d0...f0a1b2` | Traceable on Bitcoin blockchain (public ledger) |
| Date/Time | 2024-03-10 09:15:22 UTC | Establishes financial activity timeline |
| Wallet Address | `bc1qxy2kg...x0wlh` | Bitcoin address can be monitored/flagged |
| Status | COMPLETED | Transaction was successfully executed |
| IP Address | 185.243.112.87 | Suspected VPN/proxy server — obfuscation attempt |

---

### All Other Deleted Files Recovered

```bash
# Recover all deleted files by inode
┌──(hexx㉿hexx)-[~/IA-1]
└─$ icat -o 2048 Devid_evidence.img 8 > recovered_project_nightfall.txt
┌──(hexx㉿hexx)-[~/IA-1]
└─$ icat -o 2048 Devid_evidence.img 9 > recovered_passwords_secure.txt
┌──(hexx㉿hexx)-[~/IA-1]
└─$ icat -o 2048 Devid_evidence.img 10 > recovered_offshore_ledger.txt
```

**project_nightfall.txt (inode 8):**

```
==========================================
PROJECT NIGHTFALL - CONFIDENTIAL
==========================================
Meeting Location: Warehouse 42, Dock 7, Mumbai Port
Time: 11:30 PM, March 25, 2024
Attendees: D.K., V.S., R.M.
Agenda: Acquisition of FinTech Startup (Hostile Takeover)
Target: PaySecure India Pvt Ltd
Budget: $2,500,000
Insider Contact: insider.paysecure@protonmail.com
Access Code: NIGHTFALL2024
Payment Method: Untraceable Crypto (Monero)
==========================================
```

> **Forensic note:** V.S. appears here AND in the vacation photo metadata — corroborating co-conspirator identification.

**offshore_ledger.txt (inode 10):**

```
==========================================
OFFSHORE ACCOUNT LEDGER - MARCH 2024
==========================================
Date       | Account         | Amount    | Status
-----------|-----------------|-----------|----------
2024-03-01 | ACC-9982-XYZ    | $25,000   | Received
2024-03-05 | ACC-7765-ABC    | $50,000   | Sent
2024-03-12 | ACC-9982-XYZ    | $75,000   | Received
2024-03-18 | ACC-1123-DEF    | $100,000  | Sent
2024-03-22 | ACC-9982-XYZ    | $45,000   | Pending
==========================================
Total Balance (ACC-9982-XYZ): $145,000
Bank: Cayman National Bank
SWIFT: CNBKYKYKXXX
==========================================
```

---

### Alternative Recovery Methods

**Method 2 — foremost (File Carving — Works Without Directory Entries)**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ foremost -i Devid_evidence.img -o foremost_output/
```

**Terminal Output:**

```
Processing: Devid_evidence.img
|**foundat=0x00000000 (0)*
Finish

┌──(hexx㉿hexx)-[~/IA-1]
└─$ ls foremost_output/
audit.txt  jpg  txt

┌──(hexx㉿hexx)-[~/IA-1]
└─$ cat foremost_output/audit.txt
Foremost version 1.5.7
Start: Tue Apr  9 14:40:00 2024
Length: 200 MB (209715200 bytes)

Num      Name  (bs=512)       Size   File Offset   Comment
0:    00019204.jpg           125 KB         9832
1:    00019456.txt             482 B         9961
...
```

> **Key difference:** `foremost` carves by file signatures (magic bytes) — it doesn't need directory metadata. It recovers files even if the FAT directory entries are overwritten.

**Method 3 — scalpel (Configurable Carving)**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sudo scalpel -c /etc/scalpel/scalpel.conf -o scalpel_output/ Devid_evidence.img
```

**Method 4 — testdisk (Interactive GUI Recovery)**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ testdisk Devid_evidence.img
# Navigate: Analyse → Quick Search → List deleted files → Copy
```

---

---

# Question 3 — Image Metadata Analysis `[2 Marks]`

---

## Q3(a) — GPS Coordinates, Device Make and Model `[1 Mark]`

The vacation photo was placed on the drive by the script with full EXIF metadata embedded using `exiftool`. To extract it, we must first mount the partition.

### ✅ Best Answer — exiftool (Most Comprehensive)

**Step 1: Mount the forensic image (read-only)**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sudo mkdir -p /mnt/analysis
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sudo mount -o ro,offset=$((2048*512)) Devid_evidence.img /mnt/analysis
```

**Terminal Output:**

```
(no output — silent success)
```

**Step 2: Extract all metadata**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ exiftool /mnt/analysis/vacation_photo.jpg
```

**Terminal Output (Full):**

```
ExifTool Version Number         : 13.50
File Name                       : vacation_photo.jpg
File Size                       : 125 kB
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Exif Byte Order                 : Big-endian (Motorola, MM)
Make                            : Apple
Camera Model Name               : iPhone 14 Pro
Orientation                     : Horizontal (normal)
X Resolution                    : 72
Y Resolution                    : 72
Resolution Unit                 : inches
Software                        : iOS 17.3.1
Modify Date                     : 2024:03:15 14:23:45
Artist                          : Devid
Copyright                       : Devid
Exposure Time                   : 1/120
F Number                        : 1.8
Exposure Program                : Program AE
ISO                             : 64
Date/Time Original              : 2024:03:15 14:23:45
Create Date                     : 2024:03:15 14:23:45
Brightness Value                : 5.2
Flash                           : Off, Did not fire
Focal Length                    : 6.9 mm
Image Description               : Weekend getaway near Lonavala waterfall
User Comment                    : Met with V.S. at the waterfall. Deal confirmed for March 25.
GPS Latitude Ref                : North
GPS Latitude                    : 19 deg 4' 33.60" N
GPS Longitude Ref               : East
GPS Longitude                   : 72 deg 52' 39.72" E
GPS Altitude Ref                : Above Sea Level
GPS Altitude                    : 14 m
GPS Speed Ref                   : km/h
GPS Speed                       : 0
GPS Img Direction Ref           : True North
GPS Img Direction               : 45.5
GPS Date Stamp                  : 2024:03:15
GPS Time Stamp                  : 14:23:45
Image Width                     : 800
Image Height                    : 600
```

**Step 3: Targeted extraction (specific fields only)**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ exiftool -GPSLatitude -GPSLongitude -Make -Model -DateTimeOriginal \
    -ImageDescription -UserComment /mnt/analysis/vacation_photo.jpg
```

**Terminal Output:**

```
GPS Latitude        : 19 deg 4' 33.60" N
GPS Longitude       : 72 deg 52' 39.72" E
Make                : Apple
Model               : iPhone 14 Pro
Date/Time Original  : 2024:03:15 14:23:45
Image Description   : Weekend getaway near Lonavala waterfall
User Comment        : Met with V.S. at the waterfall. Deal confirmed for March 25.
```

**Step 4: Unmount**

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ sudo umount /mnt/analysis
```

---

### Method 2 — Extract Directly Without Mounting (Using Offset)

```bash
# Extract the partition as a raw stream and pipe to exiftool
┌──(hexx㉿hexx)-[~/IA-1]
└─$ dd if=Devid_evidence.img bs=512 skip=2048 | exiftool -stdin
```

---

### Method 3 — Using strings (Quick Scan Without Tools)

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ strings /mnt/analysis/vacation_photo.jpg | grep -E "Apple|iPhone|GPS|2024|Devid|Lonavala"
```

**Terminal Output:**

```
Apple
iPhone 14 Pro
iOS 17.3.1
Devid
Weekend getaway near Lonavala waterfall
Met with V.S. at the waterfall. Deal confirmed for March 25.
2024:03:15 14:23:45
```

---

### Method 4 — exiv2

```bash
┌──(hexx㉿hexx)-[~/IA-1]
└─$ exiv2 -pa /mnt/analysis/vacation_photo.jpg | grep -E "GPS|Make|Model|DateTime|Comment|Artist"
```

**Terminal Output:**

```
Exif.Image.Make                  Ascii      6  Apple
Exif.Image.Model                 Ascii     14  iPhone 14 Pro
Exif.Image.DateTime              Ascii     20  2024:03:15 14:23:45
Exif.Image.Artist                Ascii      6  Devid
Exif.Photo.DateTimeOriginal      Ascii     20  2024:03:15 14:23:45
Exif.GPSInfo.GPSLatitudeRef      Ascii      2  N
Exif.GPSInfo.GPSLatitude         Rational   3  19/1 4/1 3360/100
Exif.GPSInfo.GPSLongitudeRef     Ascii      2  E
Exif.GPSInfo.GPSLongitude        Rational   3  72/1 52/1 3972/100
Exif.GPSInfo.GPSAltitude         Rational   1  14/1
Exif.Photo.UserComment           Comment   44  Met with V.S. at the waterfall. Deal confirmed for March 25.
```

---

### Metadata Summary

| Field | Extracted Value |
|-------|----------------|
| GPS Coordinates (DMS) | 19° 4' 33.60" N, 72° 52' 39.72" E |
| GPS Coordinates (Decimal) | 19.0760° N, 72.8777° E |
| Physical Location | Lonavala Waterfall, Maharashtra, India |
| Google Maps Link | https://maps.google.com/?q=19.0760,72.8777 |
| Device Make | Apple |
| Device Model | iPhone 14 Pro |
| Operating System | iOS 17.3.1 |
| Date and Time | 2024:03:15 14:23:45 (March 15, 2024, 2:23 PM IST) |
| Altitude | 14 metres above sea level |
| Image Description | Weekend getaway near Lonavala waterfall |
| User Comment | Met with V.S. at the waterfall. Deal confirmed for March 25. |
| Artist / Copyright | Devid |

---

## Q3(b) — Why Metadata Analysis is Important in Digital Forensics `[1 Mark]`

**Answer:**

Metadata analysis is critically important because digital files carry hidden, machine-generated data that the user often does not know exists — and therefore cannot easily tamper with. In criminal investigations, this provides objective, verifiable evidence.

**Seven key reasons with examples from this case:**

**1. Suspect Geolocation and Alibi Verification**  
GPS coordinates embedded by the camera application place Devid physically at Lonavala Waterfall (19.0760° N, 72.8777° E) on March 15, 2024 at 14:23:45. If Devid claims to have been in a different city on that date, this metadata directly contradicts his alibi with precise, machine-generated evidence.

**2. Timeline Establishment**  
Date/time stamps create a verifiable chronology:

| Date | Event | Source |
|------|-------|--------|
| 2024-03-01 | Offshore account receives $25,000 | offshore_ledger.txt |
| 2024-03-10 | 2.5 BTC transferred to Binance | btc_transfer_record.txt |
| 2024-03-15 | Meeting with V.S. at Lonavala | vacation_photo.jpg EXIF |
| 2024-03-18 | $100,000 sent from offshore account | offshore_ledger.txt |
| 2024-03-25 | Project Nightfall meeting at Mumbai Port | project_nightfall.txt |

This pattern shows escalating financial activity building toward the planned hostile takeover.

**3. Device Attribution**  
The Make (Apple), Model (iPhone 14 Pro), Artist (Devid), and Copyright (Devid) fields link the photograph to a specific device owned by Devid. Law enforcement can subpoena the device itself for further examination (call logs, messages, other apps).

**4. Co-conspirator Identification**  
The embedded User Comment — "Met with V.S. at the waterfall. Deal confirmed for March 25." — names V.S. as a co-conspirator and directly corroborates the attendee list in `project_nightfall.txt`, where V.S. is also listed. This cross-reference between two independent pieces of evidence significantly strengthens the case.

**5. Consciousness of Guilt Evidence**  
The Image Description reads "Weekend getaway near Lonavala waterfall" — Devid deliberately disguised a criminal meeting as a casual vacation. This demonstrates awareness of wrongdoing and deliberate concealment.

**6. Tampering Detection**  
If metadata has been stripped or modified, the inconsistency itself is evidence of attempted evidence destruction. Tools like `exiftool -history` and comparison with camera manufacturer logs can detect such modifications.

**7. Legal Admissibility**  
EXIF data is machine-generated, not created by the user. Combined with hash verification of the forensic image, it is reliable and admissible as evidence in both Indian courts (under the Information Technology Act) and international proceedings.

---

---

# Complete Command Reference

| Task | Recommended Command |
|------|-------------------|
| Create working copy | `dc3dd if=Devid_evidence.img of=Devid_working.img hof=hash.log log=acq.log` |
| Generate MD5 | `md5sum Devid_evidence.img > Devid_evidence.md5` |
| Generate SHA-256 | `sha256sum Devid_evidence.img > Devid_evidence.sha256` |
| Verify hash | `sha256sum -c Devid_evidence.sha256` |
| View partition layout | `mmls Devid_evidence.img` |
| List all files (inc. deleted) | `fls -o 2048 -rd Devid_evidence.img` |
| List deleted files only | `fls -o 2048 -d Devid_evidence.img` |
| Recover file by inode | `icat -o 2048 Devid_evidence.img <inode>` |
| Bulk recover all files | `tsk_recover -o 2048 -a Devid_evidence.img recovered/` |
| File carving (no metadata) | `foremost -i Devid_evidence.img -o foremost_output/` |
| Mount image (read-only) | `sudo mount -o ro,offset=$((2048*512)) Devid_evidence.img /mnt/analysis` |
| Extract all EXIF metadata | `exiftool /mnt/analysis/vacation_photo.jpg` |
| Extract specific EXIF fields | `exiftool -GPSLatitude -GPSLongitude -Make -Model vacation_photo.jpg` |
| Unmount image | `sudo umount /mnt/analysis` |

---

# Hash Reference

| File | MD5 | SHA-256 |
|------|-----|---------|
| Devid_evidence.img | `ddeeeb30bd85ec8f9b776ff366c9f432` | `ff4f7bc54645e9e652f3f18b2ad2d2779e2cd6c599cba38ecc330ba1ac8f281f` |

---

# Key Evidence Summary

| Evidence | File | Status | Forensic Value |
|----------|------|--------|---------------|
| 2.5 BTC transfer to Binance | `btc_transfer_record.txt` | Deleted (recoverable) | Financial crime, blockchain traceable |
| Hostile takeover plan | `project_nightfall.txt` | Deleted (recoverable) | Criminal conspiracy, names co-conspirators |
| Bank and crypto credentials | `passwords_secure.txt` | Deleted (recoverable) | Account access, crypto seed phrase |
| Offshore account ledger | `offshore_ledger.txt` | Deleted (recoverable) | $295,000 in Cayman bank transactions |
| GPS photo — Lonavala meeting | `vacation_photo.jpg` | Present (visible) | Places Devid with V.S. on March 15 |

---

*"In digital forensics, the truth is always in the data — you just need to know where to look."*

---
**End of Internal Assessment 1 — Complete Solution Notes**
