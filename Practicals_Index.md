---
tags: [cyber-forensics, practicals, index, unit-4, unit-5]
aliases: [Practicals Index, Digital Forensics Practicals List]
date: 2026-07-17
---

# 🧪 Digital Forensics — Complete Practicals Index

> [!info] Scope
> Every hands-on / practical lab in this vault, organized by topic.
> **CTF challenges are excluded** — see the separate `CTF/` folder for those.

---

## 📋 Table of Contents

- [[#1. Lab Environment Setup]]
- [[#2. Forensic Imaging Practicals]]
- [[#3. Data Recovery Practicals]]
- [[#4. RAM / Memory Forensics Practicals]]
- [[#5. Log Analysis Practical]]
- [[#6. Student Task Series (Unit IV — 10 Tasks)]]
- [[#7. Internal Assessment Practical Exercises]]
- [[#8. Practical Exam Question Bank]]

---

## 1. Lab Environment Setup

| Practical | File | What It Covers |
|---|---|---|
| Forensics Lab Setup | [[00-Lab-Setup]] | Installing Kali-based forensics toolset: Sleuth Kit, exiftool, dc3dd, foremost, binwalk, Autopsy |
| Volatility 3 Installation | [[01-Volatility 3 Installation]] | Global install of Volatility 3 on Kali Linux for memory analysis |

---

## 2. Forensic Imaging Practicals

| Practical | File | What It Covers |
|---|---|---|
| Create a Forensics Image (Basic) | [[01. Create a Forensics Image for Practice]] | Building a 25 MB virtual pendrive image with `dd` / `dc3dd` |
| Pendrive Image with Partition Table | [[01.1 Pendrive_Image_Forensics]] | 32 MB image **with a proper partition table**, compatible with Autopsy/Sleuth Kit/fls/icat/foremost |
| Physical Drive Image Creation | [[Physical-Drive-Image-Creation]] | Imaging a **real physical drive** (not a virtual image) — acquisition & evidence handling |
| Pendrive Image Script | `Scripts/Create_Pendrive.sh` | Automated script version of the pendrive image creation practical |

---

## 3. Data Recovery Practicals

| Practical | File | What It Covers |
|---|---|---|
| Data Recovery — Complete Practical Guide | [[02. Digital_Forensics_Data_Recovery]] | End-to-end recovery workflow using `fls`, `icat`, `foremost`, `binwalk`, Autopsy, Sleuth Kit |

---

## 4. RAM / Memory Forensics Practicals

| Practical | File | What It Covers |
|---|---|---|
| RAM & Volatile Memory Field Guide | [[03. RAM_Volatile_Memory_Forensics]] | Full Volatility 2 vs Volatility 3 command reference |
| Volatility 3 Walkthrough | [[03.1 RAM Volatility 3]] | Step-by-step memory dump analysis (pstree → JSON, process/network artifacts) |
| Volatility 2 Complete Workflow | [[03.2 Volatility2_Memory_Forensics]] | Full memory forensics workflow using Volatility 2 (incident response / malware analysis angle) |

---

## 5. Log Analysis Practical

| Practical | File | What It Covers |
|---|---|---|
| Log Analysis in Digital Forensics | [[Log_Analysis_Digital_Forensics]] | Reading & interpreting Apache, auth, syslog, MySQL logs with real terminal input/output |
| Simulated Log Analysis Lab | `forensics-lab-Logs/` | Practice log set (Apache, auth, syslog, MySQL) to apply the log analysis note against |

---

## 6. Student Task Series (Unit IV — 10 Tasks)

Full challenge-and-hint style practicals — see [[Student-Task-Index]] for the master index.

| # | Task | Topic | Difficulty |
|---|---|---|---|
| 01 | [[Student-Task-01-Imaging-Hashing]] | Forensic Imaging & Hash Verification | ⭐ Beginner |
| 02 | [[Student-Task-02-Disk-Storage-Analysis]] | Disk & Storage Structure | ⭐⭐ Intermediate |
| 03 | [[Student-Task-03-File-System-Investigation]] | File System Internals (NTFS/ext4) | ⭐⭐ Intermediate |
| 04–06 | [[Student-Task-04-05-06-Deleted-Recovery]] | Deleted File Recovery (FAT32/NTFS/ext4) | ⭐⭐ Intermediate |
| 07–08 | [[Student-Task-07-08-Carving-Formatted]] | Data Carving & Formatted Partition Recovery | ⭐⭐⭐ Advanced |
| 09–10 | [[Student-Task-09-10-OS-Artifacts-Investigation]] | OS Artifacts & Full Investigation | ⭐⭐⭐ Advanced |

---

## 7. Internal Assessment Practical Exercises

| Practical | File | What It Covers |
|---|---|---|
| The Devid Case — Evidence Creation | `Internal_Assessments/Internal_Assessment-1/create_devid_evidence.sh` | Script generating a synthetic evidence image for IA-1 practice |
| IA-1 Practical Solutions | [[Internal_Assessment-1_Solutions]] | Worked practical solutions for the IA-1 evidence image |
| IA-1 Direct Solutions | [[direct_solutions]] | Direct, condensed solution walkthrough for IA-1 |

---

## 8. Practical Exam Question Bank

| Practical | File | What It Covers |
|---|---|---|
| Practical Exam Question Paper | [[Practical_Exam_Questions]] | 15-question practical exam covering imaging, data recovery, RAM forensics, log analysis, file system internals, and an integrated investigation |
| Practical Exam Answer Key | [[Practical_Exam_Answer_Key]] | Full worked solutions (commands + output + explanation) for every question in the exam paper |
| Question Paper — Word | `Practical_Exam_Question_Paper.docx` | Printable/editable version of the question paper, formatted like an official exam paper |
| Question Paper — PDF | `Practical_Exam_Question_Paper.pdf` | Same question paper exported to PDF for distribution |
| Answer Key — Word | `Practical_Exam_Answer_Key.docx` | Printable/editable version of the answer key, matching the question paper's formatting |
| Answer Key — PDF | `Practical_Exam_Answer_Key.pdf` | Same answer key exported to PDF for distribution |

---

> [!tip] Not Included Here
> `CTF/` (Phantom Ledger — The 0xE5 Incident, CTF Memory Dump) is intentionally excluded from this index — those are capture-the-flag challenges, not structured practicals.
