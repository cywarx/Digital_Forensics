---
title: "Chain of Custody — Complete Digital Forensics Guide"
course: "Post Graduate Diploma in Cyber Security and Law"
university: "University of Delhi"
subject: "Digital Forensics & Cyber Law"
tags:
  - chain-of-custody
  - digital-forensics
  - evidence
  - forensics
  - cyber-law
  - paper-204
  - cywarx
  - evidence-handling
  - DFIR
created: 2025-01-01
status: complete
type: study-note
---

# 🔗 Chain of Custody — The Complete Guide

> [!quote] 
> *"Evidence is only as strong as the integrity of its journey — from crime scene to courtroom."*

---

## 🗂️ Table of Contents

- [[#What is Chain of Custody?]]
- [[#Why Chain of Custody Matters]]
- [[#The Four Pillars of Chain of Custody]]
- [[#Step-by-Step Chain of Custody Process]]
  - [[#Step 1 — Identification]]
  - [[#Step 2 — Collection]]
  - [[#Step 3 — Packaging & Labelling]]
  - [[#Step 4 — Transportation]]
  - [[#Step 5 — Storage & Preservation]]
  - [[#Step 6 — Examination & Analysis]]
  - [[#Step 7 — Reporting]]
  - [[#Step 8 — Presentation in Court]]
  - [[#Step 9 — Return, Archive or Disposal]]
- [[#Chain of Custody Form — Complete Template]]
- [[#Timeline of a Chain of Custody — Real Case Example]]
- [[#Digital vs Physical Evidence — CoC Differences]]
- [[#Common Mistakes That Break Chain of Custody]]
- [[#Hash Values — The Digital Seal]]
- [[#Legal Framework — Chain of Custody in India]]
- [[#International Standards & Guidelines]]
- [[#Quick Revision Summary]]

---

## What is Chain of Custody?

### 🟢 Simple Explanation

> [!abstract] Think of it like this…
> Imagine a **murder weapon** — a knife — is found at a crime scene. From the moment it is picked up by the first officer, every single person who **touches, moves, examines, or stores** that knife must be **recorded**. If even one person handles it without being recorded, a defence lawyer can say: *"How do we know someone didn't plant evidence or tamper with the knife between Person A and Person B?"* — and the case could collapse.
>
> **Chain of Custody** is that complete, unbroken record.

### 📖 Formal Definition

> **Chain of Custody (CoC)** is the **chronological documentation** and **logical sequence of custody, control, transfer, analysis, and disposition** of physical or electronic evidence — from the moment of collection at the scene to its final presentation in court — ensuring that the evidence has not been **altered, tampered, or contaminated** at any point.

### 🔑 Key Terms

| Term | Meaning |
|---|---|
| **Custodian** | Person currently responsible for and in possession of the evidence |
| **Continuity of Evidence** | Unbroken record showing evidence was not tampered |
| **Integrity** | Evidence is exactly as it was when collected |
| **Provenance** | Origin and history of the evidence |
| **Exhibit Number** | Unique ID assigned to each piece of evidence |
| **Hash Value** | Digital fingerprint proving a file hasn't changed |
| **Forensic Image** | Bit-for-bit copy of digital storage media |
| **Write Blocker** | Device preventing any modification to original digital media |

---

## Why Chain of Custody Matters

### 🎯 Three Core Reasons

> [!important] 1. Legal Admissibility
> Courts will **reject evidence** if the chain of custody is broken or questionable. It doesn't matter how incriminating the evidence is — if you cannot prove it wasn't tampered with, it's inadmissible.
>
> → **BSA 2023 (Section 63)** and **IEA Section 65B** require proof of integrity for electronic evidence.

> [!important] 2. Preventing Evidence Tampering
> A documented chain ensures that **no one can secretly alter, add, or remove** evidence without it being detected. Every transfer is a checkpoint.

> [!important] 3. Credibility in Court
> A well-documented chain of custody gives the **prosecution credibility**. It proves the investigation was conducted **professionally and lawfully** — making the evidence more persuasive to a judge or jury.

### 💀 What Happens When CoC Fails?

> [!danger] Real Consequences of Broken Chain of Custody
>
> **Scenario:** An investigator collects a laptop from a suspect's office, takes it home for the weekend "to work on it," and then brings it to the forensic lab Monday.
>
> **Problem:** No record of who had access to the laptop over the weekend. Defence argues data could have been planted.
>
> **Court Result:** Evidence excluded. Case weakened or dismissed.

> [!example] Famous Example — O.J. Simpson Trial (1995)
> **Blood evidence** was found at the crime scene and on Simpson's property. However, defence attorneys successfully argued that:
> - Blood samples were mishandled
> - Vials were not properly sealed
> - Gaps existed in the chain of custody
>
> Result: "Reasonable doubt" created about the blood evidence — a major factor in the acquittal.
> **Lesson:** No matter how strong the evidence, a broken CoC can destroy a case.

---

## The Four Pillars of Chain of Custody

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHAIN OF CUSTODY                             │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │              │  │              │  │              │  │              │ │
│  │    WHO? 👤   │  │   WHAT? 📦   │  │   WHEN? 🕐   │  │   WHERE? 📍  │ │
│  │              │  │              │  │              │  │              │ │
│  │  Every person│  │  Description │  │  Exact date  │  │  Location of │ │
│  │  who handles │  │  of evidence │  │  and time of │  │  each custody│ │
│  │  the evidence│  │  at each step│  │  each action │  │  transfer    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

| Pillar | Question | Example |
|---|---|---|
| **WHO** | Which person took custody? | Inspector Rajesh Kumar, Badge #4521 |
| **WHAT** | What exactly is the evidence? | Samsung laptop, S/N: ABC123456, 512GB SSD |
| **WHEN** | Date and time of each transfer? | 14-Jan-2025, 14:32 hours |
| **WHERE** | Where was it transferred to/from? | Crime scene → Police Station Evidence Room |

---

## Step-by-Step Chain of Custody Process

> [!note] Overview — 9 Stages of Chain of Custody
```
INCIDENT/CRIME
     ↓
[1] IDENTIFICATION → Recognize potential evidence
     ↓
[2] COLLECTION → Collect without contaminating
     ↓
[3] PACKAGING & LABELLING → Seal, tag, document
     ↓
[4] TRANSPORTATION → Secure transfer to lab/storage
     ↓
[5] STORAGE & PRESERVATION → Controlled environment
     ↓
[6] EXAMINATION & ANALYSIS → Forensic analysis
     ↓
[7] REPORTING → Detailed forensic report
     ↓
[8] PRESENTATION IN COURT → Admissible evidence
     ↓
[9] RETURN / ARCHIVE / DISPOSAL → Final disposition
```

---

## Step 1 — Identification

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> This is where you **recognize** what counts as evidence at the scene. Not everything at a crime scene is evidence — you need to identify what is **relevant** to the case.
>
> Think of it like arriving at a restaurant after a food poisoning incident. The chef's phone (showing supplier communications), the kitchen logs, the leftover food — these are evidence. The restaurant's wall paintings are not.

### 📋 What to Identify

| Category | Digital Evidence Examples | Physical Evidence Examples |
|---|---|---|
| **Computing Devices** | Laptops, desktops, servers | Hard drives, USB drives, CDs |
| **Mobile Devices** | Smartphones, tablets, smartwatches | SIM cards, memory cards |
| **Network Devices** | Routers, switches, firewalls | Network cables, access point |
| **Storage Media** | External HDDs, NAS, cloud accounts | Backup tapes, optical discs |
| **Documents** | Emails, chat logs, transaction records | Printed documents, handwritten notes |
| **Accounts & Credentials** | Login sessions, browser history | Written passwords, sticky notes |
| **Logs** | System logs, access logs, CCTV footage | Physical visitor registers |

### 🔑 Rules at Identification Stage

> [!warning] Golden Rules — Do NOT Touch Yet!
> 1. **PHOTOGRAPH the scene first** — before touching anything
> 2. **SKETCH the layout** — document positions of all devices
> 3. **NOTE the state** — is the laptop open/closed? Screen on/off? What's displayed?
> 4. **DO NOT turn off** a running computer (volatile data in RAM will be lost)
> 5. **ISOLATE the network** — disconnect from internet (prevent remote wipe) but don't turn off
> 6. **CHECK for encryption** — is BitLocker/FileVault active? (if on, preserve power if possible)

> [!example] Real Scenario
> **Case:** Online banking fraud. Investigators arrive at suspect's house.
>
> **At Scene:**
> - Desktop computer (running — screen shows bank portal logged in) → IDENTIFY as primary evidence
> - Mobile phone on desk → IDENTIFY as evidence
> - Router (showing active connections) → IDENTIFY as evidence
> - Notebook with written passwords → IDENTIFY as physical evidence
> - A TV in the room → NOT evidence (irrelevant)
>
> **Action:** Photograph everything before touching. Note that desktop is running and logged in to banking portal — this is volatile evidence (RAM may contain passwords/session tokens).

### 📸 Documentation at Identification Stage

> [!note] What to Document
> - **Time** of arrival at scene (exact)
> - **Names** of all persons present
> - **Overall scene photos** (wide-angle, then close-up)
> - **Status of each device** (on/off/standby, screen content)
> - **Physical condition** (any damage, dust patterns indicating device was moved)
> - **Sketch of scene** with measurements

---

## Step 2 — Collection

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> You've identified the evidence. Now you **physically collect** it — but in a way that does **not alter, contaminate, or damage** it. This is the most critical step because mistakes here cannot be undone.

### 🔑 Collection Principles

> [!important] The Cardinal Rule of Collection
> **The original evidence must NEVER be altered.**
> For digital evidence: always work on a **forensic copy (image)** — never on the original.

### 📱 Digital Evidence Collection — Device by Device

#### 💻 For Running Computers (Live Acquisition)

```
COMPUTER IS RUNNING
        ↓
DO NOT TURN OFF (volatile data in RAM!)
        ↓
LIVE ACQUISITION:
  Step 1: Photograph screen (document running processes, open files)
  Step 2: Collect volatile data FIRST:
            → RAM dump (using Belkasoft RAM Capturer / WinPMEM)
            → Running processes list
            → Network connections (netstat)
            → Open files
            → Logged-in users
            → System time (compare with actual time — note discrepancy)
  Step 3: Take forensic image of hard drive (using FTK Imager / dd)
  Step 4: Calculate and document HASH values (MD5 + SHA-256)
  Step 5: Power off AFTER volatile data collected
```

> [!example] Why RAM Matters — Real Example
> **Case:** Ransomware attack on a company. The ransomware was running in RAM and encrypted files using a key stored ONLY in RAM.
>
> If investigators turned off the computer without RAM dump → **encryption key lost forever** → files permanently unrecoverable.
>
> By doing a **live RAM acquisition first** → key recovered from RAM → all files decrypted → suspect identified.

---

#### 💻 For Powered-Off Computers (Dead Acquisition)

```
COMPUTER IS OFF
        ↓
DO NOT TURN ON
        ↓
DEAD ACQUISITION:
  Step 1: Document physical condition (photograph)
  Step 2: Open case (if needed) — photograph internal layout
  Step 3: Remove storage drive
  Step 4: Connect drive to WRITE BLOCKER
  Step 5: Create forensic image (bit-for-bit copy)
            → Tools: FTK Imager, Autopsy, dd (Linux)
  Step 6: Calculate HASH of original drive
  Step 7: Calculate HASH of forensic image
  Step 8: COMPARE hashes — must be IDENTICAL
  Step 9: All further analysis on IMAGE only — original drive sealed
```

> [!info] What is a Write Blocker?
> A **hardware or software device** that allows you to read data from a storage device WITHOUT writing anything to it. Like a one-way valve.
>
> Without it: simply connecting a drive to a computer can modify timestamps, swap files — contaminating evidence.
>
> Types: Tableau T8-R2, WiebeTech, CRU Forensics write blockers (hardware)

---

#### 📱 For Mobile Phones

```
MOBILE PHONE FOUND
        ↓
IS IT LOCKED OR UNLOCKED?
        ↓
If UNLOCKED: Photograph screen immediately; enable Airplane Mode
If LOCKED: DO NOT attempt to unlock; place in Faraday bag
        ↓
FARADAY BAG (critical for mobiles):
  → Blocks all wireless signals (cellular, WiFi, Bluetooth)
  → Prevents remote wipe commands from reaching the device
  → Prevents new data (messages/calls) from being received
        ↓
ACQUISITION OPTIONS:
  → Logical Extraction (contacts, messages, apps — limited)
  → Physical Extraction (bit-for-bit — requires unlock or exploit)
  → JTAG/Chip-off (for locked/damaged phones — hardware level)
        ↓
Tools: Cellebrite UFED, Oxygen Forensic, MOBILedit
```

> [!danger] Common Mistake with Phones
> Investigator puts phone in evidence bag WITHOUT a Faraday bag. The suspect's accomplice sends a **remote wipe command** to the phone. All data erased.
>
> **Always use a Faraday bag for mobile devices immediately.**

---

#### 🌐 For Network Devices (Routers/Switches)

> [!note] Collection Steps
> 1. **Photograph** all connections (cables, ports, indicator lights)
> 2. **Do NOT power off** immediately — capture running configuration first
> 3. **Capture ARP tables, routing tables, active sessions** (if possible with network admin)
> 4. **Photograph/note** MAC addresses of connected devices
> 5. **Seize** the device after documentation
> 6. Preserve **DHCP logs, firewall logs** separately from ISP/admin if available

---

#### ☁️ For Cloud Evidence

> [!important] Cloud Evidence — Special Considerations
> Cloud evidence is **not physical** — you cannot "seize" AWS or Google's servers.
>
> **Methods:**
> - **Legal hold / preservation request** to cloud provider (via court order)
> - **API-based collection** (export of data from Google Workspace, Microsoft 365)
> - **Account capture** with consent (if account owner cooperates)
> - **Platform law enforcement portal** (Google LERS, Meta LEP, Apple LEA portal)
>
> **Key Issue:** Cloud data may be stored in **multiple countries** — jurisdictional complexity.

### 🧤 Physical Collection Rules

> [!tip] Basic Physical Handling
> - **Wear gloves** — prevent fingerprint contamination AND electrostatic damage
> - **Use anti-static bags** for storage media (prevent static discharge killing the drive)
> - **Do not bend** flexible media (SD cards, tapes)
> - **Handle by edges** — fingerprints can overwrite latent prints on device

---

## Step 3 — Packaging & Labelling

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> After collecting the evidence, you **seal it, label it, and document it** so that anyone looking at it later knows exactly what it is, who collected it, when, and where. This creates the first link in the chain.

### 📦 Packaging Requirements

| Evidence Type | Packaging | Reason |
|---|---|---|
| **Hard drives, USB drives** | Anti-static evidence bag | Prevent static damage |
| **Mobile phones** | Faraday bag → then evidence bag | Block signals + seal |
| **CDs/DVDs** | Paper envelope → rigid case | Prevent scratches |
| **Printed documents** | Clear plastic sleeve → evidence envelope | Preserve fingerprints, prevent degradation |
| **Entire computer** | Sealed evidence bag or taped box | Prevent access |
| **RAM sticks** | Anti-static bag | Static sensitive |

### 🏷️ Evidence Label — What Must Be on Every Label?

> [!important] Mandatory Label Fields
> Every piece of evidence MUST have a label with:
>
> ```
> ┌─────────────────────────────────────────────────┐
> │            EVIDENCE LABEL                       │
> ├─────────────────────────────────────────────────┤
> │ CASE NUMBER     : CY/2025/DEL/0047              │
> │ EXHIBIT NUMBER  : EX-03                         │
> │ DESCRIPTION     : Samsung Laptop, Black, 15"    │
> │                   Model: NP550XDA               │
> │                   Serial No: S123456789          │
> │ COLLECTED BY    : Insp. Rajesh Kumar (ID: 4521) │
> │ DATE & TIME     : 14-Jan-2025 | 14:32 hrs       │
> │ LOCATION        : Room 203, ABC Towers, Delhi    │
> │ CONDITION       : Powered ON, screen active      │
> │ HASH (SHA-256)  : a3f1d9...c4b2e7               │
> │ SEAL NUMBER     : SL-78432                       │
> └─────────────────────────────────────────────────┘
> ```

### 🔒 Sealing

> [!note] How to Seal Evidence
> 1. Place evidence in appropriate bag/container
> 2. **Sign across the seal** — so tampering is visible (signature breaks if opened)
> 3. Apply **tamper-evident tape** or **official evidence seal stickers**
> 4. **Record the seal number** on the CoC form
> 5. Photograph the sealed evidence with label visible
>
> If the seal is broken at any point → **must be documented**: who broke it, why, when, and re-sealed with new seal number recorded.

---

## Step 4 — Transportation

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> Moving evidence from the collection site (crime scene) to the forensic lab or evidence storage. Every person who handles it during transport must be documented. Think of it like a **registered parcel with tracking** — except for evidence, tracking is mandatory and legal.

### 🚗 Transportation Rules

> [!warning] Rules During Transport
> 1. **Minimum number of handlers** — fewer people = fewer links in chain = less risk
> 2. **Direct route** — no unnecessary stops or detours
> 3. **No personal stops** (no stopping at home, restaurants etc. with evidence in vehicle)
> 4. **Locked and secured** — evidence must be in a locked container or secure vehicle compartment
> 5. **Temperature sensitive** — some media degrades in heat; avoid extreme temperatures
> 6. **No magnetic fields** — keep hard drives away from speakers, magnets
> 7. **Signed handover** — when transferring from one person to another

### 📋 Handover Documentation

> [!note] Every Transfer = A New CoC Entry
> When evidence moves from Person A to Person B, BOTH must sign:
>
> ```
> TRANSFER RECORD
> ───────────────
> Transferred FROM : Insp. Rajesh Kumar
> Transferred TO   : Forensic Analyst Priya Sharma
> Date & Time      : 14-Jan-2025, 17:45 hrs
> Location         : CFSL New Delhi, Evidence Reception
> Seal Intact?     : YES — Seal No. SL-78432 verified
> Condition        : Same as collected
> Purpose          : Forensic examination
>
> Signature (From) : ______________
> Signature (To)   : ______________
> ```

---

## Step 5 — Storage & Preservation

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> Evidence that isn't being actively examined must be **stored safely** — in conditions that prevent physical degradation AND unauthorized access. Think of it like a **bank vault for evidence** — controlled, logged, and secure.

### 🏛️ Evidence Storage Requirements

| Requirement | Standard | Why |
|---|---|---|
| **Access control** | Only authorized personnel | Prevents tampering |
| **Temperature** | 15°C–25°C for electronics | Heat damages storage media |
| **Humidity** | 30%–55% RH | High humidity corrodes circuits |
| **No magnetic fields** | Away from large machinery | Magnetic fields corrupt hard drives |
| **Physical security** | Locked evidence room with access log | Unauthorized access prevention |
| **Separate storage** | Each case's evidence separated | Cross-contamination prevention |
| **Log every entry** | Name, time, purpose for every access | CoC continuity |

### 📋 Evidence Log Book — Storage Access Record

> [!example] Evidence Room Log Entry
> ```
> EVIDENCE ROOM ACCESS LOG — Case: CY/2025/DEL/0047
> ──────────────────────────────────────────────────
> Date    : 16-Jan-2025
> Time In : 09:15 hrs
> Person  : Forensic Analyst Priya Sharma (ID: FSL-221)
> Purpose : Retrieve Exhibit EX-03 (Samsung Laptop) for analysis
> Seal    : Verified intact — Seal No. SL-78432
> Witness : SI Mohan Das (ID: 3892)
>
> Time Out: 18:30 hrs
> Return  : Exhibit EX-03 returned, re-sealed, New Seal No: SL-79001
> Condition: Unchanged
>
> Signature: ______________ (Analyst)
> Signature: ______________ (Custodian)
> ```

### 💾 Long-Term Digital Evidence Preservation

> [!tip] Digital Preservation Challenges
> - **Media degradation** — hard drives fail; optical discs degrade over time
> - **Format obsolescence** — floppy disks, certain proprietary formats become unreadable
> - **Bit rot** — data corruption over time even in stored media
>
> **Solutions:**
> - Store on **multiple media types** (HDD + optical + tape)
> - **WORM (Write Once Read Many)** drives for forensic images
> - Regularly **verify hash values** — if hash changes, corruption detected
> - **Migrate** to newer formats before old ones become obsolete
> - Store forensic images on **evidence-grade NAS** with RAID

---

## Step 6 — Examination & Analysis

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> The forensic expert **analyses the evidence** to find what happened. Crucially, all analysis is done on a **forensic copy** — never the original. This is like a scientist analysing a copy of a DNA sample while keeping the original locked away.

### 🔬 Examination Process

```
EXAMINATION BEGINS
        ↓
VERIFY: Confirm seal intact before opening
        ↓
DOCUMENT: Photograph evidence before starting
        ↓
HASH VERIFICATION:
  → Calculate hash of original (should match collection hash)
  → If hashes DON'T match → STOP → document discrepancy → notify
        ↓
CREATE WORKING COPY:
  → Forensic image (FTK Imager / dd)
  → Verify image hash = original hash
  → Work ONLY on the image
        ↓
ANALYSIS:
  → File system analysis
  → Deleted file recovery
  → Email / chat recovery
  → Browser history
  → Registry analysis (Windows)
  → Timeline analysis
  → Keyword searches
  → Metadata extraction
        ↓
DOCUMENT ALL FINDINGS:
  → Screenshot every finding with timestamp
  → Note tool version, settings used
  → Note analyst name, date, time of each action
        ↓
RE-SEAL original evidence with new seal number
        ↓
REPORT writing begins
```

### 🔑 During Examination — Documentation

> [!important] Examiner's Notebook / Analysis Log
> Every analyst must maintain a log during examination:
>
> ```
> EXAMINATION LOG — Exhibit EX-03
> ─────────────────────────────────────────────
> Analyst    : Priya Sharma (FSL-221)
> Date       : 16-Jan-2025
> Start Time : 09:30 hrs
>
> 09:30 — Seal SL-78432 verified intact. Photographed.
> 09:35 — Seal broken. Original drive (WD 500GB, SN:WD45678) removed.
> 09:40 — Drive connected to Tableau T8-R2 write blocker.
> 09:45 — FTK Imager v4.7 used to create forensic image.
>          Image saved to: /cases/CY2025DEL0047/EX03.E01
> 10:15 — Image creation complete.
>          Original MD5  : 3d4e7f... [recorded]
>          Image MD5     : 3d4e7f... [MATCH ✅]
> 10:20 — Original drive re-sealed. New Seal No: SL-79001.
> 10:25 — Analysis commenced on image using Autopsy v4.21
> ...
> ```

---

## Step 7 — Reporting

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> The forensic analyst writes a **formal report** documenting everything found, how it was found, and what tools were used. This report will be presented in court. Think of it like a **doctor's medical report** — precise, factual, no opinions beyond expertise.

### 📄 Forensic Report Structure

> [!note] Standard Forensic Report Sections

```
1. EXECUTIVE SUMMARY
   → Brief overview of findings for non-technical readers

2. CASE INFORMATION
   → Case number, exhibit numbers, dates

3. ANALYST DETAILS
   → Name, qualifications, certifications

4. SCOPE OF EXAMINATION
   → What was examined; what was NOT examined

5. METHODOLOGY
   → Tools used (name + version), procedures followed

6. HASH VERIFICATION
   → Proof that evidence integrity was maintained

7. FINDINGS
   → Detailed factual findings (files, emails, browser history, etc.)
   → With timestamps and screenshots

8. TIMELINE ANALYSIS
   → Chronological sequence of events found in evidence

9. CONCLUSIONS
   → Expert opinion based on findings

10. LIMITATIONS
    → What could not be determined; what data was inaccessible

11. APPENDICES
    → Tool outputs, screenshots, hash certificates
```

---

## Step 8 — Presentation in Court

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> The chain of custody documentation and forensic findings are presented in court. The analyst may be called as an **expert witness**. The CoC form proves the evidence was handled properly throughout.

### ⚖️ In Court — What Must Be Proven

> [!important] Prosecution Must Establish
> 1. **Who collected** the evidence (first custodian)
> 2. **That every transfer** is documented and verified
> 3. **That the evidence was not altered** (hash values prove this for digital)
> 4. **That storage was secure** (no opportunity for tampering)
> 5. **That examination was on a copy** (original integrity preserved)
> 6. **Expert qualifications** of the forensic analyst

### 📋 BSA 2023 Section 63 Certificate

> [!important] The Certificate Requirement
> For digital evidence to be admissible under **BSA 2023 (Section 63)**, the prosecution must present a certificate from a responsible official stating:
> - The device producing the evidence was operating properly
> - The electronic record accurately represents the information stored
> - All processes applied to the evidence are documented
>
> This certificate is essentially a **legal attestation of the chain of custody** for digital evidence.

---

## Step 9 — Return, Archive or Disposal

### 🟢 What Happens Here?

> [!abstract] Simple Explanation
> After the case concludes (conviction, acquittal, or case closed), the evidence must be dealt with. It cannot just sit in a storage room forever.

### 📋 Disposition Options

| Option | When | Process |
|---|---|---|
| **Return to Owner** | Acquittal OR evidence belongs to victim | Court order → documented handover → owner signs receipt |
| **Forfeiture/Confiscation** | Conviction → tools of crime | Court order → government property |
| **Archival** | Long-term storage (appeals pending) | Sealed storage with retention policy |
| **Destruction** | Court orders destruction | Witnessed destruction + certificate issued |

> [!warning] Never Destroy Without Court Order
> Evidence must **never be destroyed** without a formal court order. Premature destruction can result in:
> - Contempt of court charges
> - Appeals being undermined
> - Investigator liability

---

## Chain of Custody Form — Complete Template

> [!note] 📋 Standard Chain of Custody Form

```
╔══════════════════════════════════════════════════════════════════╗
║              CHAIN OF CUSTODY FORM                              ║
║         Digital Forensics Evidence Record                       ║
╠══════════════════════════════════════════════════════════════════╣
║ CASE INFORMATION                                                 ║
║ Case Number    : _______________________________________         ║
║ Case Name      : _______________________________________         ║
║ Incident Type  : _______________________________________         ║
║ Date of Incident: ______________________________________         ║
║ Investigating Officer: __________________________________        ║
╠══════════════════════════════════════════════════════════════════╣
║ EXHIBIT INFORMATION                                              ║
║ Exhibit No.    : _______________________________________         ║
║ Description    : _______________________________________         ║
║ Make/Model     : _______________________________________         ║
║ Serial Number  : _______________________________________         ║
║ IMEI (if phone): _______________________________________         ║
║ Condition      : _______________________________________         ║
╠══════════════════════════════════════════════════════════════════╣
║ COLLECTION DETAILS                                               ║
║ Collection Location: ____________________________________        ║
║ Date & Time    : _______________________________________         ║
║ Collected By   : _______________________________________         ║
║ Witness        : _______________________________________         ║
║ State at collection: ___________________________________         ║
║ (e.g., powered on, locked, open app)                            ║
║ MD5 Hash       : _______________________________________         ║
║ SHA-256 Hash   : _______________________________________         ║
║ Seal Number    : _______________________________________         ║
╠══════════════════════════════════════════════════════════════════╣
║ CHAIN OF CUSTODY TRANSFERS                                       ║
╠═══════╦══════════╦══════════╦═════════════╦══════╦═════════════╣
║ Entry ║ Date/Time║ Released ║  Received   ║ Seal ║  Purpose    ║
║  No.  ║          ║    By    ║     By      ║  No. ║             ║
╠═══════╬══════════╬══════════╬═════════════╬══════╬═════════════╣
║  001  ║          ║          ║             ║      ║ Collection  ║
╠═══════╬══════════╬══════════╬═════════════╬══════╬═════════════╣
║  002  ║          ║          ║             ║      ║ Transport   ║
╠═══════╬══════════╬══════════╬═════════════╬══════╬═════════════╣
║  003  ║          ║          ║             ║      ║ Storage     ║
╠═══════╬══════════╬══════════╬═════════════╬══════╬═════════════╣
║  004  ║          ║          ║             ║      ║ Examination ║
╠═══════╬══════════╬══════════╬═════════════╬══════╬═════════════╣
║  005  ║          ║          ║             ║      ║ Court       ║
╚═══════╩══════════╩══════════╩═════════════╩══════╩═════════════╝
```

---

## Timeline of a Chain of Custody — Real Case Example

> [!example] 🕐 Complete Timeline — Cybercrime Case: Online Banking Fraud

### 📅 Case: CY/2025/DEL/0047 — Axis Bank Fraud ₹45 Lakh

---

**D-Day = 10-January-2025 (Complaint Filed)**

```
📅 10 JAN 2025 — 11:00 hrs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENT    : Victim Ramesh Gupta files complaint at
           Cyber Crime PS, New Delhi
           ₹45 lakh transferred without authorization
ACTION   : FIR No. 012/2025 registered
OFFICER  : Insp. Rajesh Kumar assigned
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 07:45 hrs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENT    : Suspect Vikram Singh identified and
           arrested at his residence, Sector 18, Noida
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 08:00 hrs — STEP 1: IDENTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOCATION : Suspect's bedroom, House No. 45B
ACTION   : Scene documented — photographs taken
FOUND    :
  → EX-01: HP Laptop (ON, browser showing bank portal)
  → EX-02: iPhone 13 Pro (unlocked, WhatsApp open)
  → EX-03: Kingston USB 32GB
  → EX-04: Notebook with handwritten account numbers
VOLATILE : Laptop running — decision: LIVE ACQUISITION first
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 08:15 hrs — STEP 2: COLLECTION (Volatile)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   : RAM dump captured on EX-01 (HP Laptop)
           Tool: WinPMEM v3.3
           RAM Image: 8GB captured in 4 mins
           Saved to: Evidence USB (tamper-sealed)
           Running processes captured
           Active network connections captured
           System clock: 08:14 — compared to atomic time: 08:15
           (1 min discrepancy noted)
OFFICER  : Insp. Rajesh Kumar
WITNESS  : SI Deepak Yadav
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 08:20 hrs — STEP 2: COLLECTION (EX-02 iPhone)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   : iPhone was UNLOCKED when found
           → Screenshot of WhatsApp chats taken
           → Immediately placed in Faraday bag (Bag No. FB-003)
           → Then placed in evidence bag
NOTE     : Airplane mode could not be enabled before Faraday bag
           (Faraday bag blocks all signals — equivalent protection)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 08:30 hrs — STEP 2: COLLECTION (EX-01 Laptop HDD)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   : HP Laptop powered off (after RAM dump)
           Hard drive removed: WD Blue 1TB SSD
           Connected to: Tableau T8-R2 write blocker
           Forensic image: FTK Imager v4.7
           Image type: E01 (EnCase)
           MD5  : 3d4e7f9a1b2c...
           SHA-256: a1b2c3d4...
           Hash match: ✅ VERIFIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 09:00 hrs — STEP 3: PACKAGING & LABELLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   :
  EX-01 (Laptop)  → Anti-static bag → Evidence bag → Seal SL-78432
  EX-02 (iPhone)  → Already in Faraday bag → Outer evidence seal SL-78433
  EX-03 (USB)     → Anti-static bag → Evidence bag → Seal SL-78434
  EX-04 (Notebook)→ Clear plastic sleeve → Evidence envelope → Seal SL-78435
All labels written with:
  → Case no., exhibit no., description, hash, officer name, date/time
Photos: Each sealed exhibit photographed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 09:30 hrs — STEP 4: TRANSPORTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FROM     : House No. 45B, Sector 18, Noida
TO       : CFSL (Central Forensic Science Lab), New Delhi
BY       : Insp. Rajesh Kumar + SI Deepak Yadav
VEHICLE  : Police vehicle GJ-07-PA-4521
ROUTE    : Direct — no stops
HANDOVER : Exhibits handed to FSL Evidence Reception
RECEIVED BY: FSL Custodian Ram Chandra (ID: FSL-044)
TRANSFER ENTRY: Both officers signed CoC form
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 13 JAN 2025 — 11:00 hrs — STEP 5: STORAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   : All exhibits stored in Evidence Room B, CFSL
           Shelf: B-14, Case Ref: CY/2025/DEL/0047
           Temperature: 20°C, Humidity: 45% (logged)
           Room access log entry made
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 16 JAN 2025 — 09:15 hrs — STEP 6: EXAMINATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALYST  : Priya Sharma (FSL-221, Cert: EnCE, GCFE)
ACTION   : EX-01 retrieved from storage
           Seal SL-78432 verified intact
           Seal broken — documented
           Hash re-verified before analysis: ✅ MATCH
           Working copy mounted in Autopsy v4.21
KEY FINDS:
  10:30 — Phishing kit found in /Downloads/bankphish.zip
  11:15 — Saved browser passwords: 47 bank accounts found
  13:00 — Transaction scripts found in /AppData/Local
  14:00 — Telegram message exports found
  15:00 — Analysis complete
Original drive re-sealed: New Seal SL-79001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 22 JAN 2025 — STEP 7: REPORT SUBMITTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   : Forensic Report submitted by Priya Sharma
           Report No: FSL/CFSL/2025/CY047
           BSA 2023 Sec. 63 Certificate attached
           Submitted to: Insp. Rajesh Kumar
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 15 MAR 2025 — STEP 8: COURT PRESENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION   : Exhibits produced before Sessions Court
           Priya Sharma testifies as expert witness
           CoC form presented — all transfers accounted for
           Chain intact — no gaps
           Electronic evidence admitted under BSA 2023 Sec. 63
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 30 MAR 2025 — CONVICTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT   : Vikram Singh convicted under:
           → Sec. 66C IT Act (Identity theft)
           → Sec. 66D IT Act (Cheating by impersonation)
           → Sec. 420 IPC (now BNS equivalent — Fraud)
           Sentence: 3 years + ₹1 lakh fine
EXHIBITS : Ordered confiscated (tools of crime)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Digital vs Physical Evidence — CoC Differences

| Aspect | Physical Evidence | Digital Evidence |
|---|---|---|
| **Nature** | Tangible — knife, document | Intangible — files, logs, emails |
| **Integrity check** | Visual inspection | Hash value comparison (MD5/SHA-256) |
| **Copying** | Copy changes original | Perfect bit-for-bit copy possible |
| **Contamination** | Fingerprints, DNA | Accessing file changes timestamps |
| **Degradation** | Rust, decay | Bit rot, media failure |
| **Volatility** | No (stable) | YES — RAM vanishes when powered off |
| **Volume** | Limited | Massive (TBs of data) |
| **Remote alteration** | Not possible | Possible (remote wipe, cloud delete) |
| **Tool required** | Basic (gloves, bags) | Write blockers, forensic software |
| **Key protection method** | Sealed bags, refrigeration | Write blockers + hash verification |

---

## Common Mistakes That Break Chain of Custody

> [!danger] ❌ Top 10 CoC Mistakes

| #   | Mistake                                | Consequence                                            | Prevention                                           |
| --- | -------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------- |
| 1   | **Turning off a running computer**     | RAM contents (passwords, encryption keys) lost forever | Always do live acquisition first                     |
| 2   | **No Faraday bag for phone**           | Remote wipe destroys all evidence                      | Always bag phones immediately                        |
| 3   | **Working on original drive**          | Timestamps modified; evidence contaminated             | Always use write blocker + forensic image            |
| 4   | **Gaps in transfer records**           | Defence argues tampering occurred in the gap           | Document every single transfer immediately           |
| 5   | **Not calculating hash at collection** | Cannot prove evidence unchanged later                  | Always hash at scene AND after each transfer         |
| 6   | **Broken seal not documented**         | Suggests tampering; evidence challenged                | Always document seal breaks + new seal number        |
| 7   | **Taking evidence home overnight**     | Unauthorized access; CoC broken                        | Evidence must only be in authorized secure locations |
| 8   | **No witness at collection**           | Officer's word alone — challengeable                   | Always have a witness who also signs the CoC form    |
| 9   | **Vague or incorrect labels**          | Cannot identify exhibit in court                       | Complete, accurate labels on everything              |
| 10  | **No BSA/Section 63 certificate**      | Digital evidence inadmissible in court                 | Always prepare and attach the certificate            |

---

## Hash Values — The Digital Seal

### 🟢 Simple Explanation

> [!abstract] Think of it like this…
> A hash is like a **fingerprint of a file**. If you change even **one single letter** in a 10,000-page document, the hash completely changes. This makes it mathematically impossible to alter digital evidence secretly.
>
> Hash of "Hello World" = `b94d27b9934d3e08a52e52d7da7dabfac484efe04294e576`
> Hash of "Hello World." (just added a full stop) = `completely different string`

### 📊 Common Hash Algorithms

| Algorithm | Output Length | Status | Use in Forensics |
|---|---|---|---|
| **MD5** | 128-bit (32 hex chars) | Weak (collisions possible) | Still used for verification (not authentication) |
| **SHA-1** | 160-bit (40 hex chars) | Deprecated | Not recommended |
| **SHA-256** | 256-bit (64 hex chars) | Strong ✅ | Primary standard |
| **SHA-512** | 512-bit (128 hex chars) | Very strong ✅ | High-security cases |

> [!tip] Best Practice
> Always calculate **BOTH MD5 AND SHA-256** of every piece of digital evidence. Record both in the CoC form. This provides redundancy — if MD5 is challenged, SHA-256 still stands.

### 🔄 Hash Verification at Each Stage

```
AT COLLECTION:     Hash = 3d4e7f... (documented in CoC form)
                          ↓
AT LAB RECEIPT:    Hash = 3d4e7f... ✅ MATCH → no tampering in transit
                          ↓
BEFORE ANALYSIS:   Hash = 3d4e7f... ✅ MATCH → evidence intact
                          ↓
AFTER ANALYSIS:    Hash = 3d4e7f... ✅ MATCH → original untouched
                          ↓
IN COURT:          Hash = 3d4e7f... ✅ MATCH → admissible
```

> [!danger] Hash Mismatch = Emergency
> If at **any stage** the calculated hash does NOT match the original hash:
> - STOP all proceedings
> - Document the discrepancy immediately
> - Notify the investigating officer and senior officials
> - The evidence may be **tainted** → investigation into what happened

---

## Legal Framework — Chain of Custody in India

### ⚖️ Key Legal Provisions

| Law | Section | Relevance to CoC |
|---|---|---|
| **IT Act, 2000** | Sec. 65B (now BSA Sec. 63) | Certificate of authenticity for electronic evidence |
| **IT Act, 2000** | Sec. 79A | Examiner of Electronic Evidence (expert opinion) |
| **IT Act, 2000** | Sec. 78 | Inspector-level officer for investigation |
| **BSA 2023** | Sec. 63 | Admissibility of electronic records |
| **BSA 2023** | Sec. 79 | Presumption about electronic records |
| **CrPC (now BNSS)** | Sec. 100 | Search and seizure procedures |
| **CrPC (now BNSS)** | Sec. 102 | Power to seize property |
| **Indian Evidence Act** | Sec. 45 | Expert opinion — now BSA Sec. 39 |

### 📋 CERT-In Directions 2022 — CoC Implications

> [!note] 180-Day Log Retention
> Under CERT-In Directions 2022, all service providers, intermediaries, and data centres must maintain logs for **180 days within India**.
>
> This creates a ready source of digital evidence — but investigators must request these logs within 180 days before they are deleted.

---

## International Standards & Guidelines

### 🌍 Key Standards Governing CoC

| Standard | Body | What It Says |
|---|---|---|
| **ACPO Good Practice Guide** | UK — Association of Chief Police Officers | 4 core principles of digital evidence handling (foundation of most CoC procedures) |
| **ISO/IEC 27037:2012** | International Standards Org. | Guidelines for identification, collection, acquisition, preservation of digital evidence |
| **ISO/IEC 27041:2015** | ISO | Guidance on investigation assurance |
| **ISO/IEC 27042:2015** | ISO | Analysis and interpretation of digital evidence |
| **ISO/IEC 27043:2015** | ISO | Incident investigation principles and processes |
| **NIST SP 800-86** | US — NIST | Guide to integrating forensic techniques into incident response |
| **RFC 3227** | IETF | Guidelines for evidence collection and archiving (network/volatile data) |

### 🔑 ACPO 4 Principles (Must Know for Exam)

> [!important] ACPO Principles — Foundation of Digital Forensics CoC
>
> **Principle 1:** No action taken by law enforcement agencies, persons employed within those agencies or their agents should change data which may subsequently be relied upon in court.
> → *Never alter original evidence*
>
> **Principle 2:** In circumstances where a person finds it necessary to access original data, that person must be competent to do so and be able to give evidence explaining the relevance and the implications of their actions.
> → *Only qualified people access originals; they must justify it*
>
> **Principle 3:** An audit trail or other record of all processes applied to computer-based electronic evidence should be created and preserved. An independent third party should be able to examine those processes and achieve the same result.
> → *Document everything; results must be reproducible*
>
> **Principle 4:** The person in charge of the investigation has overall responsibility for ensuring that the law and these principles are adhered to.
> → *One person is ultimately accountable*

---

## 🗒️ Quick Revision Summary

> [!summary] Chain of Custody — Master Cheat Sheet

| Stage | What Happens | Key Rule |
|---|---|---|
| **Identification** | Recognize potential evidence | Photograph before touching; don't turn off running computers |
| **Collection** | Gather evidence without altering | Live acq. first; write blocker; Faraday bag for phones |
| **Packaging** | Seal, label, anti-static bags | Sign across seal; record seal number; calculate hash |
| **Transportation** | Move to lab/storage | Minimum handlers; direct route; signed handover |
| **Storage** | Secure, controlled environment | 15-25°C; access log; separate by case |
| **Examination** | Forensic analysis | On copy ONLY; re-verify hash; analyst log every action |
| **Reporting** | Document findings | Tool versions; hash certificates; Sec. 63 certificate |
| **Court** | Present evidence | CoC form proves integrity; expert testimony |
| **Disposition** | Return/destroy/archive | Only on court order |

> [!tip] The Golden Triangle of CoC
> ```
>           DOCUMENTATION
>               /\
>              /  \
>             /    \
>            /      \
>      INTEGRITY ─── CONTINUITY
> ```
> All three must be maintained throughout. Failing any one = potentially inadmissible evidence.

---

## 📝 Exam Questions

> [!question] Previous Year Pattern Questions
> 1. What is Chain of Custody? Why is it important in digital forensics?
> 2. Explain the step-by-step process of maintaining chain of custody for a seized laptop.
> 3. What is a write blocker? Why must it be used during digital evidence collection?
> 4. What are hash values? How do they help maintain evidence integrity?
> 5. What are the ACPO Four Principles of digital evidence handling?
> 6. Explain the role of BSA 2023 Section 63 in maintaining chain of custody in court.
> 7. Distinguish between live acquisition and dead acquisition.
> 8. What mistakes can break a chain of custody? Discuss any five with consequences.
> 9. How is chain of custody maintained for mobile phone evidence? What is a Faraday bag?
> 10. Explain ISO/IEC 27037 in the context of digital evidence collection.

---

## 🔗 Related Notes

- [[Paper 204 - Unit III — Offences & Compliance]]
- [[Digital Forensics — Memory Forensics (Volatility)]]
- [[Digital Forensics — Disk Forensics]]
- [[BSA 2023 — Electronic Evidence]]
- [[Forensic Tools — FTK Imager, Autopsy, Cellebrite]]
- [[Operation Phantom Ledger — CTF Lab]]
- [[Cywarx Digital Forensics — Unit IV Notes]]

---

*📌 Maintained by Cywarx | University of Delhi — PGDCSL | Digital Forensics Course*
