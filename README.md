# 🔍 Digital Forensics Notes
**Post Graduate Diploma in Cyber Security and Law**
**Shaheed Sukhdev College of Business Studies · University of Delhi**

![Course](https://img.shields.io/badge/Course-PG%20Diploma%20in%20Cyber%20Security%20%26%20Law-blue?style=flat-square&logo=shield&logoColor=white)
![Subject](https://img.shields.io/badge/Subject-Digital%20Forensics-darkblue?style=flat-square&logo=hackthebox&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-purple?style=flat-square&logo=kalilinux&logoColor=white)

Practical, terminal-first notes for the Digital Forensics curriculum of the **PG Diploma in Cyber Security and Law** — covering theory, hands-on labs, CTF challenges, and internal assessments.

> ⚠️ All forensic images and CTF scenarios are **synthetic** and created solely for academic use.

---

## 📚 Syllabus Coverage

### Unit IV — Fundamentals of Cyber Forensics
- Introduction to Cyber Forensics
- Storage Fundamentals & File System Concepts (FAT32, NTFS, MBR)
- Data Recovery & Deleted File Recovery
- Formatted Partition Recovery
- OS Artifacts & Basic Terminology

### Unit V — Data Recovery Tools, Procedures & Ethics
- Chain of Custody & Evidence Admissibility
- Timeline Analysis (file creation / modification / access)
- Internet Usage, Swap Files, Temp Files & Cache Recovery
- Autopsy, EnCase, FTK — Introduction & Usage
- Cross-validation of findings using forensic tools
- Data Protection & Privacy

### Unit VI — Cyber Forensics Investigation
- Digital Evidence Collection & Preservation
- E-Mail Investigation, Tracking & Recovery
- IP Tracking · Encryption & Decryption
- Search & Seizure · Password Cracking · Hashcat & GPU Cracking
- eDiscovery · Open Source & Commercial Tools
- Digital Identity, E-Signatures & Biometric Data Protection

---

## 🗂️ What's Inside

| Folder | Contents |
|---|---|
| `Notes/` | Core topic notes per unit |
| `Units/` | Full unit notes + keywords glossary |
| `Tasks/` | 10 student practical tasks |
| `CTF/` | Phantom Ledger CTF (10 challenges + RAM CTF) |
| `Internal_Assessments/` | IA-1 question paper + solutions (The Devid Case) |
| `forensics-lab-Logs/` | Simulated log analysis lab (Apache, auth, syslog, MySQL) |
| `Lab_Setup/` | Environment setup + Volatility 3 install guide |
| `Scripts/` | Forensic image generation scripts |
| `PPT/` | Lecture slides |
| `Web_Notes/` | HTML-rendered reference pages |

---

## 🛠️ Tools Covered

`dc3dd` · `dd` · `mmls` · `fls` · `icat` · `tsk_recover` · `exiftool` · `Volatility 3` · `foremost` · `binwalk` · `Autopsy` · `Hashcat` · `md5sum` · `sha256sum`

---

## ⚡ Quick Start

```bash
git clone https://github.com/Ankit-Ojha16/Digital_Forensics.git
cd Digital_Forensics

# Install tools
sudo apt install sleuthkit exiftool dc3dd foremost binwalk autopsy -y

# Generate IA-1 practice image (The Devid Case)
sudo bash Internal_Assessments/Internal_Assessment-1/create_devid_evidence.sh

# Generate CTF disk image
sudo python3 "CTF/Phantom Ledger - The 0xE5 Incident/make_pendrive.py"
```

---

## 👤 Author

**Ankit Ojha** · [cywarx.com](https://cywarx.com) · [GitHub](https://github.com/Ankit-Ojha16) · [LinkedIn](https://linkedin.com/in/ankit-ojha) · [Ankit.ojha.1432@gmail.com](mailto:Ankit.ojha.1432@gmail.com)

> These notes are a **reference resource** — not official SSCBS study material. Always refer to your faculty's discussion material alongside these notes.

---
*MIT License · © 2026 Ankit Ojha*
