---
title: "Paper 204 – Unit III: Offences, Penalties & Security Compliance"
course: "Post Graduate Diploma in Cyber Security and Law"
university: "University of Delhi"
semester: "Semester 2"
paper: "Paper 204 – Cyber Law and Forensic Evidence"
unit: "Unit III"
tags:
  - cyber-law
  - IT-Act-2000
  - offences
  - penalties
  - CERT-In
  - intermediary
  - GDPR
  - HIPAA
  - PCI-DSS
  - compliance
  - DU
  - semester-2
  - paper-204
created: 2025-01-01
status: complete
---

# 📘 Unit III — Offences, Penalties & Security Compliance

> [!info] 📌 Course Details
> **Course:** Post Graduate Diploma in Cyber Security and Law
> **University:** University of Delhi | **Semester:** 2
> **Paper:** 204 — Cyber Law and Forensic Evidence

---

## 🗂️ Table of Contents

- [[#Part A — Offences & Penalties under IT Act 2000]]
  - [[#1. Offences under the IT Act 2000]]
  - [[#2. Penalty and Adjudication]]
  - [[#3. Punishments for Contraventions]]
  - [[#4. Role of Intermediaries and Their Liabilities]]
  - [[#5. Power of Government to Give Directions]]
  - [[#6. CERT-In and Its Functions]]
  - [[#7. Important Case Laws & Judicial Pronouncements]]
  - [[#8. Limitations of Cyber Law]]
- [[#Part B — Security Policies, Standards & Compliance]]
  - [[#9. Security Policies — Development & Implementation]]
  - [[#10. Compliance Frameworks — GDPR, HIPAA, PCI DSS]]
  - [[#11. Auditing, Assessment & Compliance Monitoring]]
- [[#Quick Revision Summary]]

---

# 🔴 Part A — Offences & Penalties under IT Act 2000

---

## 1. Offences under the IT Act 2000

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Just like the IPC (now BNS) has sections for physical crimes like theft and assault, the **IT Act, 2000** has specific sections that define **cybercrimes** and make them punishable. These are the "rules of the game" in cyberspace — break them and face legal consequences.

### 📋 Two Categories of Violations

```
IT Act Violations
      ├── CIVIL CONTRAVENTIONS (Chapter IX — Sec. 43–45)
      │        → Compensatory, not criminal
      │        → Handled by Adjudicating Officer
      │        → No imprisonment
      │
      └── CRIMINAL OFFENCES (Chapter XI — Sec. 65–78)
               → Criminal prosecution
               → Handled by Court of Session / Magistrate
               → Imprisonment + Fine
```

---

### 🔑 Civil Contraventions — Chapter IX

> [!note] Section 43 — Penalty for Damage to Computer Systems
> If any person **without permission** of the owner/person in charge of a computer:

| Act | Penalty |
|---|---|
| Accesses or secures access | Compensation up to **₹1 crore** |
| Downloads, copies, or extracts data | Compensation up to **₹1 crore** |
| Introduces a computer virus/contaminant | Compensation up to **₹1 crore** |
| Damages or disrupts computer/network | Compensation up to **₹1 crore** |
| Denies access (DoS attack) | Compensation up to **₹1 crore** |
| Provides assistance to any of the above | Compensation up to **₹1 crore** |
| Charges services to someone else's account | Compensation up to **₹1 crore** |
| **Destroys, deletes, alters** any information | Compensation up to **₹1 crore** |
| Steals, conceals, destroys computer source code | Compensation up to **₹1 crore** |

> [!example] Simple Example
> Ravi hacks into his company's server without permission and downloads confidential client data. Under **Sec. 43**, the company can claim **compensation** from Ravi through the Adjudicating Officer.

---

> [!important] Section 43A — Compensation for Failure to Protect Data
> If a **body corporate** (company/firm) possessing, dealing, or handling **SPDI (Sensitive Personal Data or Information)** is **negligent** in implementing reasonable security practices, causing **wrongful loss or gain** to any person — it shall pay **compensation** to the affected person.

> [!example] Simple Example
> A hospital stores patient health records (SPDI) on an unencrypted server. A hacker steals this data. The hospital is liable under **Sec. 43A** because they were negligent in not encrypting the SPDI.

---

> [!note] Section 44 — Penalty for Failure to Furnish Information
> | Situation | Penalty |
> |---|---|
> | Fails to furnish info required by Controller/CCA | ₹1.5 lakh per failure |
> | Fails to file return or furnish information | ₹5,000 per day of default |
> | Fails to maintain books/records as required | ₹10,000 per day |

---

> [!note] Section 45 — Residuary Penalty
> Any contravention of the IT Act **not specifically covered** by another section → penalty up to **₹25,000**.

---

### 🔑 Criminal Offences — Chapter XI

> [!danger] Complete Section-wise Offences & Punishments

| Section | Offence | Punishment |
|---|---|---|
| **Sec. 65** | Tampering with computer source documents (hiding, altering source code) | 3 years OR ₹2 lakh fine OR both |
| **Sec. 66** | Hacking / Computer-related offences (dishonestly/fraudulently doing acts of Sec. 43) | 3 years OR ₹5 lakh fine OR both |
| **Sec. 66A** | ~~Offensive messages through communication services~~ | **STRUCK DOWN** — Shreya Singhal 2015 |
| **Sec. 66B** | Dishonestly receiving stolen computer resource | 3 years OR ₹1 lakh OR both |
| **Sec. 66C** | Identity theft (fraudulently using someone's electronic signature/password) | 3 years AND ₹1 lakh fine |
| **Sec. 66D** | Cheating by personation using computer resource | 3 years AND ₹1 lakh fine |
| **Sec. 66E** | Violation of privacy (capturing/transmitting private parts without consent) | 3 years OR ₹2 lakh OR both |
| **Sec. 66F** | **Cyber Terrorism** | **Life Imprisonment** |
| **Sec. 67** | Publishing/transmitting obscene material online | 3 yrs (1st) / 5 yrs (repeat) + fine |
| **Sec. 67A** | Publishing/transmitting sexually explicit material | 5 yrs (1st) / 7 yrs (repeat) + fine |
| **Sec. 67B** | Child pornography (CSAM) | 5 yrs (1st) / 7 yrs (repeat) + fine |
| **Sec. 67C** | Intermediary failing to preserve records | 3 years AND fine |
| **Sec. 68** | Failure to comply with Controller's directions | 3 years OR ₹2 lakh OR both |
| **Sec. 69** | Failure to assist in interception/decryption | 7 years AND fine |
| **Sec. 69A** | Failure to comply with blocking order | 7 years AND fine |
| **Sec. 69B** | Failure to assist in monitoring/collection of traffic data | 3 years AND fine |
| **Sec. 70** | Accessing/attempting to access Protected Systems | 10 years AND fine |
| **Sec. 70B** | Failure to report cyber incident to CERT-In | 1 year OR ₹1 lakh OR both |
| **Sec. 71** | Misrepresentation to Controller or CA | 2 years OR ₹1 lakh OR both |
| **Sec. 72** | Breach of confidentiality and privacy by official | 2 years OR ₹1 lakh OR both |
| **Sec. 72A** | Disclosure of information in breach of contract | 3 years OR ₹5 lakh OR both |
| **Sec. 73** | Publishing false Digital Signature Certificate | 2 years OR ₹1 lakh OR both |
| **Sec. 74** | Publication of DSC for fraudulent purpose | 2 years OR ₹1 lakh OR both |
| **Sec. 75** | Offences committed outside India (if computer in India) | Applicable extraterritorially |

> [!warning] Cognizable vs Non-Cognizable Offences
> - **Cognizable** (police can arrest without warrant) — Sec. 66F (cyber terrorism), Sec. 67B (CSAM), Sec. 70 (protected systems)
> - **Non-Cognizable** (warrant needed) — most other offences
> Under Sec. 80 — police officer *not below Inspector* can arrest without warrant for cognizable cyber offences.

---

## 2. Penalty and Adjudication

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> If someone breaks a traffic rule, a traffic constable gives a fine on the spot. For bigger violations, you go to a court. Similarly, for **minor civil IT violations**, you go to the **Adjudicating Officer**. For **serious criminal offences**, you go to the **Court of Session**.

### 🏛️ Adjudication Process (Section 46)

```
Complaint filed (victim / company / government)
          ↓
Adjudicating Officer appointed (Director-level govt. officer)
          ↓
Notice issued to accused party
          ↓
Hearing — both sides present arguments + evidence
          ↓
AO examines electronic records, logs, expert reports
          ↓
ORDER passed:
  → Compensation awarded to victim
  → Penalty imposed on accused
          ↓
Appeal to Cyber Appellate Tribunal (within 45 days)
```

> [!tip] Key Rules of Adjudication (Section 46)
> - AO has powers of a **Civil Court** for the purpose of taking evidence
> - Proceedings are **judicial proceedings** (perjury rules apply)
> - AO must follow **principles of natural justice** — both sides must be heard
> - Maximum compensation: **₹5 crore** per complaint (if more → go to civil court)

---

## 3. Punishments for Contraventions

### 📊 Punishment Summary by Type

> [!note] Civil vs Criminal — Quick Reference

| Type | Nature | Authority | Example Sections |
|---|---|---|---|
| **Compensation** | Civil | Adjudicating Officer | Sec. 43, 43A, 44, 45 |
| **Fine** | Criminal | Court | Sec. 65, 66, 67 |
| **Imprisonment** | Criminal | Court of Session | Sec. 66F, 70, 67B |
| **Both Fine + Imprisonment** | Criminal | Court of Session | Sec. 66C, 66D, 69 |

### ⚖️ Corporate Liability — Section 85

> [!important] Section 85 — Offences by Companies
> If an offence is committed by a **company**, every person who was **in charge and responsible** for the conduct of the business at the time of the offence **shall be liable** to be proceeded against and punished.
>
> **Defence available:** If the person can prove they had no knowledge OR exercised due diligence to prevent the offence.

> [!example] Simple Example
> A tech company's server is used to host CSAM (child pornography). Under Sec. 85, the **CEO and directors** can be prosecuted if they were responsible for the company's operations — not just the technical employee.

---

## 4. Role of Intermediaries and Their Liabilities

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> WhatsApp is just a **platform** — it doesn't create your messages. If you send a threatening message on WhatsApp, is WhatsApp responsible? This question of **intermediary liability** is at the heart of this topic.
>
> An **Intermediary** is any middleman platform — ISPs, social media, cloud hosts, email providers — that handles data created by users, not by themselves.

### 📖 Definition — Section 2(1)(w)

> "Intermediary" with respect to any particular electronic records means any person who **on behalf of another person receives, stores, or transmits** that record or provides any service with respect to that record.
>
> Includes: telecom companies, ISPs, search engines, online marketplaces, cybercafes, web hosting providers, social media platforms

### 🛡️ Safe Harbour Protection — Section 79

> [!important] Section 79 — Exemption from Liability
> An intermediary shall **NOT be liable** for any third-party information, data, or communication hosted by it **IF:**
>
> 1. The intermediary's role is **only to provide access** (passive conduit)
> 2. The intermediary **did not initiate** the transmission
> 3. The intermediary **did not select** the receiver
> 4. The intermediary **did not modify** the information
> 5. The intermediary **observed due diligence** (followed IT Act + Rules)
> 6. The intermediary **removed the content promptly** upon actual knowledge of unlawful nature

> [!example] Simple Example
> A user posts a defamatory video on YouTube. If YouTube:
> - Did not create the video ✅
> - Did not select who sees it ✅
> - Removes it promptly when notified ✅
> → YouTube is **NOT liable** (Safe Harbour under Sec. 79)
>
> But if YouTube **knew** the content was illegal and **did nothing** → Safe Harbour is **lost** ❌

### ❌ When Safe Harbour is LOST

> [!warning] Section 79(3) — Loss of Safe Harbour
> Safe harbour protection is **lost** when:
> 1. The intermediary has **conspired, abetted, or induced** the unlawful act
> 2. Upon receiving **actual knowledge** (by government/court order), the intermediary **fails to remove** or disable access to the unlawful content

### 📋 Due Diligence Requirements (IT Rules 2021)

For an intermediary to maintain safe harbour, it must:

| Obligation | Requirement |
|---|---|
| **Publish Rules & Policy** | Terms of service, privacy policy, user guidelines |
| **Inform Users** | About prohibited content categories |
| **Grievance Officer** | Appoint a named grievance officer |
| **Takedown Timeline** | Remove content within **36 hours** of court/govt. order |
| **Voluntary Takedown** | Remove content within **24 hours** of complaint (certain categories) |
| **Record Retention** | Preserve records for **180 days** for investigation purposes |
| **No Hosting Prohibited Content** | Don't host content threatening national security, CSAM, defamatory material |

### 🏢 Significant Social Media Intermediaries (SSMI)

> [!info] Who qualifies as SSMI?
> Platforms with **50 lakh (5 million)+ registered users** in India.
>
> Additional obligations:
> | Obligation | Detail |
> |---|---|
> | **Chief Compliance Officer** | Indian resident; liable for compliance |
> | **Nodal Contact Person** | Available 24×7 for law enforcement |
> | **Resident Grievance Officer** | Must acknowledge complaints within 24 hours; resolve in 15 days |
> | **Monthly Compliance Report** | Publish details of complaints received + action taken |
> | **Traceability** | Messaging platforms must identify first originator of a message (for serious offences) |
> | **Proactive Monitoring** | Use tech tools to proactively identify CSAM and other illegal content |

---

## 5. Power of Government to Give Directions

### 🟢 Overview

> [!abstract] Think of it like this…
> The government has special powers to direct ISPs, platforms, and companies for **national security, law enforcement, and public order** purposes. These powers include blocking websites, intercepting communications, collecting traffic data, and protecting critical infrastructure.

---

### A. Blocking of Content — Section 69A

> [!important] Section 69A — Power to Block Online Content
> The Central Government may, in the interest of:
> - **Sovereignty and integrity of India**
> - **Defence of India**
> - **Security of the State**
> - **Friendly relations with foreign states**
> - **Public order**
> - **Preventing incitement to cognizable offences**
>
> **Direct any agency or intermediary to block** for access by the public any information generated, transmitted, received, stored, or hosted in any computer resource.

> [!note] Procedure for Blocking
> 1. Designated Officer reviews complaint
> 2. **Notice to originator/intermediary** (if possible) for reply
> 3. **Review Committee** examines the request
> 4. Order passed → intermediary must comply within **stipulated time**
> 5. **Penalty for non-compliance: 7 years + fine** (Sec. 69A)
>
> In cases of **emergency**, blocking can happen without notice (interim blocking).

> [!example] Famous Blocking Cases
> - **TikTok** — blocked in India (June 2020) under Sec. 69A citing national security
> - **PUBG Mobile, 200+ Chinese apps** — blocked 2020 under same provision
> - **ShareChat** — temporary blocking of links from certain groups
> - **Websites with pirated content** — regular blocking orders

---

### B. Interception of Communications — Section 69

> [!important] Section 69 — Power to Intercept, Monitor, Decrypt
> The Central/State Government or its authorized agency may **intercept, monitor, or decrypt any information** through any computer resource if it is satisfied that it is necessary in the interest of:
> - Sovereignty and integrity of India
> - Defence of India
> - Security of the State
> - Friendly relations with foreign states
> - Public order
> - Preventing cognizable offences
> - Investigating any offence

> [!note] Who Can Authorize Interception?
> - **Central Govt.** — Secretary, Ministry of Home Affairs
> - **State Govt.** — Secretary, Home Department
> - **In emergency** — Joint Secretary or above (but must be confirmed within 7 days)

> [!warning] Penalty for Non-Compliance (Sec. 69)
> Any person who fails to assist or comply with an interception order:
> **7 years imprisonment AND fine**

> [!example] Real-World Application
> Investigators in a terrorism case obtain an order under Sec. 69 to intercept encrypted WhatsApp messages between suspects. WhatsApp (intermediary) must assist in decrypting the communication or provide technical assistance.

---

### C. Collecting Traffic Data — Section 69B

> [!important] Section 69B — Power to Monitor and Collect Traffic Data
> The Central Government may authorize any agency to **monitor and collect traffic data or information** through any computer resource for **cyber security purposes**.

> [!info] What is Traffic Data?
> Traffic data = metadata about communications — NOT the content itself, but:
> - Source/destination IP addresses
> - Timestamps of connections
> - Volume of data transferred
> - Type of service used (email, web, VoIP)
> - Login/logout times

> [!example] Simple Example
> CERT-In monitors traffic data across Indian internet infrastructure to detect unusual patterns that could indicate a DDoS attack or data exfiltration attempt. This is done under Sec. 69B.

---

### D. Critical Infrastructure Protection — Section 70

> [!important] Section 70 — Protected Systems
> The Central Government may, by notification, **declare any computer resource which directly or indirectly affects** the facility of Critical Information Infrastructure (CII) to be a **"Protected System"**.

> [!info] What is Critical Information Infrastructure (CII)?
> Computer resources whose **incapacitation or destruction** would have a **debilitating impact** on national security, economy, public health, or safety.
>
> Examples of CII in India:
> | Sector | Examples |
> |---|---|
> | **Power** | National Power Grid, NTPC systems |
> | **Banking/Finance** | RBI systems, SWIFT, stock exchanges |
> | **Telecom** | BSNL backbone, telecom exchanges |
> | **Defence** | Military networks, DRDO systems |
> | **Transport** | Air traffic control, railways (CRIS) |
> | **Government** | NIC networks, e-governance infrastructure |
> | **Health** | Hospital networks, pharmaceutical data |

> [!danger] Penalty for Unauthorized Access to Protected System (Sec. 70)
> **10 years imprisonment AND fine** — regardless of whether damage was caused

> [!note] Section 70A — National Critical Information Infrastructure Protection Centre (NCIIPC)
> - Set up under **NTRO (National Technical Research Organisation)**
> - Designated as the nodal agency for CII protection
> - Issues guidelines, advisories, and policies for CII sectors

---

## 6. CERT-In and Its Functions

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Imagine a city has a **fire brigade** — they respond to fire emergencies, investigate causes, advise on fire safety, and coordinate with all buildings. **CERT-In** is India's **cyber fire brigade** — they respond to cyber incidents, help organizations recover, and advise on cyber security.

### 📖 Legal Basis — Section 70B, IT Act

> **Section 70B (inserted by IT Amendment Act, 2008)**
> The Central Government shall appoint an agency of the Government to be called the **Indian Computer Emergency Response Team (CERT-In)**.
>
> CERT-In shall serve as the **national nodal agency** for:
> - Performing functions relating to **cyber security**
> - Coordination of crisis management
> - Collection, analysis, and dissemination of information on **cyber incidents**

### 🏛️ Functions of CERT-In (Section 70B(4))

> [!note] Statutory Functions
> 1. **Collection, analysis, and dissemination** of information on cyber incidents
> 2. **Forecast and alerts** of cyber security incidents
> 3. **Emergency measures** for handling cyber security incidents
> 4. **Coordination of cyber incident response** activities
> 5. **Issue guidelines, advisories, vulnerability notes** and white papers
> 6. **Such other functions** relating to cyber security as may be prescribed

### 📋 CERT-In Powers (IT Rules 2013 + CERT-In Directions 2022)

> [!important] CERT-In Directions 2022 — Key Requirements
> Issued under Sec. 70B, these directions require:
>
> | Requirement | Detail |
> |---|---|
> | **Mandatory incident reporting** | Report cyber incidents to CERT-In within **6 hours** of noticing |
> | **Synchronize clocks** | All ICT systems to sync with NTP servers of NIC/NPLI |
> | **Log Retention** | Maintain logs of ICT systems for **180 days** within India |
> | **VPN Service Providers** | Must maintain subscriber info for 5 years |
> | **Virtual Asset Providers** | Crypto exchanges must maintain KYC records |
> | **Data Centres/Cloud** | Must register with CERT-In |

> [!example] Who Must Report to CERT-In?
> - Government entities
> - Service providers, intermediaries, data centres
> - Body corporates, any organization
>
> **Reportable incidents include:**
> - Data breach
> - Unauthorized access to IT systems/data
> - Ransomware attacks
> - Website defacement
> - Malware propagation
> - Identity theft/fraud

### 🔬 CERT-In's Operational Role

```
CYBER INCIDENT DETECTED
          ↓
Organization reports to CERT-In (within 6 hours)
          ↓
CERT-In Triage: Categorize severity (Critical/High/Medium/Low)
          ↓
CERT-In Response:
  → Technical advisories issued
  → Coordination with affected organization
  → Coordinate with ISPs, hosting providers
  → Coordinate with international CERTs
          ↓
Forensic Analysis + Root Cause Investigation
          ↓
Advisory/Alert published (if public interest)
          ↓
Post-incident Report
```

> [!tip] CERT-In as Expert Examiner
> CERT-In is a **notified Examiner of Electronic Evidence** under **Section 79A** of the IT Act — its reports and opinions are admissible as expert evidence in court.

---

## 7. Important Case Laws & Judicial Pronouncements

> [!note] Key Cases — Unit III Focus

### 🏛️ Landmark Cases

---

**1. Shreya Singhal v. Union of India (2015) — Supreme Court**

> [!example] Facts & Holding
> **Facts:** Two girls arrested for Facebook posts criticizing a political bandh. Arrested under Sec. 66A IT Act.
>
> **Held:** Section 66A was **unconstitutional** — violated **Article 19(1)(a)** (Freedom of Speech). Terms like "grossly offensive," "menacing" were too vague.
>
> **Impact:** Sec. 66A struck down entirely. Now, online speech can only be restricted on the narrow grounds in Article 19(2).
>
> **Relevance:** Also upheld Sec. 69A (blocking) as constitutional — but with procedural safeguards.

---

**2. Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) — Supreme Court**

> [!example] Facts & Holding
> **Facts:** Dispute about whether Sec. 65B certificate is mandatory for electronic evidence.
>
> **Held:** Section 65B (now BSA 2023 Sec. 63) certificate is **mandatory** for electronic evidence to be admissible. Court can direct concerned party to produce certificate. Overruled the relaxation given in Shafhi Mohammad (2018).
>
> **Relevance:** Fundamental case for admissibility of all electronic evidence.

---

**3. Avnish Bajaj v. State (NCT of Delhi) (2005) — Delhi High Court**

> [!example] Facts & Holding
> **Facts:** A seller posted an obscene MMS clip on Baazee.com (now eBay India). CEO Avnish Bajaj was arrested under Sec. 67 IT Act.
>
> **Held:** An intermediary's CEO cannot be personally arrested if the platform had no knowledge of the obscene content. Court granted bail, noted that the intermediary liability provisions need clarity.
>
> **Relevance:** Led to the strengthening of safe harbour provisions and intermediary guidelines.

---

**4. SMC Pneumatics v. Jogesh Kwatra (2014) — Delhi HC**

> [!example] Facts & Holding
> **Facts:** An employee sent defamatory and vulgar emails about his employer and its MD.
>
> **Held:** India's **first cyber defamation injunction** — court restrained the employee from sending such emails.
>
> **Relevance:** Established that cyber defamation through emails is actionable.

---

**5. Christian Louboutin SAS v. Nakul Bajaj (2018) — Delhi HC**

> [!example] Facts & Holding
> **Facts:** Luxury shoe brand sued an Indian website selling their branded shoes.
>
> **Held:** An intermediary that is **"active"** (curates, promotes, controls content) cannot claim safe harbour under Sec. 79. Only **"passive"** intermediaries get protection.
>
> **Relevance:** Clarified that e-commerce platforms with active roles lose safe harbour.

---

**6. Suo Motu: In Re: Blocking of Twitter Accounts (2021)**

> [!example] Context
> Various cases challenging blocking orders under Sec. 69A, including Twitter refusing to comply with government orders.
>
> **Relevance:** Ongoing legal debate about due process in blocking orders, platform accountability, and limits of Sec. 69A.

---

## 8. Limitations of Cyber Law

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Even the best law has gaps. Imagine a traffic law made in 1990 — it wouldn't cover electric scooters, ride-sharing apps, or autonomous cars. Similarly, the IT Act 2000 (made before smartphones, social media, and AI) has significant **limitations**.

### 📌 Key Limitations

> [!warning] Limitations of Cyber Law in India

#### 1. Jurisdictional Challenges
- Cybercrime is **borderless** — an attacker in Russia targeting an Indian bank; which country's law applies?
- No strong international extradition treaties specifically for cybercrime
- **Sec. 75** (extraterritorial) has limited practical enforceability

#### 2. Technology Outpaces Law
- IT Act 2000 was drafted before social media, smartphones, AI, blockchain, deepfakes
- Frequent amendments needed but law-making is slow
- **Emerging threats** like AI-generated CSAM, deepfake fraud, quantum computing attacks have no specific legal provisions

#### 3. Anonymity and Attribution
- Attackers use **Tor, VPNs, proxy chains** to hide identity
- **Attribution** (proving who did it technically) is extremely difficult
- "Hackback" rights not defined — victims cannot legally retaliate

#### 4. Lack of Data Protection Law (Until DPDPA 2023)
- India lacked a comprehensive data protection law for 23 years after IT Act
- **DPDPA 2023** passed but implementation still underway
- No independent data protection regulator yet fully functional

#### 5. Digital Divide
- Large portions of Indian population lack digital literacy
- Online fraud, phishing victims often unaware of legal remedies
- Rural police stations lack cyber forensics capability

#### 6. Intermediary Liability Ambiguity
- Fine line between "active" and "passive" intermediary not always clear
- Safe harbour provisions can be misused to avoid accountability
- **Traceability requirement** (Rule 4(2), IT Rules 2021) vs. **end-to-end encryption** — unresolved conflict

#### 7. Encryption and Privacy Conflict
- Strong encryption protects privacy but also facilitates crime
- Government demands for **backdoors** in encryption conflict with privacy rights
- No definitive law on encryption standards or backdoor mandates

#### 8. Cybercrime Reporting Gap
- Most cybercrimes go **unreported** (fear of reputational damage, lack of awareness)
- Under-resourced cyber cells in police departments
- Low conviction rates in cybercrime cases

#### 9. No Specific Laws for
- Artificial Intelligence harms
- Deepfake content (other than general provisions)
- Cryptocurrency fraud (except DPDPA + PMLA indirect coverage)
- State-sponsored cyber attacks

#### 10. Sec. 66A Vacuum
- After Shreya Singhal struck down Sec. 66A, there is a **vacuum** for regulating genuinely harmful online speech that doesn't meet IPC defamation thresholds
- Many online harassment cases fall through the cracks

---

# 🔵 Part B — Security Policies, Standards & Compliance

---

## 9. Security Policies — Development & Implementation

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Every organization has rules — dress code, office timings, leave policy. A **Security Policy** is the **rulebook for information security** — it tells everyone what they can and cannot do with company data, systems, and networks. Without it, every employee makes their own decisions about security — chaos.

### 📖 What is a Security Policy?

> **An Information Security Policy** is a **formal document** that defines an organization's approach to protecting its information assets. It sets out **rules, responsibilities, and procedures** to be followed.

### 🔄 Types of Security Policies

| Type | Purpose | Example |
|---|---|---|
| **Acceptable Use Policy (AUP)** | What employees can/cannot do with IT | No personal browsing on company systems |
| **Access Control Policy** | Who can access what | Only HR can access payroll data |
| **Password Policy** | Rules for creating and managing passwords | Minimum 12 chars, changed every 90 days |
| **Data Classification Policy** | Categorizing data by sensitivity | Public, Internal, Confidential, Top Secret |
| **Incident Response Policy** | What to do when a breach occurs | Report within 1 hour, escalation chain |
| **BYOD Policy** | Rules for personal devices at work | Mandatory MDM installation |
| **Remote Work Policy** | Security rules for WFH | Only use company VPN |
| **Backup Policy** | How and when to back up data | Daily backups, 3-2-1 rule |
| **Encryption Policy** | When and how to encrypt data | All laptops must use full disk encryption |

### 🏗️ Development of Security Policy — Step by Step

```
STEP 1: IDENTIFY ASSETS
  → What data/systems need protection?
  → Inventory of hardware, software, data
          ↓
STEP 2: RISK ASSESSMENT
  → What threats exist? (hackers, insiders, disasters)
  → What are the vulnerabilities?
  → What is the impact if breached?
          ↓
STEP 3: DEFINE POLICY OBJECTIVES
  → Confidentiality, Integrity, Availability (CIA Triad)
  → Compliance requirements (law, regulations)
          ↓
STEP 4: DRAFT THE POLICY
  → Scope (who does it apply to?)
  → Roles and responsibilities
  → Specific rules and controls
  → Penalties for violations
          ↓
STEP 5: REVIEW & APPROVAL
  → Legal team review
  → Management approval
  → Stakeholder feedback
          ↓
STEP 6: IMPLEMENTATION
  → Training and awareness programs
  → Technical controls enforced
  → Dissemination to all employees
          ↓
STEP 7: MONITORING & REVIEW
  → Regular audits
  → Update policy as threats evolve
  → Annual review minimum
```

### 🔑 The CIA Triad — Foundation of Security Policy

```
         Confidentiality
              /\
             /  \
            /    \
           /  CIA \
          /  TRIAD \
         /──────────\
    Integrity ─── Availability
```

| Principle | Meaning | Example Control |
|---|---|---|
| **Confidentiality** | Only authorized people see data | Encryption, Access Control |
| **Integrity** | Data is accurate and unaltered | Hashing, Digital Signatures |
| **Availability** | Systems are accessible when needed | Backups, Redundancy, DDoS protection |

### 📌 Security Standards

> [!info] Key Security Standards

| Standard | Full Form | What it covers |
|---|---|---|
| **ISO/IEC 27001** | Information Security Management System | Framework for entire ISMS |
| **ISO/IEC 27002** | Code of Practice for Info Security | 114 controls in 14 domains |
| **NIST CSF** | NIST Cybersecurity Framework | Identify, Protect, Detect, Respond, Recover |
| **CIS Controls** | Center for Internet Security Controls | 18 prioritized security controls |
| **SOC 2** | Service Organization Control 2 | Cloud/SaaS security (US standard) |
| **OWASP** | Open Web Application Security Project | Web application security |

---

## 10. Compliance Frameworks — GDPR, HIPAA, PCI DSS

### 🟢 What is a Compliance Framework?

> [!abstract] Think of it like this…
> A compliance framework is like a **government-mandated safety inspection checklist** for information security. If you want to operate in certain industries or handle certain types of data, you must **prove** you meet the required security standards. Failing to comply means heavy **fines, lawsuits, or losing the licence to operate**.

---

### 🇪🇺 A. GDPR — General Data Protection Regulation

> [!info] What is GDPR?
> - **Full Form:** General Data Protection Regulation
> - **Enacted by:** European Union (EU)
> - **Effective:** 25 May 2018
> - **Applies to:** Any organization **anywhere in the world** that processes data of EU residents

#### 🔑 Key Principles of GDPR

| Principle | Simple Meaning |
|---|---|
| **Lawfulness, Fairness, Transparency** | You must have a legal reason to process data; tell people what you're doing |
| **Purpose Limitation** | Collect data only for the stated purpose |
| **Data Minimisation** | Collect only what you need |
| **Accuracy** | Keep data correct and up to date |
| **Storage Limitation** | Don't keep data longer than needed |
| **Integrity & Confidentiality** | Protect data with appropriate security |
| **Accountability** | You must be able to PROVE you comply |

#### 🔑 Rights of Data Subjects (Individuals) under GDPR

| Right | What it Means |
|---|---|
| **Right of Access** | You can ask any company what data they have about you |
| **Right to Rectification** | Ask them to correct wrong data |
| **Right to Erasure ("Right to be Forgotten")** | Ask them to delete your data |
| **Right to Data Portability** | Get your data in a usable format |
| **Right to Object** | Object to processing for marketing/profiling |
| **Right to Restriction** | Limit how they process your data |

#### 💰 GDPR Penalties

> [!danger] GDPR Fines
> - **Tier 1:** Up to **€10 million** OR **2% of global annual turnover** (whichever is higher)
> - **Tier 2:** Up to **€20 million** OR **4% of global annual turnover** (whichever is higher)
>
> **Famous Fines:**
> - Meta/Facebook: **€1.2 billion** (2023) — illegal data transfers to US
> - Amazon: **€746 million** (2021) — targeted advertising practices
> - Google: **€50 million** (2019) — lack of transparency

#### 🇮🇳 India & GDPR
> Indian companies serving EU customers **must comply with GDPR**. The Indian **DPDPA 2023** is India's equivalent framework.

---

### 🇺🇸 B. HIPAA — Health Insurance Portability and Accountability Act

> [!info] What is HIPAA?
> - **Full Form:** Health Insurance Portability and Accountability Act
> - **Enacted by:** United States Congress
> - **Effective:** 1996 (Privacy Rule 2003, Security Rule 2005)
> - **Applies to:** Covered Entities (hospitals, health insurers, clinicians) and Business Associates in the US healthcare sector

#### 🔑 HIPAA Key Rules

| Rule | What it Covers |
|---|---|
| **Privacy Rule** | Protects **PHI (Protected Health Information)** — who can access and share health data |
| **Security Rule** | **Electronic PHI (ePHI)** — technical, physical, administrative safeguards |
| **Breach Notification Rule** | Covered entities must notify patients of data breaches within **60 days** |
| **Enforcement Rule** | Investigation and penalties for violations |

> [!info] What is PHI (Protected Health Information)?
> Any information that can identify a patient AND relates to their health condition, treatment, or payment:
> - Name, address, date of birth
> - Medical records, diagnoses, prescriptions
> - Health insurance information
> - Lab results, imaging

#### 🔐 HIPAA Security Safeguards

```
ADMINISTRATIVE SAFEGUARDS
  → Designated Security Officer
  → Workforce training
  → Risk assessments
  → Access management

PHYSICAL SAFEGUARDS
  → Secure workstations
  → Device controls
  → Facility access controls

TECHNICAL SAFEGUARDS
  → Access controls (passwords, MFA)
  → Audit controls (logging)
  → Encryption of ePHI
  → Transmission security (TLS)
```

#### 💰 HIPAA Penalties

> [!danger] Penalty Tiers
> | Tier | Situation | Fine Per Violation |
> |---|---|---|
> | **1** | Unknowing violation | $100–$50,000 |
> | **2** | Reasonable cause (not wilful neglect) | $1,000–$50,000 |
> | **3** | Wilful neglect, corrected | $10,000–$50,000 |
> | **4** | Wilful neglect, not corrected | $50,000+ |
>
> Maximum: **$1.9 million per violation category per year**

#### 🇮🇳 HIPAA Relevance for India
> Indian IT/BPO companies handling US healthcare data (medical transcription, health tech, BPO for US hospitals) **must comply with HIPAA** as Business Associates.

---

### 💳 C. PCI DSS — Payment Card Industry Data Security Standard

> [!info] What is PCI DSS?
> - **Full Form:** Payment Card Industry Data Security Standard
> - **Issued by:** PCI Security Standards Council (Visa, Mastercard, Amex, Discover, JCB)
> - **Current Version:** PCI DSS v4.0 (2022)
> - **Applies to:** Any organization that **stores, processes, or transmits cardholder data** (credit/debit card info)

#### 🔑 Who Must Comply?

```
You accept card payments?
          ↓
You store card numbers?
          ↓
You process card transactions?
          ↓
You transmit cardholder data?
          ↓
→ YES → PCI DSS COMPLIANCE MANDATORY
```

#### 🔐 PCI DSS — 12 Requirements (v4.0)

> [!note] PCI DSS 12 Requirements

| # | Requirement | Simple Meaning |
|---|---|---|
| 1 | Install and maintain network security controls | Firewall to protect card data |
| 2 | Apply secure configurations to all system components | Change default passwords |
| 3 | Protect stored account data | Encrypt stored card numbers |
| 4 | Protect cardholder data during transmission | Use TLS/encryption in transit |
| 5 | Protect all systems against malware | Antivirus on all systems |
| 6 | Develop and maintain secure systems and software | Patch management, secure coding |
| 7 | Restrict access to cardholder data by business need | Least privilege access |
| 8 | Identify users and authenticate access | Strong authentication, no shared accounts |
| 9 | Restrict physical access to cardholder data | Physical security of card data locations |
| 10 | Log and monitor all access to system components | Audit logs, SIEM |
| 11 | Test security systems and processes regularly | Vulnerability scans, penetration testing |
| 12 | Support info security with organizational policies | Written security policy |

#### 💰 PCI DSS Non-Compliance Penalties

> [!danger] Consequences of Non-Compliance
> - Fines: **$5,000 to $100,000 per month** (from card brands)
> - Loss of ability to **process card payments**
> - Mandatory forensic investigation costs
> - Liability for **fraud losses** on compromised cards
> - Reputational damage

> [!example] Real Cases
> - **Heartland Payment Systems (2008):** 130 million card records stolen; fined $145 million
> - **Target (2013):** 40 million cards stolen via HVAC vendor; $18.5 million settlement

---

### 📊 Comparison — GDPR vs HIPAA vs PCI DSS

| Feature | GDPR | HIPAA | PCI DSS |
|---|---|---|---|
| **Origin** | EU | USA | Industry (PCI SSC) |
| **Data Type** | All personal data of EU residents | Health/medical data (PHI) | Payment card data |
| **Scope** | Global (if EU persons affected) | US healthcare entities + associates | Global (any card processing entity) |
| **Regulator** | Data Protection Authorities (DPAs) | US Dept. of Health & Human Services | Card brands + PCI SSC |
| **Legal Basis** | Regulation (law) | Federal statute | Contractual (merchant agreement) |
| **Max Fine** | €20 million / 4% turnover | $1.9M/year | Loss of card processing rights |
| **India Relevance** | Indian cos. with EU customers | Indian IT/BPO for US healthcare | All Indian card-accepting merchants |

---

## 11. Auditing, Assessment & Compliance Monitoring

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Having a security policy is like having traffic laws. **Auditing** is like traffic enforcement — checking whether the rules are actually being followed. Without audits, policies are just paper. Assessment identifies **gaps**. Monitoring ensures **continuous compliance**.

### 🔍 Security Audit

> [!info] What is a Security Audit?
> A **systematic examination** of an organization's information systems, policies, and procedures to determine whether they comply with:
> - Internal security policies
> - Regulatory requirements (GDPR, HIPAA, PCI DSS, IT Act)
> - Industry standards (ISO 27001, NIST)

#### Types of Security Audits

| Type | Description | Example |
|---|---|---|
| **Internal Audit** | Conducted by organization's own team | IT department reviews access logs monthly |
| **External Audit** | By independent third party | PCI QSA assesses payment system |
| **Compliance Audit** | Checks adherence to specific regulations | GDPR compliance audit |
| **Technical Audit** | Tests technical controls (VAPT) | Penetration testing of web apps |
| **Forensic Audit** | Post-incident investigation | After a data breach |

### 📋 Security Assessment — Risk Assessment Process

```
STEP 1: ASSET IDENTIFICATION
  → What assets (data, systems) need protection?
          ↓
STEP 2: THREAT IDENTIFICATION
  → What threats exist for each asset?
  → (Hackers, Insiders, Natural disasters, Human error)
          ↓
STEP 3: VULNERABILITY IDENTIFICATION
  → What weaknesses could be exploited?
  → (Unpatched software, weak passwords, misconfiguration)
          ↓
STEP 4: RISK CALCULATION
  → Risk = Likelihood × Impact
          ↓
STEP 5: RISK TREATMENT
  → Accept / Mitigate / Transfer / Avoid
          ↓
STEP 6: DOCUMENT & REPORT
  → Risk Register, Treatment Plan
```

### 🔑 Compliance Monitoring — Continuous vs Periodic

| Approach | Description | Tools |
|---|---|---|
| **Continuous Monitoring** | Real-time tracking of security controls | SIEM, IDS/IPS, UEBA |
| **Periodic Assessment** | Scheduled reviews (quarterly/annual) | Vulnerability scanners, audits |
| **Automated Compliance** | Tools that continuously check policy adherence | AWS Config, Azure Policy, Qualys |
| **Log Management** | Collecting and analyzing security logs | Splunk, ELK Stack, IBM QRadar |

### 📌 Key Compliance Monitoring Activities

> [!note] What to Monitor
> 1. **Access Logs** — Who is accessing what systems and when
> 2. **Change Management** — Unauthorized system configuration changes
> 3. **Patch Status** — Are all systems up to date?
> 4. **Incident Reports** — Number and nature of security incidents
> 5. **User Behaviour** — Unusual access patterns (UEBA)
> 6. **Third-party Compliance** — Vendors and partners meeting security requirements
> 7. **Data Flows** — Is personal/sensitive data being transferred appropriately?
> 8. **Training Completion** — Are employees completing security awareness training?

### 🏆 Audit Reports & Documentation

> [!tip] Key Deliverables from Security Audits
> - **Audit Report** — Findings, gaps, recommendations
> - **Risk Register** — Documented risks with treatment status
> - **Compliance Matrix** — Requirement-by-requirement compliance status
> - **Remediation Plan** — Timeline for fixing identified gaps
> - **Evidence Package** — Screenshots, logs, policy documents proving compliance

---

## 🗒️ Quick Revision Summary

> [!summary] Unit III — Key Takeaways at a Glance

| Topic | One-liner |
|---|---|
| **Sec. 43** | Civil compensation up to ₹1 crore for unauthorized access/damage |
| **Sec. 43A** | Body corporate liable for SPDI breach due to negligence |
| **Sec. 65** | Tampering source code — 3 yrs OR ₹2L |
| **Sec. 66** | Hacking — 3 yrs OR ₹5L |
| **Sec. 66F** | Cyber terrorism — Life imprisonment |
| **Sec. 67B** | CSAM — 5 yrs (1st), 7 yrs (repeat) |
| **Sec. 70** | Unauthorized access to Protected System — 10 yrs |
| **Sec. 79** | Safe harbour for intermediaries — if passive + due diligence + prompt takedown |
| **Sec. 69A** | Blocking — national security; 7 yrs for non-compliance |
| **Sec. 69** | Interception — national security; 7 yrs for non-assistance |
| **Sec. 69B** | Traffic data monitoring — cyber security; 3 yrs for non-assistance |
| **Sec. 70A** | NCIIPC — nodal agency for Critical Infrastructure Protection |
| **Sec. 70B** | CERT-In — national cyber emergency response; 6-hour reporting |
| **Shreya Singhal** | Sec. 66A struck down — free speech |
| **Avnish Bajaj** | Intermediary liability — no personal arrest if no knowledge |
| **Cyber Law Limitations** | Jurisdiction, encryption, anonymity, tech outpacing law, attribution |
| **CIA Triad** | Confidentiality + Integrity + Availability — foundation of security policy |
| **GDPR** | EU data protection; €20M / 4% turnover fine; applies to Indian cos. with EU users |
| **HIPAA** | US health data; PHI protection; applies to Indian IT/BPO handling US health data |
| **PCI DSS** | Payment card security; 12 requirements; applies to all card-accepting merchants |
| **Security Audit** | Internal/External/Compliance/Technical/Forensic |
| **Compliance Monitoring** | Continuous (SIEM) + Periodic (audits) + Automated (cloud compliance tools) |

---

## 📝 Previous Year Question Patterns

> [!question] Likely Exam Questions

1. Explain all offences under Chapter XI of the IT Act, 2000 with their punishments.
2. What is the safe harbour protection for intermediaries under Section 79? When is it lost?
3. Discuss the powers of the Central Government to block, intercept, and monitor under Sections 69, 69A, and 69B.
4. What is CERT-In? Explain its functions and the significance of the CERT-In Directions 2022.
5. What is Critical Information Infrastructure? Explain Section 70 and the role of NCIIPC.
6. Discuss the limitations of cyber law in India.
7. Write a detailed note on the GDPR with its key principles, rights, and penalties.
8. What is HIPAA? Explain its applicability to Indian IT companies.
9. Explain PCI DSS compliance requirements. Who must comply?
10. What is a security audit? Distinguish between types of audits and explain the compliance monitoring process.
11. Discuss the Shreya Singhal and Avnish Bajaj cases and their impact on cyber law in India.
12. What is a Security Policy? Explain its development and implementation process.

---

## 🔗 Related Notes

- [[Paper 204 - Unit I — Introduction to Cyberspace]]
- [[Paper 204 - Unit II — Regulatory Framework]]
- [[Paper 204 - Unit IV]]
- [[CERT-In Directions 2022]]
- [[DPDPA 2023 — Data Protection India]]
- [[ISO 27001 — ISMS Framework]]
- [[VAPT Methodology — Compliance Testing]]

---

*📌 Maintained by Cywarx | University of Delhi — PGDCSL | Semester 2*
