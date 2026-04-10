---
tags:
  - cyber-forensics
  - lab-setup
  - kali-linux
  - tools-installation
aliases:
  - Forensics Lab Setup
  - Forensics Tools Install
date: 2026-03-17
status: complete
---

# 🧪 Cyber Forensics — Complete Lab Setup Guide
> [!abstract] Overview
> This file covers **everything you need** to set up a fully functional Cyber Forensics lab on Kali Linux — from directory structure to every tool installation with verification steps.
> Follow this **once** before attempting any task files.

---

## 📁 STEP 1 — Create Lab Directory Structure

```bash
mkdir -p ~/forensics-lab/{cases,tools,images,practice,recovered,reports,scripts}
mkdir -p ~/forensics-lab/cases/{case001,case002,case003}
mkdir -p ~/forensics-lab/practice/{fat32,ntfs,ext4,formatted,usb,ram}
mkdir -p ~/forensics-lab/images/{disk,memory,mobile}
mkdir -p ~/forensics-lab/recovered/{deleted,formatted,carved}

# Verify
tree ~/forensics-lab/
```

Expected output:
```
forensics-lab/
├── cases/
│   ├── case001/
│   ├── case002/
│   └── case003/
├── images/
│   ├── disk/
│   ├── memory/
│   └── mobile/
├── practice/
│   ├── ext4/
│   ├── fat32/
│   ├── formatted/
│   ├── ntfs/
│   ├── ram/
│   └── usb/
├── recovered/
│   ├── carved/
│   ├── deleted/
│   └── formatted/
├── reports/
├── scripts/
└── tools/
```

---

## 🔧 STEP 2 — Update System

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
echo "System updated ✓"
```

---

## 🛠️ STEP 3 — Install Core Forensics Tools (APT)

### 3.1 Disk & File System Tools

```bash
sudo apt install -y \
  sleuthkit \
  autopsy \
  testdisk \
  foremost \
  scalpel \
  dcfldd \
  ddrescue \
  gpart \
  parted \
  gparted \
  ntfs-3g \
  exfatprogs \
  extundelete \
  ext4magic \
  fatcat \
  mtools

echo "Disk tools installed ✓"
```

### 3.2 Data Analysis & Carving Tools

```bash
sudo apt install -y \
  binwalk \
  bulk-extractor \
  scrounge-ntfs \
  safecopy \
  dc3dd \
  wipe \
  secure-delete \
  hexedit \
  xxd \
  strings \
  file \
  exiftool \
  mat2 \
  ssdeep

echo "Analysis tools installed ✓"
```

### 3.3 Memory & Live Forensics

```bash
sudo apt install -y \
  volatility3 \
  lime-forensics-dkms \
  avml

echo "Memory tools installed ✓"
```

### 3.4 Network Forensics

```bash
sudo apt install -y \
  wireshark \
  tshark \
  tcpdump \
  ngrep \
  netsniff-ng \
  xplico

echo "Network tools installed ✓"
```

### 3.5 Hash & Integrity Tools

```bash
sudo apt install -y \
  hashdeep \
  md5deep \
  sha256deep \
  afflib-tools \
  libewf-dev \
  ewf-tools

echo "Hash/integrity tools installed ✓"
```

### 3.6 Utilities

```bash
sudo apt install -y \
  tree \
  unzip \
  p7zip-full \
  curl \
  wget \
  git \
  python3-pip \
  python3-venv \
  libimage-exiftool-perl \
  kpartx \
  losetup \
  cryptsetup

echo "Utilities installed ✓"
```

---

## 🐍 STEP 4 — Install Python Forensics Tools (pip)

```bash
# Always use --break-system-packages on Kali
pip3 install --break-system-packages \
  analyzeMFT \
  python-evtx \
  regipy \
  construct \
  hexdump \
  pefile \
  yara-python \
  oletools \
  volatility3

echo "Python tools installed ✓"
```

### Verify Python tools

```bash
analyzeMFT.py --help 2>/dev/null | head -3
python3 -c "import evtx; print('evtx OK')"
python3 -c "import regipy; print('regipy OK')"
python3 -c "import volatility3; print('volatility3 OK')"
```

---

## 📦 STEP 5 — Install Additional Tools from GitHub

### 5.1 Volatility3 (Latest)

```bash
cd ~/forensics-lab/tools/
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
pip3 install --break-system-packages -r requirements.txt
python3 vol.py --help | head -5
cd ~
echo "Volatility3 cloned ✓"
```

### 5.2 Volatility3 Symbol Tables (for Windows analysis)

```bash
mkdir -p ~/forensics-lab/tools/volatility3/volatility3/symbols
cd ~/forensics-lab/tools/volatility3/volatility3/symbols

