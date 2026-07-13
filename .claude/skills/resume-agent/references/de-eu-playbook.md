# Germany & Europe Market Playbook

Rules for producing CVs and cover letters for the German (first priority) and wider
European cybersecurity job market. Researched and verified July 2026 against German HR
sources (Stepstone, softgarden, Karrierebibel, Make-it-in-Germany, recruiter surveys and
ATS vendor documentation). The agent MUST read this file in Step 0 and apply the rules
below mechanically. Where a rule is conditional, the condition is stated — do not apply
German-only rules to non-German targets.

---

## 0. Decision logic — classify the JD first

Determine four facts from the JD (and company website knowledge if obvious):

1. **JD language** — German or English.
2. **Target country** — default Germany; otherwise use the country table in §6.
3. **Company type** — `international/startup` (English-first posting, du-tone, scale-up,
   US-style careers page) vs `traditional` (Mittelstand, corporate/DAX, public sector,
   bank/insurer, formal Sie-tone, "m/w/d" plus German legalese).
4. **Role type** — Werkstudent/intern, junior/entry, or experienced; GRC/compliance vs
   technical (SOC/pentest/cloud/engineering).

Then apply:

| Situation | CV language | Section labels | Photo | Cover letter |
|---|---|---|---|---|
| English JD, any company in DE | English | English | **No photo** (default) | English, §2-EN |
| German JD, traditional company | German | German (§1 table) | **Photo only for email applications** (see ATS exception below); ask user for file, proceed without if none | German Anschreiben, §2-DE |
| German JD, startup | German (English only if the ad says "English ok") | German | Optional — omit by default | German, §2-DE, slightly less formal |
| Non-German EU country | English unless JD in local language | English | Per §6 table | Per §6 table |

- **ATS-portal photo exception (verified):** any application submitted through an ATS
  portal (Personio, softgarden, SuccessFactors, Workday & co.) gets a **photo-free** parsed
  PDF even at traditional companies — German ATS guidance is unanimous that an embedded
  image is useless-to-harmful in parsing. Embed a photo only for direct **email**
  applications, or supply it as a separate JPG when a portal has a photo field.
- **Bilingual headline mirror:** put the role title bilingually in the CV tagline/headline
  when the German title differs — e.g. "Working Student Cyber Security / Werkstudent
  IT-Sicherheit" — so both German-only and English-only recruiter searches hit; do not
  rely on cross-language semantic matching in mid-market ATS.

### Werkstudent vs entry-level mode (role-type fact 4 drives this)

Trigger **entry-level mode** on JD keywords: *Junior, Berufseinstieg, Absolvent,
abgeschlossenes Studium, Festanstellung, Schichtdienst* — or any full-time permanent role
targeted after graduation. What switches:

| Item | Werkstudent mode | Entry-level mode |
|---|---|---|
| Availability line | "20 h/week during lectures, full-time in breaks" | Start date only: `Verfügbar: Vollzeit ab sofort / zum nächstmöglichen Zeitpunkt` (or `ab November 2026, nach Masterabschluss Oktober 2026` while still enrolled). Never mention hours. |
| P4 formalities | Hours + conversion intent + student-permit one-liner | Start date/notice + post-study-permit one-liner + salary range only if asked (§2 entry-level P4) |
| Salary handling | Hourly range only if forced | Annual narrow range or single figure per §5 city bands; never open-ended |
| Work-authorization line | Student wording (§1) | 18-month post-study permit wording (§5) — "no visa sponsorship required" |
| Bullets | Support verbs acceptable | Ownership verbs required (übernehmen/verantworten/durchführen — never unterstützen); named SIEM/EDR platform with concrete triage/playbook evidence |

- **Language gate (hard, entry-level only):** "verhandlungssicheres Deutsch" / C1 in a
  full-time JD is a **near-disqualifier at A2** — flag to the user before generating
  documents (verified: KPMG junior IT-security consulting requires verhandlungssicher;
  StepStone junior-consultant listings standardly C1 German + B2 English). "English
  working language / international team" = green light. English-listed junior roles are
  scarce — most English cyber listings skew 5+ years — so Werkstudent-to-hire conversion
  stays the primary route even in entry-level mode.
- **Country gate (entry-level, non-DE):** Germany → proceed. Ireland/Poland/Czechia/
  Luxembourg → proceed with the §6 permit line. Netherlands → proceed only if the
  advertised salary plausibly clears the under-30 HSM threshold (€4,357/month excl.
  holiday allowance, 2026) or the employer is an IND recognised sponsor.
  Switzerland/Austria/France/Nordics/Spain/Portugal → tell the user entry-level
  sponsorship odds are near zero (§6) before producing anything.
- Never mention anabin/ZAB in any document for private-sector roles — a German-university
  degree is self-recognizing.

- **Keyword mirroring rule:** the resume must carry the JD's exact keyword strings *in the
  JD's language*. German JD + any CV → the top keywords stay German (with an English gloss
  where it reads naturally, e.g. "Schwachstellenmanagement (vulnerability management)").
  English JD at a German company for GRC/compliance roles → additionally weave 3–5 German
  term pairs from §4 (they match recruiter database searches).
- If the JD explicitly says "kein Anschreiben nötig" / "Lebenslauf genügt" / "no cover
  letter required" → skip the cover letter and tell the user why.

---

## 1. Germany — CV rules

**Format & design** (all verified against 2025–2026 German recruiter guidance):

