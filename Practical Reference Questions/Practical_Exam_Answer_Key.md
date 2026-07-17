---
tags: [cyber-forensics, practical-exam, answer-key, solutions, unit-4, unit-5]
aliases: [Practical Exam Answer Key, Digital Forensics Practical Exam Solutions]
date: 2026-07-17
---

# 🔑 DIGITAL FORENSICS — PRACTICAL EXAMINATION ANSWER KEY

Companion solutions for [[Practical_Exam_Questions]]. Each answer gives the terminal method, the GUI (FTK Imager/Autopsy) method where applicable, and the source practical it's drawn from.

---

## Section A — Forensic Imaging & Acquisition

### Q1 — Create a forensic image + hash

**Terminal:**
```bash
dd if=/dev/zero of=pendrive.img bs=1M count=25
sha256sum pendrive.img
# forensic-grade, one pass:
dc3dd if=pendrive.img hash=sha256 log=pendrive.log
```

**FTK Imager (GUI):**
```
File → Create Disk Image → Select Source (Physical/Logical/Image File)
→ Add → Image Type: Raw (dd) or E01 → Set destination folder & filename
→ Finish → Start
```
FTK Imager automatically computes and displays the MD5/SHA-1 hash in the imaging summary once complete — this is your baseline for later integrity checks.
*(Source: [[01. Create a Forensics Image for Practice]], [[Physical-Drive-Image-Creation]])*

---

### Q2 — Partition table + mmls/fsstat + Autopsy check

```bash
dd if=/dev/zero of=pendrive.img bs=1M count=32
parted pendrive.img --script mklabel msdos mkpart primary fat16 1MiB 31MiB
mkfs.fat -F 16 -n "HEXX_USB" --offset 2048 pendrive.img

mmls pendrive.img              # shows the MBR partition table
fsstat -o 2048 pendrive.img    # confirms FAT16 filesystem details
```

**Autopsy:**
```
New Case → Add Data Source → Disk Image or VM File → Browse to pendrive.img
→ Next → Finish
```
In the tree on the left, Autopsy shows a **Volume** node for the partition with its offset and file system type — this should match the offset (`2048` sectors) and type (`FAT16`) reported by `mmls`/`fsstat`.
*(Source: [[01.1 Pendrive_Image_Forensics]])*

---

### Q3 — Mount and browse, terminal vs Autopsy

```bash
mkdir pendrive_mount
sudo mount -o loop,offset=1048576,ro,uid=1000,gid=1000 pendrive.img pendrive_mount/
ls -la pendrive_mount/
sudo umount pendrive_mount/
```

**Autopsy:** add the same image as a data source (as in Q2) and expand the volume node to browse files in the GUI file tree.

**GUI advantage:** Autopsy shows deleted files, thumbnails, and metadata inline without extra commands — good for quickly triaging a case.
**Terminal advantage:** faster for scripting/automation and works over SSH on a headless box with no desktop environment.
*(Source: [[01.1 Pendrive_Image_Forensics]], [[00-Lab-Setup]])*

---

## Section B — Data Recovery & File Carving

### Q4 — Recover a deleted file, terminal + Autopsy, hash match

```bash
fls -d pendrive.img            # lists deleted entries, e.g. inode 6: secret_notes.txt
icat pendrive.img 6 > recovered_notes.txt
sha256sum recovered_notes.txt
```

**Autopsy:**
```
Data Source tree → expand volume → "Deleted Files" node
→ right-click the file → Extract File(s) → save to disk
```
Both files should be **byte-for-byte identical**, so their SHA-256 hashes match — proving the deleted data was recovered intact, since deletion on FAT only marks the directory entry free (`0xE5`); the data blocks remain until overwritten.
*(Source: [[02. Digital_Forensics_Data_Recovery]])*

---

### Q5 — EXIF/GPS metadata, terminal + Autopsy

**Terminal:**
```bash
exiftool -GPSLatitude -GPSLongitude -Make -Model -DateTimeOriginal -UserComment vacation_photo.jpg
```

