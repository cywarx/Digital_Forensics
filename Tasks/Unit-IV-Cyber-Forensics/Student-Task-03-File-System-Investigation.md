---
tags: [cyber-forensics, student-task, file-system, NTFS, MFT, ADS, timestamps, intermediate]
task_number: 03
topic: File System Deep Investigation
difficulty: ⭐⭐ Intermediate
type: student-challenge
solution_file: "[[Task-03-File-System-Investigation]]"
---

# 🧪 Student Task 03 — File System Deep Investigation

> [!info] Objective
> Dig into NTFS and ext4 internals — read MFT entries, extract timestamps, find hidden Alternate Data Streams, and analyze inode structures.

> [!warning] Prerequisite
> Complete Tasks 01 and 02. You need `suspect_drive.img` and a working NTFS image.

---

## 📋 Your Tasks

### T3.1 — Build a Populated NTFS Image
Create a 100MB NTFS image called `ntfs_evidence.img`, mount it, and add these files:
- `Documents/project_alpha.txt` — "Project Alpha source code — CONFIDENTIAL"
- `Documents/passwords.txt` — "Password list: admin:Admin@123"
- `Temp/config.dat` — "Malware config: C2=192.168.1.100:4444"

Then **delete** `passwords.txt` and `config.dat` before unmounting.

> [!hint]- Hint
> `mkntfs -f` creates NTFS. Mount with `sudo mount -o loop`.
> To delete: `sudo rm /mnt/ntfs/Temp/config.dat`
> Unmount cleanly: `sudo umount /mnt/ntfs`

---

### T3.2 — List All Files Including Deleted
Use a TSK command to list **every** file in the image — including ones that were deleted.

> [!hint]- Hint
> The command is `fls`. What flag makes it recursive? What flag shows only deleted files?
> Look at the output carefully — what symbol marks deleted files?
> What does the number like `42-128-1` mean in the output?

---

### T3.3 — Read an MFT Entry
Pick any file from the `fls` output. Use its MFT entry number to get full metadata.

> [!hint]- Hint
> The TSK command is `istat`. Give it the image file and the MFT number.
> What 4 timestamps does it show? Which one is hardest for an attacker to fake?
> What are "data runs" in the output?

---

### T3.4 — Parse the Entire MFT
Extract the `$MFT` file from the image and parse it into a CSV showing every file's history.

> [!hint]- Hint
> First mount the image, then copy the `$MFT` file (note: Linux needs the `\$MFT` escape).
> The Python tool is `analyzeMFT.py`. What flags does it need?
> After parsing, use `grep` to find deleted entries and suspicious filenames.

---

### T3.5 — Create and Detect an ADS
This task has two parts — attacker mode and investigator mode.

**Attacker:** Hide secret data inside a normal-looking file using an Alternate Data Stream.
**Investigator:** Detect and extract that hidden stream.

> [!hint]- Hint — Attacker side
> ADS syntax: `echo "hidden content" > normalfile.txt:stream_name`
> After creating it, check with `ls -la` — what size does the file show? Is that suspicious?

> [!hint]- Hint — Investigator side
> `fls` will list ADS entries. Look for lines containing a `:` in the filename.
> To extract: `icat image.img INODE_NUMBER > recovered_content`
> What inode number do you use for a specific stream?

---

### T3.6 — Analyze an ext4 Inode
Create a small ext4 image, add and delete a file, then use `istat` and `debugfs` to examine the inode of the deleted file.

> [!hint]- Hint
> `fls -f ext4 image.img` lists files with `-f` specifying the file system type.
> `istat -f ext4 image.img INODE` shows raw inode data.
> `debugfs image.img` is interactive — type `lsdel` inside it. What does that show?

---

## ❓ Think About These

1. What does `*` mean next to a file in `fls` output?
2. An MFT entry is 1KB. The file inside it is 500 bytes. Where is the file content stored?
3. You see `$STANDARD_INFORMATION` timestamps show file was created in 2020, but `$FILE_NAME` timestamps show 2026. What does this prove?
4. A file is: `invoice.txt:payload.exe` — what is happening here?
5. In ext4, an inode stores file size, timestamps, and block pointers — but NOT the filename. Where is the filename stored?

---

## ✅ Completion Checklist

- [ ] NTFS image created with files and deletions
- [ ] `fls` output shows deleted files with `*`
- [ ] `istat` run — all 4 MACE timestamps recorded
- [ ] MFT exported and parsed to CSV
- [ ] ADS created, hidden from `ls`, detected with `fls`, content extracted with `icat`
- [ ] ext4 inode examined with `istat` and `debugfs`

---
> [!tip] Stuck? Check: `[[Task-03-File-System-Investigation]]`