- **One page** for students/juniors (the pipeline's hard rule stands); two pages max only
  with >5 years of experience.
- **Sober single-column layout**, standard fonts, no icons, no skill bars, no tables, no
  graphics, no headers/footers — German recruiters prefer content over design AND this is
  what survives Personio/SuccessFactors/Workday parsing. The pipeline's renderer already
  complies. "Template-store" designs actively hurt.
- **US-style one-page resume is accepted for English-language postings** at German
  companies — confirmed by multiple German sources. For German-language postings produce
  a German CV (labels below), still single-column.

**Personal data — what goes in and what stays out:**

- IN: name, city ("Berlin, Germany" — full street address not needed), phone, email,
  LinkedIn, GitHub/portfolio.
- OUT (modern default, AGG anti-discrimination trend): date of birth, nationality,
  marital status, religion, full address. Never add these unless the user insists.
- **Photo — conditional, adversarially verified:** ~80% of German applications still
  carry one and ~50–53% of recruiters value it; *traditional* companies may read a missing
  photo as an incomplete application, while international/startup/English-posted contexts
  are fully safe without. Rule: English posting or startup → no photo. German posting at a
  traditional company → professional photo (passport-size, neutral background — never a
  selfie; a bad photo is worse than none), BUT only in email applications — see the §0
  ATS-portal exception. The ATS-safe PDF supports `contact: photo: <path>`; the Overleaf
  .tex stays photo-free.
- **Work-authorization line (non-EU applicants — load-bearing):** uncertainty about work
  status is a top silent-rejection reason for internationals. Include one factual line in
  the tagline or Additional, in **plain language — no statute citations, no day-count
  legalese** (HR knows the rules; the signal is clarity and schedule realism):
  EN: `Valid German student residence permit — eligible to work 20 h/week during
  lectures, full-time in semester breaks; no sponsorship required.`
  DE: `Gültige Aufenthaltserlaubnis (Studium) mit Arbeitserlaubnis als Werkstudent
  (bis 20 Std./Woche).`
  Keep it to one line; the 140/280-day rule is background knowledge for form answers,
  never CV text. After graduation, swap to the 18-month post-study permit wording (§5).

**Sections:**

- English CV order (pipeline default): Summary, Skills, Experience, Projects, Education,
  Certifications, Additional.
- German CV labels (set via the YAML `labels:` mapping):

  | English | German |
  |---|---|
  | Summary | Profil |
  | Skills | Kenntnisse |
  | Experience | Berufserfahrung |
  | Projects | Projekte |
  | Education | Ausbildung |
  | Certifications | Zertifikate |
  | Additional | Weitere Angaben |

  These exact strings are recognized by German CV parsers (alongside Bildungsweg,
  Fähigkeiten, Kompetenzen, Sprachkenntnisse).
- **Languages line is mandatory** in every German/EU application (in Additional, label
  "Languages" / "Sprachkenntnisse"), CEFR levels, honest, growth-framed:
  `English (C1), German (A2–B1, continuously improving)` (adjust to the master resume's
  true state; never inflate to a flat level the candidate cannot demonstrate live, never
  omit German).
- Hobbies: only if space allows and only signal-bearing ones (CTF, OWASP chapter, security
  meetups) — one line max, otherwise omit.

**Dates:**

- English CV: `Mon YYYY – Mon YYYY` / `Mon YYYY – Present` / `Expected Mon YYYY`
  (the ATS audit enforces this).
- German CV: `MM/YYYY – MM/YYYY` / `MM/YYYY – heute` / `voraussichtlich MM/YYYY`
  (the audit accepts this numeric style when used consistently).
- Unexplained gaps > 3 months are noticed in Germany; if the master resume has one, cover
  it honestly (studies, relocation, language course) rather than hiding it.

**No signature/date on the CV** — the old convention is dead; omit it.

**Files & package (German conventions):**

- File names: `Lebenslauf_<Vorname>_<Nachname>.pdf`, `Anschreiben_<Vorname>_<Nachname>.pdf`;
  combined file `Bewerbung_<Vorname>_<Nachname>.pdf` (surname-first order is equally
  accepted — name order is flexible, clarity is not).
- If a portal takes ONE file: order = Anschreiben → Lebenslauf → Zeugnisse (by relevance,
  not date), total ≤ 5 MB. If separate fields exist, upload separately. Within the
  Zeugnisse block for Werkstudent applications: current transcript/Notenspiegel and
  Immatrikulationsbescheinigung FIRST, then prior degrees, Arbeitszeugnisse, certificates.
- Email applications: subject `Bewerbung als <Position> (ID: <ref>) – <Vorname Nachname>`,
  short factual body, PDF attached directly (no cloud links).

---

## 2. Germany — cover letter rules

Produce a cover letter for every application unless the posting waives it (§0). Reality
check (verified 2026 — do NOT quote percentages; surveys measure incompatible
populations): the CV decides, the letter is skimmed. What is solid: 56% of surveyed DAX
companies require a letter, recruiter sentiment splits near 50/50, and StepStone weights
CV vs letter importance 68% vs 22%. Recruiters read the letter when the candidate is
shortlisted or something needs explaining (career change, internationals, gaps). For an
international junior it is therefore HIGH-value: it is where visa clarity, availability,
German level, and conversion intent get explained. Front-load the strongest fit argument
into the FIRST TWO SENTENCES — that may be all that gets read.

**The letter is never machine-scored:** ATS store it as an unparsed attachment for human
review. Zero keyword-stuffing; optimize purely for persuasion.

**Length: 250–400 words, one page, 3–5 paragraphs; Werkstudent letters trend shorter —
target 200–350 words, treat 450 as a hard ceiling.**

### 2-DE — German Anschreiben (DIN 5008-informed)

Block order (the cover-letter renderer implements this):

1. **Sender block** top: name, city, phone, email (LinkedIn optional).
2. **Recipient block**: company, contact person if known, city.
3. **City + date**, right-aligned: `Berlin, 12.07.2026` (German date format).
4. **Betreff** — bold, WITHOUT the word "Betreff:":
   `Bewerbung als Werkstudent IT-Security (Referenz 12345)`.
5. **Salutation**: named contact is strongly preferred — search the JD/posting for a name
   (`Sehr geehrte Frau Schneider,` / `Sehr geehrter Herr Müller,`); fallback
   `Sehr geehrte Damen und Herren,`. Startup du-tone ads may get `Guten Tag Frau X,`.
6. **Body** (see paragraph plan).
7. **Closing formula**: `Mit freundlichen Grüßen` (safest; startups tolerate
   `Viele Grüße`) — **never a trailing comma after it**; blank line, typed full name.
8. Optional **Anlagen** line: `Anlagen: Lebenslauf, Immatrikulationsbescheinigung,
   Zeugnisse`.

**German-letter lints (deterministic, check before export):** (a) after the salutation
comma, the body continues **lowercase** unless the first word is a noun or Sie-form;
(b) no comma after "Mit freundlichen Grüßen"; (c) body text 11–12 pt (12 standard,
11 minimum).

**"Motivationsschreiben" in a company job ad almost always means the standard
Anschreiben** — deliver the one-page fit letter. Produce a true 1–2-page essay-style
Motivationsschreiben only for scholarship/university applications.

### 2-EN — English letter at a German company

Same content logic, Anglo formatting: contact header, date, `Dear Ms. Müller,` /
`Dear Hiring Team,`, body, `Kind regards,` + name. German content expectations still
apply (start date, hours, work authorization when relevant). Tone: more direct and modest
than a US letter — fact-based confidence, no selling.

### Paragraph plan (both languages)

- **P1 — hook (3–4 sentences):** the role, and ONE concrete, checkable alignment between
  you and *this* company — their product, stack, sector regulation (NIS2/DORA/TISAX if
  genuinely relevant), or the JD's core task. Never open with generic flattery or
  "I have always dreamed of…". Naming the actual day-to-day task from the JD and matching
  it to something you have actually done beats any adjective.
- **P2 — proof (the longest paragraph):** 2–3 experiences/projects mapped to the JD's
  listed tasks, with tools, scope, numbers from the master resume. This is reframing, not
  a CV repeat — pick only what maps.
- **P3 — optional second proof or company fit:** a second mapped experience, or a specific
  reason this company (not "your renowned company" — a real fact about them).
- **P4 — formalities (Werkstudent mode):** earliest start date (`Eintrittstermin`),
  weekly availability ("20 h/week during lectures, full-time in semester breaks"),
  work-authorization one-liner if non-EU, salary ONLY if the posting asks (hourly range
  only if forced), conversion intent (§5). Close with one polite call-to-action sentence.
- **P4 — formalities (entry-level mode):** replaces the hours content entirely.
  1. **Start date, not hours:** `Ich stehe ab sofort / zum nächstmöglichen Zeitpunkt zur
     Verfügung` (while still enrolled: `zum November 2026, nach Abschluss meines
     Masterstudiums im Oktober 2026`). Immediate availability is the differentiator —
     state it, don't explain it. Never contest the 6-month Probezeit.
  2. **Permit one-liner — conditional:** only when the JD hints at local-hire preference
     or asks about authorization; one clause max, no visa mechanics: "…mit
     uneingeschränkter Arbeitserlaubnis, kein Sponsoring erforderlich."
  3. **Salary — only if the posting asks:** narrow range from the §5 verified city bands
     (Berlin SOC 52–56k, Berlin GRC 54–58k, Munich/Frankfurt 55–60k, smaller cities
     46–50k € brutto/Jahr). A 58–65k ask overreaches for a fresh graduate at A2 German —
     risks disqualification and has no visa upside.
  4. **Shift willingness — conditional:** JD mentions 24/7/Schichtdienst → add
     `Bereitschaft zu Schicht- und Wochenendarbeit` explicitly — a cheap differentiator.
  5. **Gap-bridging sentence — conditional (reach ads asking 2–3 Jahre):** one sentence
     mapping Werkstudent months + named lab projects to the listed functional
     requirements — address the gap, never ignore it.

**Instant-rejection triggers (avoid absolutely):** generic template feel; wrong company
name/role (copy-paste artifacts); repeating the CV line by line; >1 page; flattery;
AI-sounding text (§7); claims contradicting the CV; salary demands when not asked.

---

## 3. ATS reality in Germany/EU

Verified 2025–2026: the US "ATS auto-rejects you by keyword score" narrative is largely a
myth in Germany. What actually happens:

- **Systems (most commonly encountered — the market is fragmented, 160+ products):**
  Personio (SMB/startups; inferred from HRIS footprint, not measured ATS share),
  softgarden/rexx/d.vinci/onlyfy (Mittelstand; recruiter surveys also rank Coveto and
  Concludis top in the mid-market), SAP SuccessFactors & Workday (corporates/DAX),
  Greenhouse/Teamtailor/Recruitee (scale-ups).
- **Identify the ATS from the careers-page URL** and adapt: `*.jobs.personio.de` /
  `*.softgarden.io` / onlyfy-Prescreen domains → parse-and-rank + literal keyword search
  (startup/SME); `myworkdayjobs.com` / SuccessFactors domains → structured screening +
  disqualifier questions (enterprise).
- **They parse, store, rank, and search — humans decide.** Score-based auto-rejection is
  rare (one small 25-recruiter survey puts it at ~8% — treat as indicative, never quote as
  established fact). Low keyword match ≠ deletion, but it does mean you rank lower and may
  never be *seen*. So keyword coverage still matters — for ranking and recruiter database
  search, not survival.
- **Knockout questions do the hard filtering:** work authorization, German level, weekly
  hours, start date, salary field. Answer form fields carefully and 100% consistently
  with the CV — an inconsistency between form and CV is a real rejection cause. When the
  user reports form questions, tell them exactly what to answer based on the resume facts.
- **Output a knockout-answer checklist with every application** (these form fields, not
  the CV, are the only true auto-reject gates): enrollment status + expected graduation;
  max 20 h/week during lectures (Werkstudent); location; "no sponsorship required"
  work-authorization answer; German level honestly stated.
- **What breaks parsing** (all already avoided by the pipeline's renderer): two-column
  layouts, tables, text in headers/footers, icons/graphics/skill bars, image-only PDFs,
  exotic fonts. Umlauts in text PDFs are fine — never mangle German words or names.
- **Recognized section headers**: the English set the pipeline uses, plus the German set
  in §1. Do not invent creative header names.
- **Language matching:** parsers handle bilingual CVs, but keyword matching is literal
  enough that the JD's-language keyword strings must appear (§0 mirroring rule).

---

## 4. Cybersecurity keyword bank (Germany/EU 2026)

Use as the vocabulary pool when the JD touches these areas — mirror the JD's exact strings
first, then fill from here truthfully (only what the master resume supports).

**Regulations & frameworks** (ranked by frequency in German security JDs):

- NIS2 / NIS2UmsuCG (in force since Dec 2025, ~30,000 companies in scope — huge JD
  driver; BSI registration deadline was 6 Mar 2026 with a final grace period to
  **31 Jul 2026** after low uptake — companies are in a live compliance scramble, so
  phrase NIS2 work as *current implementation/readiness support*, never "upcoming")
- GDPR / DSGVO, Datenschutz
- ISO/IEC 27001, ISMS (Informationssicherheitsmanagementsystem), Audit, Zertifizierung
- BSI IT-Grundschutz (public sector, KRITIS, Mittelstand)
- DORA (finance — Frankfurt/Munich roles), ICT risk management, resilience testing
- KRITIS / kritische Infrastrukturen (energy, health, transport, telecom)
- TISAX (automotive — Stuttgart/Bavaria supply chain)
- BSI C5 (cloud audits), Cyber Resilience Act / CRA (product security, emerging)

**Certifications by German junior-market value:** CompTIA Security+ (baseline, most
recognized), Microsoft SC-900 / AZ-500 (Azure-heavy market), ISO 27001 Foundation, ISC2 CC,
BSI IT-Grundschutz-Praktiker (GRC/public sector), CEH/OSCP (pentest roles). CISSP/CISM are
senior-level — never imply them for juniors.

**Technical keywords** (frequency in German junior/SOC postings): SIEM (~84% of SOC ads —
Splunk, Microsoft Sentinel, QRadar, Elastic), network fundamentals (TCP/IP, firewalls,
IDS/IPS ~80%), Python/Bash scripting (~72%), cloud security (~45% — Azure first in German
enterprises: Sentinel, Defender, Entra ID; AWS in startups), EDR (Defender for Endpoint,
CrowdStrike, SentinelOne), Schwachstellenmanagement / vulnerability management (Nessus,
Qualys, OpenVAS), IAM (Entra ID, Active Directory, RBAC, least privilege, Zero Trust),
Incident Response, SOC analysis, Security Awareness.

**German ↔ English GRC term pairs** (weave pairs into English CVs for German GRC roles):

| German | English |
|---|---|
| Informationssicherheit | information security |
| ISMS | information security management system |
| Risikoanalyse / Risikomanagement | risk analysis / risk management |
| Datenschutz (DSGVO) | data protection (GDPR) |
| Schwachstellenmanagement | vulnerability management |
| Sicherheitsrichtlinien / Sicherheitskonzepte | security policies / security concepts |
| Notfallmanagement / BCM | incident & business continuity management |
| Audit / Revision | audit / internal control |
| Awareness-Schulungen | security awareness training |
| Informationssicherheitsbeauftragter (ISB) | information security officer |

**Junior-JD shifts vs Werkstudent JDs (entry-level mode):**

- **Verb register:** junior ads use ownership language (übernimmst Verantwortung,
  eigenständige Analyse, Durchführung); Werkstudent ads use support language (unterstützt,
  Mitarbeit). Mirror the register — entry-level bullets claim ownership and outcomes,
  never assistance.
- **Tool depth:** requirement rises from "Grundkenntnisse/von Vorteil" to demonstrable
  day-to-day operation of at least one named SIEM (Splunk/Sentinel/QRadar/Elastic) plus
  EDR triage and ticketing/ITSM documentation; labs/Werkstudent work are accepted
  evidence when framed as *operation*, not exposure.
- **Certifications** move from motivation signal to strongly-preferred for SOC roles
  (Security+, CCNA, vendor SIEM certs, ISO 27001 Foundation) — they compensate for
  missing years.
- **Junior keyword cluster** (add to the vocabulary pool): Berufseinstieg, Junior
  Security Analyst / Junior Security Consultant, Absolvent, abgeschlossenes Studium,
  erste Berufserfahrung, Alert-Triage, Incident Response (NIST-Phasen), Ticketing/ITSM,
  Schichtdienst / Bereitschaft, verfügbar ab / zum nächstmöglichen Zeitpunkt,
  Gehaltsvorstellung, Probezeit, Kündigungsfrist, Arbeitserlaubnis / kein Sponsoring
  erforderlich, Blaue Karte EU, Engpassberuf.
- **Experience-bar parsing rule:** "erste Berufserfahrung" = satisfiable by
  Werkstudent/Praktikum (apply normally); "1–2 / 2–3 Jahre Berufserfahrung" = stricter
  tier (apply with the §2 gap-bridging sentence); pure Absolvent-track ads have no
  experience bar — a distinct, target-first segment.
- **Interview expectation (for §8 prep):** junior screens = HR call (often German —
  rehearse an A2-level self-intro plus an honest "A2 → B1 by start date" trajectory
  statement), then a scenario round (log triage, phishing investigation, IR phase
  walkthrough, TCP/IP basics) — not HackerRank; graduate programs add assessment centers.

**Market context** (for framing, not for pasting into letters): Bitkom (Aug 2025):
~109,000 unfilled IT jobs in Germany overall (85% of firms report shortage) — that is an
all-IT figure; do NOT quote a security-specific shortage number, none exists. Hubs: Berlin
(startups/gov), Munich & Frankfurt (finance/DORA), Stuttgart (automotive/TISAX),
Hamburg/Cologne (telecom/logistics). Werkstudent IT-security pay: ~€16–19/h typical
(sensible ask band 14–18 €; up to ~20–22 € for Master's students at large corporates).
Junior entry anchor: €45–55k. Quote salary numbers only when a form demands them.

---

## 5. Werkstudent / entry-level rules (Germany)

- **Package:** CV + cover letter + Immatrikulationsbescheinigung (enrollment certificate)
  + current transcript; certificates as available. The agent produces CV + letter and must
  REMIND the user to attach the enrollment certificate and transcript — a missing
  Immatrikulationsbescheinigung is a classic silent rejection for Werkstudent roles.
- **Availability is mandatory content:** "up to 20 h/week during lecture periods,
  full-time during semester breaks" — in the resume tagline/summary AND the letter's
  formalities paragraph. Never leave hours ambiguous.
- **Non-EU legal facts:** one plain-language line only (§1 wording — no statute
  citations, no 140/280-day text on the CV). The day rules and Werkstudentenprivileg are
  background knowledge for answering form questions consistently, nothing more.
- **Graduation horizon:** graduating soon is a *pipeline asset*, not a weakness — frame
  it: "expected graduation Oct 2026; explicitly interested in continuing full-time as a
  junior after graduation, depending on mutual fit." Signal conversion intent in the
  letter (P4) and optionally the summary. This converts "only 3 months enrolled" from an
  objection into a cheap-to-test junior hire story. **Name the mechanism** in the
  conversion sentence: "…continuing full-time under the 18-month post-study residence
  permit for German-university graduates" — one sentence, no visa-law detail. After
  graduation, the CV work-authorization line swaps to the 18-month job-seeker permit
  wording.
- **Anchor lab/CTF/GitHub bullets to a framework keyword where truthful** (ISO 27001,
  NIS2, BSI IT-Grundschutz, DSGVO, NIST CSF) — framework references are a distinct
  2025–26 screening signal even at junior level. Naked tool lists ("Kali, Burp,
  Wireshark") are banned; every tool needs a context or outcome.

### Entry-level (post-graduation) rules

- **Permit framing (the selling point, not the liability):** on graduating, the 18-month
  post-study permit (§ 20 AufenthG) grants **unrestricted** work rights — any job, any
  employer, no labour-market test, no employer action at hire. Non-extendable beyond 18
  months (a shorter initial grant can be topped up to 18). Conversion to EU Blue Card
  (**§ 18g** — the legal basis since Nov 2023, not §18b) or a §18b skilled-worker permit
  is the employee's own in-country process. Settlement: Blue Card 27 months / 21 with B1
  German; German-university graduates on a plain §18b permit qualify after **24 months**
  (the old "48 months" figure is pre-2023 law — never quote it).
- **Blue Card 2026 thresholds (2026-only values — they reset every 1 January):** standard
  **€50,700**; reduced **€45,934.20** (≈ €3,827/month) for shortage occupations incl.
  ISCO-08 group 25 ICT AND recent graduates (degree within 3 years) — this candidate
  qualifies on both tracks. Reduced-threshold applications need BA approval — "required
  and routinely granted", never "exempt". **Never treat the Blue Card figure as a salary
  floor:** §18b has no fixed threshold beyond local comparability, so a €42–45k offer is
  fully acceptable — €45,934 merely unlocks the fastest settlement track.
- **CV work-authorization line (swaps for the §1 student line after graduation):**
  EN: `Full unrestricted German work permit (18-month post-study permit, German
  university graduate) — no visa sponsorship required; EU Blue Card eligible.`
  DE: `Uneingeschränkte Arbeitserlaubnis (18-monatige Aufenthaltserlaubnis zur
  Arbeitsplatzsuche nach deutschem Hochschulabschluss) — kein Sponsoring erforderlich.`
  Condition: literally true only once the §20 permit is applied for after the final
  certificate — verify the conferral date before first use. If a strict recruiter probes
  the later Blue Card switch: "a routine employee-side application, no employer
  sponsorship process" (the employer only signs a standard Declaration of Employment).
- **Form answers:** "Do you require visa sponsorship?" → **No** (during the §20 window).
  Start-date field → `ab sofort` or a concrete date 2–4 weeks out, never blank.
- **Probezeit/notice norms:** Probezeit is almost always 6 months (legal max) with 2-week
  notice either side — never present it as negotiable. **Immediate availability is a
  differentiator**: a §20-permit candidate can start weeks before a rival serving a
  3-month Kündigungsfrist — say it via the start-date line, not by explaining the law.
- **Salary defaults when a Gehaltsvorstellung is demanded** (gross/year, narrow range or
  single figure, never open-ended; anchored mid-band because A2 German caps leverage —
  StepStone/Glassdoor/get-in-IT 2026): Berlin junior SOC/analyst **52–56k €**; Berlin
  GRC/consulting **54–58k €**; Munich/Frankfurt **55–60k €**; smaller cities/Mittelstand
  **46–50k €**. Format: `Meine Gehaltsvorstellung liegt bei 52.000–56.000 € brutto/Jahr.`
  Werkstudent-to-full-time conversions land at the lower band edge — accept it.
- **Convert student experience into professional framing:** Werkstudent roles go under
  Berufserfahrung (StepStone doctrine: Praktika/Werkstudententätigkeiten count as
  Berufserfahrung and satisfy "erste Berufserfahrung") with ownership-verb, quantified,
  tool-named bullets ("triaged 20+ SIEM alerts/week in Splunk"). Home labs become a
  "Praktische Projekte" section in the identical bullet grammar. GitHub/portfolio link
  stays prominent — top junior differentiator.
- **Trainee/graduate-program route** (structured entry, viable at A2 unless noted):
  Big Four cyber junior roles — continuous hiring, waves Mar–Jun and Sep–Nov, English
  possible in global SOC/cloud/pentest teams (German consulting tracks want B2+);
  Allianz and Siemens international graduate programs — fixed intakes, apply ~Sep–Nov for
  next year's start; Bosch JMP — rolling. **Not viable at A2:** Deutsche Telekom
  "Start up!" (C1 German + 6 months experience — revisit after B2/C1; Werkstudent tenure
  will satisfy the experience prerequisite); BWI/BSI (C1 + clearance, mostly citizenship —
  exclude).
- **Reach-application rule:** apply to postings asking 2–3 Jahre Berufserfahrung when the
  *functional* requirements are truthfully covered by Werkstudent months + lab projects —
  German ads describe the ideal candidate, not the only one. Include one explicit
  gap-bridging sentence (§2). Nuance: "erste Berufserfahrung" is satisfiable by
  Werkstudent work; a literal "1–2/2–3 Jahre" line is a stricter tier — prioritize
  Junior/Einstieg/Absolvent-tagged ads first, but do not self-filter out of reach ads.
- **Highest-leverage compensators before autumn 2026:** Security+ (or equivalent SOC
  cert) and German B1 with a certificate — the two things recruiters cite as offsetting
  missing years.
- **German A2:** list honestly with an improvement signal (§1). If the JD requires fluent
  German, do not hide it — flag the mismatch to the user in the gap analysis and let them
  decide whether to apply.
- **What makes juniors stand out to German security leads** (weight in this order):
  hands-on home labs with named tools > GitHub/portfolio with clean READMEs > CTF
  standings (TryHackMe/HackTheBox paths, ranks) > certifications > grades. Grades: include
  only if strong (German equivalent conversion, e.g. "1.6"); thesis topic if relevant.
  OWASP/BSides/CCC involvement is a real signal — include if true.

---

## 6. Country adaptation table (beyond Germany)

| Country | Photo | Personal data | Pages | Cover letter | Notes |
|---|---|---|---|---|---|
| Austria | **Expected in traditional firms** | DOB + nationality conventionally expected (not merely tolerated) | 1–2 | Moderate | Very close to German conventions; German docs for German ads |
| Switzerland | **Expected in traditional sectors** (optional at international firms/startups) | DOB, nationality AND **work-permit status** standardly stated | 1–2 | Moderate | **Arbeitszeugnisse/references matter more** — have employment certificates ready; language depends on region (DE/FR/IT) |
| Netherlands | **No** | Minimal | 1–2, short & direct | Moderate | Dutch directness — compact, achievement-first CVs; English broadly fine in tech |
| Sweden/Denmark/Finland | **No** | Minimal | 1–2 | Moderate | English widely accepted in tech; modest tone (Jantelagen) — avoid US-style selling. Sweden expects a **personligt brev**: 300–500 words, personality/culture fit, low hype — never a DIN-style letter (some large employers are dropping letters entirely) |
| France | Optional (photo more accepted than UK) | Some tolerance for personal detail | 1 page juniors | **High** — lettre de motivation still expected | French helps a lot outside international firms |
| Belgium | Usually no | Minimal | 1–2 | Moderate-high | Brussels international scene English-friendly |
| Ireland | **No** | **No DOB/age/photo** | 2 max | Moderate | English market; anti-discrimination norms like UK |
| UK | **No** | **Never DOB, age, photo, marital status** | 2 max | Moderate | Strictest anti-discrimination formatting |
| Spain | Optional | Some personal detail tolerated | 1–2 | Moderate-high | Spanish preferred outside multinationals |
| Poland | **Photo-expected zone** (a CV without one can read as unfinished — as in CZ/SK/HU) | Lean; **append the RODO clause by default** (use the employer's wording if the ad gives one — market convention, and some employers screen for it) | 1–2 | Moderate | Large English-speaking tech/SOC hub (Kraków, Warsaw, Wrocław) |
| Luxembourg | Usually no | Minimal | 1–2 | Moderate-high | Finance sector — DORA keywords land well |

- **Europass:** only for EU institutions and some public-sector/academic contexts. In the
  private sector it reads generic and verbose — never use it for company applications.
### Entry-level permit paths per country (non-EU, German-degree graduate — verified 2026)

Hard fact first: every famous post-study scheme elsewhere (Ireland Stamp 1G, Belgian
zoekjaar, Sweden/Finland/Norway search permits, Austria RWR graduate track, Swiss 6-month
window) is locked to graduates of *that country's* institutions. The one cross-border
exception, the Dutch zoekjaar, requires a top-200 world-ranked university — which a
private German university degree does not meet. Therefore: **never claim zoekjaar or
Stamp 1G eligibility, and never write "no sponsorship required" for any country except
Germany during the §20 window.**

| Country | Junior permit vehicle | CV authorization line (one line) |
|---|---|---|
| Germany | §20 post-study → Blue Card §18g / §18b | §5 wording — the only "no sponsorship" market |
| Ireland | Critical Skills Employment Permit — ICT security occupations listed, ~€38k floor, **no labour-market test** (reverify the 2026 list on enterprise.gov.ie before applying) | `Eligible for Critical Skills Employment Permit (ICT security occupation) — no labour-market test required.` |
| Netherlands | HSM via IND recognised sponsor; under-30 rate €4,357/month excl. holiday allowance (~€52k/yr, 2026); reduced graduate rate NOT available without zoekjaar eligibility | `Requires Highly Skilled Migrant sponsorship (IND recognised sponsor, standard under-30 threshold).` |
| Poland | Standard Type-A work permit, employer-managed; Blue Card (~€36.6k) above junior pay €20–31k — irrelevant | `Work-permit sponsorship required — standard employer-managed process.` |
| Czechia | Employee Card; Blue Card (~€36.4k) above junior pay €24–32k | `Work-permit sponsorship required (Employee Card) — employer-managed process.` |
| Luxembourg | Salaried-worker permit (shortage-IT relaxation); junior finance/Big-4 pay €45–55k fits | `Requires salaried-worker permit (shortage-IT occupation).` |

- **Verified top-5 realistic non-German markets for a non-EU English-speaking junior:**
  1) **Ireland** (English-native, CSEP fits junior pay), 2) **Netherlands** (recognised
  sponsors only; salary must clear the under-30 rate), 3) **Poland** (Kraków/Warsaw
  English SOC/GRC hubs — juniors do get sponsored), 4) **Czechia** (Prague/Brno
  shared-services SOCs), 5) **Luxembourg** (highest junior pay in Europe, tiny market —
  targeted tier, not volume). Germany stays the default market.
