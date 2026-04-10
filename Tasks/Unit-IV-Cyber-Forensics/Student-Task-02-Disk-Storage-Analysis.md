---
tags: [cyber-forensics, student-task, disk-analysis, MBR, partitions, intermediate]
task_number: 02
topic: Disk & Storage Structure Analysis
difficulty: ⭐⭐ Intermediate
type: student-challenge
solution_file: "[[Task-02-Disk-Storage-Analysis]]"
---

# 🧪 Student Task 02 — Disk & Storage Structure Analysis

> [!info] Objective
> Read and understand the raw structure of a disk — partition tables, sector layout, file system signatures, and how to calculate byte offsets.

> [!warning] Prerequisite
> Complete Task 01 first. You will use `suspect_drive.img` from that task.

---

## 📋 Your Tasks

### T2.1 — Create a Multi-Partition Test Disk
Create a 100MB image called `mbr_test.img` with **two partitions**: one NTFS (60MB) and one FAT32 (40MB).

> [!hint]- Hint — Creating partitions
> You need `parted` to create partitions inside an image file. Steps:
> 1. First create the raw image with `dd`
> 2. Then use `parted filename.img mklabel msdos mkpart ...`
> 3. Then format each partition — but how do you format a partition *inside* an image file?
> Look up `kpartx` — it maps partitions inside an image to loop devices like `/dev/mapper/loop0p1`

---

### T2.2 — Read the MBR Raw Bytes
Read the first 512 bytes of `mbr_test.img` in hex and find the partition table and MBR signature.

> [!hint]- Hint
> `dd` can read specific bytes: `dd if=file bs=1 skip=N count=N | xxd`
> The MBR signature is at byte offset **510–511**. What hex value should you see there?
> The partition table starts at byte offset **446**. Try reading 64 bytes from there.

---

### T2.3 — Map the Partition Layout
Use a Sleuth Kit tool to display all partitions in `mbr_test.img` and their start/end sectors.

> [!hint]- Hint
> The tool is part of **TSK (The Sleuth Kit)**. It starts with `mm` and ends with `ls`.
> What does each column in the output mean? Which column shows the start sector?

---

### T2.4 — Identify File Systems from Magic Bytes
For each image below, find the magic bytes that identify what file system it is:
- Your NTFS image
- Your FAT32 image
- An ext4 image (create one quickly with `mkfs.ext4`)

> [!hint]- Hint
> Each file system puts its signature at a specific byte offset:
> - NTFS: offset **3**, length 8 bytes → should spell something
> - FAT32: offset **54**, length 8 bytes → should spell something
> - ext4: offset **1080**, length 2 bytes → value is `0xEF53` (little-endian: `53 EF`)
> Use `dd if=image bs=1 skip=OFFSET count=N | xxd`

---

### T2.5 — Calculate Offset and Mount a Partition
From the `mmls` output in T2.3, find the start sector of the NTFS partition. Calculate the **byte offset** and mount it.

> [!hint]- Hint
> Formula: `byte offset = start_sector × sector_size`
> Default sector size = **512 bytes**
> Mount command: `sudo mount -o ro,loop,offset=CALCULATED_VALUE image.img /mnt/point`

---

### T2.6 — Measure Cluster Size and Calculate Slack Space
Mount your NTFS partition and create a small file (less than 100 bytes). Calculate how much slack space it creates.

> [!hint]- Hint
> Use `fsstat` to find the cluster size.
> Formula: `slack = (clusters_used × cluster_size) − actual_file_size`
> `ls -ls` shows disk blocks used. One block = 512 bytes usually.
> What is inside that slack space? Where did those bytes come from?

---

## ❓ Think About These

1. What are the last 2 bytes of a valid MBR in hex?
2. A partition starts at sector 2048 with 512-byte sectors. What is the byte offset?
3. Why does NTFS use "NTFS    " (with spaces) as its signature instead of just "NTFS"?
4. Your file is 1500 bytes and cluster size is 4096 bytes. How many clusters does it use? What is the slack space?
5. What is the forensic advantage of GPT over MBR?

---

## ✅ Completion Checklist

- [ ] Multi-partition image created
- [ ] MBR raw bytes read — signature `55 AA` found at offset 510
- [ ] Partition layout mapped with Sleuth Kit tool
- [ ] Magic bytes found for NTFS, FAT32, and ext4
- [ ] Partition mounted using calculated byte offset
- [ ] Cluster size found and slack space calculated

---
> [!tip] Stuck? Check: `[[Task-02-Disk-Storage-Analysis]]`
