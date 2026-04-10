---
tags: [ctf, solution, unit4, forensics, exif, metadata, gps, osint]
challenge: "02 — The Metadata Witness"
flag: "Cywarx{3x1f_k1ll5_4n0nym1ty}"
points: 75
difficulty: Easy
topic: EXIF Metadata — OS Artifacts
image: ctf1.img → /mnt/p2/Photos/fest_2024.jpg
---

# 📷 Challenge 02 — The Metadata Witness

> [!success] Flag
> `Cywarx{3x1f_k1ll5_4n0nym1ty}`

> [!info] Real World Case — Jill Dando Murder (1999)
> BBC presenter Jill Dando was shot outside her home. Barry George was convicted partly because digital evidence from his computer — including timestamps and metadata from downloaded photographs of her — placed him near the scene. Modern smartphones embed GPS coordinates, device fingerprints, and timestamps in every image by default. Most people have no idea this data exists.

---

## 📋 Challenge Summary

Two JPEG photos exist on the suspect's USB. One of them — `fest_2024.jpg` — was taken at the exact time and location the crime was committed. It also contains a hidden flag in the `UserComment` EXIF field. Mount P2 and read the metadata.

**File path:** `/mnt/p2/Photos/fest_2024.jpg`

---

## 🧠 Concept — What is EXIF?

EXIF (Exchangeable Image File Format) is metadata automatically embedded into photos by cameras and smartphones. It includes:

| Field | Contents |
|-------|----------|
| `GPSLatitude / GPSLongitude` | Exact location coordinates |
| `DateTimeOriginal` | Exact capture time |
| `Make / Model` | Device manufacturer and model |
| `UserComment` | Custom text — often overlooked |
| `Software` | App or version used |

> [!warning] EXIF Survives
> EXIF metadata survives: direct file download, copy-paste, email attachment.
> EXIF is **stripped** by: WhatsApp, Twitter, most social media platforms.
> Forensic investigators always check EXIF before trusting any photo-based alibi.

---

## 🔍 Step 1 — Mount P2 and navigate to Photos

```bash
sudo losetup -P /dev/loop0 ctf1.img
sudo kpartx -av /dev/loop0
sudo mkdir -p /mnt/p2
sudo mount /dev/mapper/loop0p2 /mnt/p2
ls /mnt/p2/Photos/
```

**Output:**
```
agra_trip.jpg  fest_2024.jpg
```

---

## 🔍 Method 1 — exiftool (standard)

```bash
exiftool /mnt/p2/Photos/fest_2024.jpg
```

**Output:**
```
ExifTool Version Number         : 12.65
File Name                       : fest_2024.jpg
File Type                       : JPEG
Make                            : Xiaomi
Camera Model Name               : Redmi Note 12
Date/Time Original              : 2024:03:17 14:32:11
GPS Latitude                    : 26 deg 54' 44.64" N
GPS Longitude                   : 75 deg 47' 14.28" E
GPS Position                    : 26 deg 54' 44.64" N, 75 deg 47' 14.28" E
User Comment                    : 3x1f_k1ll5_4n0nym1ty
Comment                         : College Fest 2024
```

> [!success] Flag in `User Comment`: `Cywarx{3x1f_k1ll5_4n0nym1ty}`

---

## 🔍 Method 2 — exiftool filter (fast)

```bash
exiftool /mnt/p2/Photos/fest_2024.jpg | grep -iE "GPS|Comment|Date|Make|Model"
```

**Output:**
```
Make                            : Xiaomi
Camera Model Name               : Redmi Note 12
Date/Time Original              : 2024:03:17 14:32:11
GPS Latitude                    : 26 deg 54' 44.64" N
GPS Longitude                   : 75 deg 47' 14.28" E
User Comment                    : 3x1f_k1ll5_4n0nym1ty
Comment                         : College Fest 2024
```

---

## 🔍 Method 3 — Python PIL (programmatic)

```python
python3 -c "
from PIL import Image
from PIL.ExifTags import TAGS

img = Image.open('/mnt/p2/Photos/fest_2024.jpg')
exif = img._getexif()
if exif:
    for tag_id, val in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f'{tag:30} : {val}')
"
```

---

## 🔍 Method 4 — exiftool on raw image (no mount needed)

```bash
# Extract all JPEGs from image first, then check EXIF
foremost -t jpg -i ctf1.img -o /tmp/jpgs/ -q
exiftool /tmp/jpgs/jpg/00000000.jpg | grep -i comment
```

---

## 🌍 GPS Location Analysis

Coordinates from `fest_2024.jpg`:
- **GPS Latitude:** 26.9124° N
- **GPS Longitude:** 75.7873° E

```python
python3 -c "
lat = 26.9124
lon = 75.7873
print(f'Google Maps: https://maps.google.com/?q={lat},{lon}')
print('Location: Jaipur, Rajasthan, India')
print('Suspect claimed to be at home — contradiction proven by GPS')
"
```

**Location:** Jaipur, Rajasthan, India — the IndusInd Bank branch area.

---

## 📸 Compare Both Photos

```bash
exiftool /mnt/p2/Photos/agra_trip.jpg | grep -E "Date|GPS"
exiftool /mnt/p2/Photos/fest_2024.jpg | grep -E "Date|GPS"
```

**Agra trip (innocent):**
```
Date/Time Original  : 2024:01:15 11:22:05
GPS Position        : 27 deg 10' 36.12" N, 78 deg 0' 17.16" E  ← Agra
```

**Fest 2024 (crime scene time):**
```
Date/Time Original  : 2024:03:17 14:32:11  ← same day as theft
GPS Position        : 26 deg 54' 44.64" N, 75 deg 47' 14.28" E  ← Jaipur bank area
```

> [!warning] Alibi Destroyed
> Rohan claimed he was at college on 2024-03-17. This photo proves he was at the bank location in Jaipur at 14:32 — after the theft at 09:31.

---

## 🔬 Key Concepts

> [!note] UserComment Field
> The `UserComment` EXIF tag is rarely displayed by default image viewers. Suspects often overlook it when trying to scrub metadata. Forensic investigators dump ALL EXIF fields — not just the common ones.

> [!note] Device Fingerprinting
> `Make: Xiaomi  Model: Redmi Note 12` uniquely identifies the physical device. Combined with serial numbers from IMEI records, this can prove which specific phone took the photo.

---

## 🔗 Related Challenges
- [[CTF-01-MBR-Hidden-Marker]] — Hidden data in MBR
- [[CTF-03-Deleted-kl-log]] — Recovering deleted files from FAT32