- **Do not target for entry-level 2026 — revisit at 2–3 years experience:** Switzerland
  (federal quotas + labour-market test), Austria (RWR graduate track Austrian-grads-only;
  German-language market), France (APS French-grads-only; junior pay below the permit
  floor; French required), Spain/Portugal (junior pay €18–30k — uneconomic), Nordics
  (search permits domestic-only; Sweden requires ≥90% of median salary from 1 Jun 2026).
- **Two-step mobility play (mention when the user targets NL/AT/BE/FR prematurely):**
  German Blue Card first; after 12 months, EU Directive 2021/1883 long-term mobility
  allows an in-country Blue Card application in a second member state — the second
  state's salary bar still applies, so this works after 1–2 years of salary growth, not
  at entry.
- **Cover-letter line for non-German countries (one factual sentence):** name the permit
  route to pre-empt recruiter uncertainty, e.g. "as a non-EU national I would join via
  the Critical Skills Employment Permit — a fast process with no labour-market test."
- **Cross-border constraint (flag in every non-DE gap analysis):** leaving Germany
  forfeits the 18-month post-study permit and usually requires employer sponsorship —
  *sponsorship willingness, not visa-route existence, is the binding constraint*. The
  Dutch orientation year (zoekjaar) covers only Dutch or top-200-world-university
  graduates — a private-university Berlin graduate may not qualify; the realistic NL
  route is HSM sponsorship at the reduced recent-graduate salary threshold.
