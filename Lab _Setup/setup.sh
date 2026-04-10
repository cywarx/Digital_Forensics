#!/bin/bash
# CYWARX CTF — Forensics Toolchain Installer
# Works on both Kali Linux and Ubuntu

set -e

# Detect distro
if grep -qi kali /etc/os-release 2>/dev/null; then
    DISTRO="kali"
else
    DISTRO="ubuntu"
fi

echo "[*] Detected: $DISTRO"

sudo apt update -y

# ── Core packages (same name on both) ─────────────────────
sudo apt install -y \
    sleuthkit \
    autopsy \
    testdisk \
    foremost \
    scalpel \
    dcfldd \
    parted \
    gparted \
    ntfs-3g \
    exfatprogs \
    extundelete \
    ext4magic \
    fatcat \
    mtools \
    dosfstools \
    util-linux \
    e2fsprogs

# ── ddrescue: different package name per distro ────────────
if [ "$DISTRO" = "kali" ]; then
    sudo apt install -y gddrescue 2>/dev/null || \
    sudo apt install -y ddrescue  2>/dev/null || \
    echo "[!] ddrescue not found — skip"
else
    # Ubuntu: gddrescue provides the ddrescue binary
    sudo apt install -y gddrescue 2>/dev/null || \
    echo "[!] gddrescue not found — skip"
fi

# ── gpart: not in Ubuntu repos, skip gracefully ───────────
sudo apt install -y gpart 2>/dev/null || \
    echo "[!] gpart not available on this distro — skip"

# ── exiftool: different package name per distro ────────────
if [ "$DISTRO" = "kali" ]; then
    sudo apt install -y exiftool 2>/dev/null || \
    sudo apt install -y libimage-exiftool-perl 2>/dev/null || \
    echo "[!] exiftool not found — skip"
else
    sudo apt install -y libimage-exiftool-perl 2>/dev/null || \
    echo "[!] exiftool not found — skip"
fi

echo ""
echo "Disk tools installed ✓"
echo ""

# ── Quick verify ───────────────────────────────────────────
echo "[*] Verifying key binaries:"
for bin in mmls fls icat autopsy testdisk foremost dcfldd mkfs.fat mkfs.ext4 losetup sfdisk exiftool fatcat; do
    if command -v "$bin" &>/dev/null; then
        echo "  [+] $bin"
    else
        echo "  [!] $bin — NOT FOUND"
    fi
done
