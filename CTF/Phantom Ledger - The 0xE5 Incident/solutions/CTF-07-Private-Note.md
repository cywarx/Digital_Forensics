---
tags: [ctf, solution, unit4, forensics, fat32, fls, icat, premeditation]
challenge: "07 — The Private Note (private_note.txt)"
flag: "Cywarx{ph4nt0m_l3dg3r_cl0s3d}"
points: 500
difficulty: Expert
topic: Deleted File Recovery — Premeditation Evidence
image: ctf1.img → P2 deleted file: private_note.txt
---

# 📝 Challenge 07 — The Private Note

> [!success] Flag
> `Cywarx{ph4nt0m_l3dg3r_cl0s3d}`

> [!info] Real World Case — Enron + CAID
> In the Enron case, deleted planning memos proved premeditation — executives had consciously planned the accounting fraud rather than "making mistakes." In CAID investigations, deleted planning documents and contact lists recovered from formatted drives have provided the premeditation evidence needed to elevate charges from possession to distribution. A private deleted note is often the most damning evidence in court.

---

## 📋 Challenge Summary

Recover `private_note.txt` — Rohan's operational plan for "Operation Phantom Ledger." This document proves **premeditation**: the theft was planned in advance, not accidental. It lists all 5 phases with checkmarks.

**Recovery target:** `private_note.txt` on P2 (inode 11)

---

## 🔍 Method 1 — fls + icat

```bash
# Find deleted files
fls -r -d -o 133120 ctf1.img
```

**Output:**
```
r/r * 11:  private_note.txt
```

```bash
# Recover and read
icat -o 133120 ctf1.img 11
```

**Output:**
```
[Private - Operation Phantom Ledger]

Phase 1: Install keylogger on bank workstation  DONE 2024-03-15
Phase 2: Capture admin credentials              DONE admin:S3cr3t@123
Phase 3: Export 75842 customer records          DONE 2024-03-17
Phase 4: FTP upload to 185.44.21.9/drop/        DONE 09:31:44
Phase 5: Delete all USB evidence                DONE (or so I thought)

Flag: ph4nt0m_l3dg3r_cl0s3d
```

> [!success] Flag: `Cywarx{ph4nt0m_l3dg3r_cl0s3d}`

---

## 🔍 Method 2 — strings grep

```bash
strings ctf1.img | grep -A10 "Phantom Ledger"
```

---

## 🔍 Method 3 — Autopsy timeline analysis

```
1. Add ctf1.img to Autopsy
2. Deleted Files → private_note.txt
3. Note creation timestamp → shows premeditation date
4. Timeline view → see all suspect activity on 2024-03-17
```

---

## 🔬 Legal Significance

> [!warning] Why this note matters in court
> This document transforms the case:
> - **Without it:** Circumstantial evidence — suspect was at the bank, data was stolen
> - **With it:** Direct evidence of premeditation — all 5 phases planned in advance
>
> Pre-planning elevates charges from:
> - Data theft → Organised cybercrime (IPC Section 66B, IT Act 2000)
> - Simple fraud → Conspiracy (IPC Section 120B)
> - Employee misuse → Industrial espionage

---

## 🔗 Related Challenges
- [[CTF-09-Full-Investigation]] — Full case reconstruction using all evidence
- [[CTF-03-Deleted-kl-log]] — The kl.log credential capture file
