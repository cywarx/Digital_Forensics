---
tags: [cyber-forensics, student-task, deleted-file-recovery, FAT32, NTFS, ext4, intermediate]
task_number: "04-05-06"
topic: Deleted File Recovery — FAT32 / NTFS / ext4
difficulty: ⭐⭐ Intermediate
type: student-challenge
solution_file: "[[Task-04-05-06-Deleted-File-Recovery]]"
---

# 🧪 Student Tasks 04–05–06 — Deleted File Recovery

> [!info] Objective
> Recover files that have been "deleted" from three different file systems using the right tool for each one.

---

# 📗 Task 04 — FAT32 Deleted File Recovery

> [!info] FAT32 Deletion Reminder
> When a file is deleted on FAT32, the **first byte of its filename** is replaced with `0xE5`. The data clusters are marked free in the FAT table but the actual bytes are untouched.

---

## Your Tasks

### T4.1 — Create and Delete Evidence
Create a 50MB FAT32 image. Add these files, then delete them:
- `customer_db.txt` — "Stolen customer database — 50,000 records"
- `accounts.txt` — "Shell company accounts: Bermuda_Holdings_Ltd"
- `meeting_notes.txt` — "Meeting notes - illegal activity discussed"

Keep `report.pdf` and `evidence.jpg` (create them with `dd if=/dev/urandom`).

> [!hint]- Hint
> Use `mkfs.fat -F32`, mount with `sudo mount -o loop`, add files with `echo ... | sudo tee`, then `sudo rm` the three text files before unmounting.

---

### T4.2 — Recover with `fls` + `icat`
List all deleted files. Then recover each deleted file by its inode number.

> [!hint]- Hint
> `fls -r -d image.img` — the `-d` flag means deleted only.
> Each line looks like: `r/r * 5: customer_db.txt`
> The number `5` is the inode. Extract with: `icat image.img 5 > recovered.txt`
> Did you get the full content back?

---

### T4.3 — Recover with TestDisk
Use TestDisk's interactive menu to browse and recover the deleted files.

> [!hint]- Hint
> Run `testdisk image.img`. Navigate: select disk → `None` (no partition table) → `Advanced` → `Undelete`.
> Use arrow keys to select a file. What key copies it? What key copies all files?

---

### T4.4 — Recover with PhotoRec
Use PhotoRec to carve files from the image without using the file system at all.

> [!hint]- Hint
> `photorec image.img` — interactive menu.
> Select: `No partition` → `Other` filesystem → choose output folder → press `C`.
> What are the filenames of the recovered files? Why do they look different from the originals?

---

# 📘 Task 05 — NTFS Deleted File Recovery

> [!info] NTFS Deletion Reminder
> NTFS keeps the MFT entry intact after deletion — only the "in-use" flag is flipped to 0. The data clusters are marked free in `$Bitmap` but untouched. This makes NTFS recovery very reliable.

---

## Your Tasks

### T5.1 — Create and Delete Evidence
Create a 100MB NTFS image. Add and then delete:
- `config.env` — "apikey=sk-abc123xyz789SUPERSECRET"
- `salary.xlsx` — "Employee salary: HeXx — $120,000"
- `clients.txt` — "Confidential client list"

Keep `main.py` and `backup.zip`.

> [!hint]- Hint
> `mkntfs -f image.img` creates NTFS. Same mount/add/delete/unmount process as before.

---

### T5.2 — Recover with `fls` + `icat`
Recover all three deleted files. Verify the content is intact.

> [!hint]- Hint
> `fls -r -d image.img` gives you MFT entry numbers.
> NTFS inode format looks like `42-128-1` — use the full string with `icat`.
> `icat image.img 42-128-1 > recovered_config.env`

---

### T5.3 — Use `ntfsundelete` — Scan First
Run `ntfsundelete --scan` on the image. What does the `%` column tell you?