- **EU Pay Transparency Directive (2023/970, national transposition due 7 Jun 2026):**
  pay ranges must be disclosed in the ad or before interview; **pay-history questions are
  banned** — decline them with a forward-looking range anchored to the posted band.
  UK/CH sit outside the directive; enforcement uneven in H2 2026. Never volunteer salary
  history.
- **Terminology footnote:** "Werkstudent" does not translate outside DE/AT — relabel the
  role as internship / part-time student position / recent-graduate junior per target
  country.

---

## 7. Human-voice rules — the output must not read as AI-written (HARD RULES)

German recruiters do not run AI detectors (GDPR/false-positive risk); they judge by style.
What they bin is text that is "generic, polished, and empty" — which is exactly what
default LLM writing produces. These rules bind every summary, bullet, and cover-letter
sentence the agent writes:

**Banned words/phrases (English):** passionate, results-driven, dynamic, synergy, delve,
leverage (as a verb), utilize, spearhead, foster, empower, cutting-edge, fast-paced
environment, proven track record, "I am confident that", "aligns perfectly", "resonates
with me", "testament to", "in today's digital landscape", "excited to contribute",
"hit the ground running", "I am writing to formally express my strong interest", and the
"leveraged X to drive Y, resulting in Z" bullet template.
**Banned (German):** "hochmotiviert", "Ich bin ein absoluter Teamplayer",
"leidenschaftlich", "ich brenne für", "mit großer Leidenschaft", "spannende
Herausforderung", "dynamisches Umfeld", "eintauchen", "Ihre Werte haben mich besonders
angesprochen" (without naming which value), empty
"innovativ/dynamisch/lösungsorientiert" strings.

