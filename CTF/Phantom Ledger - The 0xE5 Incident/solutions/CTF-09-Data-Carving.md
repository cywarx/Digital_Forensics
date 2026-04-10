---
tags: [ctf, solution, unit4, forensics, data-carving, foremost, magic-bytes, zip]
challenge: "09 — Carving the Void"
flag: "Cywarx{c4rv1ng_f1nd5_th3_truth}"
points: 250
difficulty: Hard
topic: Data Carving — Unallocated Space
image: ctf1.img → unallocated tail space (after P3)
---

# 🪚 Challenge 09 — Carving the Void

> [!success] Flag
> `Cywarx{c4rv1ng_f1nd5_th3_truth}`

> [!info] Real World Case — CAID (Child Abuse Image Database)
> UK investigators use hash-matching combined with data carving to systematically identify known illegal content on seized devices. Even when drives are completely formatted or file systems destroyed, carving tools recover files by their magic byte signatures. The same technique recovered critical evidence in WannaCry investigations when affected NHS servers were formatted before backup — carved fragments from unallocated space proved infection timelines.

---

## 📋 Challenge Summary

Three JPEG fragments and one ZIP archive are hidden in the **unallocated space** beyond the P3 partition — completely outside any file system. No `fls` entry exists for them. No `icat` inode points to them. The only way to find them is raw byte carving by magic signature.

**Location:** After sector 1,034,239 (end of P3) — in the image tail space

---

## 🧠 Concept — Data Carving

```
Traditional recovery (needs file system):
  Directory → FAT/MFT entry → cluster chain → data

Data carving (NO file system needed):
  Raw bytes → scan for FF D8 FF (JPEG start) →
  capture bytes → scan for FF D9 (JPEG end) →
  save everything between = recovered file
```

> [!important] When to use carving
> - File system destroyed (format, corruption)
> - File was never in a file system (hidden in gaps/tail)
> - File system entry deleted AND cluster overwritten
> - Anti-forensics tools zeroed the FAT/MFT
>
> Carving loses filenames but recovers content from any raw storage.

---

## 🧠 Magic Bytes Reference

| Type | Header Hex | Footer Hex | Notes |
|------|-----------|-----------|-------|
| JPEG | `FF D8 FF` | `FF D9` | Most common |
| PNG | `89 50 4E 47` | `49 45 4E 44 AE 42 60 82` | 8-byte header |
| PDF | `25 50 44 46` (%PDF) | `25 25 45 4F 46` (%%EOF) | |
| ZIP | `50 4B 03 04` (PK) | `50 4B 05 06` | |
| EXE | `4D 5A` (MZ) | none | Size-limited |

---

## 🔍 Method 1 — foremost (primary carving tool)

```bash
# Create output directory
mkdir -p /tmp/carved

# Carve all known types from full image
foremost -t jpg,zip -i ctf1.img -o /tmp/carved/ -v
```

**Output:**
```
Foremost version 1.5.7
Audit File

Foremost started at 2024-03-21 10:00:00
Output directory: /tmp/carved/
Configuration file: /etc/foremost.conf

    File: ctf1.img

Start: 2024-03-21 10:00:00
Length: 512 MB

jpg     : 3 files recovered
zip     : 1 file  recovered

Finish: 2024-03-21 10:04:32
```

```bash
# Check what was found
ls /tmp/carved/jpg/
ls /tmp/carved/zip/
cat /tmp/carved/audit.txt
```

**Output (audit.txt):**
```
jpg:  file found at 0x1F800000 (JPEG)
jpg:  file found at 0x1F900000 (JPEG)
jpg:  file found at 0x1FA00000 (JPEG)
zip:  file found at 0x1FB00000 (ZIP)
```

### Extract and read the ZIP

```bash
ls /tmp/carved/zip/
# 00000000.zip  (named by byte offset)

unzip /tmp/carved/zip/00000000.zip -d /tmp/carved/zip/extracted/
cat /tmp/carved/zip/extracted/recovered_evidence.txt
```

**Output:**
```
RECOVERED BY DATA CARVING
Suspect: Rohan Mehta
Flag: c4rv1ng_f1nd5_th3_truth
```

> [!success] Flag: `Cywarx{c4rv1ng_f1nd5_th3_truth}`

---

## 🔍 Method 2 — scalpel (faster, configurable)