**Expected output:**
```
GPS Latitude        : 19 deg 4' 33.60" N
GPS Longitude       : 72 deg 52' 39.72" E
Make                : Apple
Model               : iPhone 14 Pro
Date/Time Original  : 2024:03:15 14:23:45
User Comment        : Met with V.S. at the waterfall. Deal confirmed for March 25.
```

**Autopsy:** select the file in the file list → bottom/right panel → **"Metadata"** tab (or the **EXIF/Media** panel) shows the same GPS/Make/Model/DateTime fields extracted automatically.

**Location:** GPS `19.0760° N, 72.8777° E` corresponds to the **Lonavala area near Mumbai, Maharashtra**.
*(Source: [[Internal_Assessment-1_Solutions]])*

---

### Q6 — Carve files with no file system, terminal + Autopsy

```bash
foremost -t jpg,pdf -i pendrive.img -o recovered/
ls recovered/jpg/ recovered/pdf/
```

**Autopsy:** in the data source tree, expand **"Unallocated Space"** — Autopsy's ingest modules (File Type Identification + carving) automatically extract embedded JPEG/PDF files found there and list them under **"$CarvedFiles"**.

**Why carving works without a file system:** header signatures (JPEG `FF D8 FF`, PDF `%PDF-`) and footer signatures (JPEG `FF D9`, PDF `%%EOF`) are unique byte patterns baked into the file format itself — a carving tool scans raw bytes for these markers and extracts everything between a matched header and the next footer, with no need for any directory/inode structure to say where the file is.
*(Source: [[02. Digital_Forensics_Data_Recovery]])*

---

## Section C — Formatted Drives & File Systems

### Q7 — Find hidden files on the evidence image

```bash
sudo mount -o ro,loop pendrive.img pendrive_mount/
ls pendrive_mount/          # default listing — hidden/dot-files do NOT show

ls -la pendrive_mount/      # -a reveals hidden files (names starting with .)
# or, directly on the raw image without mounting:
fls -a pendrive.img
```

**Autopsy:** hidden/dot-files appear automatically in the file tree under the data source — no extra step needed, since Autopsy lists every entry regardless of the "hidden" attribute.

A plain `ls` (or Windows Explorer with hidden files off) silently skips any file whose name starts with `.` — a suspect can rename evidence to `.notes.txt` and it simply won't appear. An investigator must always use `-a`/`-la` (or an Autopsy-style tool that ignores the hidden flag) so nothing on the drive is missed.
*(Source: [[02. Digital_Forensics_Data_Recovery]])*

---

### Q8 — Identify unknown file system by magic bytes

```bash
xxd -l 512 unknown.img | head
# FAT32 → "FAT32   " label around byte 82
# NTFS  → "NTFS    " label around byte 3
# ext4  → magic 0xEF53 at byte offset 1080 (0x438), stored little-endian as 53 EF

fsstat unknown.img   # confirms the type fsstat itself detects
```
*(Source: [[Student-Task-02-Disk-Storage-Analysis]])*

---

### Q9 — Timestamp behaviour across media

```bash
stat original_file.txt          # note Access / Modify / Change times
cp original_file.txt /media/usb/
stat /media/usb/original_file.txt
```
**Modified** time stays the same (file content is byte-identical), but **Created** and **Accessed** times on the copy reset to the moment of the copy — because the copy is treated as a brand-new file entry on the destination file system, regardless of its content matching the original.
*(Source: [[Internal_Assessment-2/Questions]])*

---

## Section D — RAM (Memory) Forensics

### Q10 — Capture RAM with FTK Imager

```
FTK Imager → File → Capture Memory
→ Destination path: C:\evidence\memdump.mem
→ ✅ Include pagefile (optional)
→ Capture Memory
```
RAM must be captured **before** shutdown or disk imaging because it is the **most volatile** piece of evidence in the Order of Volatility — running processes, open network connections, encryption keys, and unsaved data all disappear the instant power is lost, while the disk contents remain stable and can be imaged later.
*(Source: [[Internal_Assessment-2/Topics]], [[03. RAM_Volatile_Memory_Forensics]])*

---

### Q11 — Analyse processes in the memory dump

