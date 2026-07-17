---
tags: [cyber-forensics, practical-exam, question-paper, unit-4, unit-5]
aliases: [Practical Exam Question Bank, Digital Forensics Practical Exam]
date: 2026-07-17
---

# 🧪 DIGITAL FORENSICS — PRACTICAL EXAMINATION

<div align="center">

**Post Graduate Diploma in Cyber Security and Law**

</div>

---

> [!warning] Instructions
> 1. Attempt **all 15** questions — each is independent unless stated otherwise.
> 2. For every question, submit the **exact command(s) or GUI steps** you used, along with the **output/screenshot**.
> 3. Never work on the original evidence file — always duplicate it first and work on the copy.
> 4. Hash your evidence file before you start and after you finish, and show both hashes.
> 5. You may use any of the lab tools: `dc3dd`, `dd`, Sleuth Kit (`fls`/`icat`/`mmls`/`fsstat`), `exiftool`, `foremost`, **FTK Imager**, **Autopsy**, Volatility 3.

---

## Section A — Forensic Imaging & Acquisition

> [!tip] Tools for this section
> `dd`, `dc3dd` (CLI) · **FTK Imager** (GUI, Windows) · **Autopsy** (for viewing the image afterward)

**Q1. Create a Forensic Image**
Create a **25 MB virtual pendrive image** to use as practice evidence for this exam.
- Use `dd` or `dc3dd` from the terminal, **or**
- Use **FTK Imager → File → Create Disk Image** if working on a Windows lab machine.
- Generate the image's **SHA-256 hash** immediately after creation and record it — this is your baseline integrity value for the rest of the exam.

**Q2. Add a Partition Table and Verify It**
Starting from a blank 32 MB image, add a proper **MBR partition table** with a FAT16/FAT32 partition inside it (instead of a bare filesystem).
- Confirm the partition exists using `mmls`.
- Confirm the filesystem type and details using `fsstat`.
- **Also open the same image in Autopsy** (`Add Data Source → Disk Image or VM File`) and confirm the Volume/Partition view matches what `mmls` reported.

**Q3. Mount and Browse the Evidence**
Mount your image **read-only** and list every file present on it.
- Do this once via the terminal (`mount -o ro,loop`).
- Do it a second time by adding the same image as a data source in **Autopsy** and browsing the file tree in the GUI.
- State one advantage of the GUI view over the terminal view, and one advantage of the terminal view over the GUI.

---

## Section B — Data Recovery & File Carving

> [!tip] Tools for this section
> `fls`, `icat` (CLI) · **Autopsy** (Deleted Files / File Carving modules) · `foremost`

**Q4. Recover a Deleted File**
On your mounted image, create a file, unmount, delete it (by editing the raw image or using a pre-deleted sample), then recover it.
- Recover it using `fls -d` + `icat` from the terminal.
- Recover the **same file** again using Autopsy's **"Deleted Files"** view under the Data Source tree, and export it from there.
- Confirm both recovered copies produce the **same SHA-256 hash** as each other.

**Q5. Extract Photo Metadata (EXIF/GPS)**
You are given a recovered photo, `vacation_photo.jpg`, taken from a suspect's device.
- Extract its metadata using `exiftool` from the terminal — report the **Make, Model, Date/Time Original, GPS Latitude/Longitude**, and any embedded comment.
- Open the same photo inside **Autopsy** and locate the equivalent metadata under the file's **"Metadata"** tab.
- Based on the GPS coordinates, state approximately where the photo was taken.

**Q6. Carve Files With No File System**
Given a raw disk image with damaged/missing file system metadata, recover any JPEG and PDF files hidden inside it.
- Use `foremost -t jpg,pdf` from the terminal.
- Cross-check your results using Autopsy's built-in **file-carving** (Unallocated Space analysis) module.
- Briefly explain how carving tools find files without any file system to guide them.

---

## Section C — Formatted Drives & File Systems

> [!tip] Tools for this section
> `fls`, `ls -la` · `xxd` · `fsstat` · **Autopsy**

**Q7. Find Hidden Files on the Evidence Image**
A suspect may have hidden files on the drive to avoid casual notice.
- Mount the evidence image and list its contents with a plain `ls` — note what you see.
- Now reveal hidden/dot-files using `ls -la` (or list every entry on the raw image with `fls -a`), **or** check the same image in **Autopsy**, which lists hidden files automatically in its file tree.
- Report any hidden files found and explain why an investigator should never trust a "default" file listing alone.

**Q8. Identify an Unknown File System**
You are handed a raw image with no label and no documentation.
- Use `xxd` to inspect the boot sector / superblock and identify the magic bytes that reveal the file system type (FAT / NTFS / ext4).
- Confirm your identification using `fsstat`.

**Q9. Timestamp Behaviour Across Media**
Create a file on your local machine and note its **Created / Modified / Accessed** timestamps (`stat`).
- Copy the file onto a USB drive (or a mounted image) and check its timestamps again.
- State which timestamp(s) changed, which stayed the same, and explain why.

---

## Section D — RAM (Memory) Forensics

> [!tip] Tools for this section
> **FTK Imager** (RAM capture) · Volatility 3 (analysis)

**Q10. Capture RAM**
On a Windows machine, open 3–5 different applications (e.g. Notepad, a browser, a PDF viewer).
- Use **FTK Imager → File → Capture Memory** to dump the live RAM to a `.mem` file.
- State why RAM must be captured **before** the machine is shut down or the disk is imaged (order of volatility).

**Q11. Analyse the Memory Dump — Processes**
Using the RAM image captured in Q10 (or a provided sample):
- Run `vol -f memdump.mem windows.pslist` and `windows.pstree`.
- Identify each of the applications you opened earlier in the process list output.

**Q12. Analyse the Memory Dump — Network Activity**
Using the same memory dump:
- Run `vol -f memdump.mem windows.netscan`.
- Report any active or recently closed network connections and identify the process each one belongs to.

---

## Section E — Log Analysis & Full Investigation

> [!tip] Tools for this section
> `grep` / `awk` (CLI) · **Autopsy** (Timeline module, for Q15)

**Q13. Web Server Attack Detection**
Using the sample Apache `access.log` provided in the lab logs:
- Identify the IP address that is scanning the server for hidden directories/admin panels.
- Report the tool signature (User-Agent) and the time window of the scan.

**Q14. SSH Brute-Force Detection**
Using the sample `auth.log` provided in the lab logs:
- Identify the IP address attempting an SSH brute-force attack.
- Justify your answer with the usernames tried and the timestamps involved.

**Q15. Complete Investigation (Capstone)**
You are given one full evidence image (e.g. the Devid Case image).
1. Hash the image, then mount it read-only (terminal) **and** load it into **Autopsy** as a new case.
2. Identify the file system and partition layout.
3. Recover any deleted files (via `fls`/`icat` **or** Autopsy's Deleted Files view).
4. Extract EXIF/GPS metadata from any recovered photos (`exiftool` or Autopsy's Metadata tab).
5. Build a simple timeline of file Created/Modified/Accessed times — using `mactime`, **or** Autopsy's built-in **Timeline** feature.
6. Write a short (3–4 line) summary of your findings, as you would for a chain-of-custody report.

---

*(All 15 questions are drawn from practicals already covered in class — see [[Practicals_Index]] for the full topic list. Full worked solutions: [[Practical_Exam_Answer_Key]].)*
