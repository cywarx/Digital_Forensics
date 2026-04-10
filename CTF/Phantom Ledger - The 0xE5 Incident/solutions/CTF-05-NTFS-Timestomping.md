---
tags: [ctf, solution, unit4, forensics, ntfs, mft, timestomping, istat]
challenge: "05 — The MFT Never Forgets (ntfs_evidence.img)"
flag: "Cywarx{t1m3st0mp_09}"
points: 150
difficulty: Medium
topic: NTFS MFT & Timestomping
image: ctf1.img → /mnt/p2/ntfs_evidence.img
---

# 🗂️ Challenge 05 — The MFT Never Forgets

> [!success] Flag
> `Cywarx{t1m3st0mp_09}`

> [!info] Real World Case — WannaCry (2017)
> WannaCry investigators used MFT timestamp analysis to determine the true installation time of ransomware components. Attackers had used timestomping to make malware appear as a system file from 2009. The `$FILE_NAME` attribute exposed the real installation: May 12, 2017. This attribution technique directly led to the North Korea indictment.

---

## 📋 Challenge Summary

`ntfs_evidence.img` is an NTFS disk image found on the suspect's USB. It contains a deleted file — `keylogger.exe` — whose timestamps have been **faked** using timestomping. NTFS stores **two separate timestamp sets** — find the one the attacker couldn't change to get the real creation time.

**File:** `/mnt/p2/ntfs_evidence.img` (after mounting P2)

---

## 🧠 Concept — NTFS Dual Timestamps

NTFS stores timestamps in **two separate MFT attributes**:

| Attribute | Who controls it | Can attacker modify? |
|-----------|----------------|---------------------|
| `$STANDARD_INFORMATION` | Writable via Windows API (SetFileTime) | **YES** — easily |
| `$FILE_NAME` | Written only by NTFS kernel driver | **NO** — requires kernel access |

> [!warning] Timestomping
> Attackers use tools like `timestomp.exe` or Metasploit's `timestomp` module to change `$STANDARD_INFORMATION` timestamps. This hides when malware was really installed.
> **Detection:** Compare both attributes. If they disagree → timestomping occurred.

---

## 🔍 Method 1 — Mount nested image + istat

### Step 1: Mount P2 to access ntfs_evidence.img

```bash
sudo losetup -P /dev/loop0 ctf1.img
sudo kpartx -av /dev/loop0
sudo mkdir -p /mnt/p2
sudo mount /dev/mapper/loop0p2 /mnt/p2
ls /mnt/p2/
```

### Step 2: List files in ntfs_evidence.img

```bash
fls -r /mnt/p2/ntfs_evidence.img
```

**Output:**
```
r/r 3-128-1: $MFT
r/r * 4-128-1: keylogger.exe
d/d 5-144-4: $OrphanFiles
```

The `*` means `keylogger.exe` is **deleted**.

### Step 3: Get the inode of keylogger.exe

```bash
fls -r -d /mnt/p2/ntfs_evidence.img
```

**Output:**
```
r/r * 4-128-1:  keylogger.exe
```

Inode: `4-128-1`

### Step 4: Read full MFT entry with istat

```bash
istat /mnt/p2/ntfs_evidence.img 4
```

**Output:**
```
MFT Entry Header Values:
Entry: 4        Sequence: 2
$LogFile Sequence Number: 0
Allocated Size: 0         Actual Size: 0
Flags: Not in Use  ← DELETED

$STANDARD_INFORMATION Attribute Values:
Created:  2020-01-01 00:00:00 (UTC)   ← FAKE (timestomped!)
File Modified:  2020-01-01 00:00:00 (UTC)   ← FAKE
MFT Modified:   2020-01-01 00:00:00 (UTC)   ← FAKE
File Accessed:  2020-01-01 00:00:00 (UTC)   ← FAKE

$FILE_NAME Attribute Values:
Created:  2024-03-17 09:22:41 (UTC)   ← REAL (kernel-protected)
File Modified:  2024-03-17 09:22:41 (UTC)   ← REAL
MFT Modified:   2024-03-17 09:22:41 (UTC)   ← REAL
File Accessed:  2024-03-17 09:22:41 (UTC)   ← REAL

Attributes:
Type: $STANDARD_INFORMATION (16-0)    Name: N/A  Resident
Type: $FILE_NAME (48-3)               Name: N/A  Resident
```

> [!tip] Reading the output
> - `$STANDARD_INFORMATION` shows `2020-01-01 00:00:00` — a suspicious round date. Real file creation never lands on exactly midnight Jan 1st.
> - `$FILE_NAME` shows `2024-03-17 09:22:41` — matches exactly when the theft was committed.
> - **Technique used: Timestomping**
> - **Real creation hour: 09**

### Step 5: Assemble the flag

```
Technique (leet): t1m3st0mp
Real hour (24h):  09
Flag: Cywarx{t1m3st0mp_09}
```

---

## 🔍 Method 2 — strings quick check

```bash
strings /mnt/p2/ntfs_evidence.img | grep -iE "fake|real|Flag|timestamp"
```

**Output:**
```
NTFS Forensics - keylogger.exe (deleted)
$STANDARD_INFORMATION (FAKE timestomped):
  2020-01-01 00:00:00
$FILE_NAME (REAL kernel-protected):
  2024-03-17 09:22:41
Technique: timestomping  Real hour: 09
Flag: t1m3st0mp_09
```

---

## 🔍 Method 3 — analyzeMFT (comprehensive MFT parse)

```bash
pip3 install analyzeMFT --break-system-packages

# Extract $MFT from ntfs_evidence.img
icat /mnt/p2/ntfs_evidence.img 0 > /tmp/MFT

# Parse and output to CSV
analyzeMFT.py -f /tmp/MFT -o /tmp/mft_parsed.csv

# Look at timestamps
grep -i "keylogger" /tmp/mft_parsed.csv
```

---

## 🔍 Method 4 — Autopsy (GUI)

```
1. In Autopsy, add ntfs_evidence.img as a new data source
2. Go to Deleted Files
3. Right-click keylogger.exe → File Metadata
4. Compare $SI Created vs $FN Created
5. Note the 2020-01-01 vs 2024-03-17 discrepancy
```

---

## 🔬 Key Concepts

> [!note] MACE Timestamps
> Every NTFS file has 4 timestamps in EACH attribute:
> - **M**odified — file content last changed
> - **A**ccessed — file last opened/read
> - **C**hanged — MFT entry metadata changed
> - **E**ntry Modified — $FILE_NAME updated
>
> Timestomping tools typically change all 4 in `$STANDARD_INFORMATION` but leave `$FILE_NAME` intact.

> [!note] Round-number red flag
> Timestamps of exactly `00:00:00` on `January 1st` of a suspiciously old year are a near-certain indicator of timestomping. Real file creation always has non-zero seconds and non-trivial times.

> [!warning] Detection limitation
> Advanced attackers can modify `$FILE_NAME` timestamps if they have kernel-level access (rootkit). In that case, use the `$LogFile` journal and `$UsnJrnl` change journal for corroboration.

---

## 🔗 Related Challenges
- [[CTF-03-Deleted-kl-log]] — FAT32 deleted file recovery
- [[CTF-08-RAM-Volatile-Data]] — RAM volatile evidence
