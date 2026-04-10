---
tags: [cyber-forensics, student-task, data-carving, foremost, formatted-partition, testdisk, advanced]
task_number: "07-08"
topic: Data Carving & Formatted Partition Recovery
difficulty: ⭐⭐⭐ Advanced
type: student-challenge
solution_file: "[[Task-07-08-Carving-Formatted-Recovery]]"
---

# 🧪 Student Tasks 07–08 — Data Carving & Formatted Partition Recovery

> [!info] Objective
> Task 07: Recover files by scanning raw bytes for magic byte signatures — without any file system.
> Task 08: Recover a partition whose table was destroyed or overwritten.

---

# 🔪 Task 07 — Data Carving

> [!info] Core Concept
> Data carving ignores the file system entirely. It scans every raw byte looking for known file headers (like `FF D8 FF` for JPEG) and footers. Works even when the file system is completely destroyed.

---

## Your Tasks

### T7.1 — Build a Carving Target Image
Create a 80MB FAT32 image. Add files of different types (JPEG, PDF, ZIP, TXT). Then delete ALL of them before unmounting. This simulates an attacker wiping evidence.

> [!hint]- Hint
> Use `dd if=/dev/urandom` to create fake binary files that look like real JPEGs/ZIPs by wrapping them with real magic byte headers. Or copy real small files from your system (`/usr/share/doc/` has many PDFs and text files).
> Key: the raw bytes of the files must still be in the image after deletion.

---

### T7.2 — Manual Magic Byte Hunt
Before using any carving tool, manually find file signatures in the raw image using `xxd` and `grep`.

> [!hint]- Hint
> JPEG header in hex: `ff d8 ff`
> PDF header in ASCII: `%PDF`
> ZIP header: `PK` (hex: `50 4b 03 04`)
> Try: `grep -c '%PDF' image.img` — does it find anything?
> Try: `xxd image.img | grep "ffd8 ff"` — what offset does it show?
> Also try: `strings image.img | grep -iE "secret|account|transfer"`

---

### T7.3 — Carve with `foremost`
Use `foremost` to recover all deleted files by their file signatures.

> [!hint]- Hint
> `foremost -t jpg,pdf,zip,png -i image.img -o /output/dir/`
> After it runs, look at `audit.txt` inside the output folder.
> What does the audit tell you? How many files were found? At what byte offsets?

---

### T7.4 — Carve with `scalpel`
Repeat the carving with `scalpel` — a faster alternative.

> [!hint]- Hint
> `scalpel` needs its config file edited first: `/etc/scalpel/scalpel.conf`
> Lines starting with `#` are disabled. Remove `#` from jpg, pdf, png, zip lines.
> Then: `scalpel image.img -o /output/scalpel/`
> Compare results with `foremost` — are they the same?

---

### T7.5 — Extract with `binwalk`
Run `binwalk` on the image. What does it find? Use `-e` to extract.

> [!hint]- Hint
> `binwalk image.img` scans without extracting — shows what it found and at what offsets.
> `binwalk -e image.img` extracts everything into a folder named `_image.img.extracted/`
> What types of content can `binwalk` find that `foremost` might miss?

---

### T7.6 — Artifact Extraction with `bulk_extractor`
Run `bulk_extractor` on the image. What artifacts does it find in the output folder?

> [!hint]- Hint
> `bulk_extractor -o /output/bulk/ image.img`
> Look inside the output folder — each `.txt` file contains a different artifact type.
> Which files are relevant to a financial fraud investigation?
> What does `ccn.txt` contain? What about `email.txt`?

---

## ❓ Think About These (Task 07)

1. What are "magic bytes"? Give the header bytes for JPEG in hex.
2. A file has no footer signature (like `.exe`). How does the carver know when to stop?
3. You carved a JPEG from a fragmented file. It opens but half the image is corrupted. Why?
4. `bulk_extractor` found a credit card number in unallocated space. How is that possible?
5. Carving recovered the file but the filename is `file0001.jpg`. The original was `passport_scan.jpg`. Why?

---

---

# 🗂️ Task 08 — Formatted Partition Recovery

> [!info] Core Concept
> Quick format only rewrites metadata (FAT/MFT reset). The data clusters are completely untouched. TestDisk finds old partition signatures still present in sector headers and reconstructs the partition table.

