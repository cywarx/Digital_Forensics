#!/bin/bash
# =============================================================================
# Forensic Practice Image Creation Script - The Devid Case (200MB)
# RUN WITH: sudo bash create_forensic_image.sh
# =============================================================================

set -e

echo "============================================================"
echo "  FORENSIC IMAGE CREATOR - THE Devid CASE (200MB)"
echo "============================================================"

# Clean up previous loop devices
sudo losetup -D 2>/dev/null || true

# Step 1: Create empty 200MB image file
echo "[*] Creating 200MB empty image..."
dd if=/dev/zero of=Devid_evidence.img bs=1M count=200 status=progress

# Step 2: Create MBR partition table and single FAT32 partition
echo "[*] Creating MBR partition table..."
fdisk Devid_evidence.img <<EOF
o
n
p
1

+195M
t
b
w
EOF

# Step 3: Setup loop device and format partition
echo "[*] Setting up loop device..."
LOOP_DEV=$(sudo losetup -f --show -P Devid_evidence.img)
echo "Loop device: $LOOP_DEV"

echo "[*] Formatting partition as FAT32 with label 'Devid_USB'..."
sudo mkfs.vfat -F 32 -n "Devid_USB" ${LOOP_DEV}p1

# Step 4: Mount partition
echo "[*] Mounting partition..."
MOUNT_DIR="/mnt/Devid_forensic"
sudo mkdir -p $MOUNT_DIR
sudo mount -o uid=$(id -u),gid=$(id -g),umask=000 ${LOOP_DEV}p1 $MOUNT_DIR

# =============================================================================
# Step 5: Create normal visible files
# =============================================================================
echo "[*] Creating normal user content..."

cat > $MOUNT_DIR/work_notes.txt << 'EOF'
Meeting Schedule - March 2024
------------------------------
10:00 AM - Client Call with Global Finance
02:00 PM - Team Sync (Q1 Targets)
04:30 PM - Review Offshore Accounts

Action Items:
- Transfer funds to account #8892
- Contact shadow.trader@protonmail.com
- Update ledger with March transactions
EOF

cat > $MOUNT_DIR/personal.txt << 'EOF'
Personal Reminders:
- Mom's birthday: April 15 (Buy gift)
- Dentist appointment: March 28, 11:30 AM
- Car service due: April 2
EOF

cat > $MOUNT_DIR/wifi_info.txt << 'EOF'
Network Credentials:
Home WiFi: MyHouse@2024
Office WiFi: Corp@Secure99
Coffee Shop: Guest123
EOF

# =============================================================================
# Step 6: Download nature image (waterfall/forest) with User-Agent
# =============================================================================
echo "[*] Downloading nature/waterfall image..."

# Try multiple reliable free image sources with proper User-Agent
if ! wget -q -U "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
     -O $MOUNT_DIR/vacation_photo.jpg \
     "https://images.pexels.com/photos/3225517/pexels-photo-3225517.jpeg?auto=compress&cs=tinysrgb&w=800" 2>/dev/null; then
    
    echo "[*] Trying alternative source..."
    # Alternative: Beautiful nature image from Pexels (waterfall)
    wget -q -U "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
         -O $MOUNT_DIR/vacation_photo.jpg \
         "https://images.pexels.com/photos/931007/pexels-photo-931007.jpeg?auto=compress&cs=tinysrgb&w=800" 2>/dev/null || {
        
        echo "[*] Creating local nature image using ImageMagick..."
        # Create a beautiful gradient nature-like image
        sudo apt-get install -y imagemagick 2>/dev/null || true
        convert -size 800x600 \
            -define gradient:angle=45 gradient:forestgreen-darkgreen \
            -fill white -pointsize 24 -gravity center \
            -annotate +0+0 "🌲 Nature Trail - March 2024 🌊" \
            $MOUNT_DIR/vacation_photo.jpg 2>/dev/null
    }
fi