**Banned structures:**
- Rule-of-three adjective/noun triplets ("innovative, scalable, and secure solutions").
- **Em-dashes (—) are banned outright in all generated output** — resume summaries,
  bullets, and cover letters. Rephrase with commas, periods, colons, or parentheses.
  En dashes (–) in date ranges ("04/2024 – 10/2024") are typography, not prose, and
  stay. The ATS audit and cover-letter renderer flag any em-dash deterministically.
- "Not only X but also Y" / "It's not just X, it's Y" constructions.
- Every bullet or paragraph opening with the same rhythm or with "Successfully…".
  Measurable lint: uniform bullet length/structure (every bullet 15–22 words with the
  same opening grammar) is itself a tell — vary deliberately.
- A closing paragraph of pure generic enthusiasm.
- Superlatives about oneself ("exceptional", "outstanding", "world-class").

**Required properties:**
- Every cover-letter sentence must carry a *verifiable fact or concrete referent*: their
  product/stack/regulation/JD task, or your tool/project/number/date. If a sentence could
  appear unchanged in anyone's letter to any company, rewrite it or delete it.
- Vary sentence length; short sentences are allowed and human. One idea per sentence.
- At most ONE soft-skill adjective in the whole letter, and it must be immediately backed
  by an example ("meticulous — I would rather document twice than let a detail slip").
