---
tags: [ctf, solution, unit4, forensics, mbr, disk-structure]
challenge: "01 — Sector Zero Speaks"
flag: "Cywarx{h3dd3n_m4rk3r}"
points: 175
difficulty: Medium
topic: Storage Fundamentals — MBR & Hidden Data
image: ctf1.img
---

# 🧱 Challenge 01 — Sector Zero Speaks

> [!success] Flag
> `Cywarx{h3dd3n_m4rk3r}`

> [!info] Real World Case — Manchester Arena Bombing (2017)
> Investigators recovered Salman Abedi's encrypted hard drive. Reading raw sectors directly — bypassing the OS entirely — revealed data hidden in non-standard disk regions. The same technique is used in anti-forensics cases where data is buried in the MBR bootstrap area, gaps between partitions, and volume boot records.

---

## 📋 Challenge Summary

The suspect's USB contains a flag **hidden inside the MBR bootstrap code** at byte offset `0x100` (decimal 256). This area is invisible to the OS file browser — you need raw byte access to find it.

**Evidence file:** `ctf1.img`

---

## 🧠 Concept — What is the MBR?

Every bootable disk starts with a **Master Boot Record** at sector 0 (the very first 512 bytes). Its layout:

```
Offset  Size   Contents
0x000   446    Bootstrap code (executes on boot)
0x1BE   64     4 × 16-byte partition entries
0x1FE   2      Boot signature: 55 AA
```

The bootstrap code area (446 bytes) is rarely inspected by standard tools. Data can be hidden there invisibly.

---

## 🔍 Method 1 — Python raw read (fastest)

```python
python3 -c "
f = open('ctf1.img', 'rb')
f.seek(256)
data = f.read(13)
f.close()
print('Hex:', data.hex())
print('ASCII:', data.decode('ascii'))
"
```

**Output:**
```
Hex: 6833 6464 336e 5f6d 34726b3372
ASCII: h3dd3n_m4rk3r
```

> [!success] Flag found: `Cywarx{h3dd3n_m4rk3r}`

---

## 🔍 Method 2 — dd + xxd hex dump

```bash
# Read sector 0 (full MBR) and dump as hex
dd if=ctf1.img bs=512 count=1 2>/dev/null | xxd | head -20
```

**Output:**
```
00000000: eb58 904d 5344 4f53 352e 3000 0000 0000  .X.MSDOS5.0.....
00000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................
...
00000100: 6833 6464 336e 5f6d 3472 6b33 7200 0000  h3dd3n_m4rk3r...
...
000001f0: 0000 0000 0000 0000 0000 0000 0000 55aa  ..............U.
```

Spot the flag at offset `0x100`.

---

## 🔍 Method 3 — dd skip to exact offset

```bash
# Skip 256 bytes, read 13 bytes
dd if=ctf1.img bs=1 skip=256 count=13 2>/dev/null && echo
```

**Output:**
```
h3dd3n_m4rk3r
```

---

## 🔍 Method 4 — strings + grep

```bash
strings ctf1.img | grep -i "h3dd"
```

**Output:**
```
h3dd3n_m4rk3r
```

---

## 🔍 Method 5 — Autopsy (GUI)

1. Open Autopsy → New Case → Add Data Source → `ctf1.img`
2. Go to **Data Artifacts → Other Interesting Files**
3. Or: **Hex Viewer** on the image → navigate to offset `0x100`
4. Read 13 bytes → `68 33 64 64 33 6e 5f 6d 34 72 6b 33 72`
5. Convert hex to ASCII → `h3dd3n_m4rk3r`

---

## 📊 Verify the Boot Signature

```bash
python3 -c "
f = open('ctf1.img','rb')
f.seek(510)
sig = f.read(2)
print('Boot signature:', sig.hex().upper())
print('Valid MBR:', sig == bytes([0x55,0xAA]))
"
```

**Output:**
```
Boot signature: 55AA
Valid MBR: True
```

---

## 📐 Partition Map (bonus)

```bash
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
004: 000:002 0000952320  1034239     0000081920  Linux (0x83)
```

---

## 🔬 Key Concepts

> [!note] Why offset 0x100?
> The bootstrap code area is 446 bytes. Only the first ~3 bytes are a valid jump instruction. The rest (bytes 3–445) is executable code OR arbitrary data. Tools like `fdisk`, `parted`, and Windows Disk Manager never display this region.

> [!warning] Anti-Forensics Technique
> Real attackers use this space to hide configuration data, encryption keys, or C2 server addresses. The MBR is one of the least-inspected regions in standard digital forensics workflows.

> [!tip] Hex Conversion Quick Reference
> ```
> 68 = h    33 = 3    64 = d    64 = d    33 = 3
> 6e = n    5f = _    6d = m    34 = 4    72 = r
> 6b = k    33 = 3    72 = r
> ```

---

## 🔗 Related Challenges
- [[CTF-02-EXIF-Metadata]] — GPS data hidden in JPEG EXIF
- [[CTF-03-Deleted-kl-log]] — FAT32 deleted file recovery
- [[CTF-10-Data-Carving]] — Finding files with no directory entry