```bash
# Install
sudo apt install scalpel -y

# Edit config: uncomment jpg and zip lines
sudo nano /etc/scalpel/scalpel.conf
# Uncomment:
#   jpg  y  200000000  \xff\xd8\xff\xe0  \xff\xd9
#   zip  y  10000000   PK\x03\x04

# Run
mkdir -p /tmp/scalpel_out
scalpel ctf1.img -o /tmp/scalpel_out/

# Read ZIP contents
unzip /tmp/scalpel_out/zip-0-0/*.zip -d /tmp/scalpel_out/unzipped/
cat /tmp/scalpel_out/unzipped/recovered_evidence.txt
```

---

## 🔍 Method 3 — binwalk (firmware/embedded analysis)

```bash
# Scan for embedded files
binwalk ctf1.img | tail -20
```

**Output:**
```
DECIMAL     HEXADECIMAL  DESCRIPTION
──────────────────────────────────────────────────────
...
528482304   0x1F800000   JPEG image data, JFIF standard
534773760   0x1FB00000   Zip archive data
534773760   0x1FB00000   End of Zip archive
```

```bash
# Extract all embedded files
mkdir /tmp/binwalk_out
binwalk -e ctf1.img -C /tmp/binwalk_out/
ls /tmp/binwalk_out/
```

---

## 🔍 Method 4 — Python manual carving

```python
python3 << 'EOF'
import zipfile, io

JPEG_SIG = b'\xFF\xD8\xFF'
JPEG_END = b'\xFF\xD9'
ZIP_SIG  = b'PK\x03\x04'

with open('ctf1.img', 'rb') as f:
    data = f.read()

# Find ZIP
pos = 0
while True:
    idx = data.find(ZIP_SIG, pos)
    if idx == -1: break
    print(f"ZIP found at offset: {idx} ({hex(idx)})")
    # Try to read as ZIP
    try:
        zf = zipfile.ZipFile(io.BytesIO(data[idx:idx+10000]))
        for name in zf.namelist():
            content = zf.read(name).decode('utf-8', errors='replace')
            print(f"  File: {name}")
            print(f"  Content: {content[:200]}")
    except:
        pass
    pos = idx + 1

EOF
```

---

## 🔍 Method 5 — photorec (GUI-based carving)

```bash
photorec ctf1.img
```

Navigate the menu:
```
→ Select ctf1.img
→ Select "Whole disk"
→ Select output directory /tmp/photorec_out/
→ Search
```

PhotoRec carves dozens of file types by default including JPEG and ZIP.

---

## 🔬 Understanding the Offset

```python
python3 -c "
# P3 ends at sector 1,034,239
P3E = 1034239
TAIL_BASE = (P3E + 1) * 512
print(f'P3 ends at byte: {TAIL_BASE:,}')
print(f'P3 ends at hex:  {hex(TAIL_BASE)}')
print(f'JPEG 1 at:       {hex(TAIL_BASE)}')
print(f'JPEG 2 at:       {hex(TAIL_BASE + 1*1024*1024)}')
print(f'ZIP at:          {hex(TAIL_BASE + 5*1024*1024)}')
"
```

**Output:**
```
P3 ends at byte: 529,530,880
P3 ends at hex:  0x1F900000
JPEG 1 at:       0x1F900000
JPEG 2 at:       0x1FA00000
ZIP at:          0x1FB00000
```

These are in completely **unallocated space** — no file system, no FAT, no MFT. Invisible to standard tools.

---

## 🔬 Key Concepts

> [!note] Why does carving lose filenames?
> Carving reads raw bytes — it finds headers and footers but has no knowledge of the file system's directory structure. The filename was stored in the directory entry (FAT) or MFT (NTFS), which may be gone. The file content survives; the filename does not.

> [!note] File offset as forensic evidence
> `foremost` names recovered files by their byte offset: `00000000.zip` = found at byte 0, `1FB00000.zip` = found at hex offset 0x1FB00000. This offset can be documented as evidence: "File recovered at exact byte position 529,530,880 in the image."

> [!note] Fragmented files
> If a file was fragmented across non-contiguous clusters, carving may produce a corrupted output — the bytes between header and footer may include fragments from other files. This is more common on heavily used drives.

---

## 🔗 Related Challenges
- [[CTF-04-Deleted-invoice-exe]] — Magic bytes in recovered EXE
- [[CTF-09-Full-Investigation]] — All evidence combined