- Evidence style Germans trust: role + context + tool + outcome. Numbers plausible and
  contextualized ("~20%", "150+ staff", "from 45 to 5 minutes"), never marketing-precise
  ("increased efficiency by 347%"). In traditional companies, responsibility framing
  ("responsible for rollout to 15 departments / 400+ users") lands as well as metrics.
- Modest, factual first person. It is fine — human, even — for one sentence to be plain.
  Do not polish every sentence to the same sheen; uniform gloss is itself the tell.
- The letter must contain at least TWO details that could only come from reading *this*
  JD (a named task, a named tool from their stack, their product, their sector
  regulation) and at least ONE specific first-person detail from the master resume that
  no other applicant could write.

**The interrogation rule:** German recruiters counter AI polish with writing assignments
and probing interviews, not detectors — every resume claim must survive live questioning.
Never insert a skill or number the candidate cannot defend verbally; prefer honest
project-scale numbers (dataset sizes, lab scope, people trained) over invented
business-impact percentages.

**Self-check before export:** reread the letter as a skeptical German recruiter who reads
50 letters a day. Strike anything that sounds like a template. If more than one sentence
survives in "could be anyone" form, iterate again.

---

## 8. Recruiter-reality checklist (final gate before export)

- **6–30 seconds** first screen: role-title match visible in the summary/tagline; core
  JD stack covered in the Skills block (aim to truthfully cover 90%+ of *core*
  requirements — if genuinely below ~60%, tell the user the match is weak instead of
  cosmetically inflating); location + work authorization instantly clear; clean layout.
