---
tags: [exam, cyber-law-forensics, answer-key]
---

# Practical Exam — Answer Key (Instructor Use)

Course: Post Graduate Diploma in Cyber Security Law
Paper: 92911203 Cyber Law and Forensics
Date: 27 July, 2026

This is the **instructor answer key** for `All-SETs.docx`. Every command below was actually executed on this machine (Kali Linux) against the provided lab files — the outputs shown are real, not invented. Re-running the same commands against the files in `Exam-Files/` will reproduce the same results.

## Contents
- [[#Lab file manifest]]
- [[#How each artifact was built (for reproducibility / regrading)]]
- [[#⚠️ READ FIRST — Autopsy on this machine is version 2.24, not 4.x]]
- [[#Set 1]]
- [[#Set 2]]
- [[#Set 3]]
- [[#Set 4]]

## Lab file manifest

Files are organized into **one folder per set** under `Exam-Files/`, so you can hand each student group only the folder for their assigned set:

| Set | Folder | Contains | Used in |
|---|---|---|---|
| 1 | `Set1_Pendrive_Image_and_File_Timestamps/` | `README.txt` only (student creates their own files) | Q1, Q2 |
| 2 | `Set2_Deleted_File_Recovery_and_Vacation_Photo/` | `deleted_file_lab.img`, `vacation_photo.jpg` | Q1, Q2 |
| 3 | `Set3_IT_Event_Photo_and_SSH_Log/` | `IT_Event.jpg`, `auth.log` | Q1, Q2 |
| 4 | `Set4_Access_Log_and_Secret_File/` | `access.log`, `secret_file.txt` | Q1, Q2 |

Each folder also has a matching **`.zip` beside it** in `Exam-Files/` for handing out — `Set1_….zip` … `Set4_….zip`. Each zip contains its set folder with the same space-free name, and the contents are byte-identical to the live folders (verified by SHA-256 on every file). **If you ever edit a file, re-make that set's zip**, or the handout and the answer key will drift apart:

```bash
cd Exam-Files && rm -f Set2_Deleted_File_Recovery_and_Vacation_Photo.zip \
  && zip -qr Set2_Deleted_File_Recovery_and_Vacation_Photo.zip Set2_Deleted_File_Recovery_and_Vacation_Photo
```

**Two questions name no file in the paper itself** — the wording is generic, and the student identifies the file from the folder they are given:

| Question | Paper says | Actual file |
|---|---|---|
| Set 2 Q1 | "a sample image that already has a deleted file" | `deleted_file_lab.img` |
| Set 4 Q2 | "a secret file with a missing or incorrect extension" | `secret_file.txt` |

That is intentional for Set 4 Q2 (naming it would leak the puzzle). For Set 2 Q1 it simply means the student uses whatever image is in their folder.

SHA-256 baseline hashes (for integrity-checking your master copies before distributing):

| File | SHA-256 |
|---|---|
| `deleted_file_lab.img` | `a577cf530609924f55e3e53e70a0e50bd5aa99b3d65a09e50613139a801ae5d7` |
| `vacation_photo.jpg` | `fe8c58f4f1c6a45a1491f8163f24cf9c5ffe8ac4cf33936685b7c90a1c330525` |
| `IT_Event.jpg` | `af2a7adea656efb6fb4f85933d8fac8e35e5e227d0db6a4fe46467725a248ac7` |
| `auth.log` | `7be11effe92021ea62127cc0aed693990e912d76b176c4a1818a3bd1f843ae8b` |
| `access.log` | `3cfcd134e28acb91040b6d6685942928630d602a2779c80205b10059bd45d9d2` |
| `secret_file.txt` | `db82544ecbd1530686317dc369915f82aaa0edf752c135020f84490034cefd01` |

> Give students a **copy** of their set's folder, not the original — so a re-run of this answer key always has a pristine reference copy to diff against.

> ⚠️ **These folder names are deliberately space-free, and so is the whole path above them.** Autopsy 2.24 cannot open an image from a path containing a space (see the Autopsy section below), so both the set folders *and* the parent directory were renamed: `Digital Forensics/` → `Digital_Forensics/`, and `Set 2 - Deleted File Recovery and Vacation Photo/` → `Set2_Deleted_File_Recovery_and_Vacation_Photo/`. **Keep every component space-free if you rename, copy, or redistribute this material.** Set 2 is the set that matters, being the only one whose questions require loading a disk image into Autopsy.

## How each artifact was built (for reproducibility / regrading)

- **deleted_file_lab.img** — 20 MB image, formatted FAT16 with `mkfs.vfat`. Two files copied in with `mcopy` (`evidence_note.txt`, `readme.txt`); `evidence_note.txt` then removed with `mdel` (a proper FAT directory-entry delete, not a byte-edit) so the file is truly recoverable by TSK the same way a real deleted file would be.
- **vacation_photo.jpg / IT_Event.jpg** — real photographs (not synthetic renders), so they look like genuine camera photos when opened. Sourced from Wikimedia Commons under open licenses, then all original metadata was stripped (`exiftool -all=`) and replaced with the exam's fictional Make/Model/DateTimeOriginal/GPS/Comment values:
  - `vacation_photo.jpg` — "Tropical beach sunset" (Cuba) by Aaron Escobar, CC BY 3.0. Source: https://commons.wikimedia.org/wiki/File:Tropical_beach_sunset.jpg
  - `IT_Event.jpg` — "Contest area Def Con 24" (hacking-contest floor at DEF CON 24), CC BY-SA 3.0. Source: https://commons.wikimedia.org/wiki/File:Contest_area_Def_Con_24.agr.jpg
- **auth.log** — a realistic-sized (224-line) syslog-style SSH log spanning 3 days: hourly `CRON` session noise, a handful of `sudo` sessions, several legitimate logins from internal IPs, one harmless single mistyped password — with the real attack buried inside all of that. Attacker `203.0.113.77` makes 13 failed-login attempts across 10 distinct usernames in ~88 seconds, ending in sshd's own "Too many authentication failures" disconnect.
- **access.log** — a realistic-sized (283-line) Apache combined-format log covering a full day of ordinary traffic (multiple browsers/devices, a legitimate Googlebot crawl) — with scanner `198.51.100.23` requesting 15 admin/hidden paths in ~4 seconds using User-Agent `gobuster/3.6` buried inside it. Deliberately, the scanner is **not** the top IP by raw request count (normal all-day browsing outweighs it) — the giveaway is the non-browser User-Agent plus the burst request rate, which is the more realistic and correct way to spot it.
- **secret_file.txt** — a real photograph (public-domain mountain-sunset landscape, Steve Hillebrand / U.S. Fish and Wildlife Service, source: https://commons.wikimedia.org/wiki/File:Mountain_scenic_landscape_Baboquivari_peak.jpg), with a "MEET AT PIER 9 - 02:00 - CODE: FALCON-77" message overlaid on it, converted to PNG, then saved with a deliberately **incorrect** `.txt` extension (harder than a missing extension — it actively misleads) so `file`/magic-byte inspection is required to identify it and uncover the hidden message.

All IPs used (`203.0.113.0/24`, `198.51.100.0/24`, `192.0.2.0/24`) are IANA-reserved **documentation-only** ranges (RFC 5737) — they don't belong to anyone and are standard practice for lab material, so nothing here points at a real host.

## ✅ READ FIRST — Autopsy 4.23.1 is installed; use it, not the packaged 2.24

**Two Autopsy versions now exist on this machine.** Use 4.23.1 for the exam — it answers every question as written.

| | Autopsy 4.23.1 (installed manually) | Autopsy 2.24 (`apt` package) |
|---|---|---|
| Launch | `autopsy4` (or Applications → Autopsy 4.23.1) | `autopsy` → browser at `localhost:9999` |
| Location | `/home/hexx/autopsy-4.23.1/` | `/usr/bin/autopsy` |
| Interface | Modern Java desktop GUI | Perl web app |
| **EXIF (Date/Time + GPS)** | ✅ **full support** | ❌ Make/Model/Comment only |
| Opens a bare `.jpg` | ✅ yes | ❌ disk images only |
| Paths with spaces | ✅ fine | ❌ rejected |

**Install summary (all components at their latest versions):**

| Component | Version | Notes |
|---|---|---|
| Autopsy | **4.23.1** | latest release; `~/autopsy-4.23.1/` |
| Sleuth Kit (Autopsy's) | **4.15.0** | latest; built from source into `~/autopsy-4.23.1/tsk/` |
| Java runtime | **Liberica JDK 21.0.12 Full** | bundled at `~/autopsy-4.23.1/jre`; JavaFX included |
| Sleuth Kit (system CLI) | 4.14.0 | Kali package — **deliberately left untouched** |

Three things worth knowing, all of which cost time to discover:

1. **Autopsy 4.23.1 needs Java 21, not 17** — its `sleuthkit-4.15.0.jar` is class-file version 65. It also needs **JavaFX**, which plain OpenJDK lacks; Liberica "Full" bundles it. The JDK lives inside the Autopsy directory and `etc/autopsy.conf` points at it with an absolute path, so nothing depends on the system's default Java.
2. **The shipped `sleuthkit-4.15.0.jar` contains only Windows DLLs** — its `NATIVELIBS/amd64/linux/` folder ships empty, so the JNI load fails out of the box with `Library not found in jar (libtsk_jni)`. Fix applied: Sleuth Kit 4.15.0 was compiled from source and the resulting `libtsk_jni.so` injected into the jar at that path (original preserved as `sleuthkit-4.15.0.jar.orig`).
3. **The system's `fls`/`icat`/`fsstat` were deliberately NOT upgraded.** The upstream `sleuthkit-java` .deb would have overwritten `libtsk.so.23`, which is owned by Kali's `libtsk23` package — that risks breaking the very terminal tools the exam depends on. Instead TSK 4.15.0 was installed to a private prefix and `bin/autopsy` sets `LD_LIBRARY_PATH` to it. Verified: system tools remain 4.14.0 and dpkg-managed, and **4.14.0 and 4.15.0 recover `evidence_note.txt` byte-identically** (same SHA-256), so the version difference is immaterial to any answer.
   - If you *want* the 4.15.0 CLI tools, they are at `~/autopsy-4.23.1/tsk/bin/` — run with `LD_LIBRARY_PATH=~/autopsy-4.23.1/tsk/lib`.

### Autopsy 4.23.1 workflow for this exam

1. Launch `autopsy4` → **New Case** → name it → **Next** → **Finish**.
2. **Add Data Source** → choose **Disk Image or VM File** for `deleted_file_lab.img`, or **Logical Files** to add a bare `vacation_photo.jpg` / `IT_Event.jpg` directly.
3. Select ingest modules — keep **Picture Analyzer** (the EXIF processor) enabled for the photo questions. → **Finish**.
4. Deleted files appear under **Data Sources → \<image\> → \$CarvedFiles / Deleted Files**, and in the **Views → Deleted Files** tree node.
5. Select any file → **Metadata** tab (filesystem details) and the **Results → Extracted Content → EXIF Metadata** node (camera fields).
6. Right-click a file → **Extract File(s)** to export it.

> The old Autopsy 2.24 walkthrough is kept below for reference in case you ever fall back to it, but **the 2.24 EXIF limitations no longer constrain the exam** — 4.23.1 displays Date/Time Original and GPS coordinates correctly. Verified on both exam photos.

<details>
<summary>Legacy — Autopsy 2.24 notes (only if you fall back to the apt package)</summary>

This was verified by actually launching Autopsy 2.24 and walking every GUI step (`dpkg -l | grep autopsy` → `2.24-6kali1`). **Kali's `autopsy` package is the old Perl/web-based "Autopsy Forensic Browser".** Three consequences:

**1. The GUI is a web app, not a desktop app.** You start a server and browse to it:
```bash
mkdir -p ~/autopsy_lab/evidence
autopsy -d ~/autopsy_lab/evidence
# then open http://localhost:9999/autopsy in a browser
```
There is no "Data Source tree", no "Extract File(s)", and no EXIF "Metadata" tab. The real workflow is **New Case → Add Host → Add Image File → Analyze**, and the analysis tabs are **File Analysis / Keyword Search / File Type / Image Details / Meta Data / Data Unit**.

**2. 🚨 Autopsy 2.24 REFUSES paths containing spaces.** This is the single biggest exam-day trap. `lib/Main.pm:86` defines the only characters allowed in an image path:
```perl
$::REG_IMG_PATH_WILD = '/[\w\-\_\.\/]+\*?';
```
Word characters, hyphen, underscore, dot, slash — **no space**. Feeding it a path with a space produces a bare error page reading `Invalid wild image (img_path) argument` — no hint about what is wrong, which is why this eats exam time.

### ✅ Both fixes have been applied and verified on this machine

**Fix A — the whole tree is now space-free (applied).** The per-set folders were renamed (`Set 2 - Deleted File Recovery and Vacation Photo/` → `Set2_Deleted_File_Recovery_and_Vacation_Photo/`) **and** the parent directory was renamed:

```bash
mv ~/Documents/"Digital Forensics" ~/Documents/Digital_Forensics
```

Renaming the set folders alone was *not* enough — the space in `Digital Forensics` by itself was sufficient for Autopsy to reject the path. Tested against Autopsy's own regex:

```
REJECT  /home/hexx/Documents/Digital Forensics/Practical_Sets/Exam-Files/Set2_.../deleted_file_lab.img
PASS    /home/hexx/Documents/Digital_Forensics/Practical_Sets/Exam-Files/Set2_.../deleted_file_lab.img
PASS    /home/hexx/autopsy_lab/deleted_file_lab.img
```

**Verified end-to-end in the GUI:** Autopsy 2.24 now loads the image *directly from its exam folder* — no copy step — auto-detects `Partition 1 (Type: fat16)`, and **All Deleted Files** lists `C:/evidence_note.txt` at Meta **6**. The canonical path to give Autopsy is:

```
/home/hexx/Documents/Digital_Forensics/Practical_Sets/Exam-Files/Set2_Deleted_File_Recovery_and_Vacation_Photo/deleted_file_lab.img
```

The Obsidian vault registry (`~/.config/obsidian/obsidian.json`) was updated to the new path at the same time, and the vault was confirmed to open cleanly afterwards.

**Fix B — the copy-to-`~/autopsy_lab/` route still works, and is the safer thing to teach.** Even with Fix A in place, keep this in the student instructions: it is one command, it works on any machine regardless of where the folder lives, and it reinforces the "never work on the original evidence" habit:

```bash
mkdir -p ~/autopsy_lab
cp "Set2_Deleted_File_Recovery_and_Vacation_Photo/deleted_file_lab.img" ~/autopsy_lab/
sha256sum "Set2_Deleted_File_Recovery_and_Vacation_Photo/deleted_file_lab.img" ~/autopsy_lab/deleted_file_lab.img
# then give Autopsy: /home/<user>/autopsy_lab/deleted_file_lab.img
```

Verified — both hashes read `a577cf530609924f55e3e53e70a0e50bd5aa99b3d65a09e50613139a801ae5d7`, and `fls -d` / `icat` recover `evidence_note.txt` identically from the copy. **Make students run that `sha256sum` on both files**: it proves copying evidence does not alter it, which is exactly the integrity principle Set 1 Q1 is testing.

> **If you move this material to another machine**, keep every folder in the path space-free, or fall back to Fix B. The restriction is Autopsy-only — the terminal tools (`fls`, `icat`, `exiftool`, `grep`) handle spaces fine when the path is quoted.

**3. Choose "Partition", not "Disk", on the Add Image screen.** `deleted_file_lab.img` is a bare FAT16 filesystem made with `mkfs.vfat` — it has no partition table. Leaving the default "Disk" makes Autopsy hunt for a nonexistent volume table. Select **Partition** and it correctly reports `Partition 1 (Type: fat16)`.

A harmless cosmetic bug you can ignore: the File Analysis listing prints `Error Parsing File (Invalid Characters?): V/V …: $OrphanFiles` above the file table. That is Autopsy 2.24 choking on its own `$OrphanFiles` pseudo-entry; the real files list correctly underneath it. Also, a few button images are missing from `/usr/share/autopsy/pict/`, so one or two buttons render invisible — they are still there and still clickable.

</details>

## Regenerating fresh copies for exam day

```bash
# fresh disk image + logs + photos + secret file are already sorted per set in Exam-Files/
# just copy out each set's folder per student group so originals stay untouched:
cp -r "Exam-Files/Set2_Deleted_File_Recovery_and_Vacation_Photo" "StudentCopy-Group-A"
```

---

# Set 1

**Folder:** `Exam-Files/Set1_Pendrive_Image_and_File_Timestamps/` (no provided files — see the README inside)

These two questions are **"create your own evidence"** tasks — every student's file, hash, and inode numbers will be different. Below is a real, verified run of the exact commands, done on this machine, to confirm the instructions work end-to-end and to show what a correct answer looks like.

## Q1 — Create a 25 MB pendrive image + baseline hash

**Question:** Create a 25 MB virtual pendrive image for this exam. Use `dd`/`dc3dd` (or FTK Imager on Windows). Generate its SHA-256 hash right after creation.

The exam question allows **either `dd` or `dc3dd`** (or FTK Imager on Windows). Both methods are verified below — accept either.

### Method A — `dd` + `sha256sum`

**Commands (input):**
```bash
dd if=/dev/zero of=pendrive.dd bs=1M count=25 status=progress
sha256sum pendrive.dd
```

**Actual output:**
```
25+0 records in
25+0 records out
26214400 bytes (26 MB, 25 MiB) copied, 0.0320451 s, 818 MB/s

394c345f0b0c63ee652627a62eed069244d35c4d5134e4f07d4eabb51afda47e  pendrive.dd
```

### Method B — `dc3dd` (hashes during imaging, no separate step)

`dc3dd` is the forensic fork of `dd`: it computes the hash **while** imaging and writes an audit log, so the hash is produced in the same pass rather than as a separate afterwards command. This is the more forensically-sound of the two.

> ⚠️ **Important syntax difference — students will trip on this.** `dc3dd` does **not** accept `bs=`/`count=`. It sizes the read in **sectors** via `cnt=`, so `dc3dd if=/dev/zero of=pendrive.dd bs=1M count=25` **fails** with:
> ```
> [!!] unrecognized option bs=1M
> dc3dd aborted at 2026-07-27 09:35:46 +0530
> ```
> 25 MiB ÷ 512-byte sectors = **51200 sectors**, so the correct option is `cnt=51200`.

**Commands (input):**
```bash
dc3dd if=/dev/zero of=pendrive.dd cnt=51200 hash=sha256 log=pendrive_hash.txt
sha256sum pendrive.dd          # independent cross-check
```

**Actual output:**
```
dc3dd 7.2.646 started at 2026-07-27 09:37:09 +0530
compiled options:
command line dc3dd if=/dev/zero of=pendrive_dc3dd.dd cnt=51200 hash=sha256 log=pendrive_hash.txt
sector size: 512 bytes (assumed)
   26214400 bytes ( 25 M ) copied ( 100% ), 0.201881 s, 124 M/s

input results for pattern `00':
   51200 sectors in
   394c345f0b0c63ee652627a62eed069244d35c4d5134e4f07d4eabb51afda47e (sha256)

output results for file `pendrive_dc3dd.dd':
   51200 sectors out

dc3dd completed at 2026-07-27 09:37:09 +0530
```

Note the hash `394c345f…` is **identical** to the `dd` + `sha256sum` result — the two methods agree, as they must.

**Method B+ (bonus credit) — `hof=` for self-verifying output.** Using `hof=` instead of `of=` makes `dc3dd` re-read and hash the *written* file and compare it against the input hash, printing `[ok]` on a match. This proves the write was faithful, not just that the input was hashed:

```bash
dc3dd if=/dev/zero hof=pendrive.dd cnt=51200 hash=sha256 log=verify.log
```

```
output results for file `pendrive_verified.dd':
   51200 sectors out
   [ok] 394c345f0b0c63ee652627a62eed069244d35c4d5134e4f07d4eabb51afda47e (sha256)
```

That `[ok]` is a verified read-back — award full marks plus bonus to any student who gets there.

**What to check when grading:** the image is exactly 26,214,400 bytes (25 × 1024 × 1024), and the student recorded a SHA-256 hash *immediately* after creation.

> **Note on the expected hash value:** because the image is created from `/dev/zero`, it is 25 MiB of zero bytes and is therefore **fully deterministic** — every student who does this correctly will get the *same* hash, `394c345f0b0c63ee652627a62eed069244d35c4d5134e4f07d4eabb51afda47e`. This is a handy grading shortcut: a different hash means either a different size or a non-zero fill (e.g. they used `/dev/urandom`, which is also acceptable if the method is sound — just verify the size and their recorded baseline instead).

**Grading tip:** ask the student to re-hash the file at the end of the exam (`sha256sum pendrive.dd` again) — if it still matches their recorded baseline, integrity is proven.

## Q2 — File timestamps before/after copying

**Question:** Create a file, note its Created/Modified/Accessed timestamps with `stat`. Copy it to a USB drive (or mounted image), check timestamps again, and explain any differences.

**Commands (input):**
```bash
echo "This is my exam evidence file." > myfile.txt
stat myfile.txt

mkdir -p fake_usb
cp myfile.txt fake_usb/myfile.txt
stat fake_usb/myfile.txt
```

**Actual output:**
```
  File: myfile.txt
  Size: 31          Blocks: 8          IO Block: 4096   regular file
Device: 0,47        Inode: 15328       Links: 1
Access: 2026-07-24 15:24:31.763732539 +0530
Modify: 2026-07-24 15:24:31.763732539 +0530
Change: 2026-07-24 15:24:31.763732539 +0530
 Birth: 2026-07-24 15:24:31.763732539 +0530

  File: fake_usb/myfile.txt
  Size: 31          Blocks: 8          IO Block: 4096   regular file
Device: 0,47        Inode: 15333       Links: 1
Access: 2026-07-24 15:24:33.775785234 +0530
Modify: 2026-07-24 15:24:33.781342018 +0530
Change: 2026-07-24 15:24:33.781342018 +0530
 Birth: 2026-07-24 15:24:33.775785234 +0530
```

**Answer / explanation the student should give:** a plain `cp` does **not** preserve timestamps — Modify/Access/Change/Birth on the copy all show the *copy* time (15:24:33), not the original creation time (15:24:31). This is because `cp` (without `-p`/`--preserve=timestamps`) creates a brand-new inode and writes fresh data, so the filesystem stamps it with "now." A student who instead runs `cp -p myfile.txt fake_usb/` would find Modify time *is* preserved, while Change/Access still reflect the copy — that contrast is worth full credit if they demonstrate it.

**Verified `cp -p` run (for reference):**
```
  File: fake_usb/myfile_p.txt
Access: 2026-07-27 09:35:26.776832706 +0530   <- copy time
Modify: 2026-07-27 09:35:24.764183349 +0530   <- PRESERVED from original
Change: 2026-07-27 09:35:26.781482855 +0530   <- copy time (cannot be forged)
 Birth: 2026-07-27 09:35:26.780150378 +0530   <- copy time
```

> **Subtle point worth bonus marks:** `cp -p` is *supposed* to preserve Access time too, yet above it shows the copy time. The reason is that `cp` had to **read** the source to copy it, and that read updated the *source's* own Access time first — `cp -p` then faithfully preserved that just-updated value. Re-running `stat myfile.txt` after the copy confirms the original's Access time also moved to 09:35:26.
>
> The forensic lesson: **merely reading evidence alters its Access timestamp.** This is exactly why examiners work from write-blocked copies and hash-verified images rather than touching the original media — and why Change time (`ctime`) matters, since unlike Modify time it cannot be set by `touch` or preserved by `cp -p`.

**Grading tip:** the specific timestamp values will differ per student (they depend on wall-clock time and their own filenames/inodes) — grade on whether they correctly *identify and explain* the shift, not on matching these exact numbers.

---

# Set 2

**Folder:** `Exam-Files/Set2_Deleted_File_Recovery_and_Vacation_Photo/` — run the commands below from inside this folder.

## Q1 — Recover a deleted file (fls/icat + Autopsy)

**Question:** Using the provided sample image (`deleted_file_lab.img`) that already has a deleted file, recover it two ways: (1) `fls -d` + `icat` in the terminal, (2) Autopsy's "Deleted Files" view — export it from there too.

### Step 1 — confirm the filesystem (context, not required but useful)

**Command:**
```bash
fsstat deleted_file_lab.img | head -15
```

**Actual output:**
```
FILE SYSTEM INFORMATION
--------------------------------------------
File System Type: FAT16

OEM Name: mkfs.fat
Volume ID: 0x61c27958
Volume Label (Boot Sector): LABDISK
Volume Label (Root Directory): LABDISK
File System Type Label: FAT16

Sectors before file system: 0

File System Layout (in sectors)
Total Range: 0 - 40959
* Reserved: 0 - 3
```

### Step 2 — list deleted entries

**Command:**
```bash
fls -d deleted_file_lab.img
```

**Actual output:**
```
r/r * 6:	evidence_note.txt
```

The `*` marks it as deleted. Its inode/meta-address is **6**.

### Step 3 — recover it with icat

**Command:**
```bash
icat deleted_file_lab.img 6
```

**Actual output (recovered file content):**
```
CONFIDENTIAL - CASE FILE NOTES
Suspect meeting scheduled for 03:00 AM at the old warehouse on Dock Street.
Do not share this file outside the investigation team.
```

Recovery was verified byte-for-byte against the original before deletion (`diff` reported no differences) — the deletion was a real FAT directory-entry delete (via `mdel`), not a fabricated scenario, so `icat`'s output above is a genuine forensic recovery, not a scripted answer.

### Step 4 — recover the same file in Autopsy 4.23.1 (recommended)

Launch with `autopsy4` (or Applications → Autopsy 4.23.1).

1. **New Case** → Case Name e.g. `Set2_Exam` → **Next** → optional case number/examiner → **Finish**.
2. **Add Data Source** → **Disk Image or VM File** → **Next**.
3. Browse to the image — spaces in the path are fine in 4.x:
   ```
   /home/hexx/Documents/Digital_Forensics/Practical_Sets/Exam-Files/Set2_Deleted_File_Recovery_and_Vacation_Photo/deleted_file_lab.img
   ```
   → **Next**.
4. Ingest modules: the defaults are fine for this question (keep **Picture Analyzer** on if you also want the EXIF questions in the same case) → **Next** → **Finish**. Wait for the ingest bar to complete.
5. In the left tree, the deleted file appears in either place:
   - **Data Sources → deleted_file_lab.img → LABDISK → /** — `evidence_note.txt` is shown with a **red ✗ overlay** on its icon marking it deleted, or
   - **Views → Deleted Files → File System** — the direct equivalent of 2.24's "All Deleted Files".
6. Select it. The lower viewer has tabs — **Text**/**Strings** shows the recovered content, **Metadata** shows the filesystem details (allocation status, times, MD5, and meta address **6**).
7. Right-click → **Extract File(s)** to export it. *(This is the 4.x wording; 2.24 called it "Export".)*

**Engine-level verification performed on this machine.** Rather than trust the menus, the exam image was pushed through Autopsy 4.23.1's *own* ingest code path (`SleuthkitCase.newCase` + `makeAddImageProcess` — exactly what **Add Data Source** invokes), and the deleted file was read back through the same datamodel the GUI renders:

```
TSK version: 4.15.0
DELETED FILE FOUND
  name      : evidence_note.txt
  meta addr : 6
  size      : 162
  --- recovered content ---
  CONFIDENTIAL - CASE FILE NOTES
  Suspect meeting scheduled for 03:00 AM at the old warehouse on Dock Street.
  Do not share this file outside the investigation team.
```

**Meta address 6, 162 bytes** — the identical inode and size that `fls -d` and `icat` report in the terminal, and that Autopsy 2.24 reported. All three routes agree, which is the grading check.

<details>
<summary>Legacy — Step 4 via Autopsy 2.24 (verified GUI walkthrough, kept as fallback)</summary>


> These steps were performed end-to-end in the actual Autopsy 2.24 web GUI on this machine. Read the ⚠️ section near the top of this document first — in particular, **every folder in the path must be space-free**.

Start the Autopsy server (the evidence locker is where Autopsy stores its cases — it is *not* your evidence):
```bash
mkdir -p ~/autopsy_lab/evidence
autopsy -d ~/autopsy_lab/evidence
```
Then open **http://localhost:9999/autopsy**.

Since Fix A was applied, the image can now be loaded **straight from its exam folder** — verified working:
```
/home/hexx/Documents/Digital_Forensics/Practical_Sets/Exam-Files/Set2_Deleted_File_Recovery_and_Vacation_Photo/deleted_file_lab.img
```
Optionally have students copy it first (Fix B) — still recommended as good evidence-handling practice:
```bash
cp "deleted_file_lab.img" ~/autopsy_lab/     # then use /home/<user>/autopsy_lab/deleted_file_lab.img
```

1. **New Case** → Case Name e.g. `Set2_Exam` → **Create Case**. (Names allow only letters, numbers, symbols — no spaces.)
2. **Add Host** → accept the default `host1` → **Add Host**.
3. **Add Image** → **Add Image File**. On the *Add a New Image* screen:
   - **Location:** the full path from above (must start with `/`, and contain no spaces)
   - **Type:** select **Partition** ← *not* the default "Disk"
   - **Import Method:** **Symlink** (default — does not modify the original)
   - → **Next**
4. Autopsy reports `Partition 1 (Type: fat16)`, Mount Point `C:`, File System Type `fat16`. Leave Data Integrity on **Ignore** (or pick *Calculate* for a bonus integrity check) → **Add** → **OK**.
5. On the Host Manager, select the `C:/` volume → **Analyze**.
6. Click the **File Analysis** tab. `evidence_note.txt` is listed **in red with a check in the `Del` column** — that is Autopsy 2.24's deleted-file marker.
7. Click **All Deleted Files** in the left sidebar (this is 2.24's equivalent of 4.x's "Deleted Files" view). It lists exactly one entry:

   | Type | Name | Size | Meta |
   |---|---|---|---|
   | r/r | `C:/evidence_note.txt` | 162 | **6** |

   Note **Meta = 6** — the identical inode `fls -d` reported, confirming the GUI and terminal are reading the same structure.
8. Click the filename. The lower pane switches to **Deleted File Recovery Mode** and displays the recovered contents:
   ```
   Contents Of File: C:/evidence_note.txt

   CONFIDENTIAL - CASE FILE NOTES
   Suspect meeting scheduled for 03:00 AM at the old warehouse on Dock Street.
   Do not share this file outside the investigation team.
   ```
9. To export: click **Export** in that pane's link row (`ASCII (display - report) * Hex (display - report) * ASCII Strings (display - report) * Export * Add Note`), **or** open the **Meta Data** tab for entry 6 and use **Export Contents**. There is no "Extract File(s)" — that is 4.x wording.

**Cross-check that proves both methods agree.** The Meta Data tab for entry 6 reports:
```
File Type (Recovered): ASCII text
MD5 of recovered content:   bd29d4cf8a76f09427ec04a849d88e9c
SHA-1 of recovered content: 9ec75ae5a91e370bb9a21a10a0d935dc075335b6
Directory Entry: 6
Not Allocated
Size: 162
Name: _VIDEN~1.TXT
```
Running the terminal recovery through the same hashes gives byte-identical values:
```bash
icat deleted_file_lab.img 6 | md5sum    # bd29d4cf8a76f09427ec04a849d88e9c
icat deleted_file_lab.img 6 | sha1sum   # 9ec75ae5a91e370bb9a21a10a0d935dc075335b6
```

</details>

> **Teaching point worth marks — `Name: _VIDEN~1.TXT`** (visible in Autopsy 2.24's Meta Data tab; 4.x shows the long name only). That is not corruption. FAT marks a file deleted by overwriting the **first byte of its 8.3 short name** with `0xE5`, which Autopsy renders as `_`. The `e` of `evidence` is genuinely gone from the directory entry — the long-name entry is what lets TSK still show `evidence_note.txt`. This is *why* FAT deletion is so recoverable: only one byte of the name is destroyed, while the file's data and its starting cluster remain untouched.

**Answer:** the recovered file is `evidence_note.txt` (inode/dir-entry 6, 162 bytes), containing the "CONFIDENTIAL - CASE FILE NOTES..." text shown above. All recovery routes — `icat`, Autopsy 4.23.1, and Autopsy 2.24 — must produce identical content; grade on the matching MD5/SHA-1 above.

## Q2 — vacation_photo.jpg metadata

**Question:** Use the terminal to find its metadata (Make, Model, Date/Time Original, GPS, Comment), then confirm the same fields in Autopsy's Metadata tab, and state where the photo was taken. (The exam doesn't name a specific tool — `exiftool` is the standard one for this job, used below.)

**Command:**
```bash
exiftool -Make -Model -DateTimeOriginal -GPSLatitude -GPSLongitude -Comment vacation_photo.jpg
```

**Actual output:**
```
Make                            : Apple
Camera Model Name               : iPhone 12
Date/Time Original              : 2025:06:15 14:32:10
GPS Latitude                    : 48 deg 51' 30.24" N
GPS Longitude                   : 2 deg 17' 40.20" E
Comment                         : Family vacation trip - Paris, June 2025
```

### ✅ In Autopsy 4.23.1 — fully answerable as written

**Autopsy 4.23.1 is installed and displays every field this question asks for**, including Date/Time Original and GPS coordinates. Verified by running Autopsy's own EXIF stack (`EXIFProcessor` backed by `metadata-extractor-2.19.0.jar`) against this exact photo:

```
JpegComment | JPEG Comment       = Family vacation trip - Paris, June 2025
Exif IFD0   | Make               = Apple
Exif IFD0   | Model              = iPhone 12
Exif SubIFD | Date/Time Original = 2025:06:15 14:32:10
GPS         | GPS Latitude       = 48° 51' 30.24"   (Ref N)
GPS         | GPS Longitude      = 2° 17' 40.2"     (Ref E)
```

**In the GUI:** Add the photo via **Add Data Source → Logical Files** (4.23.1 can ingest a bare `.jpg` — 2.24 could not), keep the **Picture Analyzer** ingest module enabled, then select the file and read either the **Metadata** tab or **Results → Extracted Content → EXIF Metadata**. The values match the `exiftool` output above exactly — that agreement is the grading check.

<details>
<summary>Legacy — the Autopsy 2.24 limitation (no longer applies)</summary>

**Autopsy 2.24 has no EXIF parser at all.** This was tested directly: the photo was placed in a FAT16 image, loaded into Autopsy 2.24, and its **Meta Data** tab inspected. What it actually prints is:

```
File Type:
JPEG image data, Exif standard: [TIFF image data, big-endian, direntries=5,
manufacturer=Apple, model=iPhone 12, GPS-Data], comment: "Family vacation trip -
Paris, June 2025", baseline, precision 8, 2000x1333, components 3
```

That line is simply the output of the `file` command, which Autopsy shells out to. So from Autopsy 2.24 a student **can** obtain:

| Field | Available in Autopsy 2.24? |
|---|---|
| Make (`Apple`) | ✅ yes — shown as `manufacturer=Apple` |
| Model (`iPhone 12`) | ✅ yes — shown as `model=iPhone 12` |
| Comment | ✅ yes — shown verbatim |
| **Date/Time Original** | ❌ **no — not displayed anywhere** |
| **GPS coordinates** | ❌ **no — only the flag `GPS-Data`, never the actual latitude/longitude** |

Two further limits: Autopsy 2.24 analyses **disk images only**, so a bare `vacation_photo.jpg` cannot be opened directly — it must first be placed inside an image (or the question answered in the terminal); and its "Meta Data" tab means *filesystem* metadata (directory entry, allocation status, sectors, MD5/SHA-1), not camera metadata.

> **Grading guidance:** award full marks for the `exiftool` answer, which is what the question's own wording ("use the terminal to find its metadata") actually asks for. For the Autopsy half, accept the `manufacturer` / `model` / `comment` line from the Meta Data tab, and **do not penalise a student for failing to produce Date/Time or GPS from Autopsy — it is not obtainable in this version.** A student who explicitly notices and *states* that Autopsy 2.24 shows only `GPS-Data` without coordinates has demonstrated better tool understanding than one who silently copies the exiftool values across, and deserves bonus credit.
>
> **This has been resolved** — Autopsy 4.23.1 was installed for exactly this reason. The paper needs no rewording.

</details>

**Answer key:**
| Field | Value |
|---|---|
| Make | Apple |
| Model | iPhone 12 |
| Date/Time Original | 2025:06:15 14:32:10 |
| GPS coordinates | 48.8584° N, 2.2945° E |
| Comment | Family vacation trip - Paris, June 2025 |
| **Location** | **Paris, France** (these coordinates are the Eiffel Tower / central Paris area) |

---

# Set 3

**Folder:** `Exam-Files/Set3_IT_Event_Photo_and_SSH_Log/` — run the commands below from inside this folder.

## Q1 — IT_Event.jpg metadata

**Question:** Use the terminal to find its metadata (Make, Model, Date/Time Original, GPS, Comment), then find the same info in Autopsy's Metadata tab. (The exam doesn't name a specific tool — `exiftool` is the standard one for this job, used below.)

**Command:**
```bash
exiftool -Make -Model -DateTimeOriginal -GPSLatitude -GPSLongitude -Comment IT_Event.jpg
```

**Actual output:**
```
Make                            : Samsung
Camera Model Name               : Galaxy S21
Date/Time Original              : 2026:03:10 09:05:44
GPS Latitude                    : 12 deg 58' 17.76" N
GPS Longitude                   : 77 deg 35' 40.56" E
Comment                         : IT Security Awareness Event - March 2026
```

### ✅ In Autopsy 4.23.1 — fully answerable as written

Verified against this exact photo using Autopsy's own EXIF stack:

```
JpegComment | JPEG Comment       = IT Security Awareness Event - March 2026
Exif IFD0   | Make               = Samsung
Exif IFD0   | Model              = Galaxy S21
Exif SubIFD | Date/Time Original = 2026:03:10 09:05:44
GPS         | GPS Latitude       = 12° 58' 17.76"   (Ref N)
GPS         | GPS Longitude      = 77° 35' 40.56"   (Ref E)
```

Same GUI route as [[#Q2 — vacation_photo.jpg metadata]]: **Add Data Source → Logical Files**, keep **Picture Analyzer** enabled, then read the **Metadata** tab or **Results → Extracted Content → EXIF Metadata**. Values must match the `exiftool` output above.

<details>
<summary>Legacy — the Autopsy 2.24 limitation (no longer applies)</summary>

In 2.24 the **Meta Data** tab showed only a `file`-derived line with `manufacturer=Samsung, model=Galaxy S21, GPS-Data` — Make/Model/Comment obtainable, but **Date/Time Original and GPS coordinates were not**. Resolved by installing Autopsy 4.23.1.

</details>

**Answer key:**
| Field | Value |
|---|---|
| Make | Samsung |
| Model | Galaxy S21 |
| Date/Time Original | 2026:03:10 09:05:44 |
| GPS coordinates | 12.9716° N, 77.5946° E |
| Comment | IT Security Awareness Event - March 2026 |
| Location (bonus context) | Bengaluru, India |

## Q2 — Identify the SSH brute-force IP in auth.log

**Question:** Find the IP attempting an SSH brute-force attack; justify with usernames tried and timestamps.

This log is now a realistic-sized dump — 224 lines spanning 3 days of routine `CRON`/`sudo`/legitimate-login noise, with the attack buried inside it (that's the point: a real auth.log is mostly noise).

### Step 1 — count failed logins per IP

**Command:**
```bash
wc -l auth.log
grep "Failed password" auth.log | grep -oE '[0-9]{1,3}(\.[0-9]{1,3}){3}' | sort | uniq -c | sort -rn
```

**Actual output:**
```
224 auth.log

     13 203.0.113.77
      1 198.51.100.9
      1 10.0.0.15
```

`203.0.113.77` is the attacker — 13 failed logins vs. only single, isolated failures from two other IPs (one is an internal user who simply mistyped a password once and then logged in fine — not an attack pattern).

### Step 2 — usernames tried by that IP

**Command:**
```bash
grep "203.0.113.77" auth.log | grep -oE "user [a-zA-Z]+|for root" | sort -u
```

**Actual output:**
```
for root
user admin
user administrator
user backup
user guest
user oracle
user postgres
user root
user test
user ubuntu
user user
```

> **Counting note for graders:** this command prints **11 lines but only 10 distinct usernames**. `root` is matched twice — once as `user root` (the 03:14:09 attempt against a *non-existent* account, logged as "invalid user root") and once as `for root` (the 03:15:12–03:15:24 attempts against the *real* root account, logged without "invalid user"). Don't mark a student wrong for answering either 10 or 11 as long as they list the usernames correctly; 10 distinct accounts is the precise answer.

### Step 3 — timestamps involved

**Command:**
```bash
grep "203.0.113.77" auth.log
```

**Actual output (excerpt — full log in `auth.log`):**
```
Jul 19 03:14:02 labserver sshd[18342]: Failed password for invalid user admin from 203.0.113.77 port 40000 ssh2
Jul 19 03:14:09 labserver sshd[18343]: Failed password for invalid user root from 203.0.113.77 port 40001 ssh2
...
Jul 19 03:15:30 labserver sshd[18355]: Disconnecting authenticating user root 203.0.113.77 port 40200: Too many authentication failures [preauth]
```

**Answer key:**
- **Attacker IP:** `203.0.113.77`
- **Usernames tried:** admin, root, test, oracle, ubuntu, administrator, guest, user, postgres, backup (10 distinct usernames + repeated attempts against `root`)
- **Time window:** `03:14:02` → `03:15:30` on Jul 19 (≈ 88 seconds, attempts every 6–7 seconds — classic automated brute-force cadence)
- **Confirms attack:** ends with `sshd` itself disconnecting the session for "Too many authentication failures" — a built-in sshd defense triggering, which is strong corroborating evidence.

---

# Set 4

**Folder:** `Exam-Files/Set4_Access_Log_and_Secret_File/` — run the commands below from inside this folder.

## Q1 — Identify the directory-scanning IP in access.log

**Question:** Find the IP scanning for hidden directories/admin panels; report its User-Agent (tool signature) and time window.

This log is now a realistic-sized dump — 283 lines of a full day's ordinary traffic (regular browsers, mobile UAs, a legitimate Googlebot crawl) with the scan buried inside it.

### Step 1 — a wrong turn worth knowing about: raw request count does *not* find it

**Command:**
```bash
wc -l access.log
awk -F'"' '{print $1}' access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```

**Actual output:**
```
283 access.log

     28 203.0.113.120
     24 203.0.113.90
     23 203.0.113.44
     22 203.0.113.60
     22 203.0.113.155
```

The scanning IP isn't even in this top 5 — a normal visitor browsing on and off all day racks up *more total requests* than a 5-second automated burst. **Lesson:** total hit count is the wrong signal here; you need to look at the User-Agent and the request *rate*, not the daily total.

### Step 2 — see all distinct User-Agents in the log

**Command:**
```bash
grep -oE '"[^"]+"$' access.log | sort -u
```

**Actual output:**
```
"gobuster/3.6"
"Mozilla/5.0 (Android 14; Mobile; rv:126.0) Gecko/126.0 Firefox/126.0"
"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
"Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
```

Every other User-Agent here is a real browser (or Google's own crawler, identifiable and well-behaved). `gobuster/3.6` is the one that isn't a browser at all — it's a known directory-brute-forcing tool.

### Step 3 — find which IP used it, and confirm the paths/time window

**Command:**
```bash
grep "gobuster" access.log | awk '{print $1}' | sort -u
grep "198.51.100.23" access.log
```

**IP found:** `198.51.100.23` (the only IP using `gobuster/3.6`)

**Actual output (excerpt):**
```
198.51.100.23 - - [21/Jul/2026:04:02:11 +0000] "GET /admin/ HTTP/1.1" 404 196 "-" "gobuster/3.6"
198.51.100.23 - - [21/Jul/2026:04:02:11 +0000] "GET /administrator/ HTTP/1.1" 404 196 "-" "gobuster/3.6"
198.51.100.23 - - [21/Jul/2026:04:02:11 +0000] "GET /wp-admin/ HTTP/1.1" 404 196 "-" "gobuster/3.6"
...
198.51.100.23 - - [21/Jul/2026:04:02:15 +0000] "GET /db_backup.sql HTTP/1.1" 404 196 "-" "gobuster/3.6"
```

**Answer key:**
- **Scanning IP:** `198.51.100.23`
- **Tool signature (User-Agent):** `gobuster/3.6`
- **Time window:** `04:02:11` → `04:02:15` UTC on 21 Jul 2026 (15 requests to admin/hidden paths — `/admin/`, `/administrator/`, `/wp-admin/`, `/backup/`, `/.git/config`, `/config.php.bak`, `/phpmyadmin/`, `/dashboard/`, `/panel/`, `/.env`, `/server-status`, `/db_backup.sql`, etc. — in under 5 seconds, far faster than a human)

## Q2 — Identify the real type of the secret file

**Question:** The secret file has a missing/incorrect extension. Find its real file type and show the steps used.

The file is named **`secret_file.txt`** — a deliberately *incorrect* extension (not just a missing one), meant to mislead: a student who trusts the name will expect plain text and either try to `cat`/open it in a text editor, or assume it's uninteresting.

### Step 1 — trust the name and try to read it as text (the wrong turn students will naturally take first)

**Command:**
```bash
head -c 60 secret_file.txt | cat -v
```

**Actual output:**
```
M-^IPNG^M
^Z
^@^@^@^MIHDR^@^@^DM-0^@^@^C!^H^B^@^@^@wM-^M-_M-p^@^A^@^@IDATxM-^\M-^LM-}M-mM-^RM-lM-:M-^N,^H:@JM-^QM-kT[M-?
```

Garbage — this is not text. The `.txt` extension lied. Time to check the real file type.

### Step 2 — try the `file` command (reads magic bytes, ignores the name/extension)

**Command:**
```bash
file secret_file.txt
```

**Actual output:**
```
secret_file.txt: PNG image data, 1200 x 801, 8-bit/color RGB, non-interlaced
```

### Step 3 — confirm manually via the hex signature

**Command:**
```bash
xxd secret_file.txt | head -2
```

**Actual output:**
```
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 04b0 0000 0321 0802 0000 0077 dedf  .......!.....w..
```

`89 50 4E 47 0D 0A 1A 0A` is the standard **PNG magic number** — confirms `file`'s verdict independently of any tool's guess. The `.txt` extension was simply wrong.

### Step 4 — rename it correctly and open it to reveal the hidden content

```bash
cp secret_file.txt /tmp/secret_file.png
xdg-open /tmp/secret_file.png   # now opens correctly as an image
```

The image itself contains a **hidden message** overlaid on a landscape photo — a yellow banner reading:

> **MEET AT PIER 9 - 02:00 - CODE: FALCON-77**

This is the "evidence" the question is really after — students only see it once they've correctly identified the file type and renamed/opened it as a PNG.

**Answer key:**
- **Given (wrong) name:** `secret_file.txt`
- **Real file type:** PNG image (1200×801, RGB)
- **Correct extension:** `.png`
- **Hidden content once viewed correctly:** "MEET AT PIER 9 - 02:00 - CODE: FALCON-77"
- **Method:** the file extension/name is *not* what determines file type — the first bytes of the file (its "magic number"/signature) do. `file` reads those signature bytes against its magic database; here they match PNG's signature exactly, confirmed by manually inspecting the hex dump. Trusting a `.txt` extension and treating the content as text would have missed the hidden evidence entirely.
