---
tags: [ctf, solution, unit4, forensics, fat32, fls, icat, hidden-partition, ext4]
challenge: "Bonus A — Stolen Records (customer_export.csv)"
flag: "No flag — evidence file (proves 75842 records stolen)"
points: Evidence
difficulty: Easy-Medium
topic: Deleted File Recovery — Victim Data
image: ctf1.img → P2 deleted file: customer_export.csv

---

# 🗃️ Bonus A — The Stolen Records

> [!info] Real World Case — IndusInd Bank Data Theft (Simulated)
> This file represents the actual stolen goods. In real cases, recovering the victim database proves the **extent of harm** and helps identify affected individuals for notification. Under India's IT Act 2000 and the proposed DPDP Act 2023, recovery of stolen personal data is mandatory evidence for both prosecution and regulatory notification.

---

## 📋 Purpose

`customer_export.csv` is not a flag challenge — it is the **primary crime evidence**. Recovering it proves:
1. What was stolen (personal banking data)
2. How much was stolen (75,842 records)
3. Who owns the data (IndusInd Bank customers)
4. When it was exported (2024-03-17 09:22:11)
5. Where it was sent (ftp://185.44.21.9/drop/)

---

## 🔍 Recovery

```bash
fls -r -d -o 133120 ctf1.img | grep customer
```

**Output:**
```
r/r * 9:   customer_export.csv
```

```bash
icat -o 133120 ctf1.img 9
```

**Output:**
```
CustomerID,Name,AccountNo,Balance,Email,Phone
10001,Priya Sharma,HDFC-9981,245000,priya.s@gmail.com,9812345678
10002,Amit Kumar,SBI-4421,89500,amit.k@yahoo.com,9823456789
10003,Sunita Verma,ICICI-7762,512000,sunita.v@gmail.com,9834567890
10004,Rajesh Gupta,AXIS-3319,67000,rajesh.g@hotmail.com,9845678901
... [75842 records CONFIDENTIAL]
Exported: admin  2024-03-17 09:22:11
Sent to: ftp://185.44.21.9/drop/customer_export.csv
```

---

# 🔒 Bonus B — Hidden Partition (P3 ext4)

> [!success] Bonus Discovery
> Finding P3 demonstrates full disk forensics understanding

---

## 📋 Purpose

The hidden ext4 partition (P3) is not mentioned in any challenge description. Students who run `mmls` discover it automatically. It contains backup credentials — showing how attackers maintain persistence through secondary access paths.

---

## 🔍 Step 1 — Discover via mmls

```bash
mmls ctf1.img
```

**Output:**
```
004: 000:002 0000952320  0001034239  0000081920  Linux (0x83)
```

Most students working only with FAT32 tools will never see this.

---

## 🔍 Step 2 — Mount P3

```bash
sudo mkdir -p /mnt/p3
sudo mount /dev/mapper/loop0p3 /mnt/p3
ls /mnt/p3/
cat /mnt/p3/private.txt
```

**Output:**
```
Hidden ext4 partition found!
Visible only with: mmls ctf1.img  or  fdisk -l ctf1.img

FTP:       rohan_upload / Upl04d!99  @  185.44.21.9
Secondary: admin / S3cr3t@123  @  10.0.0.55
```

---

## 🔍 Alternative — Direct offset mount

```bash
# No kpartx needed — direct byte offset
sudo mount -o loop,offset=487587840 ctf1.img /mnt/p3
```

---

## 🔬 Why Hidden Partitions Matter

> [!note] Real Attack Technique
> In APT (Advanced Persistent Threat) operations, attackers create extra partitions, hidden volumes (VeraCrypt/TrueCrypt), and Linux ext4 partitions on Windows machines. Standard Windows disk management doesn't display ext4. A standard `ls /mnt/usb` only shows mounted FAT32 — ext4 is completely invisible without `mmls` or `fdisk`.

> [!tip] Always run mmls first
> Before analysing any image, run `mmls image.img` to see the complete partition layout including hidden partitions, unallocated gaps, and non-standard partition types. This is step 2 in every forensic investigation (step 1 is hash verification).
