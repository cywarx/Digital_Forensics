---
tags: [ctf, solution, unit4, forensics, fat32, fls, icat, ftp, exfiltration]
challenge: "06 — The FTP Trail (winscp_session.log)"
flag: "Cywarx{qu1ck_f0rm4t_15_n0t_w1p3}"
points: 200
difficulty: Medium-Hard
topic: Deleted File Recovery — FTP Exfiltration Evidence
image: ctf1.img → P2 deleted file: winscp_session.log
---

# 📡 Challenge 06 — The FTP Trail

> [!success] Flag
> `Cywarx{qu1ck_f0rm4t_15_n0t_w1p3}`

> [!info] Real World Case — Twitter Hack (2020)
> 17-year-old Graham Ivan Clark used FTP-based tools to exfiltrate stolen session tokens and credentials. Forensic analysis of deleted WinSCP and FileZilla session logs recovered the exact server addresses, timestamps, and transfer volumes — even after Clark had quick-formatted his drives. The logs were recovered in under 3 hours by FBI forensic teams.

---

## 📋 Challenge Summary

Rohan used WinSCP to upload the stolen customer database to an external FTP server. He deleted the session log to hide the server address and credentials. Recover `winscp_session.log` from the P2 partition to find the FTP server and the flag.

**Recovery target:** `winscp_session.log` on P2 (BACKUP, offset 133120)

---

## 🧠 Concept — Why "Quick Format Doesn't Wipe"

The flag `qu1ck_f0rm4t_15_n0t_w1p3` refers to a common misconception: that quick formatting a drive erases its contents.

```
QUICK FORMAT does:
  ✓ Rewrites the File Allocation Table (FAT headers)
  ✓ Marks all clusters as "free" in the bitmap
  ✗ Does NOT zero any data clusters

RESULT: All data is still physically present — just "unmapped"
Tools: TestDisk reconstructs the map; strings/foremost bypass it entirely
```

---

## 🔍 Method 1 — fls + icat (primary)

### Step 1: List all deleted files on P2

```bash
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

### Step 2: Recover winscp_session.log (inode 10)

```bash
icat -o 133120 ctf1.img 10
```

**Output:**
```
WinSCP 6.1 Log
[09:28:55] Connect 185.44.21.9:22
[09:28:56] Login: rohan_upload / Upl04d!99
[09:29:00] Upload customer_export.csv (76,418,048 bytes)
[09:31:44] Upload complete  612 KB/s
FTP: ftp://185.44.21.9  user=rohan_upload  pass=Upl04d!99
Flag: qu1ck_f0rm4t_15_n0t_w1p3
```

> [!success] Flag: `Cywarx{qu1ck_f0rm4t_15_n0t_w1p3}`

---

## 🔍 Method 2 — strings search

```bash
strings ctf1.img | grep -A8 "WinSCP"
```

**Output:**
```
WinSCP 6.1 Log
[09:28:55] Connect 185.44.21.9:22
[09:28:56] Login: rohan_upload / Upl04d!99
...
Flag: qu1ck_f0rm4t_15_n0t_w1p3
```

---

## 🔍 Method 3 — grep for FTP indicators

```bash
strings ctf1.img | grep -iE "ftp://|winscp|upload|rohan_upload"
```

**Output:**
```
FTP: ftp://185.44.21.9  user=rohan_upload  pass=Upl04d!99
WinSCP 6.1 Log
[09:28:55] Connect 185.44.21.9:22
```

---

## 🔍 Method 4 — TestDisk (if P2 was quick-formatted)

If the FAT table was wiped (simulating a quick format scenario):

```bash
testdisk ctf1.img
```

Navigate:
```
→ Analyse → Quick Search
→ Select P2 partition → P (list files)
→ Browse to find winscp_session.log
→ C to copy
```

---

## 🔍 Method 5 — Bulk Extractor (automated artifact harvesting)

```bash
mkdir /tmp/be_out
bulk_extractor -o /tmp/be_out ctf1.img
cat /tmp/be_out/url.txt        # FTP server URLs
cat /tmp/be_out/email.txt      # email addresses found
cat /tmp/be_out/credentials.txt # usernames/passwords
```

Bulk Extractor automatically finds URLs, email addresses, credentials, and network indicators without needing file system access.

---

## 🔬 Evidence Chain

Reading the recovered file, we can build a complete timeline:

```
2024-03-15  09:00   Keylogger installed on bank workstation
2024-03-17  09:15   Admin credentials captured: admin:S3cr3t@123
2024-03-17  09:22   75842 customer records exported to CSV
2024-03-17  09:28   WinSCP opened — connected to 185.44.21.9:22
2024-03-17  09:29   customer_export.csv (76.4MB) upload started
2024-03-17  09:31   Upload complete at 612 KB/s
2024-03-17  09:31   Rohan deleted all USB evidence files
```

> [!warning] Key Finding
> The file `winscp_session.log` proves:
> 1. The suspect deliberately connected to a remote FTP server
> 2. The exact server address: `185.44.21.9`
> 3. The exact credentials used: `rohan_upload / Upl04d!99`
> 4. The exact file transferred: `customer_export.csv` (76.4MB = 75842 records)
> 5. The exact time: `09:28:55 – 09:31:44`

---

## 🔬 Key Concepts

> [!note] WinSCP Session Logs
> WinSCP (Windows Secure Copy) is a popular SFTP/FTP client. It creates session logs by default in `%APPDATA%\WinSCP\`. These logs contain server addresses, usernames, transfer file names, sizes, and timestamps. Even when deleted, they remain in cluster space.

> [!note] Quick Format Reality
> Windows Quick Format (right-click → Format → Quick) only:
> - Rewrites the FAT header and root directory entries
> - Zeros the first few sectors
> - Marks all clusters as "free" in the allocation table
>
> It **does not** zero data sectors. `strings ctf1.img` proves this instantly.

---

## 🔗 Related Challenges
- [[CTF-03-Deleted-kl-log]] — Keylogger credentials (kl.log)
- [[CTF-07-Deleted-customer-csv]] — The stolen customer database
- [[CTF-09-Full-Investigation]] — Complete case reconstruction