```bash
vol -f memdump.mem windows.pslist
vol -f memdump.mem windows.pstree
```
Each row reports `PID`, `PPID`, `ImageFileName`, and `CreateTime`. The applications opened before capture (e.g. `notepad.exe`, `chrome.exe`, `AcroRd32.exe`) appear as their own process entries, typically nested under `explorer.exe` in the `pstree` output — confirming they were resident in memory at capture time.
*(Source: [[03.1 RAM Volatility 3]], [[01-Volatility 3 Installation]])*

---

### Q12 — Analyse network activity in the memory dump

```bash
vol -f memdump.mem windows.netscan
```
Columns: `Proto`, `LocalAddr:Port`, `ForeignAddr:Port`, `State` (`ESTABLISHED`/`CLOSED`/`LISTENING`), `PID`, `Owner`. Match the `PID`/`Owner` column back to the process list from Q11 to identify which application owned each connection. `netscan` can recover connections that were already closed by capture time, since it scans the memory pool directly rather than relying on a live connection table.
*(Source: [[03. RAM_Volatile_Memory_Forensics]])*

---

## Section E — Log Analysis & Full Investigation

### Q13 — Web server directory scan detection

```bash
grep -E "DirBuster|Nikto|dirbuster|gobuster" /var/log/apache2/access.log
```
**Attacker IP:** `185.220.101.5`
**Signature:** User-Agents `Nikto/2.1.6` and `DirBuster-1.0-RC1`
**Time window:** `01/Apr/2026 02:00:10 → 02:00:40` — dozens of requests to `/DVWA/`, `/phpmyadmin/`, `/wp-admin/`, `/admin/`, `/backup/`, `/uploads/`, `/includes/`, `/config/`, `/db/` in seconds, mostly returning 403/404.
*(Source: [[Log_Analysis_Digital_Forensics]], `forensics-lab-Logs/`)*

---

### Q14 — SSH brute-force detection

```bash
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
```
**Attacker IP:** `185.220.101.5`
**Evidence:** repeated `Failed password for root`, then `admin`, at roughly one attempt per second starting `Apr 1 02:00:01` — many different usernames tried in rapid succession from a single source IP is the classic brute-force signature (compare to the earlier `172.16.0.5` entries, which show only 2 failed attempts before the connection closed — reconnaissance, not a sustained attack).
*(Source: [[Log_Analysis_Digital_Forensics]], `forensics-lab-Logs/`)*

---

### Q15 — Complete investigation (capstone)

```bash
# 1. Hash and mount read-only
sha256sum Devid_evidence.img
sudo mount -o ro,loop,offset=1048576 Devid_evidence.img /mnt/evidence
```
Also open the image as a **new case in Autopsy** (`Add Data Source → Disk Image or VM File`) alongside the terminal work.

```bash
# 2 & 3. File system, partition layout, deleted files
mmls Devid_evidence.img
fsstat -o 2048 Devid_evidence.img
fls -d -o 2048 Devid_evidence.img
icat -o 2048 Devid_evidence.img <inode> > recovered/btc_transfer_record.txt
```
Or recover the same files via Autopsy's **"Deleted Files"** view.

```bash
# 4. Metadata from recovered photo
exiftool /mnt/evidence/vacation_photo.jpg
```
Or via Autopsy's **Metadata** tab on the file.

```bash
# 5. Timeline
fls -o 2048 -m / Devid_evidence.img > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv
```
Or use Autopsy's built-in **Timeline** feature (bottom toolbar) for the same MAC-time view in a GUI.

**6. Summary (example):**
> The 200 MB FAT32 image contained four visible files and four deleted files, all recovered successfully via both Sleuth Kit and Autopsy. The recovered photo `vacation_photo.jpg` carried GPS coordinates placing the device near Lonavala on 2024-03-15, corroborated by a recovered text file referencing a "deal confirmed for March 25" — consistent with the timeline showing all suspicious files created and deleted within the same session.

*(Source: [[Student-Task-09-10-OS-Artifacts-Investigation]], [[Internal_Assessment-1_Solutions]])*