---

## Your Tasks

### T8.1 — Simulate a Formatted Drive
Create a 150MB image with two partitions (NTFS + FAT32). Add evidence files to the NTFS partition. Then **quick-format** the NTFS partition — simulating a suspect "wiping" evidence.

> [!hint]- Hint
> Create image → `parted` to partition → `kpartx -a` to map → `mkntfs -f` to format → mount and add files → unmount → `mkntfs -f` again on the same partition to "format" it.
> After the second format, the files are "gone." Now recover them.

---

### T8.2 — Recover with TestDisk — Quick Search
Run TestDisk on the image. Use Quick Search to find the old partition.

> [!hint]- Hint
> `testdisk image.img`
> Navigation: select image → `Intel` → `Analyse` → `Quick Search`
> If it finds partitions, what letter appears next to them? What does `P` mean vs `D`?
> To restore: press `Write` — what does this actually do to the image?

---

### T8.3 — Mount the Recovered Partition
After TestDisk writes the partition table, calculate the offset and mount the recovered partition.

> [!hint]- Hint
> `mmls image.img` shows the new partition layout with start sectors.
> Calculate: `byte offset = start_sector × 512`
> `sudo mount -o ro,loop,offset=OFFSET image.img /mnt/recovered`
> Are your evidence files visible? Were they really "destroyed" by the format?

---

### T8.4 — TestDisk Deep Search
Start with a new image where Quick Search finds nothing. Use Deep Search instead.

> [!hint]- Hint
> In TestDisk: after Quick Search shows nothing → `Back` → `Deep Search`
> Deep Search scans every single sector for file system signatures — much slower but finds more.
> When might you need Deep Search instead of Quick Search?

---

### T8.5 — PhotoRec on a Formatted Partition
When TestDisk cannot reconstruct the partition, use PhotoRec to carve files from raw bytes.

> [!hint]- Hint
> `photorec image.img`
> Select: `No partition` (scan entire image) → `Other` → choose output folder → `C`
> What is the key difference between what TestDisk gives you vs what PhotoRec gives you?
> (Think: folder structure, filenames, vs just file content)

---

### T8.6 — GPT Backup Recovery
Create a GPT-partitioned image. Deliberately corrupt the primary GPT header (sector 1). Watch normal tools fail. Then use TestDisk to recover from the backup.

> [!hint]- Hint
> `parted image.img mklabel gpt mkpart ...`
> Corrupt sector 1: `dd if=/dev/zero of=image.img bs=512 count=1 seek=1 conv=notrunc`
> Try `mmls image.img` — does it work now? What error do you get?
> Where does GPT store its backup table? (Hint: very last sectors of the disk)
> TestDisk reads both — select `EFI GPT` as partition type.

---

## ❓ Think About These (Task 08)

1. What exactly does Quick Format change on the disk? What does it NOT change?
2. Full Format on Windows Vista and later — what additional step does it do that Quick Format skips?
3. TestDisk recovered your partition. What specifically did it write to make it work again?
4. A partition was deleted 6 months ago and the disk has been heavily used since. Can TestDisk still recover it? Why or why not?
5. TestDisk vs PhotoRec — when would you choose one over the other?

---

## ✅ Completion Checklist

**Task 07 — Data Carving**
- [ ] Carving target image built with embedded files, all deleted
- [ ] Magic bytes found manually with `xxd` and `grep`
- [ ] `foremost` output checked — files recovered, audit.txt read
- [ ] `scalpel` config edited, run, results compared to foremost
- [ ] `binwalk -e` run — extracted content examined
- [ ] `bulk_extractor` output folder browsed — artifact types noted

**Task 08 — Formatted Partition Recovery**
- [ ] Image created, evidence added, quick-formatted
- [ ] TestDisk Quick Search run — partition found or not found noted
- [ ] Recovered partition mounted — evidence files visible
- [ ] Deep Search tried on a separate image
- [ ] PhotoRec used as fallback — filename loss observed
- [ ] GPT header corrupted and recovered from backup

---
> [!tip] Stuck? Check: `[[Task-07-08-Carving-Formatted-Recovery]]`
