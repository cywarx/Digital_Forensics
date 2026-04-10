#!/usr/bin/env python3
"""
HeXx Corp — Forensic Practice Image Creator (v3.0 STABLE)

✔ MBR partition (Autopsy compatible)
✔ FAT16 filesystem
✔ Robust offset detection (sfdisk JSON)
✔ Auto root privilege check
✔ Clean error handling

Run:
    sudo python3 pendrive.py
"""

import os, sys, subprocess, io, zipfile, json, shutil
from pathlib import Path

# ── root check ──────────────────────────────────────────────────
def require_root():
    if os.geteuid() != 0:
        print("❌ This script requires root privileges.")
        print("👉 Run with: sudo python3 pendrive.py")
        sys.exit(1)

# ── dependency check ─────────────────────────────────────────────
def check_deps():
    missing = []
    for cmd in ["dd","mkfs.fat","mcopy","mdel","sfdisk","losetup"]:
        if subprocess.run(["which",cmd], capture_output=True).returncode != 0:
            missing.append(cmd)

    try:
        from PIL import Image
    except ImportError:
        missing.append("pillow (pip install pillow)")

    if missing:
        print("❌ Missing dependencies:", ", ".join(missing))
        print("Install:")
        print("sudo apt install dosfstools mtools util-linux sleuthkit foremost")
        print("pip install pillow")
        sys.exit(1)

# ── file generator ───────────────────────────────────────────────
def make_files(out: Path):
    from PIL import Image, ImageDraw
    out.mkdir(parents=True, exist_ok=True)

    # visible image
    img = Image.new("RGB", (400, 300), (30, 60, 120))
    d = ImageDraw.Draw(img)
    d.text((60,100), "HeXx Corp", fill=(255,215,0))
    img.save(out/"employee_badge.jpg","JPEG")

    # secret image
    img2 = Image.new("RGB",(300,200),(10,10,10))
    d2 = ImageDraw.Draw(img2)
    d2.text((30,80),"TOP SECRET", fill=(255,0,0))
    img2.save(out/"secret_plan.png","PNG")

    # visible files
    (out/"readme.txt").write_text("Internal USB Drive\n")
    (out/"system.log").write_text("User accessed secret files\n")

    # deleted files
    (out/"secret_notes.txt").write_text("Password: Tr0j@n_H0rs3\n")
    (out/"flag.ctf").write_text("CTF{hexx_autopsy_fixed}\n")

    # zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z:
        z.writestr("data.txt","hidden info")
    (out/"project_files.zip").write_bytes(buf.getvalue())

    print("  ✅ Payload created")

# ── build image ─────────────────────────────────────────────────
def build_image(out_dir: Path, img_path="pendrive.img"):
    run = lambda cmd: subprocess.run(cmd, check=True, capture_output=True)

    print("\n[1/7] Creating blank image...")
    run(["dd","if=/dev/zero",f"of={img_path}","bs=1M","count=32","status=none"])

    print("[2/7] Creating MBR partition...")
    script = "label: dos\n,30M,6,*\n"
    subprocess.run(["sfdisk", img_path], input=script.encode(), check=True)

    print("[3/7] Reading partition offset...")
    data = json.loads(subprocess.check_output(["sfdisk","--json",img_path]))
    start_sector = data["partitiontable"]["partitions"][0]["start"]
    offset = start_sector * 512

    print(f"       Start sector: {start_sector}")
    print(f"       Offset: {offset}")

    print("[4/7] Attaching loop device...")
    loop = subprocess.check_output(
        ["losetup","-f","--show","-o",str(offset),img_path]
    ).decode().strip()

    print(f"       Loop device: {loop}")

    try:
        print("[5/7] Formatting FAT16...")
        run(["mkfs.fat","-F","16","-n","HEXX_USB", loop])

        print("[6/7] Writing files...")
        visible = ["readme.txt","employee_badge.jpg","system.log","project_files.zip"]
        deleted = ["secret_notes.txt","secret_plan.png","flag.ctf"]

        for f in visible:
            run(["mcopy","-i",loop,str(out_dir/f),f"::{f}"])
            print(f"       + {f}")

        for f in deleted:
            run(["mcopy","-i",loop,str(out_dir/f),f"::{f}"])

        for f in deleted:
            run(["mdel","-i",loop,f"::{f}"])
            print(f"       🗑 {f}")

    finally:
        print("[7/7] Detaching loop device...")
        subprocess.run(["losetup","-d",loop])

    print("\n✔ Image created successfully!")

# ── summary ─────────────────────────────────────────────────────
def summary(img):
    print("\n===== FORENSIC IMAGE READY =====")
    print(f"Image: {img}")
    print("FS   : FAT16 (MBR partitioned)")
    print("""
VISIBLE FILES:
  readme.txt
  employee_badge.jpg
  system.log
  project_files.zip

DELETED FILES:
  secret_notes.txt
  secret_plan.png
  flag.ctf

TEST COMMANDS:
  fls pendrive.img
  fls -d pendrive.img
  icat pendrive.img 3
  foremost -i pendrive.img -o out/
""")

# ── main ────────────────────────────────────────────────────────
if __name__ == "__main__":
    require_root()

    IMG = "pendrive.img"
    TMP = Path("_tmp_payload")

    print("HeXx Forensic Image Creator v3.0\n")

    check_deps()
    make_files(TMP)
    build_image(TMP, IMG)
    summary(IMG)

    shutil.rmtree(TMP, ignore_errors=True)
