---
tags: [ctf, solution, unit4, forensics, fat32, deleted-recovery, fls, icat]
challenge: "03 — Deleted But Not Gone (kl.log)"
flag: "Cywarx{s3ct0r_z3r0_n3v3r_li3s}"
points: 100
difficulty: Easy-Medium
topic: FAT32 Deleted File Recovery
image: ctf1.img → P2 (offset 133120)
---

# 🗑️ Challenge 03 — Deleted But Not Gone

> [!success] Flag
> `Cywarx{s3ct0r_z3r0_n3v3r_li3s}`

> [!info] Real World Case — Enron Scandal (2001)
> Employees deleted over 200,000 incriminating emails before the SEC investigation. Forensic teams used Sleuth Kit tools identical to `fls` and `icat` to recover them from FAT-based mail servers. Those recovered emails directly convicted executives who claimed they knew nothing. The phrase "deleted but not gone" defined digital forensics as a legal discipline.

---

## 📋 Challenge Summary

Rohan deleted `kl.log` — his keylogger capture file containing the bank admin credentials. He thought deletion meant destruction. In FAT32, deletion only marks the first byte of the directory entry as `0xE5`. The data clusters are **completely untouched**.

**Recovery target:** `kl.log` on P2 (BACKUP partition, offset sector 133120)

---

## 🧠 Concept — FAT32 Deletion

```
BEFORE deletion:
  Directory entry:  k l . l o g [size] [cluster] [date]
  First byte:       0x6B  ('k')
  FAT chain:        [cluster 8] → [END]
  Data cluster 8:   "[KeyLogger Log]\n..."   ← FULL DATA

AFTER deletion:
  Directory entry:  0xE5 l . l o g [size] [cluster] [date]
  First byte:       0xE5  (deleted marker)
  FAT chain:        [0x0000] → [free]      ← chain cleared
  Data cluster 8:   "[KeyLogger Log]\n..."   ← UNTOUCHED!
```

> [!important] The key insight
> Only the **directory entry first byte** changes to `0xE5`.
> The **data clusters are never zeroed** until overwritten by new data.

---

## 🔍 Method 1 — fls + icat (Sleuth Kit) ← Primary Method

### Step 1: List deleted files on P2

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

The `*` means **deleted**. The number is the **inode** (FAT directory entry number).

### Step 2: Recover kl.log using icat

```bash
icat -o 133120 ctf1.img 8
```

**Output:**
```
[KeyLogger Log]
Date: 2024-03-17 09:15:22  Machine: ROHAN-LAPTOP
09:15:48 - Typed: S3cr3t@123
09:22:11 - Clipboard: 75842 records for export
09:28:55 - Window: WinSCP - 185.44.21.9
09:31:44 - Transfer complete: customer_export.csv 76.4MB
Credentials: admin:S3cr3t@123
Flag: s3ct0r_z3r0_n3v3r_li3s
```

### Step 3: Save to file

```bash
icat -o 133120 ctf1.img 8 > recovered_kl.log
cat recovered_kl.log
```

---

## 🔍 Method 2 — Autopsy (GUI)

```
1. Autopsy → New Case → Add Image → ctf1.img
2. Wait for ingest to complete
3. Left panel → Data Sources → ctf1.img → vol2 (BACKUP)
4. Click "Deleted Files" in the tree
5. Find kl.log → right-click → Extract File
6. Open in text editor → read flag
```

---

## 🔍 Method 3 — strings (quick dirty)

```bash
strings ctf1.img | grep -A5 "KeyLogger"
```

**Output:**
```
[KeyLogger Log]
Date: 2024-03-17 09:15:22  Machine: ROHAN-LAPTOP
09:15:48 - Typed: S3cr3t@123
...
Flag: s3ct0r_z3r0_n3v3r_li3s
```

---

## 🔍 Method 4 — foremost carving

```bash
mkdir /tmp/fm_out
foremost -t all -i ctf1.img -o /tmp/fm_out/ -q
ls /tmp/fm_out/
```

Then look in the output folder for recovered text files.

---

## 🔍 Method 5 — istat (examine inode metadata)

```bash
# Show full metadata for kl.log inode
istat -o 133120 ctf1.img 8
```

**Output:**
```
Directory Entry: 8
Allocated: No   ← deleted
File Attributes: File
Size: 247
Name: kl.log

Directory Entry Times:
Written:   2024-03-17 09:31:45
Accessed:  2024-03-17 09:31:45
Created:   2024-03-17 09:15:22

Sectors:
1060 1061 1062 1063
```

This proves the file existed and was last written at 09:31:45 — right after the WinSCP upload completed.

---

## 🔬 Key Concepts

> [!note] 0xE5 Deletion Marker
> FAT32 deletion replaces only the first character of the filename with `0xE5` (the byte for a smiling face in old DOS character sets). This was a design choice for speed — zeroing clusters would be slow on 1980s hardware.

> [!note] fls vs ls
> `ls /mnt/p2` reads the live mounted file system — deleted files are invisible.
> `fls -r -d -o 133120 ctf1.img` reads the raw FAT directly and shows all entries including deleted ones. Always use `fls` in forensics.

> [!note] Why inode 8?
> FAT32 doesn't have true inodes. Sleuth Kit assigns sequential numbers to directory entries. Count from the root: the root directory itself is inode 2, then each file/folder gets the next number.

---

## 🔗 Related Challenges
- [[CTF-04-Deleted-invoice-exe]] — Recovering the keylogger binary (MZ bytes)
- [[CTF-05-Deleted-winscp-log]] — FTP exfiltration log recovery
- [[CTF-09-Full-Investigation]] — Combining all recovered evidence
