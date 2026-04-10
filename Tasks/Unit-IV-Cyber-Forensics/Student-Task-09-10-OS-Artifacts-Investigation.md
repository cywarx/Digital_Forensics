---
tags: [cyber-forensics, student-task, OS-artifacts, event-logs, volatility, full-investigation, advanced]
task_number: "09-10"
topic: OS Artifacts & Full Investigation Simulation
difficulty: ⭐⭐⭐ Advanced
type: student-challenge
solution_file: "[[Task-09-10-OS-Artifacts-Full-Investigation]]"
---

# 🧪 Student Tasks 09–10 — OS Artifacts & Full Investigation

---

# 🖥️ Task 09 — OS Artifact Analysis

> [!info] Objective
> Windows leaves hundreds of forensic traces even after files are deleted. Learn to read Prefetch files, Event Logs, Registry hives, and RAM dumps.

> [!warning] Note on Windows Artifacts
> These tasks work best on a mounted Windows forensic image. If you don't have one, use the mock artifact structure from the solution file, or practice on your own Windows VM.

---

## Your Tasks

### T9.1 — Set Up a Mock Artifact Structure
Create a directory tree that simulates a mounted Windows image with Prefetch files, Event Log paths, and Registry hive locations.

> [!hint]- Hint
> Create: `win_artifacts/{Prefetch,System32/winevt/Logs,config,Users/Suspect}/`
> Inside Prefetch: create fake `.pf` files named like real ones:
> `KEYLOGGER.EXE-A1B2C3D4.pf`, `WINSCP.EXE-E5F6A7B8.pf`, `CMD.EXE-89305D47.pf`
> The filename format is: `PROGRAM.EXE-XXXXXXXX.pf` where X is a hash of the path.

---

### T9.2 — What Story Do Prefetch Files Tell?
Look at just the **filenames** of the `.pf` files you created. Without parsing them, answer: what can you already tell about what the suspect did?

> [!hint]- Hint
> `ls ~/forensics-lab/practice/win_artifacts/Prefetch/`
> A Prefetch file existing for `KEYLOGGER.EXE` proves what?
> A Prefetch file persists even after the original `.exe` is deleted — why is this forensically powerful?
> Install `prefetch-parser` and parse real `.pf` files if you have them: what extra detail do you get?

---

### T9.3 — Parse Windows Event Logs
Use the Python EVTX parser to extract key events from a `.evtx` file.

> [!hint]- Hint
> Install: `pip3 install python-evtx --break-system-packages`
> Parse: `evtxdump.py Security.evtx | grep -A5 "EventID"`
> Key Event IDs to hunt:
> - `4625` = failed login (brute force?)
> - `4624` = successful login
> - `4698` = scheduled task created (persistence!)
> - `1102` = security log cleared (anti-forensics!)
> What does it mean if you see many `4625` events from the same IP in 30 seconds?

---

### T9.4 — Registry Forensics — USB History
Parse a Windows SYSTEM registry hive to find every USB device ever connected.

> [!hint]- Hint
> Install: `pip3 install regipy --break-system-packages`
> The key path is: `ControlSet001\Enum\USBSTOR`
> Each subkey = a different device type. Each sub-subkey = a unique serial number.
> Why is the serial number forensically valuable? What can you match it to?

---

### T9.5 — RAM Analysis with Volatility3
Run basic Volatility3 commands on a RAM dump to find what was running when the system was captured.

> [!hint]- Hint
> `python3 vol.py -f ram.dump windows.pslist` — running processes
> `python3 vol.py -f ram.dump windows.netscan` — network connections at time of capture
> `python3 vol.py -f ram.dump windows.cmdline` — command history per process
> `python3 vol.py -f ram.dump windows.malfind` — suspicious injected code
> If you find `powershell.exe` with a weird command line — what does that suggest?

---

### T9.6 — Extract Strings from pagefile.sys
Run `strings` on a `pagefile.sys` or `hiberfil.sys` and search for sensitive data.

> [!hint]- Hint
> `strings pagefile.sys | grep -iE "password|secret|api.key|token"`
> `strings pagefile.sys | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | sort -u`
> Why does pagefile.sys contain sensitive data even after programs are closed?
> What makes `hiberfil.sys` even more valuable than `pagefile.sys`?

---

## ❓ Think About These (Task 09)

1. A Prefetch file for `MIMIKATZ.EXE` exists but `mimikatz.exe` itself has been deleted. What can you prove in court?
2. Event ID `1102` appears in the log. What did the attacker do and why?
3. USBSTOR shows a USB drive serial number. How could you use this to prove a specific physical drive was used?
4. Volatility shows a process in `psscan` that is NOT in `pslist`. What does this mean?
5. Why is `hiberfil.sys` considered "RAM on disk"? When is it created?

---

---

# 🚨 Task 10 — Full Forensic Investigation Simulation

> [!info] Your Case: Operation Phantom Ledger
> A bank employee `jsmith` is suspected of:
> - Installing a keylogger on coworkers' machines
> - Stealing 75,000 customer records
> - Uploading them to an FTP server at `185.44.21.9`
> - Deleting all evidence and quick-formatting a USB drive
>
> You receive: a laptop image and a formatted USB image.
> **Your job: reconstruct the crime and document everything.**

---

## Your Tasks

### T10.1 — Build the Simulation
Create both images — laptop (150MB NTFS) and USB (50MB FAT32) — with realistic evidence, then simulate what the suspect did (delete files + format USB).