# Download Windows symbols
wget https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip
unzip windows.zip
rm windows.zip
echo "Volatility symbols installed ✓"
```

### 5.3 KAPE-equivalent: Triage Collector Script

```bash
cat > ~/forensics-lab/scripts/triage_collect.sh << 'EOF'
#!/bin/bash
# Quick triage collector for mounted Windows image
MOUNT=$1
OUTPUT=$2
mkdir -p $OUTPUT

echo "[*] Collecting artifacts from $MOUNT"
cp -r "$MOUNT/Windows/System32/winevt/Logs/" "$OUTPUT/EventLogs/" 2>/dev/null
cp -r "$MOUNT/Windows/Prefetch/" "$OUTPUT/Prefetch/" 2>/dev/null
cp "$MOUNT/Windows/System32/config/SAM" "$OUTPUT/SAM" 2>/dev/null
cp "$MOUNT/Windows/System32/config/SYSTEM" "$OUTPUT/SYSTEM" 2>/dev/null
cp "$MOUNT/Windows/System32/config/NTUSER.DAT" "$OUTPUT/NTUSER.DAT" 2>/dev/null
echo "[+] Triage complete: $OUTPUT"
EOF
chmod +x ~/forensics-lab/scripts/triage_collect.sh
echo "Triage script created ✓"
```

---

## 🖼️ STEP 6 — Create Practice Disk Images

> [!important] Run this ONCE
> These images are used across all task files. Creating them here saves time.

### 6.1 FAT32 Practice Image

```bash
dd if=/dev/zero of=~/forensics-lab/images/disk/fat32_practice.img bs=1M count=50
mkfs.fat -F32 ~/forensics-lab/images/disk/fat32_practice.img
echo "FAT32 image created ✓"
```

### 6.2 NTFS Practice Image

```bash
dd if=/dev/zero of=~/forensics-lab/images/disk/ntfs_practice.img bs=1M count=100
sudo mkntfs -f ~/forensics-lab/images/disk/ntfs_practice.img
echo "NTFS image created ✓"
```

### 6.3 ext4 Practice Image

```bash
dd if=/dev/zero of=~/forensics-lab/images/disk/ext4_practice.img bs=1M count=100
mkfs.ext4 ~/forensics-lab/images/disk/ext4_practice.img
echo "ext4 image created ✓"
```

### 6.4 Formatted Partition Image

```bash
dd if=/dev/zero of=~/forensics-lab/images/disk/formatted_practice.img bs=1M count=200
sudo parted ~/forensics-lab/images/disk/formatted_practice.img \
  mklabel msdos \
  mkpart primary ntfs 1MiB 150MiB \
  mkpart primary fat32 150MiB 200MiB
echo "Formatted partition image created ✓"
```

---

## 📂 STEP 7 — Configure Scalpel

```bash
# Backup original config
sudo cp /etc/scalpel/scalpel.conf /etc/scalpel/scalpel.conf.bak

# Enable common file types (remove # from lines)
sudo sed -i 's/^#\(.*jpg.*\)/\1/' /etc/scalpel/scalpel.conf
sudo sed -i 's/^#\(.*pdf.*\)/\1/' /etc/scalpel/scalpel.conf
sudo sed -i 's/^#\(.*png.*\)/\1/' /etc/scalpel/scalpel.conf
sudo sed -i 's/^#\(.*zip.*\)/\1/' /etc/scalpel/scalpel.conf
sudo sed -i 's/^#\(.*gif.*\)/\1/' /etc/scalpel/scalpel.conf

echo "Scalpel configured ✓"
```

---

## 🔍 STEP 8 — Configure Autopsy

```bash
# First launch sets up database
autopsy &
sleep 5
# Opens at: http://localhost:9999/autopsy

# Or use Autopsy 4 (newer GUI):
# Download from https://www.autopsy.com/download/
# sudo apt install default-jdk
# java -version
echo "Autopsy launched — open browser at http://localhost:9999/autopsy"
```

---

## ✅ STEP 9 — Verify All Tools

```bash
echo "=== VERIFICATION REPORT ===" > ~/forensics-lab/tool_check.txt
echo "Date: $(date)" >> ~/forensics-lab/tool_check.txt
echo "" >> ~/forensics-lab/tool_check.txt