echo "[*] Embedding GPS metadata into vacation_photo.jpg..."

# Install exiftool if not present
if ! command -v exiftool &> /dev/null; then
    echo "[*] Installing exiftool..."
    sudo apt-get update -qq && sudo apt-get install -y libimage-exiftool-perl 2>/dev/null || true
fi

# Embed complete GPS and device metadata
exiftool -overwrite_original \
    -GPSLatitude="19.0760" \
    -GPSLatitudeRef="N" \
    -GPSLongitude="72.8777" \
    -GPSLongitudeRef="E" \
    -GPSAltitude="14" \
    -GPSAltitudeRef="0" \
    -DateTimeOriginal="2024:03:15 14:23:45" \
    -CreateDate="2024:03:15 14:23:45" \
    -ModifyDate="2024:03:15 14:23:45" \
    -Make="Apple" \
    -Model="iPhone 14 Pro" \
    -Software="iOS 17.3.1" \
    -Artist="Devid" \
    -Copyright="Devid" \
    -ImageDescription="Weekend getaway near Lonavala waterfall" \
    -UserComment="Met with V.S. at the waterfall. Deal confirmed for March 25." \
    $MOUNT_DIR/vacation_photo.jpg 2>/dev/null

echo "    ✓ GPS: 19.0760 N, 72.8777 E (Lonavala/Mumbai region)"
echo "    ✓ Date/Time: 2024:03:15 14:23:45"
echo "    ✓ Device: Apple iPhone 14 Pro"
echo "    ✓ Description: Weekend getaway near Lonavala waterfall"
echo "    ✓ Comment: Met with V.S. at the waterfall. Deal confirmed for March 25."

# =============================================================================
# Step 7: Create files that will be DELETED
# =============================================================================
echo "[*] Creating files to be deleted..."

cat > $MOUNT_DIR/btc_transfer_record.txt << 'EOF'
==========================================
BITCOIN TRANSFER CONFIRMATION
==========================================
From: Devid
To: Binance Exchange (Crypto Wallet)
Amount: 2.5 BTC
Transaction ID: a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
Date: 2024-03-10 09:15:22 UTC
Wallet Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
Status: COMPLETED
IP Address: 185.243.112.87
==========================================
EOF

cat > $MOUNT_DIR/project_nightfall.txt << 'EOF'
==========================================
PROJECT NIGHTFALL - CONFIDENTIAL
==========================================
Meeting Location: Warehouse 42, Dock 7, Mumbai Port
Time: 11:30 PM, March 25, 2024
Attendees: D.K., V.S., R.M.
Agenda: Acquisition of FinTech Startup (Hostile Takeover)
Target: PaySecure India Pvt Ltd
Budget: $2,500,000
Insider Contact: insider.paysecure@protonmail.com
Access Code: NIGHTFALL2024
Payment Method: Untraceable Crypto (Monero)
==========================================
EOF

cat > $MOUNT_DIR/passwords_secure.txt << 'EOF'
==========================================
SECURE CREDENTIALS - DO NOT SHARE
==========================================
Bank Account (HDFC): Devid / Winter2026!
Bank Account (ICICI): DKumar / Mumbai@123
Email (Primary): Devid@protonmail.com / 7Hj9#kL2$mN8
Email (Backup): dkumar1985@gmail.com / BlueSky@2024
Crypto Wallet Seed: witch collapse practice feed shame open despair creek road again ice least
Server SSH: root@185.243.112.87:2222 / R3dL!0n2024#
VPN Credentials: user8432 / jF8$dK9#wP2
Encrypted Volume Password: MumbaiRains2024!
==========================================
EOF