> [!hint]- Hint
> Laptop evidence to create then delete:
> - `Temp/kl_config.dat` — "keylogger.exe config: logfile=C:/Temp/kl.log"
> - `Temp/ftp_log.txt` — "FTP Upload: ftp://185.44.21.9/drop/ — SUCCESS"
> - `Documents/customer_export.csv` — "Customer DB - 75,000 records"
>
> USB evidence to create then quick-format:
> - `customer_export.csv` and `server_creds.txt`
>
> Also create mock Prefetch files: `KEYLOGGER.EXE-xxxx.pf`, `WINSCP.EXE-xxxx.pf`

---

### T10.2 — Evidence Acquisition
Hash both images before doing anything else.

> [!hint]- Hint
> `sha256sum laptop.img > hashes.txt`
> `sha256sum usb.img >> hashes.txt`
> This is your evidence lock — every analysis step starts here.

---

### T10.3 — Disk Structure Analysis
Map the partition layout of both images.

> [!hint]- Hint
> Which TSK tool shows partition layout?
> Save output to `disk_analysis.txt` in your case folder.

---

### T10.4 — Find and Recover Deleted Evidence
List all deleted files on the laptop image. Recover them.

> [!hint]- Hint
> `fls -r -d laptop.img` — get inode numbers of deleted files
> `icat laptop.img INODE > recovered_filename`
> Can you recover `kl_config.dat`? `ftp_log.txt`? `customer_export.csv`?
> What do the contents prove about the crime?

---

### T10.5 — Recover Evidence from Formatted USB
The USB was quick-formatted. Recover its contents using at least two methods.

> [!hint]- Hint
> Method 1: `fls -r -d usb.img` — FAT32 may still show deleted entries
> Method 2: `foremost -t all -i usb.img -o /recovered/usb/`
> Method 3: `strings usb.img | grep -iE "185\.|ftp|customer|password"`
> Which method gives you the best evidence? Why?

---

### T10.6 — Prefetch Evidence
List all Prefetch files on the laptop image. Identify the suspicious ones.

> [!hint]- Hint
> `fls -r laptop.img | grep -i "\.pf"`
> What programs does the Prefetch evidence prove were run?
> Can you prove the keylogger was executed even though the `.exe` file is deleted?

---

### T10.7 — Strings Analysis
Search for the FTP server IP address and credentials in raw image bytes.

> [!hint]- Hint
> `strings laptop.img | grep "185\.44\.21\.9"`
> `strings usb.img | grep -iE "ftp|jsmith|password"`
> Even after deletion, text strings survive in unallocated space — why?

---

### T10.8 — Generate the Investigation Report
Write a complete report tying all evidence together.

> [!hint]- Hint
> Your report must include:
> - Case number and investigator details
> - SHA256 hashes of both images (from T10.2)
> - Each finding with: what you found, where you found it, what tool, what it proves
> - Timeline of events (what happened first, second, third...)
> - Conclusion: what can you prove happened?
>
> Use the chain of custody template from `[[Physical-Drive-Image-Creation]]` as a starting point.

---

### T10.9 — Final Integrity Check
Re-hash both images. Confirm they have not changed since acquisition.

> [!hint]- Hint
> `sha256sum laptop.img` — compare to the hash in `hashes.txt` from T10.2
> If they match: your analysis was forensically sound
> If they differ: you modified evidence — your findings may be inadmissible

---

## ❓ Final Exam Questions

Answer these without looking at any notes. If you can answer all 10, you understand the entire unit.

1. What is the **first** thing you do when you receive a suspect device?
2. What does `conv=noerror,sync` in a `dd` command protect against?
3. A file is deleted on NTFS. The MFT entry number is 42. Run the two commands to (a) check it still exists and (b) recover it.
4. You format a USB drive with Quick Format. Is the data gone? Explain why or why not.
5. `ntfsundelete --scan` shows a file at 30%. What does this mean for recovery?
6. You find `MIMIKATZ.EXE-A1B2C3D4.pf` in a Prefetch folder. The `.exe` is deleted. What can you prove?
7. Event ID `1102` appears in the Security log. What happened and why is it significant?
8. `pagefile.sys` and `hiberfil.sys` — what is the difference and why are both valuable?
9. TestDisk says it found your partition but `PhotoRec` loses all filenames — explain why.
10. Why must both the source hash AND the image hash be computed? What does a mismatch prove?

---

## ✅ Final Completion Checklist

**Task 09 — OS Artifacts**
- [ ] Mock artifact directory structure built
- [ ] Prefetch filenames analyzed — suspicious programs identified
- [ ] Event log parsing practiced — key Event IDs noted
- [ ] Registry USBSTOR path explored
- [ ] Volatility3 commands run on a RAM dump
- [ ] `pagefile.sys` strings extracted and searched

**Task 10 — Full Investigation**
- [ ] Both simulation images created with realistic evidence
- [ ] Both images hashed before analysis
- [ ] Disk structure mapped for both images
- [ ] Deleted files recovered from laptop — content read
- [ ] USB evidence recovered via 2+ methods
- [ ] Prefetch shows keylogger execution
- [ ] FTP IP found in raw strings
- [ ] Full investigation report written
- [ ] Final hash check passed — images unchanged

---
> [!tip] Stuck? Check: `[[Task-09-10-OS-Artifacts-Full-Investigation]]`

> [!success] If you completed all 10 tasks — you have covered the entire Unit IV curriculum hands-on. Every topic from the theory notes now has a practical footprint in your lab.
