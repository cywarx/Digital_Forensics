#!/bin/bash

set -e

IMG="pendrive.img"
SIZE_MB=500
MOUNT_DIR="./pendrive_mount"
LABEL="FRNSC500"
HASH_FILE="evidence.sha256"

echo "[0/8] Cleaning old setup..."
sudo umount "$MOUNT_DIR" 2>/dev/null || true
sudo losetup -D 2>/dev/null || true
rm -f "$IMG" "$HASH_FILE"
mkdir -p "$MOUNT_DIR"

echo "[1/8] Creating $SIZE_MB MB image..."
dd if=/dev/zero of="$IMG" bs=1M count=$SIZE_MB status=progress

echo "[2/8] Creating MBR partition..."
parted "$IMG" --script mklabel msdos
parted "$IMG" --script mkpart primary fat32 1MiB 100%

echo "[3/8] Attaching loop device (with partitions)..."
LOOP=$(sudo losetup -Pf --show "$IMG")
echo "     Loop device: $LOOP"

PART="${LOOP}p1"

# Wait until partition appears (important)
sleep 1

if [ ! -e "$PART" ]; then
    echo "❌ Partition not found: $PART"
    exit 1
fi

echo "[4/8] Formatting partition as FAT32..."
sudo mkfs.vfat -F 32 -n "$LABEL" "$PART"

echo "[5/8] Detaching loop device..."
sudo losetup -d "$LOOP"

echo "[6/8] Generating SHA256 hash..."
sha256sum "$IMG" | tee "$HASH_FILE"

echo ""
echo "[✔] Image created successfully!"
echo "    Image       : $IMG"
echo "    Mount point : $MOUNT_DIR"
echo "    Hash file   : $HASH_FILE"
echo ""

# =========================
# INTERACTIVE MOUNT
# =========================

read -p "👉 Mount image now? (y/N): " choice

if [[ "$choice" == "y" || "$choice" == "Y" ]]; then

    echo "[7/8] Attaching loop device again..."
    LOOP=$(sudo losetup -Pf --show "$IMG")
    PART="${LOOP}p1"

    sleep 1

    echo "[8/8] Mounting..."
    sudo mount -o uid=$(id -u),gid=$(id -g) "$PART" "$MOUNT_DIR"

    echo ""
    echo "[✔] Mounted successfully!"
    echo "    Device : $PART"
    echo "    Mount  : $MOUNT_DIR"
    echo ""
    echo "⚠️  Image is still mounted (intentional)"
    echo ""
    echo "👉 To unmount later:"
    echo "   sudo umount $MOUNT_DIR"
    echo "   sudo losetup -d $LOOP"

else
    echo ""
    echo "[ℹ️] Mount skipped."
    echo ""
    echo "👉 To mount manually:"
    echo ""
    echo "   sudo losetup -Pf --show $IMG"
    echo "   sudo mount -o uid=\$(id -u),gid=\$(id -g) /dev/loopXp1 $MOUNT_DIR"
    echo ""
fi