cat > $MOUNT_DIR/offshore_ledger.txt << 'EOF'
==========================================
OFFSHORE ACCOUNT LEDGER - MARCH 2024
==========================================
Date       | Account         | Amount    | Status
-----------|-----------------|-----------|----------
2024-03-01 | ACC-9982-XYZ    | $25,000   | Received
2024-03-05 | ACC-7765-ABC    | $50,000   | Sent
2024-03-12 | ACC-9982-XYZ    | $75,000   | Received
2024-03-18 | ACC-1123-DEF    | $100,000  | Sent
2024-03-22 | ACC-9982-XYZ    | $45,000   | Pending
==========================================
Total Balance (ACC-9982-XYZ): $145,000
Bank: Cayman National Bank
SWIFT: CNBKYKYKXXX
==========================================
EOF

sync

# =============================================================================
# Step 8: Delete the suspicious files
# =============================================================================
echo "[*] Deleting suspicious files (traces remain for recovery)..."
rm $MOUNT_DIR/btc_transfer_record.txt
rm $MOUNT_DIR/project_nightfall.txt
rm $MOUNT_DIR/passwords_secure.txt
rm $MOUNT_DIR/offshore_ledger.txt

sync

# =============================================================================
# Step 9: Show visible files
# =============================================================================
echo ""
echo "[*] Visible files on drive:"
ls -la $MOUNT_DIR/

# =============================================================================
# Step 10: Unmount and cleanup
# =============================================================================
echo ""
echo "[*] Unmounting and cleaning up..."
sudo umount $MOUNT_DIR
sudo losetup -d $LOOP_DEV
sudo rmdir $MOUNT_DIR

# =============================================================================
# Step 11: Generate hash values
# =============================================================================
echo "[*] Generating hash values..."
md5sum Devid_evidence.img > Devid_evidence.md5.txt
sha256sum Devid_evidence.img > Devid_evidence.sha256.txt

# =============================================================================
# Step 12: Display summary
# =============================================================================
echo ""
echo "============================================================"
echo "  [✓] FORENSIC IMAGE CREATED SUCCESSFULLY!"
echo "============================================================"
echo ""
echo "Filename: Devid_evidence.img"
echo "Size: 200MB"
echo "Volume Label: Devid_USB"
echo "Partition: MBR, FAT32 (Offset: 2048 sectors)"
echo ""
echo "--- HASH VALUES ---"
cat Devid_evidence.md5.txt
echo ""
cat Devid_evidence.sha256.txt
echo ""
echo "--- FILES PRESENT (Visible) ---"
echo "  - work_notes.txt"
echo "  - personal.txt"
echo "  - wifi_info.txt"
echo "  - vacation_photo.jpg"
echo ""
echo "--- FILES DELETED (Recoverable) ---"
echo "  - btc_transfer_record.txt"
echo "  - project_nightfall.txt"
echo "  - passwords_secure.txt"
echo "  - offshore_ledger.txt"
echo ""
echo "--- GPS METADATA (vacation_photo.jpg) ---"
echo "  Location: 19.0760 N, 72.8777 E (Lonavala Waterfall, near Mumbai)"
echo "  Date/Time: 2024:03:15 14:23:45"
echo "  Device: Apple iPhone 14 Pro"
echo "  Description: Weekend getaway near Lonavala waterfall"
echo "  Comment: Met with V.S. at the waterfall. Deal confirmed for March 25."
echo ""
echo "============================================================"
echo "  COMMANDS TO ANALYZE THE IMAGE"
echo "============================================================"
echo ""
echo "# View partition layout:"
echo "  mmls Devid_evidence.img"
echo ""
echo "# List deleted files:"
echo "  fls -o 2048 -rd Devid_evidence.img"
echo ""
echo "# Recover deleted file:"
echo "  icat -o 2048 Devid_evidence.img <inode>"
echo ""
echo "# Mount and view metadata:"
echo "  sudo mkdir -p /mnt/analysis"
echo "  sudo mount -o ro,offset=\$((2048*512)) Devid_evidence.img /mnt/analysis"
echo "  exiftool /mnt/analysis/vacation_photo.jpg"
echo "  sudo umount /mnt/analysis"
echo ""
echo "============================================================"