tools=(
  "sleuthkit:tsk_version"
  "autopsy:autopsy --version"
  "testdisk:testdisk /list"
  "foremost:foremost -V"
  "scalpel:scalpel -V"
  "dcfldd:dcfldd --version"
  "binwalk:binwalk --help"
  "bulk_extractor:bulk_extractor --version"
  "exiftool:exiftool -ver"
  "hashdeep:hashdeep -V"
  "volatility3:python3 -m volatility3 --version"
  "extundelete:extundelete --version"
  "strings:strings --version"
  "xxd:xxd --version"
)

for entry in "${tools[@]}"; do
  tool="${entry%%:*}"
  cmd="${entry##*:}"
  if eval "$cmd" &>/dev/null; then
    echo "  [✓] $tool" | tee -a ~/forensics-lab/tool_check.txt
  else
    echo "  [✗] $tool — MISSING" | tee -a ~/forensics-lab/tool_check.txt
  fi
done

echo ""
echo "Full report: ~/forensics-lab/tool_check.txt"
```

---

## 🖥️ STEP 10 — Optional: VirtualBox Shared Folder Setup

> [!tip] If using Kali in VirtualBox
> Set up shared folder to easily transfer evidence files from host.

```bash
# Install Guest Additions (if not already done)
sudo apt install -y virtualbox-guest-utils virtualbox-guest-x11

# Mount shared folder from host
sudo mkdir /mnt/shared
sudo mount -t vboxsf SharedFolder /mnt/shared

# Auto-mount on boot
echo "SharedFolder /mnt/shared vboxsf defaults,uid=1000,gid=1000 0 0" | \
  sudo tee -a /etc/fstab

echo "Shared folder configured ✓"
```

---

## 📋 Tool Summary Table

| Category | Tool | Purpose | Install Method |
|---|---|---|---|
| Imaging | `dcfldd` | Forensic imaging + hashing | apt |
| Imaging | `ddrescue` | Recovery from damaged disks | apt |
| File System | `sleuthkit` | CLI forensic analysis suite | apt |
| File System | `autopsy` | GUI forensic suite | apt |
| Partition | `testdisk` | Partition + file recovery | apt |
| Carving | `foremost` | File signature carving | apt |
| Carving | `scalpel` | Configurable carving | apt |
| Carving | `photorec` | GUI carving (part of testdisk) | apt |
| Carving | `binwalk` | Firmware/embedded extraction | apt |
| NTFS | `ntfsundelete` | NTFS file recovery | part of ntfs-3g |
| ext4 | `extundelete` | ext4 file recovery | apt |
| ext4 | `ext4magic` | Advanced ext4 recovery | apt |
| Memory | `volatility3` | RAM dump analysis | pip/git |
| Analysis | `bulk_extractor` | Extract emails/URLs/hashes | apt |
| Metadata | `exiftool` | EXIF/metadata extraction | apt |
| Hashing | `hashdeep` | Hash sets for verification | apt |
| Hex | `xxd` / `hexedit` | Raw hex viewing/editing | apt |
| Registry | `regipy` | Windows registry parsing | pip |
| Event Logs | `python-evtx` | Windows .evtx parsing | pip |
| MFT | `analyzeMFT` | NTFS MFT deep parsing | pip |

---

## 🚀 Quick Start After Setup

```bash
# Every time you start a new investigation:
cd ~/forensics-lab

# 1. Create case directory
mkdir -p cases/case_$(date +%Y%m%d)/evidence

# 2. Image the media
sudo dcfldd if=/dev/sdX of=cases/case_$(date +%Y%m%d)/evidence/disk.img \
  hash=sha256 hashlog=cases/case_$(date +%Y%m%d)/evidence/hash.log bs=4096

# 3. Verify hash
sha256sum cases/case_$(date +%Y%m%d)/evidence/disk.img

# 4. Mount read-only
sudo mount -o ro,loop cases/case_$(date +%Y%m%d)/evidence/disk.img /mnt/evidence

# 5. Open Autopsy for GUI analysis
autopsy &
```

> [!success] Lab is Ready!
> Once all steps above are done, proceed to the Task files in order:
> - `Task-01` → Forensic Imaging & Hashing
> - `Task-02` → Disk & Storage Analysis
> - `Task-03` → File System Investigation
> - `Task-04` → Deleted File Recovery (FAT32)
> - `Task-05` → Deleted File Recovery (NTFS)
> - `Task-06` → Deleted File Recovery (ext4)
> - `Task-07` → Data Carving
> - `Task-08` → Formatted Partition Recovery
> - `Task-09` → OS Artifact Analysis
> - `Task-10` → Full Forensic Investigation Simulation
