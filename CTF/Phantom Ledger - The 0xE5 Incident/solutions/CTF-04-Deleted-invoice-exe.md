---
tags: [ctf, solution, unit4, forensics, magic-bytes, file-signatures, fls, icat]
challenge: "04 — What Am I Really? (invoice.exe)"
flag: "Cywarx{MZ_exe_h1dd3n_4s_txt}"
points: 50
difficulty: Easy
topic: File Signatures & Magic Bytes
image: ctf1.img → P2 deleted file: invoice.exe
---

# 🔍 Challenge 04 — What Am I Really?

> [!success] Flag
> `Cywarx{MZ_exe_h1dd3n_4s_txt}`

> [!info] Real World Case — Malware Attribution (WannaCry, 2017)
> WannaCry analysts identified the ransomware as a Windows PE executable by its `MZ` magic bytes — even after attackers had renamed and repacked it to disguise it. Magic byte analysis is the first step in any malware triage. In the Enron case, forensic teams also identified renamed executable shredding tools by their file signatures, proving deliberate evidence destruction.

---

## 📋 Challenge Summary

Rohan deleted a file named `invoice.exe` — a Windows keylogger executable. Even though it's deleted, `fls` can find it and `icat` can recover it. Reading the first two bytes reveals `MZ` — the Windows PE magic bytes — confirming it's a real executable, not an invoice document.

**Recovery target:** `invoice.exe` on P2 (BACKUP, offset 133120)

---

## 🧠 Concept — Magic Bytes

Every file type has a characteristic byte sequence at its start called **magic bytes** or a **file signature**. These exist regardless of the filename or extension.

```
File Type   Magic Bytes (Hex)      ASCII     Notes
─────────   ──────────────────     ─────     ──────────────────
Windows EXE 4D 5A                  MZ        Mark Zbikowski
JPEG Image  FF D8 FF               ...       Start of image
PNG Image   89 50 4E 47 0D 0A      .PNG\r\n  8-byte signature
PDF         25 50 44 46            %PDF      Ends with %%EOF
ZIP/DOCX    50 4B 03 04            PK        Phil Katz
Linux ELF   7F 45 4C 46            .ELF      Executable
```

`MZ` = Mark Zbikowski, MS-DOS developer. Every Windows EXE/DLL starts with these bytes since 1981.

---

## 🔍 Method 1 — fls + icat + xxd

### Step 1: Find the deleted file

```bash
fls -r -d -o 133120 ctf1.img
```

**Output:**
```
r/r * 7:   invoice.exe
r/r * 8:   kl.log
r/r * 9:   customer_export.csv
...
```

### Step 2: Recover the file

```bash
icat -o 133120 ctf1.img 7 > recovered_invoice.bin
```

### Step 3: Check magic bytes

```bash
xxd recovered_invoice.bin | head -3
```

**Output:**
```
00000000: 4d5a 9000 0300 0000 0400 00ff ff00 0000  MZ..............
00000010: b800 0000 0000 0000 4000 0000 0000 0000  ........@.......
00000020: 5468 6973 2070 726f 6772 616d 2063 616e  This program can
```

**First 2 bytes: `4D 5A` = `MZ` = Windows PE Executable**

### Step 4: Confirm with file command

```bash
file recovered_invoice.bin
```

**Output:**
```
recovered_invoice.bin: MS-DOS executable, MZ for MS-DOS
```

### Step 5: Read the flag inside

```bash
strings recovered_invoice.bin
```

**Output:**
```
This program cannot be run in DOS mode.
KEYLOGGER v2.1
server=185.44.21.9:4444
logfile=C:\Users\Rohan\AppData\Local\Temp\kl.log
Flag: MZ_exe_h1dd3n_4s_txt
```

> [!success] Flag: `Cywarx{MZ_exe_h1dd3n_4s_txt}`

---

## 🔍 Method 2 — foremost file carving

```bash
mkdir /tmp/carve_out
foremost -t exe -i ctf1.img -o /tmp/carve_out/ -q
ls /tmp/carve_out/exe/
```

**Output:**
```
00000000.exe
```

```bash
strings /tmp/carve_out/exe/00000000.exe | grep Flag
```

**Output:**
```
Flag: MZ_exe_h1dd3n_4s_txt
```

---

## 🔍 Method 3 — Python magic bytes check

```python
python3 -c "
import subprocess, sys

# Get inode from fls
fls = subprocess.run(
    'fls -r -d -o 133120 ctf1.img',
    shell=True, capture_output=True, text=True
)
for line in fls.stdout.splitlines():
    if 'invoice' in line:
        inode = line.split()[1].rstrip(':')
        print(f'Found invoice.exe at inode {inode}')
        
        # Recover file
        data = subprocess.run(
            f'icat -o 133120 ctf1.img {inode}',
            shell=True, capture_output=True
        ).stdout
        
        # Check magic bytes
        print(f'First 2 bytes: {data[:2].hex().upper()}')
        print(f'ASCII: {chr(data[0])}{chr(data[1])}')
        print(f'File type: {\"Windows EXE\" if data[:2]==b\"MZ\" else \"Unknown\"}')
"
```

**Output:**
```
Found invoice.exe at inode 7
First 2 bytes: 4D5A
ASCII: MZ
File type: Windows EXE
```

---

## 🔍 Method 4 — binwalk analysis

```bash
# Recover first
icat -o 133120 ctf1.img 7 > invoice_recovered.bin

# Analyse with binwalk
binwalk invoice_recovered.bin
```

**Output:**
```
DECIMAL   HEXADECIMAL   DESCRIPTION
────────────────────────────────────
0         0x0           MS-DOS executable, MZ for MS-DOS
```

---

## 🔬 Key Concepts

> [!note] Why is this important in real cases?
> Attackers often rename malware to look like legitimate files: `invoice.pdf`, `report.docx`, `svchost.exe` in the wrong directory. Magic byte analysis catches these immediately — regardless of what the file is named.

> [!note] The file command
> `file` on Linux reads the first bytes of any file and identifies it by magic bytes. It completely ignores the extension. This is the fastest triage tool for unknown files.

> [!note] MZ history
> The MZ signature dates to MS-DOS 1.0 (1981). Mark Zbikowski designed the DOS executable format. Every single Windows executable for 40+ years has started with his initials.

---

## 🔗 Related Challenges
- [[CTF-03-Deleted-kl-log]] — Recovering kl.log (credential capture log)
- [[CTF-10-Data-Carving]] — Carving with foremost when no FAT entry exists