- **Consistency:** CV, cover letter, and any form answers must agree on dates, hours,
  start date, German level. Recruiters cross-check LinkedIn — remind the user if the
  tailored resume drifts far from their public profile.
- **Follow-up etiquette:** first follow-up at 10–14 days, **email only — phone-first is
  intrusive in German corporate culture**; optional second touch ~day 21 (email or
  LinkedIn); thank-you within 24–48 h after interviews; never more than two nudges.
  Timeline expectations are role-aware: Werkstudent IT processes typically close in
  3–6 weeks (2–3 rounds); the ~55-day median applies to general/full-time hiring — tell
  the user not to panic at silence.
- **Referrals matter — with honest numbers:** ~25–30% of German hires come via personal
  networks, and nearly **half of immigrants' FIRST jobs in Germany** are found through
  contacts (the stronger argument for this candidate). Where relevant, suggest pairing
  the application with one targeted LinkedIn message to the hiring manager and attendance
  at OWASP chapter / BSides / CCC events — but never send anything on their behalf.

---

Last multi-agent audit: wf_f05409e6-aee (22 agents, 7 dimensions, adversarially
verified), integrated 2026-07-13. Full audit report:
`output/research-audit-2026-07-13.md`.
Entry-level extension integrated: wf_7bdfae85-b08 (13 agents, 3 dimensions, visa numbers
verified against official sources), 2026-07-13.
