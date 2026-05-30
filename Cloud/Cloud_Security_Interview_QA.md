# ☁️ Cloud Security — Interview Questions & Answers
> **For Freshers | First Job in Cloud Security**
> Simple language. Short answers. Interview-ready.

---

## 🗺️ Topics Covered

| # | Topic |
|---|-------|
| 1 | [[#Cloud Basics]] |
| 2 | [[#IaaS PaaS SaaS]] |
| 3 | [[#EC2]] |
| 4 | [[#EBS]] |
| 5 | [[#S3]] |
| 6 | [[#Docker]] |
| 7 | [[#NACL and Security Groups]] |
| 8 | [[#Bastion Host]] |
| 9 | [[#Incident Response]] |
| 10 | [[#PII]] |
| 11 | [[#General Cloud Security]] |

---

---

# Cloud Basics

---

**Q1. What is Cloud Computing?**

> Cloud computing means using someone else's computers, storage, and software over the internet and paying only for what you use — just like paying an electricity bill instead of building your own power plant.

---

**Q2. What are the main cloud service providers?**

> The top three are:
> - **AWS** (Amazon Web Services) — most popular
> - **Microsoft Azure**
> - **Google Cloud Platform (GCP)**

---

**Q3. What are the types of cloud deployment models?**

> There are 4 types:
> - **Public Cloud** — shared infrastructure (e.g., AWS). Used by startups, developers.
> - **Private Cloud** — used by one organization only (e.g., bank's own data center).
> - **Hybrid Cloud** — mix of public and private. Sensitive data on private, rest on public.
> - **Community Cloud** — shared by organizations with similar needs (e.g., government hospitals).

---

**Q4. What is the Shared Responsibility Model?**

> It means security is divided between the cloud provider and the customer.
> - **AWS is responsible for** — physical security of data centers, hardware, network, and hypervisor.
> - **You (customer) are responsible for** — your data, OS patching, firewall rules (Security Groups), IAM users, passwords, encryption settings, and application security.
> 
> Simple way to remember: **AWS secures the cloud. You secure what you put IN the cloud.**

---

**Q5. What is a Region and Availability Zone in AWS?**

> - **Region** = A geographic location where AWS has data centers. Example: `ap-south-1` = Mumbai.
> - **Availability Zone (AZ)** = One or more data centers within a region. Mumbai has 3 AZs: `ap-south-1a`, `ap-south-1b`, `ap-south-1c`.
> - Multiple AZs exist so that if one data center fails, your application keeps running in another. This is called **High Availability**.

---

**Q6. What is a VPC?**

> VPC stands for **Virtual Private Cloud**. It is your own private, isolated network inside AWS. Think of it like your own gated housing society inside AWS's huge city. You control who enters, what subnets exist, and what the routing rules are. Every AWS account gets a default VPC automatically.

---

**Q7. What is the difference between a Public Subnet and a Private Subnet?**

> - **Public Subnet** — has a route to the Internet Gateway. Resources here can be accessed from the internet. Example: web servers.
> - **Private Subnet** — no direct internet access. Resources here are hidden from the internet. Example: databases, backend servers.
> 
> Best practice: Keep databases in private subnets and only expose web servers in public subnets.

---

**Q8. What is IAM in AWS?**

> IAM stands for **Identity and Access Management**. It controls who can do what in your AWS account.
> - **Users** = individual people (e.g., developer, admin)
> - **Groups** = collection of users (e.g., Developers group)
> - **Roles** = permissions assigned to AWS services (e.g., EC2 can access S3)
> - **Policies** = JSON documents that define what is allowed or denied
> 
> IAM follows the **Principle of Least Privilege** — give only the minimum permissions needed.

---

**Q9. What is the Principle of Least Privilege?**

> Give a user, application, or service only the minimum permissions they need to do their job — nothing more. 
> 
> Example: A developer who only needs to read from S3 should NOT have permission to delete EC2 instances. Over-permissive access is one of the biggest causes of cloud breaches.

---

**Q10. What is MFA and why is it important in cloud?**

> MFA stands for **Multi-Factor Authentication**. It adds a second layer of security beyond just a password. Even if your password is stolen, the attacker cannot login without the second factor (like a 6-digit OTP from your phone).
> 
> In AWS, MFA must be enabled on the **root account** at minimum. Best practice is to enable it for all IAM users.

---

---

# IaaS PaaS SaaS

---

**Q11. What is IaaS? Give an example.**

> IaaS stands for **Infrastructure as a Service**. The provider gives you raw infrastructure — virtual machines, storage, and networking. You install and manage everything on top including the OS and applications.
> 
> Example: **AWS EC2**. You launch a virtual machine, install Ubuntu, configure Nginx, and deploy your app. You manage the OS. AWS manages the physical hardware.

---

**Q12. What is PaaS? Give an example.**

> PaaS stands for **Platform as a Service**. The provider gives you a ready-made platform to deploy your application. You only manage your code and data. The provider handles OS, runtime, and servers.
> 
> Example: **AWS Elastic Beanstalk** or **Heroku**. You just upload your Python or Java code. The platform automatically handles server setup, scaling, and load balancing.

---

**Q13. What is SaaS? Give an example.**

> SaaS stands for **Software as a Service**. A complete application delivered over the internet. You just log in and use it. No installation, no maintenance required.
> 
> Examples: **Gmail, Zoom, Slack, Salesforce, Office 365**. Google manages all the servers, databases, and updates. You just open gmail.com and use it.

---

**Q14. What is the key difference between IaaS, PaaS, and SaaS?**

> The difference is **how much you manage vs how much the provider manages**.
> 
> | Model | You Manage | Provider Manages |
> |-------|-----------|-----------------|
> | IaaS | OS, App, Data | Hardware, Network |
> | PaaS | App, Data only | OS, Runtime, Servers |
> | SaaS | Nothing (just use it) | Everything |
> 
> Simple memory trick: **IaaS = Rent a kitchen. PaaS = Rent a restaurant. SaaS = Order food on Zomato.**

---

**Q15. Which cloud model gives maximum control to the customer?**

> **IaaS** gives maximum control because you manage from the OS level upward — you choose the OS, install software, configure everything. But with maximum control comes maximum responsibility for security.

---

---

# EC2

---

**Q16. What is EC2?**

> EC2 stands for **Elastic Compute Cloud**. It is a virtual machine (computer) running in AWS's data center that you can rent and use over the internet. You choose the OS, CPU, RAM, and storage. You pay per hour. When you don't need it, you stop it and stop paying.

---

**Q17. What is an AMI?**

> AMI stands for **Amazon Machine Image**. It is a pre-configured template (snapshot) of an operating system used to launch EC2 instances. Think of it like a pre-installed OS DVD. When you launch an EC2, you pick an AMI: "I want Ubuntu 22.04" or "I want Windows Server 2022". You can also create your own custom AMI from an existing EC2 instance.

---

**Q18. What is the difference between Stop and Terminate in EC2?**

> - **Stop** = Shut down the instance like turning off a PC. The instance can be restarted later. Data on the EBS (hard disk) is preserved. You are NOT charged for compute when stopped (but EBS storage is still billed).
> - **Terminate** = Permanently delete the instance. It is gone forever. The root EBS volume is also deleted by default. This action cannot be undone.
> 
> Simple: **Stop = Switch off. Terminate = Throw in the trash.**

---

**Q19. What is an Elastic IP?**

> An Elastic IP is a **fixed, static public IP address** in AWS. Normally, when you stop and start an EC2 instance, it gets a new public IP each time. An Elastic IP stays the same even after restarts. Useful when you need a permanent address for your server (like a domain pointing to a fixed IP).

---

**Q20. How do you connect to a Linux EC2 instance?**

> You connect using **SSH** (Secure Shell) with a key pair (.pem file).
> ```bash
> chmod 400 my-key.pem
> ssh -i my-key.pem ubuntu@<EC2-PUBLIC-IP>
> ```
> - The .pem file is the private key downloaded when launching the EC2.
> - AWS stores the matching public key on the instance.
> - Password login is disabled by default — only key-based login works.

---

**Q21. What is EC2 User Data?**

> User Data is a script that runs automatically when an EC2 instance starts for the first time. It is used to automate setup tasks like installing software, updating packages, or starting services without manually logging in.
> 
> Example: Automatically install and start Nginx when EC2 boots:
> ```bash
> #!/bin/bash
> apt update -y
> apt install nginx -y
> systemctl start nginx
> ```

---

**Q22. What are EC2 instance types? Give examples.**

> EC2 instance types define the hardware specifications (CPU, RAM, GPU). Different types are optimized for different workloads:
> - **t3.micro** — General purpose, cheap. Good for dev/test. Free tier eligible.
> - **c5.large** — Compute optimized. Good for web servers.
> - **r5.large** — Memory optimized. Good for databases.
> - **p3.xlarge** — GPU instances. Good for machine learning.
> 
> The naming format is: `family` + `generation` + `.` + `size`. Example: `t3.micro` = t-family, 3rd generation, micro size.

---

**Q23. What is a Security Group in EC2?**

> A Security Group is a virtual firewall attached to an EC2 instance that controls what traffic is allowed in (inbound) and out (outbound). It works like a doorman at your flat — only allowed guests can enter.
> 
> Key points:
> - Only ALLOW rules (no deny option)
> - Stateful — if inbound is allowed, the response automatically goes out
> - Applied at the instance level

---

**Q24. What is the biggest security risk with EC2?**

> The most common EC2 security risks are:
> - **Port 22 (SSH) open to 0.0.0.0/0** — allows anyone to brute force your server
> - **Unpatched OS** — old kernel or packages with known CVEs
> - **SSRF via Instance Metadata** — if a web app on EC2 has SSRF vulnerability and IMDSv1 is enabled, attacker can access `http://169.254.169.254` to steal IAM credentials
> - **.pem key file accidentally uploaded to GitHub**

---

---

# EBS

---

**Q25. What is EBS?**

> EBS stands for **Elastic Block Store**. It is a virtual hard disk (drive) that you attach to an EC2 instance to store data. Just like plugging a hard drive into your laptop. EBS stores your OS files, application data, and databases. Data on EBS persists even when EC2 is stopped — it does not get deleted.

---

**Q26. What is an EBS Snapshot?**

> An EBS Snapshot is a **point-in-time backup** of an EBS volume stored in S3. It captures the complete state of your disk at that moment. You can use it to restore your disk if something goes wrong, create a new volume, or copy data to another region.
> 
> Snapshots are **incremental** — the first snapshot copies the full disk, but every snapshot after that only saves the changes (not the full disk again). This saves storage cost.

---

**Q27. What is the difference between EBS and Instance Store?**

> | Feature | EBS | Instance Store |
> |---------|-----|----------------|
> | Data persists after stop? | Yes ✅ | No ❌ (lost forever) |
> | Speed | Fast | Faster (physically attached) |
> | Backup option | Snapshots available | No backup |
> | Use case | OS, databases, important data | Temporary cache only |
> 
> **Critical:** Never store important data on Instance Store. If the EC2 stops or crashes, all Instance Store data is permanently gone.

---

**Q28. What are the types of EBS volumes?**

> - **gp3 / gp2** — General Purpose SSD. Most common. Good for OS and general workloads.
> - **io1 / io2** — Provisioned IOPS SSD. Very fast. Used for high-performance databases.
> - **st1** — Throughput HDD. For big data and log processing.
> - **sc1** — Cold HDD. Cheapest. For data that is rarely accessed.
> 
> For most use cases, **gp3** is the recommended default choice.

---

**Q29. How do you secure EBS volumes?**

> - **Enable encryption** — EBS supports AES-256 encryption using AWS KMS. Data at rest and data in transit between EC2 and EBS is encrypted.
> - **Do not make snapshots public** — public snapshots expose your entire disk to anyone.
> - **Delete unused volumes** — old unattached volumes are a security and cost risk.
> - **Automate snapshots** — use AWS Data Lifecycle Manager to take regular backups.

---

---

# S3

---

**Q30. What is S3?**

> S3 stands for **Simple Storage Service**. It is AWS's object storage service used to store any type of file — images, videos, documents, backups, logs. Think of it as Google Drive for businesses but with unlimited storage, accessed via a URL. Files are stored in **buckets** (containers) and each file is called an **object**.

---

**Q31. What is an S3 Bucket?**

> An S3 bucket is a container (like a folder) that holds your files (objects) in S3. Key points:
> - Bucket names must be **globally unique** across all of AWS
> - A bucket belongs to one specific AWS region
> - You can store unlimited objects in a bucket
> - Each object can be up to 5 TB in size

---

**Q32. What is the most common S3 security vulnerability?**

> **Public S3 Buckets** — when a bucket's permissions are misconfigured to allow public access, anyone on the internet can view and download all files in that bucket.
> 
> This is one of the most common causes of data breaches in cloud. Companies have exposed customer databases, financial records, source code with passwords, and medical records through misconfigured S3 buckets.
> 
> Fix: Enable **Block Public Access** setting on every bucket. It is now the default in new AWS accounts.

---

**Q33. What is S3 Versioning?**

> S3 Versioning keeps **multiple versions of the same file**. Every time you upload a new version of a file, the old version is preserved. If someone accidentally deletes or overwrites a file, you can restore the previous version.
> 
> Example: You upload `report.pdf`, then upload a new version of `report.pdf`. Both versions are stored. You can go back to the old version anytime.

---

**Q34. What are S3 Storage Classes?**

> S3 offers different storage classes based on how frequently you access the data:
> - **S3 Standard** — for frequently accessed data. Fast, slightly expensive.
> - **S3 Standard-IA** — for infrequently accessed data. Cheaper, same speed.
> - **S3 Glacier** — for archival data rarely accessed. Very cheap, hours to retrieve.
> - **S3 Glacier Deep Archive** — cheapest. For data kept for compliance only. Retrieval takes up to 12 hours.
> - **S3 Intelligent-Tiering** — automatically moves data between tiers based on usage.

---

**Q35. How do you control access to S3?**

> Access to S3 is controlled in 3 ways:
> - **Bucket Policy** — a JSON document attached to the bucket defining who can access it and what they can do. Most common method.
> - **IAM Policy** — attached to IAM users/roles to define their S3 permissions.
> - **Block Public Access** — a master switch that overrides all other settings to prevent any public access. Should always be ON unless you intentionally need public access.

---

**Q36. What is S3 encryption?**

> S3 supports encryption to protect data:
> - **In Transit** — use HTTPS (TLS). Never use HTTP for S3.
> - **At Rest** (3 options):
>   - **SSE-S3** — AWS manages the keys automatically. Easiest option.
>   - **SSE-KMS** — You manage keys through AWS KMS. Provides audit trail of who decrypted what.
>   - **SSE-C** — You provide your own encryption keys.
> 
> Best practice: Always enable SSE-KMS for sensitive data so you have a full audit trail.

---

---

# Docker

---

**Q37. What is Docker?**

> Docker is a platform that packages an application with all its dependencies (libraries, configuration, runtime) into a single portable unit called a **container**. The container runs the same way on any machine — your laptop, a test server, or a cloud instance. This solves the classic "it works on my machine" problem.

---

**Q38. What is the difference between a Docker Image and a Container?**

> - **Image** = A frozen, read-only template. Like a class in programming or an AMI in AWS. The image has all the instructions to build the container.
> - **Container** = A running instance of an image. Like an object created from a class. You can run many containers from one image.
> 
> Simple: **Image = Recipe. Container = The cooked food.**

---

**Q39. What is a Dockerfile?**

> A Dockerfile is a text file with step-by-step instructions to build a Docker image. Docker reads this file and creates the image automatically.
> 
> Example:
> ```dockerfile
> FROM python:3.11        # Start from Python base image
> WORKDIR /app            # Set working directory
> COPY . .                # Copy app files
> RUN pip install flask   # Install dependencies
> CMD ["python", "app.py"]# Start the app
> ```

---

**Q40. What is the difference between a Container and a Virtual Machine?**

> | Feature | Virtual Machine | Docker Container |
> |---------|----------------|-----------------|
> | Size | GBs (full OS inside) | MBs (no full OS) |
> | Startup Time | 1-2 minutes | Seconds |
> | Performance | Slower | Faster |
> | Isolation | Full (own kernel) | Process-level |
> | Use Case | Run different OS | Run apps portably |
> 
> Containers are lighter and faster because they share the host OS kernel instead of running their own.

---

**Q41. What are the most important Docker commands?**

> ```bash
> docker build -t myapp:v1 .        # Build image from Dockerfile
> docker run -d -p 8080:80 myapp:v1 # Run container (port 8080 on host → 80 in container)
> docker ps                          # List running containers
> docker ps -a                       # List all containers (including stopped)
> docker stop container-name         # Stop a container
> docker rm container-name           # Remove a container
> docker images                      # List all images
> docker pull nginx                  # Download image from Docker Hub
> docker exec -it container /bin/bash# Get shell inside running container
> docker logs container-name         # View container output/logs
> ```

---

**Q42. What is Docker Hub?**

> Docker Hub is a public registry (like GitHub but for Docker images) where you can store, share, and download Docker images. Official images for popular software like Nginx, MySQL, Python, Ubuntu are available on Docker Hub. You pull images from Docker Hub using `docker pull image-name`.

---

**Q43. What are the main Docker security risks?**

> - **Running containers as root** — if container is hacked, attacker gets root access
> - **Hardcoded secrets in Dockerfile** — passwords, API keys visible to anyone with the image
> - **Outdated base images** — old images have unpatched CVEs (security vulnerabilities)
> - **Docker socket mounted** (`/var/run/docker.sock`) — gives container full control over the host
> - **Privileged containers** (`--privileged`) — container gets root access to the host OS
> 
> Fix: Scan images with **Trivy** (`trivy image myapp:v1`) to find CVEs before deploying.

---

**Q44. What is Docker Compose?**

> Docker Compose is a tool to define and run multi-container applications using a single YAML file (`docker-compose.yml`). Instead of running multiple `docker run` commands, you define all services in one file and start everything with one command: `docker-compose up`. Example: running a web app + database + cache together.

---

---

# NACL and Security Groups

---

**Q45. What is a Security Group in AWS?**

> A Security Group is a virtual firewall that controls inbound and outbound traffic for an AWS resource (like EC2). It works at the **instance level**.
> 
> Key points:
> - **Stateful** — if you allow inbound traffic, the response is automatically allowed out
> - **Allow rules only** — you can only allow traffic, not explicitly deny
> - All rules are evaluated before making a decision
> - Default: all inbound denied, all outbound allowed

---

**Q46. What is a NACL (Network Access Control List)?**

> A NACL is a firewall that controls traffic at the **subnet level** in a VPC. It applies to all resources inside that subnet.
> 
> Key points:
> - **Stateless** — inbound and outbound rules are independent. Return traffic must be explicitly allowed.
> - **Allow AND Deny rules** — you can block specific IPs
> - Rules are evaluated in number order (lowest number first, first match wins)
> - Default NACL allows all traffic

---

**Q47. What is the key difference between NACL and Security Group?**

> | Feature | Security Group | NACL |
> |---------|---------------|------|
> | Level | Instance | Subnet |
> | State | Stateful | Stateless |
> | Rules | Allow only | Allow + Deny |
> | Default | Deny all inbound | Allow all |
> | Block specific IP | ❌ Cannot | ✅ Can |
> 
> **Simple memory trick:** Security Group = Doorman at your flat. NACL = Security guard at the society gate. To reach your flat, a visitor must pass BOTH.

---

**Q48. If you want to block a specific attacker's IP address, do you use NACL or Security Group?**

> You use **NACL** because Security Groups only have ALLOW rules — you cannot explicitly deny a specific IP using Security Groups. NACL supports both ALLOW and DENY rules, so you can add a DENY rule for the attacker's IP at the subnet level.

---

**Q49. What is meant by "Stateful" and "Stateless" in networking?**

> - **Stateful (Security Group)** — tracks the connection. If you allow an inbound request, the response is automatically allowed back out. You don't need a separate outbound rule for return traffic.
> - **Stateless (NACL)** — does NOT track connections. Every packet is evaluated independently. If you allow inbound HTTP traffic, you must also create an outbound rule to allow the HTTP response back out (on ephemeral ports 1024-65535).

---

**Q50. What is the default behavior of Security Groups?**

> By default:
> - **Inbound** — ALL traffic is DENIED (nothing gets in unless you add an allow rule)
> - **Outbound** — ALL traffic is ALLOWED (everything gets out by default)
> 
> When you create a Security Group, it starts with no inbound rules (all blocked) and one outbound rule allowing all traffic.

---

---

# Bastion Host

---

**Q51. What is a Bastion Host?**

> A Bastion Host (also called a Jump Server) is a special EC2 instance placed in a **public subnet** that acts as the only entry point for administrators to access servers in the **private subnet**. It is heavily secured and monitored. Admins SSH into the Bastion first, then from the Bastion SSH into private servers.

---

**Q52. Why do we need a Bastion Host?**

> Private EC2 instances have no public IP and no internet route — you cannot directly SSH into them from the internet. That's the point — they are hidden for security. But admins still need to access them for maintenance. The Bastion Host solves this by acting as a secure intermediary:
> 
> `Your Laptop → SSH → Bastion (Public) → SSH → Private EC2`

---

**Q53. How do you SSH into a private EC2 using a Bastion Host?**

> **Two-hop method:**
> ```bash
> # Step 1: SSH into Bastion
> ssh -i bastion-key.pem ec2-user@<BASTION_PUBLIC_IP>
> 
> # Step 2: From Bastion, SSH into private server
> ssh -i private-key.pem ec2-user@<PRIVATE_EC2_IP>
> ```
> 
> **Better method — ProxyJump (one command):**
> ```bash
> ssh -J ec2-user@<BASTION_IP> ec2-user@<PRIVATE_EC2_IP> -i private-key.pem
> ```

---

**Q54. How do you secure a Bastion Host?**

> - Allow SSH (port 22) only from specific admin IPs — never open to 0.0.0.0/0
> - Use key-based authentication only — disable password login
> - Keep OS fully patched and updated
> - Run no other services on Bastion — it should only be a jump server
> - Enable full command logging and send to CloudWatch
> - Use the smallest instance type needed (t3.micro is enough)
> - Set up alerts for failed SSH login attempts

---

**Q55. What is the modern alternative to a Bastion Host?**

> **AWS Systems Manager (SSM) Session Manager**. It lets you access EC2 instances without:
> - Opening port 22 (SSH)
> - Having a public IP on the instance
> - Managing SSH keys
> 
> Access is done over HTTPS, controlled by IAM, and all sessions are automatically logged to CloudWatch. It is more secure, easier to manage, and costs less than running a Bastion EC2 instance.

---

---

# Incident Response

---

**Q56. What is Incident Response?**

> Incident Response is the organized, step-by-step process a team follows when a security attack or breach is detected. The goal is to detect it quickly, stop it from spreading, remove the threat, restore normal operations, and learn from it to prevent future incidents.

---

**Q57. What are the phases of Incident Response?**

> There are 6 phases (NIST framework):
> 1. **Preparation** — Set up tools, write playbooks, train the team before any incident
> 2. **Identification** — Detect and confirm that an incident has occurred
> 3. **Containment** — Stop the attack from spreading (isolate the affected system)
> 4. **Eradication** — Remove the threat completely (delete malware, close vulnerability)
> 5. **Recovery** — Restore systems to normal operation from clean backups
> 6. **Lessons Learned** — Review what happened, why, and how to prevent it next time

---

**Q58. What would you do first if you discovered a compromised EC2 instance?**

> First, I would **contain** it — stop the attack from spreading:
> 1. Take an EBS snapshot of the instance (preserve evidence for forensics)
> 2. Attach a quarantine Security Group that blocks ALL inbound and outbound traffic (isolates the instance)
> 3. Revoke any IAM credentials associated with the instance
> 4. Do NOT terminate the instance yet — you need it for investigation
> 
> Then investigate what happened, eradicate the threat, and recover from a clean backup.

---

**Q59. What is AWS CloudTrail?**

> AWS CloudTrail is a service that logs every API call made in your AWS account. It records:
> - **Who** made the call (IAM user, role, or service)
> - **What** action was taken (e.g., `DeleteBucket`, `RunInstances`)
> - **When** it happened (timestamp)
> - **Where** the request came from (source IP address)
> 
> CloudTrail is your **audit log / CCTV footage** for AWS. It is the first place you look during an incident investigation. It should always be enabled in all regions.

---

**Q60. What is AWS GuardDuty?**

> AWS GuardDuty is a **threat detection service** that uses machine learning to automatically analyze CloudTrail logs, VPC Flow Logs, and DNS logs to detect suspicious activity. It alerts you about things like:
> - Unusual API calls from unknown locations
> - EC2 instance communicating with known malware IPs
> - Crypto mining activity detected
> - Compromised IAM credentials being used
> 
> You just enable it with one click — no agents to install. It runs 24/7 in the background.

---

**Q61. What is the difference between CloudTrail and CloudWatch?**

> - **CloudTrail** = Logs **API calls and account activity**. Answers "Who did what and when?" Used for security auditing and incident investigation.
> - **CloudWatch** = Monitors **performance metrics and application logs**. Answers "How is my system performing?" Used for operational monitoring, alerts, and dashboards.
> 
> Simple: **CloudTrail = Security CCTV. CloudWatch = Performance dashboard.**

---

**Q62. What is AWS Macie?**

> AWS Macie is a security service that uses machine learning to automatically **discover and protect sensitive data (PII) stored in S3 buckets**. It scans buckets and alerts you if it finds things like Aadhaar numbers, credit card numbers, email addresses, names, or other personal data — especially in buckets that are unencrypted or publicly accessible.

---

---

# PII

---

**Q63. What is PII?**

> PII stands for **Personally Identifiable Information**. It is any data that can identify a specific individual — either on its own or when combined with other data.
> 
> Examples of PII:
> - Full name, Aadhaar number, PAN card
> - Email address, phone number, home address
> - Date of birth, passport number
> - Biometric data (fingerprint, face photo)
> - Bank account number, credit card number

---

**Q64. What is the difference between Direct PII and Indirect PII?**

> - **Direct PII** — directly identifies a person on its own. Example: Aadhaar number, full name, email address.
> - **Indirect PII** — does not identify alone but can identify when combined with other data. Example: age + city + job title together can narrow down to one person. IP address, cookie ID, device ID are also indirect PII.

---

**Q65. What is GDPR?**

> GDPR stands for **General Data Protection Regulation**. It is a privacy law of the European Union that protects the personal data of EU residents. Key rules:
> - You must get user **consent** before collecting their data
> - Users have the **Right to be Forgotten** (delete their data on request)
> - Users can access all data held about them
> - Data breaches must be reported within **72 hours**
> - Heavy fines for violations (up to 4% of global annual revenue)

---

**Q66. What is India's data protection law?**

> India's data protection law is the **Digital Personal Data Protection (DPDP) Act 2023**. It protects the personal data of Indian residents. Key points:
> - Companies must get user **consent** before processing personal data
> - Data must be used only for the **stated purpose**
> - Data should not be kept longer than necessary
> - Users can request correction or deletion of their data
> - Data fiduciaries (companies) must report breaches to the DPDB (Data Protection Board)

---

**Q67. What is the difference between Pseudonymization and Anonymization?**

> - **Pseudonymization** — replaces identifying information with a fake ID. The original identity can be recovered using a lookup table. The data is still considered PII because it can be reversed. Example: replacing "Ankit Ojha" with user ID "A-2847".
> - **Anonymization** — completely removes all identifying information so the data cannot be traced back to any individual. It is no longer PII. Example: replacing name with just "age: 29, region: Rajasthan".
> 
> GDPR compliance: anonymized data is not subject to GDPR. Pseudonymized data still is.

---

**Q68. How should PII be stored securely in cloud?**

> - Store PII in **private S3 buckets only** — never public
> - **Encrypt at rest** using SSE-KMS (AES-256)
> - **Encrypt in transit** using HTTPS/TLS
> - Apply **strict IAM policies** — only people who need it can access PII
> - **Log all access** using CloudTrail
> - **Collect minimum data** — only what is necessary
> - **Delete PII** when no longer needed
> - Use **Amazon Macie** to detect PII in S3 and get alerts

---

---

# General Cloud Security

---

**Q69. What is the CIA Triad in security?**

> The CIA Triad is the foundation of information security:
> - **Confidentiality** — only authorized people can access the data (encryption, access control)
> - **Integrity** — data is accurate and not tampered with (checksums, hashing)
> - **Availability** — systems and data are accessible when needed (backups, redundancy, DDoS protection)
> 
> All security controls are designed to protect one or more of these three properties.

---

**Q70. What is encryption? What is the difference between encryption at rest and in transit?**

> Encryption is the process of converting readable data into unreadable form so only authorized parties with the decryption key can read it.
> 
> - **Encryption at rest** — data is encrypted when stored on disk (e.g., EBS volume, S3 object). Protects against physical theft of storage media.
> - **Encryption in transit** — data is encrypted while traveling over the network (e.g., HTTPS/TLS). Protects against network eavesdropping (man-in-the-middle attacks).
> 
> Best practice: always enable both.

---

**Q71. What is a CVE?**

> CVE stands for **Common Vulnerabilities and Exposures**. It is a publicly disclosed security vulnerability in software that has been given a unique ID (e.g., CVE-2021-44228 = Log4Shell). The CVE system allows security teams worldwide to reference the same vulnerability using the same ID. Each CVE has a CVSS score (0-10) indicating severity: Critical, High, Medium, Low.

---

**Q72. What is CVSS?**

> CVSS stands for **Common Vulnerability Scoring System**. It is a numerical score from 0 to 10 that rates the severity of a security vulnerability:
> - **9.0 - 10.0** = Critical
> - **7.0 - 8.9** = High
> - **4.0 - 6.9** = Medium
> - **0.1 - 3.9** = Low
> - **0.0** = None
> 
> CVSS score is used to prioritize which vulnerabilities to fix first — Critical and High first.

---

**Q73. What is Zero Trust Security?**

> Zero Trust is a security model based on the principle: **"Never trust, always verify."** Instead of trusting anyone inside the network automatically, every user, device, and service must be verified every time before being granted access.
> 
> In cloud: don't assume internal traffic is safe. Verify identity, check permissions, use least privilege, and log everything — even for internal requests.

---

**Q74. What is Multi-Factor Authentication (MFA)? Why is it important?**

> MFA requires users to provide two or more verification factors to log in:
> - Something you **know** (password)
> - Something you **have** (OTP from phone app)
> - Something you **are** (fingerprint/face)
> 
> Even if your password is stolen, the attacker cannot log in without the second factor. In AWS, MFA should be enabled on the root account and all IAM users. It is one of the most effective controls against account takeover.

---

**Q75. What is a Data Breach?**

> A data breach is a security incident where sensitive, confidential, or protected data is accessed, stolen, or exposed by an unauthorized person. In cloud, common causes are:
> - Public S3 buckets
> - Weak or stolen IAM credentials
> - Unpatched vulnerabilities in EC2
> - Misconfigured security groups exposing databases
> - Insider threats
> 
> Companies must notify affected users and regulators (within 72 hours under GDPR) when a breach occurs.

---

**Q76. What is DDoS and how does AWS protect against it?**

> DDoS stands for **Distributed Denial of Service**. It is an attack where thousands of machines flood a server with traffic to overwhelm it and make it unavailable to real users.
> 
> AWS protection:
> - **AWS Shield Standard** — automatically protects all AWS customers from common DDoS attacks at no extra charge
> - **AWS Shield Advanced** — paid service for advanced DDoS protection with 24/7 DDoS response team
> - **AWS WAF** — Web Application Firewall that blocks malicious HTTP requests (SQLi, XSS, etc.)
> - **CloudFront + Route 53** — absorb DDoS traffic before it reaches your server

---

**Q77. What is AWS WAF?**

> AWS WAF stands for **Web Application Firewall**. It filters HTTP/HTTPS web traffic and blocks malicious requests before they reach your application. It protects against:
> - SQL Injection (SQLi)
> - Cross-Site Scripting (XSS)
> - Bad bots and scrapers
> - Known attacker IPs
> - Rate limiting (block IPs making too many requests)
> 
> AWS WAF is deployed in front of CloudFront, Application Load Balancer, or API Gateway.

---

**Q78. What is the difference between Authentication and Authorization?**

> - **Authentication** = Verifying **who you are**. Proving your identity. Example: logging in with username + password + MFA.
> - **Authorization** = Verifying **what you are allowed to do**. Checking your permissions. Example: after login, can you delete S3 buckets or only read them?
> 
> Simple: **Authentication = Who are you? Authorization = What can you do?**

---

**Q79. What is AWS KMS?**

> AWS KMS stands for **Key Management Service**. It is a managed service for creating and controlling encryption keys used to encrypt your data across AWS services. Key features:
> - Creates and stores encryption keys securely (in hardware security modules)
> - Integrates with S3, EBS, RDS, CloudTrail for encryption
> - Every encryption/decryption action is logged in CloudTrail
> - You control who can use each key (using key policies)

---

**Q80. What is the difference between Vulnerability Assessment and Penetration Testing?**

> - **Vulnerability Assessment (VA)** — identifies and lists all known vulnerabilities in a system using automated scanning tools. It tells you WHAT is vulnerable but does not exploit it. Like a health checkup that lists all problems.
> - **Penetration Testing (PT)** — goes one step further. It actively tries to exploit the vulnerabilities to prove they are real and measure the actual impact. Like a doctor who not only finds problems but also demonstrates how serious they are.
> 
> VA = Find weaknesses. PT = Find weaknesses + prove you can exploit them.

---

---

## 📝 Quick Revision Cheatsheet

```
Cloud Types    → Public | Private | Hybrid | Community
Shared Resp    → AWS secures hardware. You secure your config + data.
IAM            → Users, Groups, Roles, Policies. Least Privilege always.

IaaS           → EC2. Rent a kitchen. You manage OS up.
PaaS           → Elastic Beanstalk. Rent a restaurant. Manage code only.
SaaS           → Gmail. Order food. Just use it.

EC2            → Virtual machine. AMI = OS template. Stop ≠ Terminate.
EBS            → Hard disk for EC2. Persistent. Snapshot = Backup.
S3             → Object storage. Bucket + Objects. Public bucket = breach.

Docker         → Container = App + deps in a box. Image → Container.
               → Risks: root container, docker.sock, hardcoded secrets.
               → Scan: trivy image name:tag

Security Group → Instance level. Stateful. Allow only. All rules checked.
NACL           → Subnet level. Stateless. Allow + Deny. Rules numbered.
               → Block specific IP? Use NACL (SG cannot deny!)

Bastion Host   → Jump server in public subnet to access private EC2.
               → Modern: SSM Session Manager (no port 22, no keys)

IR Phases      → Prepare → Identify → Contain → Eradicate → Recover → Learn
               → Compromised EC2? Quarantine SG → Snapshot → Investigate

CloudTrail     → Logs all API calls. Security CCTV. Always enable.
GuardDuty      → AI threat detection. Enable with one click.
Macie          → Finds PII in S3 automatically.
KMS            → Manages encryption keys. Audit trail of who used keys.

PII            → Data that identifies a person. Encrypt + minimize.
GDPR           → EU law. Consent required. 72hr breach notification.
DPDP Act 2023  → India's data protection law.
Pseudonymization → Reversible. Still PII.
Anonymization   → Irreversible. Not PII.

CIA Triad      → Confidentiality + Integrity + Availability
MFA            → Password + OTP. Stops 99% of account takeovers.
CVSS           → Vulnerability severity score. 9-10 = Critical.
CVE            → Unique ID for a known vulnerability.
Auth vs Authz  → Authentication = Who are you? Authorization = What can you do?
VA vs PT       → VA finds vulnerabilities. PT finds + exploits them.
```

---

*Tags: #interview #fresher #cloud #aws #security #vapt*
*Made for first job in Cloud Security — Ankit Ojha*