> [!hint]- Hint
> `ntfsundelete image.img --scan`
> The percentage = how much of the file's clusters are still unoverwritten.
> 100% = full recovery. 45% = partial recovery (corrupted file). 0% = gone.
> Now run `--undelete --match '*'` — what option controls minimum recovery percentage?

---

### T5.4 — Examine the `$I30` Directory Index
Check if deleted filenames are still visible in the directory index even after deletion.

> [!hint]- Hint
> The root directory in NTFS is MFT entry **5**.
> `istat image.img 5` shows the directory's MFT entry.
> Try: `icat image.img 5-144-4 > I30_raw.bin` then `strings I30_raw.bin`
> Can you still see the deleted filenames?

---

# 📙 Task 06 — ext4 Deleted File Recovery

> [!info] ext4 Deletion Warning
> ext4 may **zero out block pointers** in the inode when a file is deleted. This is different from FAT32 and NTFS. Recovery depends heavily on how recently the file was deleted and the journal state.

---

## Your Tasks

### T6.1 — Create and Delete Evidence
Create an 80MB ext4 image. Add and delete:
- `id_rsa` — "SSH private key content would be here"
- `crontab.bak` — "Cron job: * * * * * /tmp/backdoor.sh"
- `hidden/exfil.tar` — inside a subdirectory

> [!hint]- Hint
> `mkfs.ext4 image.img` — note: no `-F32` flag, and no `-f` like NTFS.
> `sudo mount -o loop image.img /mnt/ext4_lab`

---

### T6.2 — Try `extundelete`
Attempt to recover all deleted files. Note what was and was not recovered.

> [!hint]- Hint
> `extundelete image.img --restore-all`
> Check the `RECOVERED_FILES/` directory.
> If nothing recovered — why might that be with ext4? (Think: block pointer zeroing)

---

### T6.3 — Try `ext4magic`
Use the journal to attempt recovery with a time window.

> [!hint]- Hint
> `ext4magic image.img -r -d /output/dir/`
> The `-a` and `-b` flags set a time range using Unix timestamps.
> `date -d "1 hour ago" +%s` gives you a Unix timestamp.
> How does the journal help recover files that `extundelete` could not?

---

### T6.4 — Use `debugfs` Manually
Drop into the interactive `debugfs` shell. List deleted inodes and try to dump one.

> [!hint]- Hint
> `sudo debugfs image.img`
> Inside the shell, type: `lsdel` — lists deleted inodes with their sizes.
> To extract: `dump <INODE_NUMBER> /path/to/save/file`
> Type `quit` to exit.

---

### T6.5 — Fallback Carving with `foremost`
When inode-based recovery fails, carve from raw bytes instead.

> [!hint]- Hint
> `foremost -t all -i image.img -o /output/dir/`
> Check the `audit.txt` file — what file types were found and at what offsets?

---

## ❓ Think About These (All Three Tasks)

1. FAT32 deletes a file — first byte of filename becomes `___`?
2. NTFS deletes a file — what changes in the MFT entry? What stays the same?
3. ext4 deletes a file — what may be zeroed that makes recovery harder than NTFS?
4. `ntfsundelete` shows a file at 45% — what does this mean for the recovered file?
5. Why does PhotoRec lose filenames even when it recovers file content?

---

## ✅ Completion Checklist

**Task 04 — FAT32**
- [ ] Evidence files created and deleted
- [ ] Recovered with `fls + icat`
- [ ] Recovered with TestDisk interactive menu
- [ ] Recovered with PhotoRec — noted filename difference

**Task 05 — NTFS**
- [ ] Evidence files created and deleted
- [ ] Recovered with `fls + icat`
- [ ] `ntfsundelete --scan` run — percentages noted
- [ ] `$I30` index examined for ghost filenames

**Task 06 — ext4**
- [ ] Evidence files created and deleted
- [ ] `extundelete` attempted — result noted
- [ ] `ext4magic` attempted with time range
- [ ] `debugfs lsdel` run — deleted inodes listed
- [ ] `foremost` carving as fallback

---
> [!tip] Stuck? Check: `[[Task-04-05-06-Deleted-File-Recovery]]`
