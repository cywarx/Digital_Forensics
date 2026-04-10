---
tags: [cyber-forensics, student-tasks, index, unit-4]
aliases: [Student Task Index, Forensics Task List]
date: 2026-03-17
---

# 🎯 Cyber Forensics — Student Task Index

> [!abstract] How to Use These Files
> Each task file gives you **the challenge and hints only** — no full solutions.
> Try every task yourself first. Only open the linked solution file when you are genuinely stuck.
> The hints are layered — read Hint 1 before Hint 2 before giving up.

---

## 📋 Task Sequence

| Task | Topic | Difficulty | Status |
|---|---|---|---|
| [[Student-Task-01-Imaging-Hashing]] | Forensic Imaging & Hash Verification | ⭐ Beginner | |
| [[Student-Task-02-Disk-Storage-Analysis]] | Disk & Storage Structure | ⭐⭐ Intermediate | |
| [[Student-Task-03-File-System-Investigation]] | File System Internals (NTFS/ext4) | ⭐⭐ Intermediate | |
| [[Student-Task-04-05-06-Deleted-Recovery]] | Deleted File Recovery (FAT32/NTFS/ext4) | ⭐⭐ Intermediate | |
| [[Student-Task-07-08-Carving-Formatted]] | Data Carving & Formatted Partition Recovery | ⭐⭐⭐ Advanced | |
| [[Student-Task-09-10-OS-Artifacts-Investigation]] | OS Artifacts & Full Investigation | ⭐⭐⭐ Advanced | |

---

## 🗺️ Skill Map — What Each Task Teaches

```
Task 01 ──► dd, dcfldd, sha256sum, mount -o ro
Task 02 ──► lsblk, mmls, xxd, fsstat, parted
Task 03 ──► fls, istat, icat, analyzeMFT, ADS, debugfs
Task 04 ──► fls+icat on FAT32, testdisk, photorec
Task 05 ──► fls+icat on NTFS, ntfsundelete, $I30
Task 06 ──► extundelete, ext4magic, debugfs lsdel
Task 07 ──► foremost, scalpel, binwalk, bulk_extractor
Task 08 ──► testdisk deep search, GPT backup recovery
Task 09 ──► prefetch, evtx, registry, volatility3
Task 10 ──► everything combined in one real case
```

---

## 💡 Ground Rules

> [!warning] Do These Before Every Task
> 1. Make sure your lab directory exists: `~/forensics-lab/`
> 2. Never work on original evidence — always work on copies
> 3. Hash before and after every imaging operation
> 4. When you mount anything, always use `-o ro,noatime`

> [!tip] Hint System
> Each task has collapsible hints — click the arrow to expand.
> Try for at least **10 minutes** before opening a hint.
> Try for at least **5 more minutes** before opening Hint 2.
> Only open the solution file when all hints are exhausted.

---

## 📚 Reference Files

| File | What Is It |
|---|---|
| [[Unit-IV-Cyber-Forensics-Complete]] | Full theory notes for all topics |
| [[Cyber-Forensics-Keywords-Glossary]] | Every keyword explained simply |
| [[Physical-Drive-Image-Creation]] | How to image a real physical drive |
| [[00-Lab-Setup]] | Tool installation and lab setup guide |

---

## 🏆 Milestone Checks

After Task 02 you should be able to: read raw bytes from a disk, identify any file system by magic bytes, mount a partition from an image file.

After Task 06 you should be able to: recover deleted files from any of the three major file systems using the right tool for each.

After Task 08 you should be able to: recover data from a quick-formatted drive and rebuild a destroyed partition table.

After Task 10 you should be able to: run a complete end-to-end forensic investigation from acquisition to report.
