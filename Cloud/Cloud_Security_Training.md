# ☁️ Cloud Security — Complete Training Notes
> **Trainer: Ankit Ojha** | VAPT × Cloud Security
> *Simple language. Real-world examples. Deep concepts.*

---

## 🗺️ Table of Contents

| # | Topic |
|---|-------|
| 1 | [[#Types of Cloud Services]] |
| 2 | [[#IaaS vs PaaS vs SaaS]] |
| 3 | [[#EC2 — Elastic Compute Cloud]] |
| 4 | [[#EBS — Elastic Block Store]] |
| 5 | [[#S3 — Simple Storage Service]] |
| 6 | [[#Docker — Containers]] |
| 7 | [[#NACL vs Security Groups]] |
| 8 | [[#Bastion Host]] |
| 9 | [[#Incident Response in Cloud]] |
| 10 | [[#PII — Personally Identifiable Information]] |
| 11 | [[#Resume — Cloud Security Projects]] |

---

> 🧠 **Golden Rules Before You Begin**
> - EC2 = Your computer in the cloud
> - EBS = Hard disk attached to EC2
> - S3 = Google Drive for businesses
> - Docker = Lunchbox that carries your app everywhere
> - Security Group = Doorman at your flat door
> - NACL = Security guard at the society gate
> - Bastion Host = The one allowed entry gate into a fort
> - IaaS / PaaS / SaaS = Rent a kitchen / Rent a restaurant / Order food

---

---

# Types of Cloud Services

> **Simple Definition:** Cloud = Someone else's computer that you use over the internet and pay only for what you use — just like electricity.

---

## 🌍 Real World Analogy

> You don't build a power plant at home to get electricity.
> You just plug in, use it, and pay the bill.
> **Cloud is exactly this — but for computers, storage, databases, and software.**

---

## 📦 4 Types of Cloud Deployment

### 1. 🏢 Public Cloud

**What it is:** Resources owned and managed by a cloud provider (AWS, Azure, GCP) and shared among thousands of customers over the internet.

**Real World Example:**
> Imagine a large apartment building in Mumbai.
> 500 families live there. They all share the lift, electricity backup, security guards.
> But each family has their own locked flat and their own key.
> → You share infrastructure but your data is private to you.

**Examples:** AWS (Amazon), Microsoft Azure, Google Cloud Platform

**Who uses it:** Startups, developers, e-commerce companies, apps

**Pros:** No upfront cost → Pay only what you use → Scale instantly → No hardware to manage

**Cons:** Data on someone else's servers → Less physical control → Shared environment

---

### 2. 🏠 Private Cloud

**What it is:** Cloud infrastructure built and used by ONE organization only. It looks like a cloud but only you use it.

**Real World Example:**
> You build your own house with your own generator, your own water tank, your own security guard.
> Nobody else enters. You have full control of everything.

**Examples:** SBI's internal data center, DRDO's private infrastructure, Hospital IT systems

**Who uses it:** Banks, Government, Military, Hospitals

**Pros:** Full control → Maximum security → Meets strict compliance (RBI, HIPAA, etc.)

**Cons:** Very expensive to build → You manage all hardware and software

---

### 3. 🔀 Hybrid Cloud

**What it is:** Mix of Public + Private. Sensitive data stays in private cloud. Non-critical workloads use public cloud.

**Real World Example:**
> A bank keeps customer account data and transaction history in their private data center (safe, regulated).
> But the bank's website, mobile app, and marketing campaigns run on AWS (cheap, scalable).
> Best of both worlds — security where needed, cost savings where possible.

**Pros:** Flexible → Cost-efficient → Sensitive data stays compliant

**Cons:** Complex to manage → Needs expertise to connect both environments securely

---

### 4. 🌐 Community Cloud

**What it is:** Shared infrastructure used by a specific group of organizations that have similar needs (e.g., all hospitals, all government departments).

**Real World Example:**
> All government hospitals in Rajasthan share one cloud platform for patient records.
> They all need the same compliance rules (patient privacy), so they share the cost and infrastructure.

---

## 📊 Comparison Table

| Feature | Public | Private | Hybrid | Community |
|---------|--------|---------|--------|-----------|
| Cost | Low 💚 | High 🔴 | Medium 🟡 | Medium 🟡 |
| Security | Medium | High | High | Medium |
| Control | Low | Full | Partial | Shared |
| Best For | Startups | Banks/Govt | Enterprises | Specific sectors |
| Example | AWS | SBI DC | Bank + AWS | Govt hospitals |

---

## 🔐 Shared Responsibility Model (Must Know for VAPT!)

> This is the most important concept in cloud security.
> **AWS secures the cloud. YOU secure what you put IN the cloud.**

```
AWS is responsible for:
  ✅ Physical data center security (locks, cameras, guards)
  ✅ Network hardware (routers, switches)
  ✅ Hypervisor (the software that runs VMs)
  ✅ Storage hardware reliability

YOU (Customer) are responsible for:
  ✅ Your data and encryption
  ✅ Operating system patching
  ✅ Security Group / Firewall rules
  ✅ IAM users, passwords, MFA
  ✅ S3 bucket permissions (public/private)
  ✅ Application vulnerabilities
```

> 🚨 **90% of cloud breaches happen because customers misconfigure their OWN settings.**
> Examples: S3 bucket left public, root account with no MFA, overly permissive IAM roles.

---

## ❓ Interview Questions

> **Q: What is the Shared Responsibility Model?**
> AWS secures the physical infrastructure. You are responsible for everything you configure inside it — IAM, S3 permissions, OS patches, firewall rules.

> **Q: Why would a bank use Hybrid Cloud?**
> Customer financial data stays on private cloud for compliance. The bank's website and app use public cloud for scalability and cost savings.

> **Q: What is the most common cloud security mistake?**
> Misconfigured S3 buckets (left public), no MFA on root account, overly permissive IAM policies.

---

---

# IaaS vs PaaS vs SaaS

> **The most commonly asked interview question in cloud.**
> Think of it as: **How much do you want to manage yourself?**

---

## 🍕 Real World Analogy — Pizza!

| Situation | You Manage | Provider Manages |
|-----------|-----------|-----------------|
| **Make pizza at home** | Everything (flour, oven, toppings, cooking) | Nothing |
| **IaaS** = Rent a kitchen | Your recipe, cooking, toppings | Kitchen, oven, gas |
| **PaaS** = Order from restaurant | Just eat your pizza | Kitchen + cooking + service |
| **SaaS** = Order Zomato delivery | Nothing | Everything — just open your mouth |

---

## 🏗️ IaaS — Infrastructure as a Service

**What it is:** You rent the raw infrastructure — virtual machines, storage, networks. You install and manage everything on top.

**Real World Example:**
> Renting a flat in Mumbai. The builder gives you 4 walls and a roof.
> You buy furniture, install AC, paint walls, get internet connection.
> The builder doesn't care what you do inside — it's your responsibility.

**AWS Services:** EC2 (VMs), EBS (Storage), VPC (Network)

**Who uses it:** Developers, DevOps engineers, companies building their own software

**You manage:** OS, runtime, middleware, applications, data, security configs

**Provider manages:** Hardware, data center, hypervisor

**Example use case:**
> A startup wants to run their own web server.
> They launch an EC2 instance (IaaS), install Ubuntu, configure Nginx, deploy their app.
> Full control. Full responsibility.

---

## 🧱 PaaS — Platform as a Service

**What it is:** You get a ready-made platform to build and deploy your application. No need to manage OS or servers.

**Real World Example:**
> Renting a fully furnished flat. Kitchen has appliances, AC is installed, internet is connected.
> You just bring your suitcase and start living.
> You focus on your work — not on managing the flat.

**AWS Services:** Elastic Beanstalk, AWS Lambda, RDS (Managed Database)

**Other Examples:** Heroku, Google App Engine, Azure App Service

**Who uses it:** Developers who want to focus on code, not infrastructure

**You manage:** Your application code and data only

**Provider manages:** OS, runtime, middleware, servers, storage, networking

**Example use case:**
> A developer wants to deploy a Python Flask app.
> They use AWS Elastic Beanstalk (PaaS) — just upload the code.
> AWS automatically handles server setup, load balancing, scaling.

---

## 📱 SaaS — Software as a Service

**What it is:** A complete, ready-to-use application delivered over the internet. You just log in and use it. No installation, no maintenance.

**Real World Example:**
> Ordering food on Zomato. You don't cook, don't buy ingredients, don't wash dishes.
> Just open the app, order, eat.

**Examples:** Gmail, Google Docs, Zoom, Slack, Salesforce, Office 365

**Who uses it:** End users, businesses, everyone

**You manage:** Your account settings and data only

**Provider manages:** Everything — hardware, OS, database, application, updates

**Example use case:**
> Your company uses Gmail for email. Nobody installs mail servers.
> Google manages everything. You just log in at mail.google.com.

---

## 📊 Full Comparison Table

| Feature              | IaaS            | PaaS              | SaaS       |
| -------------------- | --------------- | ----------------- | ---------- |
| **Manage OS**        | You ✅           | Provider ✅        | Provider ✅ |
| **Manage Runtime**   | You ✅           | Provider ✅        | Provider ✅ |
| **Manage App**       | You ✅           | You ✅             | Provider ✅ |
| **Manage Data**      | You ✅           | You ✅             | You ✅      |
| **Control Level**    | High            | Medium            | Low        |
| **Expertise needed** | High            | Medium            | None       |
| **AWS Example**      | EC2             | Elastic Beanstalk | WorkMail   |
| **Real example**     | Your own server | Heroku            | Gmail      |

---

## 🔐 Security Perspective

```
IaaS Security Risks:
  → Unpatched OS (you forgot to update Ubuntu)
  → Misconfigured Security Groups (port 22 open to world)
  → No disk encryption on EBS

PaaS Security Risks:
  → Insecure application code (SQLi, XSS in your app)
  → Misconfigured environment variables (API keys in code)
  → Insecure dependencies in your app

SaaS Security Risks:
  → Weak passwords / no MFA on accounts
  → Overly permissive sharing settings (Google Doc public to internet)
  → Third-party OAuth apps with too much access
```

---

## ❓ Interview Questions

> **Q: What is the difference between IaaS and PaaS?**
> IaaS gives you raw VMs — you manage OS and everything above. PaaS gives you a ready platform — you only manage your code and data.

> **Q: Give 3 examples of SaaS.**
> Gmail, Zoom, Salesforce. You just log in — provider manages everything.

> **Q: Which model gives maximum control?**
> IaaS — you manage from OS upward. But maximum responsibility too.

> **Q: A developer wants to deploy code without managing servers. Which model?**
> PaaS. Example: AWS Elastic Beanstalk or Heroku.

---

---

# EC2 — Elastic Compute Cloud

> **Simple Definition:** EC2 = A virtual computer (server) running in AWS's data center that you can rent and use over the internet.

---

## 🖥️ Real World Analogy

> Imagine you need a computer for your office.
> Instead of buying a ₹1 lakh desktop, you rent one from AWS.
> You pay per hour. When you don't need it, you shut it down and stop paying.
> That computer lives in AWS's data center in Mumbai, but you control it fully.

---

## 🔑 Key Concepts

### What is an Instance?
> An "instance" is just one running EC2 virtual machine.
> You can launch 1 instance or 1000 instances — all in minutes.

### What is an AMI? (Amazon Machine Image)
> AMI = A snapshot/template of an OS (like a pre-installed DVD).
> You pick an AMI when launching EC2: "I want Ubuntu 22.04" or "Windows Server 2022".
> Think of it like choosing which OS DVD to install.

### Instance Types
> Different EC2 types = Different hardware specs (CPU, RAM, GPU)

| Type | Optimized For | Example Use |
|------|--------------|-------------|
| t3.micro | General (cheap) | Dev/test servers |
| c5.large | Compute (CPU heavy) | Web servers |
| r5.large | Memory (RAM heavy) | Databases |
| p3.xlarge | GPU | AI/ML training |
| i3.large | Storage (fast I/O) | Big data |

> **Tip:** t2.micro / t3.micro is FREE TIER on AWS — perfect for learning!

---

## 🔄 EC2 Lifecycle (States of an Instance)

```
[Launch] → [Pending] → [Running] ← → [Stopped] → [Terminated]
                           ↕
                       [Rebooting]
```

| State | What's Happening | Billed? |
|-------|-----------------|---------|
| **Pending** | Starting up | No |
| **Running** | Active, working | YES 💸 |
| **Stopped** | Off, like shutdown PC | No (but EBS billed) |
| **Terminated** | Deleted forever | No |

> 🚨 **Stopped ≠ Terminated!**
> Stopped = PC switched off (can restart)
> Terminated = PC thrown in the trash (gone forever)

---

## 🌐 Regions and Availability Zones

```
Region = A geographic area (e.g., ap-south-1 = Mumbai)
  └── Availability Zone (AZ) = A data center within that region
        ├── ap-south-1a  (Data center A in Mumbai)
        ├── ap-south-1b  (Data center B in Mumbai)
        └── ap-south-1c  (Data center C in Mumbai)
```

**Why multiple AZs?**
> If one data center catches fire, your app is still running in the other AZ.
> This is called **High Availability**.

---

## 🔐 How You Connect to EC2

### Linux EC2 → SSH
```bash
# Download the .pem key file when launching EC2
# Then connect via terminal:

chmod 400 my-key.pem
ssh -i my-key.pem ubuntu@<EC2-PUBLIC-IP>

# Input:  your .pem key file + EC2 public IP
# Output: terminal access to your cloud server
```

### Windows EC2 → RDP
```
Use Remote Desktop Protocol (RDP)
Input: EC2 Public IP + Username + Password
Output: Windows Desktop of your cloud server
```

---

## 💡 Key EC2 Features

### Elastic IP
> Normal EC2 gets a new IP every time you restart.
> Elastic IP = A fixed public IP that stays the same even after restart.
> Real World: Like getting a permanent phone number instead of a temporary one.

### User Data (Startup Script)
> A script that runs automatically when EC2 first starts.
```bash
#!/bin/bash
# This runs automatically on first boot
apt update -y
apt install nginx -y
systemctl start nginx
# Input:  Script written during EC2 launch
# Output: Nginx web server auto-installed when instance starts
```

### Key Pairs
> EC2 uses public/private key authentication (not passwords) for SSH.
> AWS stores the **public key** on the instance.
> You keep the **private key** (.pem file) on your laptop.
> Think of it: Public key = Lock. Private key = Your key.

---

## 🔐 Security Perspective (VAPT Angle)

```
Common EC2 Vulnerabilities:
  🔴 Port 22 (SSH) open to 0.0.0.0/0 (whole internet)
  🔴 Port 3389 (RDP) open to 0.0.0.0/0
  🔴 Default username/password not changed
  🔴 Old AMI with unpatched OS (outdated kernel, old OpenSSL)
  🔴 .pem key file uploaded to GitHub accidentally
  🔴 Instance metadata service (IMDS) accessible to app → SSRF attack
  🔴 No CloudTrail logging (no audit trail)
```

### SSRF via Instance Metadata (Important Attack!)
```
URL: http://169.254.169.254/latest/meta-data/

If a web app on EC2 is vulnerable to SSRF,
attacker can fetch:
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

Output: AWS access keys, secret keys, session tokens
→ Full account takeover possible!

Fix: Use IMDSv2 (requires token, blocks simple SSRF)
```

---

## ❓ Interview Questions

> **Q: What is EC2?**
> Virtual machine in AWS cloud. You rent it by the hour, choose OS, configure it, and connect via SSH/RDP.

> **Q: Difference between Stop and Terminate?**
> Stop = shutdown (can restart, data preserved). Terminate = delete forever.

> **Q: What is an AMI?**
> A template/snapshot of an OS used to launch EC2 instances. Like a pre-installed OS image.

> **Q: What is SSRF via EC2 metadata?**
> If a web app on EC2 has SSRF vulnerability, attacker can access http://169.254.169.254 to steal IAM credentials.

> **Q: What is an Elastic IP?**
> A static public IP that stays the same even after instance restarts. Normal EC2 IPs change on restart.

---

---

# EBS — Elastic Block Store

> **Simple Definition:** EBS = A hard disk (drive) that you attach to your EC2 instance. Just like plugging a USB drive or HDD into your PC.

---

## 💾 Real World Analogy

> Your EC2 instance is a laptop.
> EBS is the hard drive of that laptop.
> Without EBS, your laptop has no disk — you can't save anything.
> EBS stores your OS files, application data, databases — everything on disk.

---

## 🔑 Key Concepts

### Volume
> An EBS volume = one virtual hard disk.
> You can attach it to EC2 just like plugging in an external HDD.

### Root Volume vs Data Volume
```
Root Volume → Where OS is installed (C:\ in Windows, / in Linux)
              Automatically created when you launch EC2.

Data Volume → Extra disk you attach for storing data.
              Like adding a second hard drive to your PC.
```

### Persistence
> EBS data **persists** even when EC2 is stopped.
> When you terminate EC2, root EBS is deleted by default (unless you uncheck "Delete on termination").
> Data volumes are NOT deleted on termination by default.

---

## 📦 Types of EBS Volumes

| Type | Full Name | Speed | Use Case | Cost |
|------|-----------|-------|----------|------|
| **gp3** | General Purpose SSD | Fast | Most workloads, boot volumes | 💚 Low |
| **gp2** | General Purpose SSD (old) | Fast | Legacy general use | 💛 Low |
| **io1/io2** | Provisioned IOPS SSD | Very Fast | Databases (MySQL, Oracle) | 🔴 High |
| **st1** | Throughput HDD | Medium | Big data, log processing | 💛 Medium |
| **sc1** | Cold HDD | Slow | Archival, rarely accessed | 💚 Cheapest |

> **IOPS** = Input/Output Operations Per Second. More IOPS = faster disk.

---

## 📸 Snapshots (Super Important!)

**What is a Snapshot?**
> A snapshot = A photograph of your EBS volume at a specific moment.
> It backs up your entire disk to S3.
> You can restore it later or create a new volume from it.

**Real World Example:**
> Before doing a major OS update, you take a snapshot.
> If the update breaks everything, you restore from snapshot — back to normal in minutes.
> Think of it like System Restore in Windows, but much more powerful.

```
EBS Volume → Create Snapshot → Stored in S3
                                    ↓
                             Restore Volume     (same region)
                             Create AMI         (make it a launchable image)
                             Copy to another region  (disaster recovery)
```

**Snapshots are incremental:**
> First snapshot = full copy of disk (100 GB)
> Second snapshot = only the CHANGES since last snapshot (e.g., 2 GB)
> Saves storage cost! 💸

---

## 🔁 EBS vs Instance Store

| Feature | EBS | Instance Store |
|---------|-----|----------------|
| Persistence | Yes (survives stop/start) | No (deleted on stop!) |
| Speed | Fast (network attached) | Very Fast (physically attached) |
| Backup | Snapshots available | No backup option |
| Use Case | Databases, OS | Temp cache, buffer |
| Cost | Billed separately | Included in instance price |

> 🚨 **Instance Store = Temporary Storage!**
> If your EC2 stops or crashes → ALL instance store data is GONE.
> Never store important data on instance store.

---

## 🔐 Security Perspective

```
Common EBS Security Issues:
  🔴 EBS volumes not encrypted → data readable if physical drive stolen
  🔴 Public snapshots → anyone can see your data
  🔴 Snapshots shared with wrong AWS account
  🔴 No backup policy → data loss risk

Best Practices:
  ✅ Always enable EBS encryption (uses AWS KMS)
  ✅ Never make snapshots public
  ✅ Automate snapshots (AWS Data Lifecycle Manager)
  ✅ Delete old/unused volumes and snapshots (cost + security)
```

### EBS Encryption
```
When enabled:
  → Data at rest is encrypted (AES-256)
  → Data in transit between EC2 and EBS is encrypted
  → Snapshots are also encrypted
  → Uses AWS KMS (Key Management Service) for keys

Input: Enable encryption checkbox when creating volume
Output: All data on that volume is automatically encrypted
```

---

## ❓ Interview Questions

> **Q: What is EBS?**
> Virtual hard disk in AWS that attaches to EC2. Persistent storage — survives instance stop/start.

> **Q: What is an EBS Snapshot?**
> A backup (point-in-time copy) of an EBS volume stored in S3. Incremental — only changes are saved after first snapshot.

> **Q: Difference between EBS and Instance Store?**
> EBS is persistent (data survives stop). Instance Store is temporary (data lost when instance stops or crashes).

> **Q: What happens to EBS when EC2 is terminated?**
> Root volume is deleted by default. Additional data volumes are retained by default (configurable).

> **Q: How do you encrypt EBS?**
> Enable encryption when creating the volume. AWS KMS manages the keys. Also, data in transit is encrypted automatically.

---

---

# S3 — Simple Storage Service

> **Simple Definition:** S3 = Google Drive / Dropbox of AWS, but designed for businesses to store unlimited files at very low cost. Files are accessed via URL.

---

## 🪣 Real World Analogy

> Imagine a massive warehouse (Amazon's actual warehouse analogy!).
> You rent as many shelves (buckets) as you want.
> On each shelf, you place boxes (objects/files) of any size.
> You can access any box by its address (URL) from anywhere in the world.

---

## 🔑 Key Concepts

### Bucket
> A bucket = A top-level container (like a folder, but globally unique).
> Bucket names must be **globally unique** across ALL of AWS.
> A bucket belongs to a specific region.

### Object
> An object = A file stored in S3 (photo, video, PDF, backup, log file, etc.)
> Each object has:
> - **Key** = file name/path (e.g., `photos/vacation/img001.jpg`)
> - **Value** = the actual file content
> - **Metadata** = info about the file (size, content type, date)
> - **Version ID** = if versioning is enabled

### S3 URL Structure
```
https://bucket-name.s3.region.amazonaws.com/object-key

Example:
https://ankit-training.s3.ap-south-1.amazonaws.com/notes/cloud.pdf

Input: Upload a file to S3 bucket
Output: A unique URL to access that file from anywhere
```

---

## 📦 S3 Storage Classes (Cost vs Speed)

| Storage Class | Use Case | Retrieval | Cost |
|---------------|----------|-----------|------|
| **S3 Standard** | Active data, frequent access | Instant | 💸 Medium |
| **S3 Standard-IA** | Infrequent access, still important | Instant | 💚 Lower |
| **S3 One Zone-IA** | Non-critical, infrequent | Instant | 💚 Lower |
| **S3 Glacier Instant** | Archive, rare access | Instant | 💚 Cheap |
| **S3 Glacier Flexible** | Long-term archive | Minutes/Hours | 💚 Very cheap |
| **S3 Glacier Deep Archive** | Compliance, never touch | Hours | 💚 Cheapest |
| **S3 Intelligent-Tiering** | Unknown access pattern | Auto | 💛 Smart |

> **Real World:** Your company stores employee photos in Standard (accessed daily).
> Old audit logs from 2019 go to Glacier Deep Archive (cheap, rarely needed, but legally required to keep 7 years).

---

## 🔑 Key S3 Features

### Versioning
```
Off (default): New upload overwrites old file.

On: Every upload creates a new version. Old versions kept.
    Input:  Upload same file 3 times with versioning on
    Output: 3 separate versions stored, all recoverable

Use case: Protect against accidental deletion or overwrite
```

### Static Website Hosting
```
S3 can host a static website (HTML, CSS, JS — no server needed!)
Input:  Upload index.html to S3, enable static hosting
Output: Website URL like http://mybucket.s3-website-ap-south-1.amazonaws.com
Cost:   Almost free (pay only for storage + bandwidth)
```

### S3 Lifecycle Rules
```
Automatically move or delete files based on age:
Input:  Rule: "After 30 days → move to Standard-IA. After 365 days → move to Glacier."
Output: Files automatically migrate, saving cost
```

### S3 Replication
```
Cross-Region Replication (CRR): Copies objects to another region automatically.
Use case: Disaster Recovery (if Mumbai region fails, data is in Singapore)

Same-Region Replication (SRR): Copies within same region.
Use case: Compliance, log aggregation
```

---

## 🔐 S3 Security (Critical for VAPT!)

### Access Control
```
1. Bucket Policy (JSON)   → Controls access at bucket level
2. ACL (Access Control)   → Legacy, object-level control
3. IAM Policy             → Controls which AWS users can access
4. Block Public Access    → Master switch to prevent public exposure
```

### S3 Public Bucket — Most Common Cloud Vulnerability!
```
Misconfigured S3 bucket = Public to entire internet

How to check (OSINT/Recon):
  URL: https://bucket-name.s3.amazonaws.com/
  Tool: AWS CLI → aws s3 ls s3://bucket-name --no-sign-request
  Tool: s3scanner, bucket_finder, S3Recon

What attackers find in exposed buckets:
  → Customer PII data (names, emails, phone numbers)
  → Database backups with credentials
  → Source code with hardcoded API keys
  → Medical records, financial documents
  → Employee records
```

### S3 Bucket Policy Example (Secure — Block All Public)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```
> This policy: Denies any access that doesn't use HTTPS. Forces encryption in transit.

### S3 Encryption
```
In Transit: HTTPS (TLS) — always use, never HTTP
At Rest:
  SSE-S3    → AWS manages keys automatically (easiest)
  SSE-KMS   → You manage keys via AWS KMS (more control, audit trail)
  SSE-C     → You provide your own keys (maximum control)
  Client-Side → You encrypt before uploading (AWS never sees plaintext)
```

---

## ❓ Interview Questions

> **Q: What is an S3 bucket?**
> A container for storing files (objects) in AWS. Globally unique name. Stores unlimited data.

> **Q: What are the biggest S3 security risks?**
> Public buckets exposing sensitive data, no encryption at rest, no MFA delete, misconfigured bucket policies.

> **Q: What is S3 versioning?**
> Keeps multiple versions of the same object. Protects against accidental deletion or overwrite.

> **Q: What is MFA Delete?**
> An extra protection — you need MFA (phone code) to permanently delete objects or disable versioning. Prevents accidental/malicious deletion.

> **Q: How do you find exposed S3 buckets in a pentest?**
> Tools: s3scanner, AWS CLI with `--no-sign-request`. Check bucket URL directly. Also search GitHub for hardcoded bucket names in code.

---

---

# Docker — Containers

> **Simple Definition:** Docker = A way to package your application with EVERYTHING it needs (code, libraries, settings) into one portable box called a **container**. Works the same everywhere.

---

## 📦 Real World Analogy

> **The Tiffin Box (Lunchbox) Analogy:**
> Your mom packs your lunch in a tiffin box.
> The tiffin has dal, rice, sabzi — everything together.
> You can carry that tiffin to office, college, train — it doesn't matter.
> The food inside is always the same.
>
> **Docker container = tiffin box for your software.**
> Your app + all dependencies + config — all packed together.
> Works on any computer, any server, any cloud. No "it works on my machine" problem.

---

## 🔑 Key Concepts

### Container vs Virtual Machine

```
Virtual Machine (EC2):                   Docker Container:
┌────────────────────┐                   ┌──────────────────┐
│  Your App          │                   │  Your App        │
│  Libraries         │                   │  Libraries       │
│  OS (Ubuntu Full)  │  ← 20 GB!         │  (No full OS)    │ ← 200 MB!
│  Hypervisor        │                   │  Docker Engine   │
│  Physical Server   │                   │  Physical Server │
└────────────────────┘                   └──────────────────┘
Boots in: 1-2 minutes                   Starts in: Seconds!
```

| Feature | VM | Docker Container |
|---------|-----|-----------------|
| Size | GBs (full OS) | MBs (no full OS) |
| Startup Time | Minutes | Seconds |
| Isolation | Full (separate kernel) | Process-level |
| Performance | Slower | Faster |
| Portability | Less portable | Very portable |

---

### Dockerfile
> A text file with instructions to BUILD a Docker image.
> Like a recipe — tells Docker exactly how to construct your container.

```dockerfile
# Dockerfile Example — Python Web App

FROM python:3.11              # Start from official Python image
WORKDIR /app                  # Set working directory inside container
COPY requirements.txt .       # Copy requirements file
RUN pip install -r requirements.txt   # Install dependencies
COPY . .                      # Copy all app code
EXPOSE 5000                   # Tell Docker: app runs on port 5000
CMD ["python", "app.py"]      # Command to run when container starts

# Input:  This Dockerfile + your app code
# Output: A Docker image ready to run anywhere
```

### Image vs Container

```
Dockerfile → (build) → Image → (run) → Container

Image = Frozen template (like AMI in EC2, like a class in programming)
Container = Running instance of that image (like an EC2 instance, like an object)

One image → launch 100 containers
```

---

## 🛠️ Docker Commands (Most Important)

```bash
# Build an image from Dockerfile
docker build -t myapp:v1 .
# Input:  Dockerfile in current directory
# Output: Docker image named "myapp" with tag "v1"

# Run a container
docker run -d -p 8080:5000 --name mycontainer myapp:v1
# -d = run in background (detached)
# -p 8080:5000 = map port 8080 (host) → 5000 (container)
# --name = give it a name
# Input:  image name
# Output: running container, app accessible at http://localhost:8080

# List running containers
docker ps
# Output: Container ID, Image, Status, Ports, Name

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop mycontainer

# Remove a container
docker rm mycontainer

# Pull image from Docker Hub
docker pull nginx
# Input:  image name from hub.docker.com
# Output: image downloaded to local machine

# Push image to Docker Hub
docker push yourusername/myapp:v1

# View container logs
docker logs mycontainer
# Output: stdout/stderr from the container

# Execute command inside running container
docker exec -it mycontainer /bin/bash
# -it = interactive terminal
# Output: shell inside the container (like SSH into it)
```

---

## 🔗 Docker Networking

```
bridge (default) → containers on same host talk to each other
host             → container uses host's network directly (no isolation)
none             → completely isolated, no network
overlay          → containers across multiple hosts (Docker Swarm/K8s)

Example:
docker network create mynetwork
docker run --network=mynetwork myapp
```

---

## 💾 Docker Volumes (Persistent Storage)

```
Problem: Container data is lost when container is deleted!
Solution: Docker Volumes = Mount a host directory into the container

docker run -v /host/data:/container/data myapp
# Input:  /host/data on your server
# Output: Container can read/write to /host/data persistently

Even if container dies, data on /host/data survives!
```

---

## 🐙 Docker Compose (Multi-Container Apps)

```yaml
# docker-compose.yml
# Run a web app + database together with one command

version: '3'
services:
  web:
    build: .
    ports:
      - "8080:5000"
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret123
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

```bash
docker-compose up -d
# Input:  docker-compose.yml
# Output: Web app + Postgres DB both running, connected to each other
```

---

## 🔐 Docker Security (VAPT Angle)

```
Common Docker Vulnerabilities:

🔴 Running containers as root
   Fix: Add USER directive in Dockerfile to run as non-root

🔴 Hardcoded secrets in Dockerfile (passwords, API keys)
   Fix: Use environment variables or AWS Secrets Manager

🔴 Using outdated base images with CVEs
   Fix: Scan images with trivy, Snyk, or Grype
   Command: trivy image myapp:v1

🔴 Docker socket exposed (/var/run/docker.sock)
   Risk: Anyone with access to socket = root on the host
   Fix: Never mount docker.sock in containers unnecessarily

🔴 No resource limits (CPU/Memory)
   Risk: One container consumes all host resources (DoS)
   Fix: Set --memory and --cpus limits

🔴 Privileged containers
   docker run --privileged → container has root access to HOST
   Fix: Never use --privileged in production

🔴 Exposed ports unnecessarily
   Fix: Only expose ports that need to be publicly accessible
```

### Image Scanning for CVEs
```bash
# Install trivy
apt install trivy

# Scan Docker image for vulnerabilities
trivy image nginx:latest
# Output: List of CVEs in the image with severity (CRITICAL, HIGH, MEDIUM, LOW)

trivy image myapp:v1
# Input:  any Docker image
# Output: CVE report — vulnerabilities in OS packages and app libraries
```

---

## ❓ Interview Questions

> **Q: What is Docker and why use it?**
> Docker packages apps + dependencies into containers. Same container runs anywhere — no "works on my machine" issues. Faster than VMs, very portable.

> **Q: Difference between Image and Container?**
> Image = frozen template (like a class). Container = running instance of that image (like an object).

> **Q: What is the risk of running containers as root?**
> If the container is compromised, attacker gets root privileges which may lead to container escape and access to the host.

> **Q: What is container escape?**
> A vulnerability where an attacker breaks out of the container and gains access to the underlying host OS. Critical severity in cloud environments.

> **Q: How do you find secrets in Docker images?**
> Inspect Dockerfile and image layers: `docker history image:tag`. Use tools like `trufflehog` or `detect-secrets`. Check environment variables with `docker inspect`.

---

---

# NACL vs Security Groups

> **The most important AWS networking concept for security.**
> Both control traffic — but at different levels.

---

## 🏘️ Real World Analogy

> Imagine a big housing society in Jaipur.
>
> **NACL = Society Gate Security Guard**
> - Controls who enters and exits the entire society
> - Checks everyone — residents, delivery boys, visitors
> - Has a list of rules: "No entry after 11 PM", "Allow bikes from Gate 1 only"
> - Works at SOCIETY level (affects everyone inside)
>
> **Security Group = Doorman at Your Individual Flat Door**
> - Controls who enters YOUR specific flat
> - Has its own rules: "Allow only family members"
> - Works at FLAT level (affects only your flat)
>
> To reach your flat, a visitor must:
> 1. Pass the society gate (NACL) ✅
> 2. Pass your flat door (Security Group) ✅
> Both must allow the traffic!

---

## 🔐 Security Groups

**What it is:** A virtual firewall attached to an EC2 instance (or RDS, Lambda, etc.) that controls inbound and outbound traffic at the INSTANCE level.

### Key Properties
```
✅ Stateful: If you allow inbound traffic, the response is automatically allowed outbound.
            You don't need a separate outbound rule for return traffic.

✅ Allow rules ONLY: You can only ALLOW traffic. There is NO DENY rule option.
                    (If traffic doesn't match any allow rule → it's automatically denied)

✅ Instance level: Applied to individual EC2 instances.

✅ Evaluates ALL rules: All rules are evaluated before deciding.
```

### Example — Web Server Security Group
```
Inbound Rules:
┌──────────┬────────┬───────────────┬─────────────────────────┐
│ Type     │ Port   │ Source        │ Meaning                 │
├──────────┼────────┼───────────────┼─────────────────────────┤
│ HTTP     │ 80     │ 0.0.0.0/0     │ Allow all web traffic   │
│ HTTPS    │ 443    │ 0.0.0.0/0     │ Allow all HTTPS         │
│ SSH      │ 22     │ 203.0.113.5/32│ Allow only MY IP        │
└──────────┴────────┴───────────────┴─────────────────────────┘

Outbound Rules:
┌──────────┬────────┬───────────────┬─────────────────────────┐
│ All      │ All    │ 0.0.0.0/0     │ Allow all outbound      │
└──────────┴────────┴───────────────┴─────────────────────────┘

Note: Because it's STATEFUL — when browser sends HTTP request,
the response goes back automatically even without specific outbound rule.
```

---

## 🌐 NACL — Network Access Control List

**What it is:** A firewall at the **subnet level** in a VPC. Controls traffic entering and leaving an entire subnet.

### Key Properties
```
✅ Stateless: Inbound and outbound rules are INDEPENDENT.
             If you allow inbound on port 80, you must ALSO create
             an outbound rule for the response traffic.

✅ Allow AND Deny rules: You can explicitly DENY specific IPs or ports.

✅ Subnet level: Applies to ALL instances in a subnet.

✅ Rules have NUMBER order: Rules evaluated lowest number first.
                           First matching rule wins. Stop processing.

Default NACL: Allows ALL traffic in and out (open by default).
Custom NACL: Denies ALL traffic by default (you add allow rules).
```

### Example — NACL Rules
```
Inbound Rules:
┌──────┬──────────┬──────┬────────────────┬──────────┐
│ Rule#│ Protocol │ Port │ Source         │ Action   │
├──────┼──────────┼──────┼────────────────┼──────────┤
│ 100  │ TCP      │ 80   │ 0.0.0.0/0      │ ALLOW    │
│ 110  │ TCP      │ 443  │ 0.0.0.0/0      │ ALLOW    │
│ 120  │ TCP      │ 22   │ 203.0.113.5/32 │ ALLOW    │
│ 130  │ TCP      │ 22   │ 45.33.32.156/32│ DENY 🚫  │ ← Block attacker IP
│ *    │ ALL      │ ALL  │ 0.0.0.0/0      │ DENY     │ ← Default deny all
└──────┴──────────┴──────┴────────────────┴──────────┘

Outbound Rules (must define because STATELESS):
┌──────┬──────────┬─────────────┬────────────────┬──────────┐
│ Rule#│ Protocol │ Port        │ Destination    │ Action   │
├──────┼──────────┼─────────────┼────────────────┼──────────┤
│ 100  │ TCP      │ 1024-65535  │ 0.0.0.0/0      │ ALLOW    │
│ *    │ ALL      │ ALL         │ 0.0.0.0/0      │ DENY     │
└──────┴──────────┴─────────────┴────────────────┴──────────┘

Port 1024-65535 = Ephemeral ports (used for response traffic)
Without this outbound rule, responses never leave! (Stateless problem)
```

---

## 📊 NACL vs Security Groups — Full Comparison

| Feature | Security Group | NACL |
|---------|---------------|------|
| Level | Instance | Subnet |
| State | **Stateful** | **Stateless** |
| Rules | Allow ONLY | Allow + Deny |
| Rule Evaluation | All rules evaluated | Rules in number order (first match) |
| Default | Deny all inbound | Allow all (default NACL) |
| Applied to | EC2/RDS/Lambda | Entire subnet |
| Use case | Instance firewall | Subnet-level control, block IPs |
| Can block specific IP | ❌ No | ✅ Yes |

---

## 🔐 Security Perspective

```
When to use Security Groups:
  ✅ Define what services an instance exposes (port 80, 443, 22)
  ✅ Allow only specific instances to talk to each other
     (e.g., web server can talk to DB on port 3306, but nothing else can)

When to use NACL:
  ✅ Block a specific attacker's IP address quickly (NACL can DENY)
  ✅ Add extra layer of protection to a subnet
  ✅ PCI-DSS / compliance requirement for subnet-level controls

Defense in Depth:
  Use BOTH together. NACL blocks bad IPs at subnet gate.
  Security Group controls what each instance exposes.
```

### Common Pentest Finding: Security Group Too Permissive
```
Finding: Port 22 (SSH) open to 0.0.0.0/0 in Security Group
Risk:     Anyone on the internet can attempt SSH brute force
Fix:      Restrict port 22 to specific admin IP only
          Or use SSM Session Manager (no SSH at all!)

Finding: Port 3306 (MySQL) open to 0.0.0.0/0
Risk:     Database directly accessible from internet
Fix:      Only allow port 3306 from web server's security group
```

---

## ❓ Interview Questions

> **Q: What is the key difference between NACL and Security Group?**
> Security Group is stateful (return traffic automatic), applies to instances, only allow rules. NACL is stateless (must define both inbound + outbound), applies to subnets, can allow AND deny.

> **Q: You want to block a specific hacker's IP. NACL or Security Group?**
> NACL — because Security Groups can only ALLOW. NACL can explicitly DENY a specific IP.

> **Q: Why must NACL have ephemeral ports in outbound rules?**
> Because NACL is stateless — response traffic uses ephemeral ports (1024-65535). Without this outbound rule, responses can't leave the subnet.

> **Q: If NACL allows traffic but Security Group denies it, does the packet get through?**
> No. Both must allow the traffic. It's AND logic — traffic passes only if NACL allows AND Security Group allows.

---

---

# Bastion Host

> **Simple Definition:** Bastion Host = A special, hardened server that acts as the ONLY gateway to access servers in your private network. Like a secure drawbridge to a fort.

---

## 🏰 Real World Analogy

> Imagine a royal fort (your private AWS servers).
> The fort has thick walls on all sides — no doors, no windows (no direct internet access).
> The only way IN is through ONE heavily guarded gate with security checks — the Bastion Host.
> Every visitor must pass through this gate. The gate is armed, monitored, and logged.
> Inside the fort, people move freely. But outsiders can ONLY enter via this one gate.

---

## 🔑 Why Do We Need Bastion Host?

### The Problem:
```
You have:
  Public Subnet  → EC2 Web Server (accessible from internet ✅)
  Private Subnet → EC2 Database Server (NO internet access 🔒)

Problem: How do you SSH into the private DB server to do maintenance?
         You can't access it directly from the internet (that's the point!)

Without Bastion:
  Internet → [?] → Private EC2   ← IMPOSSIBLE (no route)

With Bastion:
  Internet → Bastion (Public Subnet) → Private EC2  ← POSSIBLE ✅
```

### The Solution — Bastion Host Architecture:
```
Your Laptop
    │
    │ SSH (Port 22) — only YOUR IP allowed
    ▼
┌─────────────────────────────────────────────────┐
│  PUBLIC SUBNET                                  │
│  ┌──────────────────┐                           │
│  │   BASTION HOST   │ ← Only entry point        │
│  │  (Jump Server)   │                           │
│  └────────┬─────────┘                           │
└───────────┼─────────────────────────────────────┘
            │ SSH (Port 22) — only Bastion allowed
            ▼
┌─────────────────────────────────────────────────┐
│  PRIVATE SUBNET                                 │
│  ┌──────────────────┐  ┌──────────────────┐     │
│  │  Private EC2 #1  │  │  Private EC2 #2  │     │
│  │  (Web Server)    │  │  (Database)      │     │
│  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ How to Connect via Bastion Host

### Method 1: Manual 2-Hop SSH
```bash
# Step 1: SSH into Bastion Host
ssh -i bastion-key.pem ec2-user@<BASTION_PUBLIC_IP>
# Now you're on the Bastion server

# Step 2: From Bastion, SSH into Private Server
ssh -i private-key.pem ec2-user@<PRIVATE_EC2_IP>
# Now you're on the private server!

# Input:  Your .pem keys + IPs
# Output: Shell access to private EC2
```

### Method 2: SSH Agent Forwarding (More Convenient)
```bash
# On your local machine:
ssh-add bastion-key.pem           # Add key to SSH agent
ssh-add private-key.pem           # Add private server key too

ssh -A -i bastion-key.pem ec2-user@<BASTION_IP>
# -A = Forward SSH agent (your keys come with you to Bastion)

# From Bastion, no key needed on server:
ssh ec2-user@<PRIVATE_EC2_IP>
# Your local keys are forwarded automatically!

# Input:  Both keys added to agent, connect with -A flag
# Output: Seamless access to private servers without copying keys to Bastion
```

### Method 3: ProxyJump (Best Practice — Direct in One Command)
```bash
ssh -J ec2-user@<BASTION_IP> ec2-user@<PRIVATE_EC2_IP> -i private-key.pem

# Or in ~/.ssh/config:
Host bastion
  HostName <BASTION_PUBLIC_IP>
  User ec2-user
  IdentityFile ~/.ssh/bastion-key.pem

Host private-server
  HostName <PRIVATE_EC2_IP>
  User ec2-user
  IdentityFile ~/.ssh/private-key.pem
  ProxyJump bastion

# Now just:
ssh private-server
# Input:  SSH config file
# Output: Direct tunnel to private server via Bastion in one command!
```

---

## 🔐 Hardening the Bastion Host (Security Best Practices)

```
✅ Allow SSH (port 22) ONLY from specific admin IPs (not 0.0.0.0/0!)
✅ Use key-based authentication ONLY (disable password login)
✅ Enable MFA for SSH login (google-authenticator PAM module)
✅ Enable full audit logging (all commands logged to CloudWatch)
✅ Keep OS patched and updated at all times
✅ Use the SMALLEST instance type needed (t3.micro is enough)
✅ Run NO other services on Bastion (no web server, no DB)
✅ Enable VPC Flow Logs on Bastion subnet
✅ Set up CloudWatch alerts for failed SSH attempts
✅ Rotate SSH keys regularly
✅ Consider AWS SSM Session Manager (no Bastion needed at all!)
```

---

## 🆚 Bastion vs AWS SSM Session Manager

> **AWS SSM Session Manager = Modern replacement for Bastion Host**

| Feature | Bastion Host | SSM Session Manager |
|---------|-------------|---------------------|
| Port 22 needed | YES | NO (HTTPS outbound only) |
| Public IP needed | YES | NO |
| Key management | You manage .pem keys | IAM-based, no keys |
| Audit logging | Manual setup | Automatic to CloudWatch |
| Cost | EC2 cost | Free (included in SSM) |
| Security | Good | Better |

> 🏆 For new architectures: Use **SSM Session Manager** instead of Bastion.
> No open ports, no SSH keys, full audit trail, works from browser!

---

## 🔐 Security Perspective (VAPT Angle)

```
Bastion Host Attack Scenarios:
  🔴 Port 22 open to 0.0.0.0/0 → Brute force attack possible
  🔴 Weak SSH key passphrase → Key compromised → all private servers exposed
  🔴 Old OS on Bastion → Unpatched CVEs → Server compromise
  🔴 Bastion used for other purposes → Larger attack surface
  🔴 SSH keys copied to Bastion → Key theft from Bastion = access to all privates

Testing Checklist:
  [ ] Is port 22 restricted to specific IPs?
  [ ] Are SSH keys properly protected?
  [ ] Is Bastion patched? (check OS version, OpenSSH version)
  [ ] Are all commands logged?
  [ ] Is there a separate Bastion per environment (Dev/Prod)?
```

---

## ❓ Interview Questions

> **Q: What is a Bastion Host?**
> A hardened EC2 in a public subnet that acts as the only SSH gateway to private EC2 instances. Administrators SSH to Bastion first, then jump to private servers.

> **Q: Why can't you directly SSH into a private EC2?**
> Private EC2 has no public IP and no internet gateway route. It's unreachable from the internet — by design.

> **Q: What is SSH ProxyJump?**
> An SSH feature that lets you connect to a private server via a jump host (Bastion) in a single command, tunneling through the Bastion automatically.

> **Q: What is the modern alternative to Bastion Host?**
> AWS Systems Manager (SSM) Session Manager. No port 22, no SSH keys, no public IP needed. Access via HTTPS, logged automatically to CloudWatch.

---

---

# Incident Response in Cloud

> **Simple Definition:** Incident Response (IR) = The step-by-step process you follow when a security attack or breach happens in your cloud environment. Like a fire drill, but for cyber attacks.

---

## 🚨 Real World Analogy

> Your house gets broken into.
> Do you panic and randomly call people? No.
> You follow steps:
> 1. Secure the area (don't let thief go deeper)
> 2. Call police (report)
> 3. Gather evidence (CCTV, fingerprints)
> 4. Fix the entry point (broken lock)
> 5. Review and improve security
>
> **Incident Response is exactly this — but for cloud security breaches.**

---

## 📋 NIST Incident Response Framework (6 Phases)

```
Phase 1: PREPARATION
Phase 2: IDENTIFICATION
Phase 3: CONTAINMENT
Phase 4: ERADICATION
Phase 5: RECOVERY
Phase 6: LESSONS LEARNED (Post-Incident)
```

---

## 🔍 Phase 1: Preparation

**Before any incident happens, you prepare:**

```
✅ Create IR playbooks (written procedures for each attack type)
✅ Enable AWS CloudTrail (logs all API calls)
✅ Enable AWS GuardDuty (threat detection)
✅ Enable VPC Flow Logs (network traffic logging)
✅ Set up CloudWatch Alerts (abnormal behavior alerts)
✅ Define your IR team and their roles
✅ Backup all critical data (S3 + EBS snapshots)
✅ Document your architecture (what's running where)
✅ Practice tabletop exercises (simulation drills)
```

---

## 🔍 Phase 2: Identification

**Detecting that an incident has occurred:**

```
AWS Tools for Detection:
  AWS GuardDuty     → AI-based threat detection
                       Detects: Unusual API calls, crypto mining, port scans,
                                compromised EC2, S3 data exfiltration attempts

  AWS CloudTrail    → Logs every API call made in your account
                       Who did what, when, from where

  AWS Config        → Detects configuration changes
                       "S3 bucket was made public at 3:14 PM"

  AWS Security Hub  → Centralizes all security findings in one dashboard

  VPC Flow Logs     → Logs all network connections in/out of your VPC

Common Signs of Compromise:
  🔴 Unusual EC2 instances launched (attacker mining crypto)
  🔴 New IAM user created or permissions escalated
  🔴 S3 bucket permissions changed to public
  🔴 Root account login (should never happen normally)
  🔴 API calls from unknown geographic location
  🔴 High outbound data transfer (data exfiltration)
  🔴 Spike in EC2 CPU usage (crypto mining)
  🔴 New security group rule opened to 0.0.0.0/0
```

---

## 🔒 Phase 3: Containment

**Stop the attack from spreading. Like sealing a fire door.**

```
Short-term Containment (immediate, fast):
  → Isolate the compromised EC2 instance:
     Attach a "quarantine" security group (deny ALL traffic)

  → Revoke compromised IAM credentials immediately:
     aws iam delete-access-key --access-key-id AKIAXXXXXXXX

  → Disable the compromised IAM user:
     aws iam update-login-profile --no-password-reset-required
     aws iam attach-user-policy --policy-arn DisablePolicyARN

  → Take EBS snapshot of compromised instance (preserve evidence)
  → Enable termination protection (prevent attacker deleting evidence)

Long-term Containment:
  → Deploy clean replacement instances from golden AMI
  → Apply emergency security group rules
  → Rotate ALL credentials (access keys, passwords, API keys)
  → Enable MFA everywhere if not already done
```

### Isolating a Compromised EC2
```bash
# Create a quarantine security group (allows nothing)
aws ec2 create-security-group \
  --group-name quarantine-sg \
  --description "Zero traffic - compromised instance"

# Attach quarantine SG to compromised instance
aws ec2 modify-instance-attribute \
  --instance-id i-0abc123 \
  --groups sg-quarantine123

# Input:  Compromised instance ID
# Output: Instance completely isolated from all traffic
#         (attacker loses access, forensics can begin)
```

---

## 🧹 Phase 4: Eradication

**Remove the threat completely:**

```
✅ Identify root cause (how did attacker get in?)
✅ Terminate compromised instances
✅ Delete malicious IAM users, roles, policies created by attacker
✅ Remove backdoors (unauthorized SSH keys, cron jobs, startup scripts)
✅ Scan all instances for malware
✅ Patch the vulnerability that was exploited
✅ Revoke and regenerate ALL credentials
✅ Review and tighten IAM policies (principle of least privilege)
```

---

## ✅ Phase 5: Recovery

**Restore normal operations safely:**

```
✅ Deploy clean instances from verified AMI (before compromise)
✅ Restore data from clean backups (pre-incident snapshots)
✅ Test all services work correctly
✅ Monitor extra closely for 24-48 hours post-recovery
✅ Gradually restore access (don't open everything at once)
✅ Communicate status to stakeholders
```

---

## 📚 Phase 6: Lessons Learned

**Learn from the incident to prevent recurrence:**

```
Post-Incident Review Questions:
  → How did the attacker get in? (initial access vector)
  → How long were they in? (dwell time)
  → What did they access or exfiltrate?
  → What controls failed?
  → What controls worked?
  → What will we do differently?

Deliverable: Incident Report Document
  - Timeline of events
  - Root cause analysis
  - Evidence collected
  - Actions taken
  - Recommendations
```

---

## 🔧 AWS Incident Response Tools Summary

| Tool | Purpose | What It Logs/Detects |
|------|---------|---------------------|
| **CloudTrail** | API audit logging | Every API call: who, what, when, where |
| **GuardDuty** | Threat detection | Suspicious behavior, malware, compromised accounts |
| **CloudWatch** | Monitoring & alerts | Metrics, logs, custom alarms |
| **VPC Flow Logs** | Network logging | All traffic in/out of VPC |
| **AWS Config** | Config change tracking | "What changed and when" |
| **Security Hub** | Centralized security | Aggregates all findings |
| **Macie** | Data security | Finds PII/sensitive data in S3 |
| **Inspector** | Vulnerability scanning | CVEs in EC2 OS and containers |

---

## ❓ Interview Questions

> **Q: What are the 6 phases of incident response?**
> Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned

> **Q: How do you isolate a compromised EC2 in AWS?**
> Attach a quarantine security group that denies all inbound and outbound traffic. Take an EBS snapshot first for forensics.

> **Q: What is AWS GuardDuty?**
> An AI-based threat detection service that monitors CloudTrail, VPC Flow Logs, and DNS logs to detect malicious activity. No agent needed — just enable it.

> **Q: What should you do FIRST when you discover a breach?**
> Contain — stop the spread. Then preserve evidence (snapshot). Then investigate. Never delete evidence before investigation.

> **Q: What is CloudTrail and why is it critical for IR?**
> CloudTrail logs every AWS API call with timestamp, user identity, source IP, and action taken. It's your "CCTV footage" of everything that happened in your AWS account.

---

---

# PII — Personally Identifiable Information

> **Simple Definition:** PII = Any data that can identify a specific person, either on its own or combined with other data.

---

## 👤 Real World Analogy

> Imagine a school register.
> It has: student name, roll number, address, phone number, parent name.
> If someone steals this register, they can find you, call you, visit your house.
> They know WHO you are. That's PII.
>
> **PII = Data that points to a specific real human being.**

---

## 📋 What is PII?

### Direct PII (Identifies alone)
```
✅ Full name
✅ Aadhaar number / PAN number / Passport number
✅ Social Security Number (SSN) — USA
✅ Date of birth
✅ Email address
✅ Phone number
✅ Home address
✅ Biometric data (fingerprint, iris scan, face photo)
✅ Driver's license number
✅ Bank account number / Credit card number
```

### Indirect PII (Identifies when combined)
```
⚠️ Age + City + Job Title (alone not enough, combined = identifiable)
⚠️ IP address (can be traced to person)
⚠️ Cookie IDs (tracks user across websites)
⚠️ Device ID / IMEI number
⚠️ Location data (GPS history)
⚠️ Browsing history
```

### Sensitive PII (Extra Protection Required)
```
🔴 Medical/Health records
🔴 Financial information (salary, account statements)
🔴 Sexual orientation / Gender identity
🔴 Religious beliefs
🔴 Political views
🔴 Racial or ethnic origin
🔴 Criminal record
🔴 Child data (under 18 — extra strict rules!)
```

---

## 🌍 PII Laws and Regulations

| Law | Region | What It Covers |
|-----|--------|---------------|
| **GDPR** | European Union | All personal data of EU residents. Strict consent, right to delete. |
| **DPDP Act 2023** | India 🇮🇳 | India's Digital Personal Data Protection Act. Consent required. |
| **HIPAA** | USA | Health/medical data |
| **PCI-DSS** | Global | Credit card / payment card data |
| **COPPA** | USA | Children's data (under 13) |
| **IT Act 2000** | India 🇮🇳 | Sensitive personal data, cybercrime |

### Key GDPR Rights (Most Important Globally)
```
Right to Access      → "Show me all data you have on me"
Right to Erasure     → "Delete all my data" (Right to be Forgotten)
Right to Portability → "Give me my data in a portable format"
Right to Rectification → "Correct wrong data about me"
Right to Object      → "Stop processing my data"
```

---

## ☁️ PII in AWS Cloud

### AWS Services That Handle PII:
```
Amazon Macie:
  → Automatically discovers and protects PII in S3 buckets
  → Uses ML to detect: SSNs, credit card numbers, names, addresses
  → Alerts you if PII is found in unencrypted or public buckets

Input:  Enable Macie, point it at S3 buckets
Output: Report of where PII is stored, risk level, recommendations

AWS KMS (Key Management Service):
  → Encrypts PII data at rest
  → Manages encryption keys
  → Full audit trail of who decrypted what and when

AWS CloudTrail:
  → Logs who accessed PII data, when, from where
  → Evidence for GDPR/DPDP compliance audit
```

---

## 🔐 Handling PII Securely (Best Practices)

```
COLLECTION:
  ✅ Collect MINIMUM necessary PII (data minimization)
  ✅ Get explicit consent before collecting
  ✅ Tell users why you're collecting it (purpose limitation)

STORAGE:
  ✅ Encrypt PII at rest (AES-256)
  ✅ Encrypt in transit (TLS/HTTPS)
  ✅ Store in private S3 buckets ONLY (never public!)
  ✅ Separate PII database from other data
  ✅ Implement strict IAM — only those who NEED it can access

PROCESSING:
  ✅ Log all access to PII data
  ✅ Use pseudonymization (replace name with random ID in logs)
  ✅ Anonymize data for analytics (remove identifying fields)

DELETION:
  ✅ Delete PII when no longer needed
  ✅ Honor "Right to Erasure" requests within 30 days (GDPR)
  ✅ Secure deletion (overwrite data, not just delete pointer)
```

### Pseudonymization vs Anonymization
```
Original Record:
  Name: Ankit Ojha | DOB: 1995-05-15 | Disease: Diabetes

Pseudonymization (reversible):
  UserID: A-2847 | DOB: 1995-05-15 | Disease: Diabetes
  → Name replaced with random ID. A lookup table links ID→Name.
  → Still PII (can be reversed). But much safer than raw name.

Anonymization (irreversible):
  Age: 29 | Region: Rajasthan | Disease: Diabetes
  → All identifying info removed. Cannot be traced back.
  → No longer PII. Can share freely.
```

---

## 🔍 PII in Penetration Testing

```
When you find PII during a pentest:
  ✅ Document it as a finding (severity: HIGH/CRITICAL)
  ✅ Do NOT download, copy, or exfiltrate real PII data
  ✅ Note the location, access method, and data type seen
  ✅ Report immediately if it's a live production database
  ✅ Use sample/dummy data for testing wherever possible

Common PII Exposure Findings:
  🔴 S3 bucket public → contains customer database with names+emails
  🔴 API endpoint returning full PII without authentication
  🔴 Log files containing credit card numbers or SSNs
  🔴 Database backup (.sql file) accessible via misconfigured S3
  🔴 Error messages leaking user data in stack traces
  🔴 Insecure Direct Object Reference (IDOR) exposing other users' PII
```

---

## ❓ Interview Questions

> **Q: What is PII? Give 5 examples.**
> PII = Data that identifies a person. Examples: Full name, Aadhaar number, email address, phone number, biometric data.

> **Q: What is the difference between pseudonymization and anonymization?**
> Pseudonymization replaces identity with a fake ID (reversible — still PII). Anonymization removes all identifying information (irreversible — no longer PII).

> **Q: What is GDPR's "Right to be Forgotten"?**
> Any EU resident can request a company delete all personal data about them. Company must comply within 30 days.

> **Q: What AWS service detects PII in S3?**
> Amazon Macie — uses machine learning to scan S3 buckets and flag PII like SSNs, credit card numbers, names, and addresses.

> **Q: You find a public S3 bucket with customer names and emails during a pentest. What do you do?**
> Document the finding with severity HIGH/CRITICAL. Note the bucket name, what's exposed, and access method. Report to client immediately. Do NOT download the data. Recommend immediate remediation: block public access, apply bucket policy, enable Macie.

---

---

# Resume — Cloud Security Projects

> **Add these projects to your resume to show real AWS + Security hands-on experience.**
> Each project is described with what you did, tools used, and what you found.

---

## 🏆 How to Write Cloud Security Projects on Resume

```
Format: [Action Verb] + [What You Did] + [Tool/Technology] + [Result/Impact]

Bad:  "Did AWS security testing"
Good: "Identified 12 critical misconfigurations in AWS environment including
       public S3 buckets, overly permissive IAM roles, and unencrypted EBS volumes
       using Prowler, Scout Suite, and AWS CLI; provided detailed remediation report"
```

---

## 💼 Project 1: AWS Cloud Security Assessment

**Description:**
> Conducted comprehensive AWS security assessment of a multi-service environment covering EC2, S3, IAM, VPC, and RDS using automated and manual techniques.

**Resume Bullet Points:**
```
• Performed AWS cloud security assessment identifying 18 misconfigurations 
  including 3 publicly accessible S3 buckets exposing 50,000+ customer records,
  using Prowler v3, Scout Suite, and AWS CLI

• Discovered overly permissive IAM roles with wildcard (*) permissions and 
  root account without MFA enabled; documented findings per CIS AWS Benchmark v1.4

• Identified 2 EC2 instances with SSH (port 22) open to 0.0.0.0/0 and 
  Instance Metadata Service v1 enabled, demonstrating SSRF-to-credential-theft 
  attack path using IMDSv1

• Produced detailed remediation report with CVSS scores, business impact, 
  and step-by-step fix instructions; all findings remediated within 30 days
```

**Tools Used:** `Prowler`, `Scout Suite`, `AWS CLI`, `Pacu (AWS exploitation framework)`, `Cloudsplaining`

---

## 💼 Project 2: S3 Bucket Misconfiguration Discovery

**Description:**
> Researched and discovered exposed S3 buckets belonging to target organizations through OSINT and automated scanning.

**Resume Bullet Points:**
```
• Discovered 5+ publicly accessible S3 buckets via OSINT and automated tools 
  (s3scanner, bucket-finder) exposing database backups, source code with 
  hardcoded API keys, and employee PII data

• Demonstrated data exfiltration impact and documented full attack chain 
  from public S3 discovery → credential extraction → account privilege escalation

• Reported findings through responsible disclosure program; received 3 
  Hall of Fame acknowledgments and 2 bug bounty rewards
```

**Tools Used:** `s3scanner`, `bucket-finder`, `AWS CLI`, `truffleHog`, `gitleaks`

---

## 💼 Project 3: Docker Container Security Assessment

**Description:**
> Performed security assessment of a containerized application environment, identifying vulnerabilities in Docker images and runtime configurations.

**Resume Bullet Points:**
```
• Assessed Docker-based application environment identifying 23 CVEs in base 
  images using Trivy, including 4 CRITICAL severity vulnerabilities in outdated 
  OpenSSL and glibc versions

• Identified hardcoded AWS access keys in Dockerfile environment variables 
  and container running as root, demonstrating container escape risk

• Discovered Docker socket mounted in application container (/var/run/docker.sock),
  demonstrating full host compromise via socket abuse

• Provided remediation: multi-stage builds, non-root USER directive, secrets 
  management via AWS Secrets Manager, image scanning in CI/CD pipeline
```

**Tools Used:** `Trivy`, `Grype`, `Hadolint`, `Docker Bench for Security`, `Dive`, `truffleHog`

---

## 💼 Project 4: Cloud IAM Privilege Escalation Research

**Description:**
> Researched and demonstrated IAM privilege escalation paths in AWS environments.

**Resume Bullet Points:**
```
• Mapped 15+ IAM privilege escalation techniques in AWS including 
  PassRole abuse, Lambda function injection, and CloudFormation stack 
  manipulation using Pacu framework and custom Python scripts

• Built lab environment simulating real-world IAM misconfigurations;
  demonstrated path from low-privilege developer account to 
  AdministratorAccess in under 10 minutes

• Published 3 blog posts on AWS privilege escalation techniques 
  attracting 5,000+ views; contributed findings to MITRE ATT&CK Cloud matrix
```

**Tools Used:** `Pacu`, `Cloudsplaining`, `Parliament`, `AWS CLI`, `Boto3 (Python)`

---

## 💼 Project 5: Incident Response Simulation

**Description:**
> Built and executed a cloud incident response lab simulating a real-world AWS account compromise.

**Resume Bullet Points:**
```
• Designed and executed AWS incident response simulation: simulated 
  EC2 compromise via SSRF → metadata credential theft → IAM privilege 
  escalation → S3 data exfiltration

• Implemented detection using AWS GuardDuty, CloudTrail analysis, 
  and VPC Flow Log investigation; reduced mean-time-to-detect (MTTD) 
  from 45 minutes to 8 minutes through automated alerting

• Developed IR playbook covering containment (quarantine SG), 
  eradication (credential rotation), and recovery procedures; 
  playbook adopted by 2 client organizations
```

**Tools Used:** `AWS GuardDuty`, `CloudTrail`, `CloudWatch`, `AWS Security Hub`, `Velociraptor`, `Python (Boto3)`

---

## 🔧 Cloud Security Tools for Your Resume

```
Enumeration/Assessment:
  Prowler          → CIS/NIST benchmark checks for AWS
  Scout Suite      → Multi-cloud security auditing
  Cloudsplaining   → IAM policy analysis, finds overly permissive policies
  Pacu             → AWS exploitation framework (like Metasploit for AWS)
  CloudMapper      → AWS network visualization

S3 Specific:
  s3scanner        → Scan for public buckets
  bucket-finder    → Brute force bucket names

Container Security:
  Trivy            → CVE scanner for Docker images
  Grype            → Another image vulnerability scanner
  Hadolint         → Dockerfile linter (finds security issues)
  Docker Bench     → CIS Docker benchmark checks

Secrets Detection:
  truffleHog       → Find secrets in code, Git history, S3
  gitleaks         → Detect secrets in Git repositories

Threat Detection:
  AWS GuardDuty    → Enable it! (AI threat detection)
  CloudTrail       → Always enable in ALL regions
  AWS Macie        → PII detection in S3

Python SDK:
  Boto3            → AWS Python SDK (automate everything)
```

---

## 📜 Cloud Certifications to Add

```
✅ AWS Certified Cloud Practitioner (CLF-C02) — Entry level, 3 months prep
✅ AWS Certified Security - Specialty (SCS-C02) — Security focused, 6 months
✅ AWS Certified Solutions Architect - Associate (SAA-C03) — Architecture
✅ Certified Cloud Security Professional (CCSP) — Vendor neutral
✅ Google Cloud Professional Cloud Security Engineer
```

---

## ❓ Interview Questions on Resume Projects

> **Q: Walk me through your AWS security assessment methodology.**
> Start with reconnaissance (account structure, regions used). Then automated scans (Prowler for CIS benchmarks). Then manual review (IAM policies, S3 bucket policies, Security Groups). Then test high-risk findings. Finally, report with CVSS scores and remediation steps.

> **Q: What is Pacu?**
> An open-source AWS exploitation framework similar to Metasploit. Used to enumerate permissions, escalate privileges, and test attack paths in AWS environments.

> **Q: How do you find hardcoded secrets in Docker images?**
> Use `docker history image:tag` to see all layers. Use `truffleHog` or `gitleaks` to scan image layers. Check environment variables with `docker inspect`. Look at Dockerfile `ENV` and `ARG` directives.

> **Q: What is the SSRF to credential theft attack path in AWS?**
> If a web app on EC2 has SSRF and IMDSv1 is enabled, attacker sends request to http://169.254.169.254/latest/meta-data/iam/security-credentials/[role-name] via the vulnerable app to get temporary AWS credentials. With those credentials, attacker can call AWS APIs with the instance's IAM role permissions.

---

---

## 📝 Final Revision — Everything in 2 Minutes

```
Cloud Types:    Public (AWS) | Private (Bank DC) | Hybrid | Community
Service Models: IaaS (EC2) = Rent kitchen | PaaS (Beanstalk) = Rent restaurant | SaaS (Gmail) = Order food

EC2:  Virtual machine. AMI = OS template. Stop ≠ Terminate. SSH with .pem key.
      Attack: SSRF via 169.254.169.254 to steal IAM credentials.

EBS:  Hard disk for EC2. Persistent. Snapshot = Backup to S3 (incremental).
      Risk: Unencrypted volumes, public snapshots.

S3:   Object storage. Bucket + Objects. Public bucket = Most common cloud breach.
      Defense: Block Public Access, encrypt, enable Macie, MFA Delete.

Docker: Container = App + dependencies in one box. Image → Container.
        Risks: Root container, docker.sock mount, hardcoded secrets, unpatched images.
        Scan: trivy image name:tag

NACL: Subnet-level. Stateless. Allow + Deny. Rules numbered.
SG:   Instance-level. Stateful. Allow only. All rules evaluated.
      SG = Flat doorman. NACL = Society gate guard.
      Want to block specific IP? → Use NACL (SG has no deny!)

Bastion: Jump server. Public subnet → SSH → Private subnet.
         Modern alternative: AWS SSM Session Manager (no port 22 needed!)

IR Phases: Prepare → Identify → Contain → Eradicate → Recover → Learn
           Isolate compromised EC2: attach quarantine security group.
           Key tools: CloudTrail (audit) | GuardDuty (detect) | Macie (PII)

PII: Data that identifies a person. Encrypt + minimize + consent required.
     India law: DPDP Act 2023. EU law: GDPR.
     AWS tool for PII: Amazon Macie (scans S3).

Resume Projects: AWS assessment, S3 OSINT, Docker CVE scan, IAM privesc, IR simulation.
Tools to know: Prowler, Scout Suite, Pacu, Trivy, s3scanner, Cloudsplaining, Boto3
```

---

*Tags: #cloud #aws #security #vapt #ec2 #s3 #docker #iam #nacl #bastion #incidentresponse #pii #training*

*Made with ❤️ for training future cloud security professionals — Ankit Ojha*
