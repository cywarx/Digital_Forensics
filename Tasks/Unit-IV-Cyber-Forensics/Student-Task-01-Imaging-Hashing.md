---
tags: [cyber-forensics, student-task, imaging, hashing, beginner]
task_number: 01
topic: Forensic Imaging & Hash Verification
difficulty: ⭐ Beginner
type: student-challenge
solution_file: "[[Task-01-Forensic-Imaging-Hashing]]"
---

# 🧪 Student Task 01 — Forensic Imaging & Hash Verification

> [!info] Objective
> Create a forensic image of a practice drive and verify its integrity using hash values.

---

## 📋 Your Tasks

### T1.1 — Create a Practice Suspect Drive
Create a **30MB FAT32 image file** called `suspect_drive.img` in `~/forensics-lab/practice/` that contains these files:
- `transfer.txt` — with text: `"Wire transfer: $250,000 → Account 9988-XXXX"`
- `notes.txt` — with any suspicious text
- `docs/merger.txt` — inside a subfolder

> [!hint]- Hint 1 — Creating the raw image
> You need a tool that creates raw files from a data source. Think about what command reads from `/dev/urandom` and writes to a file with a specific size.
> `dd if=??? of=??? bs=1M count=???`

> [!hint]- Hint 2 — Adding a file system
> A raw image has no structure. You need `mkfs` with a specific flag for FAT32.
> `mkfs.??? -F?? filename.img`

> [!hint]- Hint 3 — Adding files to it
> You cannot just copy files in — you need to **mount** it first using a loop device.
> `sudo mount -o ??? suspect_drive.img /mnt/suspect`

---

### T1.2 — Image it with `dd`
Copy `suspect_drive.img` to `~/forensics-lab/cases/case001/dd_copy.img` using `dd`.

> [!hint]- Hint
> You need: `if=` (source), `of=` (destination), `bs=512`, and two conversion options that handle bad sectors gracefully.
> What does `conv=noerror` do? What does `conv=sync` do? Why do you need both?

---

### T1.3 — Image it with `dcfldd` (with live hashing)
Do the same copy again but this time use `dcfldd` so it hashes while copying.

> [!hint]- Hint
> `dcfldd` has extra parameters: `hash=`, `hashlog=`, and `status=`
> What algorithm should you use? Where should the hashlog be saved?

---

### T1.4 — Verify the Hash
Prove that your `dcfldd_copy.img` is identical to the original `suspect_drive.img`.

> [!hint]- Hint
> Run `sha256sum` on **both** the original and the copy. What must be true about the output?
> Try: `diff <(sha256sum file1) <(sha256sum file2)` — what does no output mean?

---

### T1.5 — Mount Read-Only
Mount `dd_copy.img` so you can browse it but **cannot modify** it.

> [!hint]- Hint
> `mount` has an `-o` flag for options. Which option makes it read-only?
> Which option prevents access timestamp updates? Why does that matter for forensics?
> After mounting, try `echo "test" > /mnt/evidence/test.txt` — what should happen?

---

### T1.6 — Write a Chain of Custody Document
Create a file `chain_of_custody.txt` inside `~/forensics-lab/cases/case001/` documenting what you did.

> [!hint]- Hint
> It should contain: case number, date, investigator name, device details, SHA256 hash of original, SHA256 hash of copy, and a log of every action you took with timestamps.
> Use `date` command inside a bash heredoc to auto-insert timestamps.

---

## ❓ Think About These

Answer these in your notes before checking the solution:

1. Why do we never work on the original evidence?
2. If your original hash is `abc123` and your image hash is `abc124` — what happened?
3. What does `conv=noerror,sync` protect against?
4. Why use `mount -o noatime`?
5. What is the difference between `dd` and `dcfldd`?

---

## ✅ Completion Checklist

- [ ] `suspect_drive.img` created with 3 evidence files
- [ ] Imaged with `dd` — file exists in case001 folder
- [ ] Imaged with `dcfldd` — hash log saved
- [ ] Hash verified — original and copy match
- [ ] Image mounted and confirmed read-only
- [ ] Chain of custody document written

---
> [!tip] Stuck? Check your solution file: `[[Task-01-Forensic-Imaging-Hashing]]`
> Try yourself first — only look when truly stuck!
