# Internal Assessment-1 — Short Solutions
## The Devid Case

**Evidence File:** `Devid_evidence.img` (200 MB · MBR · FAT32)

---

## Q1. Create Copy and Verify Hash `[4 Marks]`

### (a) Create a working copy

**Command:**
```bash
dc3dd if=Devid_evidence.img of=Devid_working.img hash=sha256 hof=Devid_working.hash log=acquisition.log
```

**Output:**
```zsh
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

> **Note:** `dc3dd` copies and hashes in one pass and produces a forensic acquisition log — preferred over plain `dd` for court-admissible work.

---

### (b) Generate MD5 and SHA-256 hashes of the original image

**Commands:**
```bash
md5sum Devid_evidence.img > Devid_evidence.md5.txt

sha256sum Devid_evidence.img > Devid_evidence.sha256.txt
```

```zsh
cat Devid_evidence.md5.txt Devid_evidence.sha256.txt 
```

**Output:**
```zsh
5d7a6565a327bcebf92bb96d8d413bd1  Devid_evidence.img

4ec013c17ddf4d5acff3351d2086da76231d7532b3a0cf51b71a5683311f10c3  Devid_evidence.img

```

**Verify the working copy matches:**
```bash
sha256sum -c Devid_evidence.sha256.txt
```

**Output:**
```zsh
Devid_evidence.img: OK
```

---

### (c) Why is hash verification critical before forensic analysis?

Hash verification ensures **evidence integrity** — it mathematically proves the working copy is a bit-for-bit identical clone of the original seized evidence.

- **MD5 / SHA-256** are one-way functions: even a single flipped bit produces a completely different hash.
- Before analysis, the hash confirms the image was not accidentally modified during transfer or storage.
- After analysis, matching hashes confirm no tampering occurred — making findings **admissible in court**.
- In India, the **Information Technology Act, 2000** and **Section 65B of the Indian Evidence Act** require proof that digital evidence has not been altered.

---

## Q2. Analyse Partition and Recover Deleted Files `[4 Marks]`

### (a) Partition layout — command and starting sector offset

**Command:**
```zsh
mmls Devid_evidence.img
```

**Output:**
```zsh
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000401407   0000399360   Win95 FAT32 (0x0b)
003:  -------   0000401408   0000409599   0000008192   Unallocated
     
```

**Starting sector offset of the main FAT32 partition = `2048`**

---

### (b) List all deleted files

**Command:**
```bash
fls -o 2048 -rd Devid_evidence.img
```

**Output:**
```
r/r * 16:       btc_transfer_record.txt
r/r * 7843:     project_nightfall.txt
r/r * 7846:     passwords_secure.txt
r/r * 7849:     offshore_ledger.txt
```

> The `*` prefix marks entries as deleted. The number before `:` is the inode.

---

### (c) Recover a deleted file — `offshore_ledger.txt` (inode 8)

**Command:**
```bash
icat -o 2048 Devid_evidence.img 7849 > offshore_ledger.txt
```

```zsh
cat offshore_ledger.txt
```

**Output:**
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

**Summary:** The file is a secret offshore account ledger showing $295,000 in transactions through Cayman National Bank during March 2024 — strong evidence of money laundering.

---

## Q3. Image Metadata Analysis `[2 Marks]`

### (a) GPS coordinates, device make and model

**Step 1 — Mount the image (read-only):**
```bash
sudo mkdir -p /mnt/analysis
sudo mount -o ro,offset=$((2048*512)) Devid_evidence.img /mnt/analysis
```

**Step 2 — Extract metadata with exiftool:**

```bash
exiftool /mnt/analysis/vacation_photo.jpg
```

```bash
exiftool -GPSLatitude -GPSLongitude -GPSAltitude -Make -Model \
    -DateTimeOriginal -ImageDescription -UserComment \
    /mnt/analysis/vacation_photo.jpg
```

**Output:**
```
GPS Latitude                    : 19 deg 4' 33.60" N
GPS Longitude                   : 72 deg 52' 39.72" E
GPS Altitude                    : 14 m Above Sea Level
Make                            : Apple
Camera Model Name               : iPhone 14 Pro
Date/Time Original              : 2024:03:15 14:23:45
Image Description               : Weekend getaway near Lonavala waterfall
User Comment                    : Met with V.S. at the waterfall. Deal confirmed for March 25.
```

**Step 3 — Unmount:**
```bash
sudo umount /mnt/analysis
```

**Findings:**

| Field | Value |
|-------|-------|
| GPS Coordinates | 19.0760° N, 72.8777° E |
| Physical Location | Lonavala Waterfall, Maharashtra, India |
| Device Make | Apple |
| Device Model | iPhone 14 Pro |
| Date & Time | 2024:03:15 14:23:45 |

---

### (b) Why is metadata analysis important in digital forensics?

EXIF metadata is machine-generated and invisible to the casual user, making it difficult to tamper with — and therefore highly reliable as evidence.

**Key reasons:**

1. **Geolocation & alibi verification** — GPS coordinates place Devid at Lonavala Waterfall on March 15, 2024. If he claimed to be elsewhere that day, this directly contradicts his alibi.
2. **Timeline construction** — The timestamp (14:23:45) can be cross-referenced against phone records, CCTV footage, or other digital evidence to build a precise activity timeline.
3. **Device attribution** — Make/Model/Artist fields link the photo to a specific device owned by Devid, which can be seized for further examination.

**Example from this case:**  
The `UserComment` field reads *"Met with V.S. at the waterfall. Deal confirmed for March 25."* — this directly corroborates the attendee list in the recovered `project_nightfall.txt` file (which names V.S. as a co-conspirator), connecting two independent pieces of evidence and strengthening the case for criminal conspiracy.

---

*End of Short Solutions — Internal Assessment 1*
