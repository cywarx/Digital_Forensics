---
title: "Paper 204 – Unit II: Regulatory Framework of the IT Act, 2000"
course: "Post Graduate Diploma in Cyber Security and Law"
university: "University of Delhi"
semester: "Semester 2"
paper: "Paper 204 – Cyber Law and Forensic Evidence"
unit: "Unit II"
tags:
  - cyber-law
  - IT-Act-2000
  - digital-signature
  - electronic-evidence
  - BSA-2023
  - certifying-authority
  - DU
  - semester-2
  - paper-204
created: 2025-01-01
status: complete
---

# 📘 Unit II — Regulatory Framework of the IT Act, 2000

> [!info] 📌 Course Details
> **Course:** Post Graduate Diploma in Cyber Security and Law
> **University:** University of Delhi | **Semester:** 2
> **Paper:** 204 — Cyber Law and Forensic Evidence

---

## 🗂️ Table of Contents

- [[#1. Digital Signature]]
- [[#2. Electronic Signature]]
- [[#3. Reliable Electronic Signature]]
- [[#4. Secured Electronic Signature]]
- [[#5. Electronic Records]]
- [[#6. Electronic Governance]]
- [[#7. Controller of Certifying Authorities (CCA)]]
- [[#8. Certifying Authority (CA)]]
- [[#9. Adjudicating Officer]]
- [[#10. Appellate Tribunal (Cyber Appellate Tribunal)]]
- [[#11. Rules Announced Under the IT Act]]
- [[#12. Electronic Evidence — Power to Investigate & Expert Opinion]]
- [[#13. Admissibility of Electronic Evidence — BSA 2023]]
- [[#Quick Revision Summary]]

---

## 1. Digital Signature

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Imagine you sign a paper document with your **handwritten signature** to prove it came from you. A **Digital Signature** does the same thing — but for **electronic documents** like PDFs, emails, contracts.
>
> It proves:
> - ✅ **Who** sent the document (Authentication)
> - ✅ The document was **not changed** after signing (Integrity)
> - ✅ The sender **cannot deny** sending it (Non-repudiation)

### 📖 Legal Definition

> **Section 2(1)(p) — IT Act, 2000**
> A Digital Signature means "authentication of any electronic record by a subscriber by means of an **electronic method or procedure** in accordance with the provisions of **Section 3**."

Under **Section 3**, digital signatures use an **Asymmetric Crypto System** — a pair of mathematically related keys:

```
SENDER (Ankit)                          RECEIVER (Bank)
─────────────                           ───────────────
Has: Private Key 🔐                     Has: Ankit's Public Key 🔓
     (Secret, only Ankit has it)              (Available to everyone)

Step 1: Ankit signs the document with his PRIVATE KEY
Step 2: Creates a "hash" (unique fingerprint) of the document
Step 3: Encrypts the hash with Private Key → This is the Digital Signature
Step 4: Sends document + Digital Signature to Bank
Step 5: Bank uses Ankit's PUBLIC KEY to decrypt the signature
Step 6: Bank generates hash of received document
Step 7: If both hashes MATCH → ✅ Authentic & Unmodified
```

### 🔑 Key Technical Concepts

| Concept | Simple Explanation | Technical Term |
|---|---|---|
| **Private Key** | Your secret password for signing | Used to ENCRYPT the hash |
| **Public Key** | Shared openly for verification | Used to DECRYPT the hash |
| **Hash Function** | Creates a unique "fingerprint" of the document | SHA-256, MD5 |
| **Key Pair** | Private + Public key together | Asymmetric Key Pair |
| **Certificate** | Proof that the Public Key belongs to you | Digital Signature Certificate (DSC) |

### ⚖️ Legal Validity — IT Act, 2000

> [!important] Section 5 — Legal Recognition
> **Where any law provides that information shall be authenticated by affixing a signature**, such requirement is satisfied if the information is authenticated by means of a **Digital Signature** in the manner prescribed.
>
> → A digital signature has the **same legal standing as a handwritten signature**.

> [!example] Real Life Uses
> - **Income Tax Returns** — filed with Digital Signature
> - **Company incorporation** — MCA21 uses DSC
> - **Government tenders** — e-procurement portals
> - **Banking** — digitally signed loan agreements
> - **Court filings** — e-filing with DSC

---

## 2. Electronic Signature

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> A **Digital Signature** is like using a **special seal** with a private key. An **Electronic Signature** is a **broader concept** — it includes ANY electronic method used to sign documents.
>
> Examples of Electronic Signatures:
> - Typing your name at the end of an email — ✅ Electronic Signature
> - Clicking "I Agree" on a website — ✅ Electronic Signature
> - Using Aadhaar OTP to sign — ✅ Electronic Signature (e-Sign)
> - Drawing your signature on a tablet — ✅ Electronic Signature
> - Using a Digital Signature Certificate — ✅ Digital Signature (also an Electronic Signature)

### 📖 Legal Definition

> **Section 2(1)(ta) — IT (Amendment) Act, 2008**
> "Electronic Signature" means authentication of any electronic record by a subscriber by means of the **electronic technique** specified in the **Second Schedule** and includes **Digital Signature**.

> [!tip] Simple Rule
> **Digital Signature ⊂ Electronic Signature**
> All Digital Signatures are Electronic Signatures, but NOT all Electronic Signatures are Digital Signatures.

### 🔄 Digital Signature vs Electronic Signature

| Feature | Digital Signature | Electronic Signature |
|---|---|---|
| **Technology** | Asymmetric cryptography (PKI) | Any electronic method |
| **Security** | Very high | Varies (low to high) |
| **Legal basis** | Sec. 3 + First Schedule | Sec. 3A + Second Schedule |
| **Certificate needed?** | Yes (DSC from CA) | Not always |
| **Examples** | DSC on MCA21, IT returns | OTP-based e-Sign, click-wrap |
| **Introduced** | IT Act 2000 | IT Amendment Act 2008 |

---

## 3. Reliable Electronic Signature

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Not every electronic signature is trustworthy. A **Reliable Electronic Signature** is one that meets certain **minimum standards of security** to ensure it is genuinely linked to the signer and the data.

### 📖 Legal Basis — Section 3A, IT Act

An Electronic Signature is considered **reliable** if:

> [!note] Four Conditions (Section 3A)
> 1. The **signature creation data** is linked only to the signatory
> 2. The data was under the **sole control of the signatory** at the time of signing
> 3. Any **alteration to the signature** after signing is detectable
> 4. Any **alteration to the data** after signing is detectable

> [!example] Simple Example
> Pooja signs a contract using Aadhaar OTP e-Sign.
> - The OTP is linked only to her Aadhaar (linked to her)
> - Only she received the OTP on her registered phone (sole control)
> - If the contract PDF is modified after signing, the signature becomes invalid (alteration detectable)
> → This is a **Reliable Electronic Signature** ✅

---

## 4. Secured Electronic Signature

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> A **Secured Electronic Signature** is the **highest level** of electronic signature — it has been verified to be completely tamper-proof and reliably linked to the signer using additional security procedures.

### 📖 Legal Basis — Section 15, IT Act

> [!note] Section 15 — Secure Electronic Signature
> An Electronic Signature shall be deemed to be a **secure electronic signature** if:
> 1. The **signature creation data** at the time of signing was **unique** to the signatory
> 2. It was capable of identifying the signatory
> 3. It was created in a manner under the **sole control** of the signatory
> 4. It is **linked to the electronic record** in a way that detects any subsequent alteration

### Hierarchy of Signatures

```
Electronic Signature (broadest — any electronic authentication)
        ↑
Reliable Electronic Signature (meets Section 3A conditions)
        ↑
Secure Electronic Signature (meets Section 15 + highest assurance)
        ↑
Digital Signature (specific PKI-based implementation)
```

---

## 5. Electronic Records

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Any document, data, or information that exists in **electronic/digital form** is an Electronic Record.
>
> - A Word document saved on your laptop → ✅ Electronic Record
> - An email in your inbox → ✅ Electronic Record
> - A WhatsApp chat screenshot → ✅ Electronic Record
> - A scanned copy of a paper document → ✅ Electronic Record
> - A database entry in a bank server → ✅ Electronic Record

### 📖 Legal Definition

> **Section 2(1)(t) — IT Act, 2000**
> "Electronic Record" means data, record or data generated, **image or sound stored, received or sent in an electronic form** or micro film or computer generated micro fiche.

### ⚖️ Legal Recognition of Electronic Records

| Section | What it Says | Simple Meaning |
|---|---|---|
| **Sec. 4** | Legal recognition of electronic records | A digital document is as valid as a paper document |
| **Sec. 6** | Use of electronic records in Government | Govt. can accept forms/applications electronically |
| **Sec. 7** | Retention of electronic records | Electronic records can substitute paper records for retention |
| **Sec. 8** | Publication of rules in electronic gazette | Official Gazette can be published electronically |

### 📌 Conditions for Electronic Record Retention (Sec. 7)

> [!note] Three Conditions
> 1. Information must be **accessible** for future reference
> 2. Stored in the **format** in which it was generated/sent/received (or in a format that can be demonstrated to accurately represent it)
> 3. Details about **origin, destination, date and time** of sending/receiving must be retained

> [!example] Practical Example
> A bank sends you a loan sanction letter by email. Under Sec. 7:
> - The bank must store this email (accessible)
> - In its original format or accurate representation
> - With metadata showing when it was sent and to whom
> → This is valid retention of an electronic record ✅

---

## 6. Electronic Governance

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> **Electronic Governance (e-Governance)** means the government providing its **services, information, and communication electronically** — instead of making you stand in long queues at government offices.
>
> Instead of going to an office to file your income tax → you do it on the **Income Tax Portal**
> Instead of mailing a physical application for a passport → you apply on **Passport Seva Portal**

### 📖 Legal Basis — Chapter III (Sections 4–10A)

| Section | Subject | Simple Meaning |
|---|---|---|
| **Sec. 4** | Legal recognition of electronic records | Digital docs = Paper docs in law |
| **Sec. 5** | Legal recognition of digital signatures | Digital sign = Handwritten sign |
| **Sec. 6** | Use of electronic records in Govt. | Govt. can accept digital forms/filings |
| **Sec. 6A** | Delivery of services by service providers | Private parties can deliver govt. services digitally |
| **Sec. 7** | Retention of electronic records | Digital storage = Physical storage |
| **Sec. 7A** | Audit of documents etc. maintained electronically | Digital documents can be audited |
| **Sec. 8** | Publication of rules in electronic gazette | E-gazette is official |
| **Sec. 9** | No mandatory use of electronic records | Govt. cannot FORCE digital-only access |
| **Sec. 10** | Power to make rules for digital signatures | Central Govt. can regulate |
| **Sec. 10A** | Validity of contracts formed electronically | Online contracts are valid |

> [!example] Real-World e-Governance Examples (India)
> | Portal | Service |
> |---|---|
> | **DigiLocker** | Digital documents (Aadhaar, driving license, marksheets) |
> | **IRCTC** | Railway ticket booking |
> | **MCA21** | Company registration, annual filings |
> | **GST Portal** | Tax filing and returns |
> | **UMANG App** | Unified govt. service delivery |
> | **e-Court Services** | Online case status, e-filing |
> | **Passport Seva** | Passport application online |

> [!tip] Key Point for Exam
> **Section 9** is important — it says the government CANNOT compel a person to use electronic means exclusively. Physical options must still exist.

---

## 7. Controller of Certifying Authorities (CCA)

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> Imagine there are multiple banks issuing currency notes. You need a **Reserve Bank of India (RBI)** to regulate all these banks and ensure the currency is genuine. Similarly, many companies issue **Digital Signature Certificates (DSC)**. The **Controller of Certifying Authorities (CCA)** is the regulatory authority that oversees all of them — like an RBI for digital signatures.

### 📖 Legal Basis — Section 17, IT Act, 2000

> **Section 17** — The Central Government may appoint a **Controller of Certifying Authorities (CCA)** and as many Deputy Controllers and Assistant Controllers as it deems fit.

### 🏛️ Powers and Functions of CCA

> [!note] Functions of Controller (Section 18)
> The Controller may perform all or any of the following functions:
>
> 1. **Exercising supervision** over Certifying Authorities
> 2. **Certifying public keys** of Certifying Authorities
> 3. **Laying down standards** to be maintained by Certifying Authorities
> 4. **Specifying** the qualifications and experience of employees of CAs
> 5. **Specifying** conditions under which CAs shall conduct their business
> 6. **Specifying** the content and form of Digital Signature Certificates
> 7. **Specifying** security procedures for operation of secure systems
> 8. **Resolving conflicts** of interests between CAs and subscribers
> 9. **Maintaining** a database of public keys (publicly accessible)

### 🔑 Key Powers

| Power | Section | Description |
|---|---|---|
| **Issue License** | Sec. 21 | Grant licence to Certifying Authorities |
| **Suspend/Revoke CA** | Sec. 25 | Suspend or revoke CA's licence |
| **Issue Directions** | Sec. 68 | Direct any person to intercept/block information |
| **Investigate** | Sec. 28 | Access any system operated by CA |
| **Recognize Foreign CAs** | Sec. 19 | Recognize digital signatures of foreign CAs |

> [!info] Current CCA
> The **Controller of Certifying Authorities (CCA)** operates under the **Ministry of Electronics & Information Technology (MeitY)**, Government of India.
> Website: **cca.gov.in**
>
> Licensed CAs in India include: eMudhra, NSDL, Sify, CDAC, NIC, IDRBT

---

## 8. Certifying Authority (CA)

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> When you buy a product and see the **ISI mark**, you trust that the product meets quality standards. A **Certifying Authority (CA)** is like the organization that puts an "ISI mark" on digital identities.
>
> It issues a **Digital Signature Certificate (DSC)** which says:
> "We have verified that this Public Key truly belongs to **Ankit Ojha** — you can trust it."

### 📖 Legal Definition

> **Section 2(1)(g) — IT Act, 2000**
> "Certifying Authority" means a person who has been **granted a licence** to issue a Digital Signature Certificate under **Section 24**.

### 📋 Licence to Issue DSC — Section 21

> [!note] Requirements to Get CA Licence (Section 21)
> Any person can apply to the Controller for a CA licence. They must:
> 1. Fulfill the qualifications and experience prescribed
> 2. Demonstrate adequate infrastructure (servers, security)
> 3. Comply with the procedures of the Controller
> 4. Pay the prescribed fee

### 🔄 How a CA Issues a Digital Signature Certificate

```
SUBSCRIBER (e.g., Ankit) applies to CA (e.g., eMudhra)
          ↓
Submits identity proof (Aadhaar, PAN, documents)
          ↓
CA verifies identity (in-person or video KYC)
          ↓
CA generates Key Pair (or subscriber generates it)
          ↓
CA issues Digital Signature Certificate (DSC)
          ↓
DSC contains: Subscriber's Name + Public Key + CA's Digital Signature + Validity Period
          ↓
Subscriber uses Private Key to sign documents
          ↓
Receiver uses Subscriber's Public Key (from DSC) to verify
```

### 📌 Duties of Certifying Authorities (Section 30–34)

> [!note] Key Duties
> | Section | Duty |
> |---|---|
> | **Sec. 30** | Disclose its practices in a **Certification Practice Statement (CPS)** |
> | **Sec. 31** | Maintain security procedures and practices |
> | **Sec. 32** | Keep records of all issued certificates |
> | **Sec. 33** | Disclose information to the Controller if required |
> | **Sec. 34** | Ensure reliable **Trusted System** |

### 📜 Digital Signature Certificate (DSC)

> [!info] Contents of a DSC (Section 35)
> A Digital Signature Certificate must specify:
> - Public key of the subscriber
> - Name and address of the subscriber
> - Name of the Certifying Authority
> - Digital Signature of the CA
> - Validity period (start and end dates)
> - Serial number of the certificate

> [!example] Types of DSC in India
> | Class | Who Uses | Purpose |
> |---|---|---|
> | **Class 1** | Individuals | Low assurance, email verification |
> | **Class 2** | Individuals/Companies | IT returns, ROC filing (phased out 2021) |
> | **Class 3** | High-value transactions | e-Tendering, e-Auctions, high-security filings |
> | **DGFT** | Exporters/Importers | DGFT portal filings |

### ❌ Suspension & Revocation of DSC

| Action | Section | Ground |
|---|---|---|
| **Suspension by CA** | Sec. 37 | If subscriber requests, or CA has reason to believe DSC was issued incorrectly |
| **Revocation by CA** | Sec. 38 | Death of subscriber, company dissolved, private key compromised |
| **Suspension by Controller** | Sec. 25 | If CA's licence is suspected to be misused |

---

## 9. Adjudicating Officer

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> If someone causes you financial loss by hacking your computer, you cannot always go to a full criminal court for small disputes. The **Adjudicating Officer** is like a **special government judge** who handles **civil disputes and compensation claims** related to IT Act violations — quickly and without heavy court procedures.

### 📖 Legal Basis — Section 46, IT Act, 2000

> **Section 46** — The Central Government shall appoint any officer **not below the rank of a Director** to the Central Government to be an **Adjudicating Officer** for holding an enquiry into contravention of any provisions of the IT Act.

### 🔑 Jurisdiction and Powers

> [!note] Powers of Adjudicating Officer
> | Power | Description |
> |---|---|
> | **Summon** | Call any person to give evidence |
> | **Examine on oath** | Take sworn statements |
> | **Compel document production** | Ask for any electronic or physical records |
> | **Award compensation** | Award up to **₹5 crore** in disputes |
> | **Impose penalty** | Penalize contraventions of the IT Act |

### 📋 Matters Handled by Adjudicating Officer

> [!example] Types of Cases
> - Someone hacked your website — claim compensation (Sec. 43)
> - A company failed to protect your personal data (Sec. 43A)
> - Unauthorized interception of data
> - Denial of service attacks causing loss

> [!warning] Limit of Jurisdiction
> If the **claim amount exceeds ₹5 crore**, the matter goes directly to a **competent court** and NOT to the Adjudicating Officer.

### 🏛️ Procedure

```
Complaint filed by aggrieved person
          ↓
Adjudicating Officer issues notice to accused
          ↓
Hearing — both parties present their case
          ↓
Officer examines evidence (electronic records, logs)
          ↓
Order passed — compensation/penalty awarded
          ↓
Appeal → Cyber Appellate Tribunal (within 45 days)
```

---

## 10. Appellate Tribunal (Cyber Appellate Tribunal)

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> If you are unhappy with the decision of the **Adjudicating Officer**, you can **appeal** to a higher authority. The **Cyber Appellate Tribunal (CyAT)** is that higher body — like a specialized **appellate court** for IT disputes.

### 📖 Legal Basis — Section 48, IT Act, 2000

> **Section 48** — The Central Government shall establish one or more appellate tribunals to be known as the **Cyber Appellate Tribunal (CyAT)**.

### 🔑 Composition

> [!note] Who Sits on the CyAT?
> - **Presiding Officer** — Person qualified to be a judge of a High Court
> - Appointed by the **Central Government**
> - Serves for **5 years** or until age **65**, whichever is earlier

### ⚖️ Jurisdiction and Powers

| Power | Description |
|---|---|
| **Hear appeals** | Against Adjudicating Officer orders |
| **Hear appeals** | Against Controller's orders (Sec. 24, 25) |
| **Summon** | Call parties and witnesses |
| **Civil court powers** | Discovery, inspection, examination of witnesses |
| **Pass interim orders** | Stay execution during appeal |

### 🔄 Appeal Process

```
Adjudicating Officer / Controller passes Order
          ↓
Aggrieved party files appeal to CyAT
(within 45 days of receiving order — extendable for sufficient cause)
          ↓
CyAT hears both parties
          ↓
CyAT passes order (confirm / modify / set aside)
          ↓
Further appeal → HIGH COURT (on question of law)
          ↓
Supreme Court (final)
```

> [!tip] Important for Exam
> - Appeal to CyAT: within **45 days**
> - Further appeal from CyAT: **High Court** (not Sessions Court)
> - No court below High Court can entertain appeals from CyAT

### 📌 CyAT vs Regular Court

| Feature | Cyber Appellate Tribunal | Civil/Criminal Court |
|---|---|---|
| **Nature** | Quasi-judicial tribunal | Court of law |
| **Procedure** | Simpler, faster | Formal court procedure |
| **Jurisdiction** | IT Act disputes only | General civil/criminal |
| **Appeal from** | Adjudicating Officer | Trial Court |
| **Appeal to** | High Court | High Court |

---

## 11. Rules Announced Under the IT Act

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> The IT Act is like a **Constitution** for cyber law — it sets the broad framework. The **Rules** are like the **Bye-Laws** — they give specific details on HOW to implement the Act.

### 📋 Major Rules Under IT Act, 2000

> [!note] Important Rules and Their Purpose

| Rule | Year | Key Purpose |
|---|---|---|
| **IT (Certifying Authorities) Rules** | 2000 | Licensing, operations, standards for CAs |
| **IT (Security Procedure) Rules** | 2004 | Procedures for secure electronic records and signatures |
| **IT (Reasonable Security Practices & Procedures) Rules** | 2011 | Data protection by body corporates — **SPDI Rules** |
| **IT (Intermediaries Guidelines) Rules** | 2011 | Duties of intermediaries (ISPs, websites) |
| **IT (Electronic Service Delivery) Rules** | 2011 | Electronic delivery of government services |
| **IT (Guidelines for Cyber Café) Rules** | 2011 | Regulation of cyber cafes |
| **IT (Intermediary Guidelines & Digital Media Ethics Code) Rules** | 2021 | Updated rules for social media, OTT, digital news |

---

### 🔑 Most Important Rules (Detail)

#### A. IT (SPDI) Rules, 2011 — Data Protection

> [!important] Sensitive Personal Data or Information (SPDI)
> Under Rule 3, **SPDI** includes:
> - Passwords
> - Financial information (bank account, credit card details)
> - Physical, physiological and mental health conditions
> - Sexual orientation
> - Medical records and history
> - Biometric data

**Obligations on Body Corporates:**
1. Must have a **Privacy Policy**
2. Obtain **written consent** before collecting SPDI
3. Collect only for **lawful purpose**
4. Allow **review and withdrawal** of consent
5. Maintain **reasonable security practices** (ISO 27001 recommended)
6. Liability under **Sec. 43A** if SPDI is not protected

---

#### B. IT (Intermediary Guidelines) Rules, 2021

> [!note] Who is an Intermediary?
> Any platform that transmits, stores, or hosts third-party content:
> - Social media (Facebook, Twitter/X, Instagram)
> - Search engines (Google)
> - E-commerce (Amazon, Flipkart)
> - ISPs, Cloud providers, Messaging apps (WhatsApp)

**Key Obligations:**
| Obligation | Requirement |
|---|---|
| **Publish Rules** | Publish privacy policy, user agreements, community standards |
| **Takedown** | Remove unlawful content within **36 hours** of court/government order |
| **Grievance Officer** | Appoint a grievance officer (resident in India for significant platforms) |
| **Traceability** | Significant Social Media Intermediaries (SSMIs) must trace origin of messages |
| **User Verification** | Voluntary user verification mechanism |

> [!example] Significant Social Media Intermediary (SSMI)
> Platforms with **50 lakh+ registered users** in India (e.g., WhatsApp, Facebook, Twitter/X, YouTube, Instagram) have additional obligations under the 2021 Rules:
> - Chief Compliance Officer (Indian resident)
> - Nodal Contact Person (Indian resident)
> - Resident Grievance Officer

---

## 12. Electronic Evidence — Power to Investigate & Expert Opinion (IT Act)

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> When a cybercrime happens, police need to **collect, preserve, and present digital evidence** in court. The IT Act gives specific powers to investigators and requires **expert opinion** to understand technical evidence — because judges aren't always tech experts.

### 🔍 Power to Investigate — IT Act Provisions

#### Section 78 — Power to Investigate

> **Section 78** — Notwithstanding anything in the Code of Criminal Procedure, 1973, a police officer not below the rank of **Inspector** shall investigate any offence under the IT Act.

> [!tip] Why is this important?
> Before this provision, any Sub-Inspector could investigate cases. Sec. 78 ensures that **only Inspectors or above** handle cyber offence investigations — ensuring better expertise.

#### Section 79A — Electronic Evidence Examiner

> [!important] Section 79A (inserted by IT Amendment Act, 2008)
> The Central Government may, for the purposes of providing **expert opinion** on electronic form evidence before any court or other authority, **notify any department, body or agency of the Central or State Government** as an **Examiner of Electronic Evidence**.
>
> → The opinion of such an Examiner shall be **admissible in evidence**.

> [!example] Notified Examiners of Electronic Evidence
> The Central Government has notified:
> - **CERT-In** (Computer Emergency Response Team – India)
> - **CDAC** (Centre for Development of Advanced Computing)
> - **CBI (Cyber Division)**
> - State Forensic Science Laboratories (FSLs) — some states
>
> These bodies can provide **expert opinion** in court on digital evidence.

### 🔬 Investigation of Electronic Evidence — Key Steps

```
CRIME REPORTED (e.g., hacking, online fraud)
          ↓
FIR registered at Cyber Crime Police Station
          ↓
Inspector (minimum rank) takes up investigation (Sec. 78)
          ↓
COLLECTION OF DIGITAL EVIDENCE:
  • Seizure of devices (phones, laptops, servers)
  • Forensic image/clone of storage media
  • Preservation of metadata and logs
  • Hash values (MD5/SHA-256) calculated
          ↓
EXPERT EXAMINATION:
  • Sent to notified Examiner (Sec. 79A)
  • Forensic analysis performed
  • Expert report prepared
          ↓
COURT SUBMISSION:
  • Electronic evidence presented
  • Expert opinion filed as Section 79A report
  • Admissibility determined under BSA 2023
```

### 📌 Key Principles of Digital Evidence Handling

> [!warning] Four Core Principles (ACPO Guidelines — widely followed)
> 1. **No action shall change digital evidence** — original data must not be altered
> 2. **Competent person for original access** — only trained personnel should access original evidence
> 3. **Audit trail** — complete record of all processes applied to digital evidence must be maintained
> 4. **Person in charge bears overall responsibility** — Investigation officer is responsible

---

## 13. Admissibility of Electronic Evidence — BSA, 2023

### 🟢 What is it? (Simple Explanation)

> [!abstract] Think of it like this…
> A WhatsApp message, a banking transaction log, an email — these are all **digital evidence**. But can a judge accept them in court? The **Bharatiya Sakshya Adhiniyam (BSA), 2023** — which replaced the **Indian Evidence Act, 1872** — governs exactly **when and how electronic evidence is admissible** in Indian courts.

### 📖 Background

> [!info] BSA 2023 — What Changed?
> The **Bharatiya Sakshya Adhiniyam, 2023** replaced the **Indian Evidence Act, 1872** (IEA) with effect from **1 July 2024**.
>
> Key improvements over IEA for electronic evidence:
> - Broader definition of electronic records
> - More structured admissibility conditions
> - Explicit inclusion of electronic and digital records
> - Updated certificate requirements

### 📋 Electronic Evidence under BSA, 2023

#### Section 57 — Documents in Evidence (BSA 2023)
Corresponds to **Section 3** of IEA — "Documents" now explicitly includes:

> [!note] Definition of "Document" under BSA 2023
> Includes any matter expressed or described upon any substance by means of letters, figures, or marks — AND also includes:
> - **Electronic records**
> - **Server logs**
> - **Digital data**
> - **Emails, messages, websites**
> - **Information stored in electronic form**

#### Section 61 — Admissibility of Electronic Records (BSA 2023)

> **Section 61 BSA 2023** (previously **Section 65B IEA**):
> All documents, including **electronic records**, may be proved in accordance with the provisions of this Act.

#### Section 63 — Admissibility Conditions (Certificate Requirement)

This is the **most critical provision** for electronic evidence admissibility.

> [!important] Section 63 BSA 2023 — The Certificate Requirement
> An **electronic record** is admissible as evidence **only if** accompanied by a certificate that:
>
> 1. **Identifies** the electronic record containing the statement
> 2. **Describes** the manner in which the electronic record was produced
> 3. **Gives particulars** of the device involved in the production of the record
> 4. **Certifies** that the device was operating properly, OR if not, that it did not affect the electronic record
> 5. Is **signed by a responsible official** who has authority over the device
>
> This certificate is treated as **evidence of the facts stated therein**.

### 🔄 BSA 2023 vs Indian Evidence Act, 1872

| Aspect | IEA 1872 (Old) | BSA 2023 (New) |
|---|---|---|
| **Electronic evidence section** | Section 65B | Section 63 |
| **Certificate requirement** | Section 65B(4) certificate | Section 63 certificate |
| **Digital records definition** | Section 3 (amended) | Section 57 (broader) |
| **Original document rule** | Primary/Secondary distinction | Simplified |
| **Devices covered** | "Computer output" | Broader — all electronic devices |

### ⚖️ Key Case Laws on Electronic Evidence

> [!example] Important Case Laws

**1. Anvar P.V. v. P.K. Basheer (2014) — Supreme Court**
- A Section 65B certificate is **mandatory** for admissibility of electronic evidence
- Without the certificate, electronic evidence is **inadmissible**
- Overruled earlier position that allowed secondary evidence without certificate

**2. Shafhi Mohammad v. State of Himachal Pradesh (2018) — Supreme Court**
- A **relaxation** — certificate not always mandatory if the party seeking to produce evidence **does not own the device**
- Court said strict application of 65B may cause injustice

**3. Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) — Supreme Court (3-judge bench)**
- Settled the conflict between Anvar and Shafhi Mohammad
- **65B certificate IS mandatory**
- However, court can **direct the concerned person to provide** the certificate
- Clarified: certificate needed at the **time of production of evidence** in court, NOT necessarily at the time of seizure

> [!tip] Post-BSA 2023 Position
> The same principles apply under **Section 63 BSA 2023**. The certificate requirement continues to be mandatory for electronic evidence to be admissible.

### 📌 Types of Electronic Records Commonly Produced as Evidence

| Type | Example | Admissibility Issues |
|---|---|---|
| **Emails** | Phishing evidence, communication logs | Certificate from email server admin required |
| **WhatsApp/Chats** | Threat messages, contracts | Screenshot + Sec. 63 certificate |
| **CCTV Footage** | Location evidence | Continuity of recording, storage integrity |
| **Bank Logs** | Financial fraud trail | Bank's authorized officer certificate |
| **Website logs** | Hacking traces, access records | Server admin certificate |
| **Mobile call records** | CDR (Call Detail Records) | Telecom operator's certificate |
| **Social media posts** | Defamation, evidence of crime | Platform operator or printout + certificate |
| **GPS/Location data** | Alibi evidence, tracking | Device manufacturer / service provider |

> [!warning] Common Mistakes in Electronic Evidence
> 1. **Not taking hash values** — original + copy can't be verified as identical
> 2. **No chain of custody** — evidence loses credibility
> 3. **Forgetting the certificate** — evidence becomes inadmissible
> 4. **Working on original** — always work on a forensic clone, never the original
> 5. **Metadata alteration** — accessing a file changes its "last accessed" timestamp

---

## 🗒️ Quick Revision Summary

> [!summary] Unit II — Key Takeaways at a Glance

| Topic | One-liner |
|---|---|
| **Digital Signature** | PKI-based authentication using Private-Public key pair; Sec. 3 IT Act |
| **Electronic Signature** | Broader term — any electronic authentication method; Sec. 3A IT Act |
| **Reliable e-Signature** | Meets 4 conditions of Sec. 3A — linked to signatory, sole control, alteration detectable |
| **Secure e-Signature** | Highest assurance — Sec. 15; unique, identifies signatory, sole control, detects alteration |
| **Electronic Record** | Sec. 2(1)(t) — any data/image/sound stored/sent electronically |
| **e-Governance** | Secs. 4–10A — digital filing, e-gazette, digital contracts; Sec. 9 = no forced digital-only |
| **CCA** | Controller of Certifying Authorities — Sec. 17; regulates CAs, maintains public key DB |
| **CA** | Certifying Authority — licensed by CCA under Sec. 21 to issue DSCs |
| **Adjudicating Officer** | Sec. 46; Director-level officer; handles civil compensation up to ₹5 crore |
| **Cyber Appellate Tribunal** | Sec. 48; appeals from AO/Controller; High Court qualification; appeal within 45 days |
| **SPDI Rules 2011** | Passwords, financial info, health data, biometrics = SPDI; Sec. 43A liability |
| **Intermediary Rules 2021** | 50L+ users = SSMI; 36-hr takedown; CCI + Grievance Officer mandatory |
| **Sec. 78** | Inspector (minimum) to investigate IT Act offences |
| **Sec. 79A** | Govt. notified bodies (CERT-In, CDAC) give expert opinion on electronic evidence |
| **BSA 2023 Sec. 63** | Electronic records need a **certificate** to be admissible; replaces IEA Sec. 65B |
| **Arjun Panditrao (2020)** | Sec. 65B certificate MANDATORY; court can direct person to produce it |

---

## 📝 Previous Year Question Patterns

> [!question] Likely Exam Questions

1. Explain the concept of Digital Signature under the IT Act, 2000. How does it differ from an Electronic Signature?
2. What is a Reliable Electronic Signature? What are the conditions under Section 3A?
3. Write a detailed note on the functions and powers of the **Controller of Certifying Authorities**.
4. Explain the role and functions of a **Certifying Authority**. How is a Digital Signature Certificate issued?
5. Who is an **Adjudicating Officer** under the IT Act? Discuss his powers and procedure.
6. What is the **Cyber Appellate Tribunal**? How is it constituted? What is the appeals procedure?
7. Discuss the major **Rules** framed under the IT Act, 2000. Explain SPDI Rules 2011 in detail.
8. What is Electronic Governance? Discuss its legal framework under the IT Act.
9. Explain **Section 79A** of the IT Act. Who are the notified Examiners of Electronic Evidence?
10. Discuss the admissibility of electronic evidence under the **BSA, 2023**. What is the certificate requirement and what does the Arjun Panditrao case say?

---

## 🔗 Related Notes

- [[Paper 204 - Unit I — Introduction to Cyberspace]]
- [[Paper 204 - Unit III]]
- [[Digital Personal Data Protection Act 2023]]
- [[Bharatiya Sakshya Adhiniyam 2023]]
- [[Cyber Forensics — Evidence Collection]]
- [[CERT-In — Role and Functions]]

---

*📌 Maintained by Cywarx | University of Delhi — PGDCSL | Semester 2*
