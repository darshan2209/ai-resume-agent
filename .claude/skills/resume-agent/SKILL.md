---
name: resume-agent
description: AI Resume Rewriting Agent — tailors your master resume to a pasted job description via gap analysis, ATS-keyword rewrite, deterministic ATS audit, fix loop, and ATS-safe PDF + Overleaf LaTeX export. Use whenever the user pastes a job description, names a target role, or asks to tailor/optimize/rewrite the resume for a job.
---

# Resume Agent

Tailor your master resume (`base/resume.yaml`) to one job description, producing an ATS-optimized one-page PDF and a Jake's-Resume LaTeX file. Run the five steps below in order. The ONLY allowed stop is Step 0 when no JD was provided. Never ask permission between steps — execute the whole pipeline and report at the end.

**Paths are relative to the repository root.** Run all commands from the repo root, or prefix them with the absolute path to your clone. On first use, ensure `base/resume.yaml` exists (`cp base/resume.example.yaml base/resume.yaml`, then fill in real details) and dependencies are installed (`pip install -r requirements.txt`).

**TRUTHFULNESS GUARDRAIL (hard rule):** never invent employers, titles, dates, degrees, certifications, tools, or metrics that are not in `base/resume.yaml` — only reframe, reorder, reweight, and re-emphasize true content; numbers may only come from the master resume.

## STEP 0 — Inputs

1. The JD is the text the user pasted (or a role + company they named with enough detail). If there is no JD in the message, ask for it and stop — this is the only permitted stop.
2. Read the master resume: `base/resume.yaml`.
3. Create `<outdir>` = `output/<company-role-slug>/` (lowercase, hyphenated, e.g. `output/acme-compliance-werkstudent/`).
4. Save the JD verbatim to `<outdir>/jd.txt`.

## STEP 1 — Gap analysis

Persona: a senior recruiter with 25 years in this exact industry — blunt, no sugar-coating. Compare master resume vs JD and write `<outdir>/gap_analysis.md` containing, in this order:

- **Match score 1–10** with reasoning.
- **Top 10 missing ATS keywords**, ranked by importance, using the JD's *exact phrases*.
- **Skills gaps** (real capability gaps, not just wording).
- **Industry terminology** the resume should adopt.
- **Seniority-language check** — does the language match the level the JD targets?
- **Unaddressed technical requirements.**
- **Missing soft skills** the JD signals.

## STEP 2 — Rewrite

Persona: an expert ATS resume writer. Write `<outdir>/resume.yaml` in the canonical schema below. Rules:

- Achievement formula: "Achieved X by Y resulting in Z".
- One page. Bullets max 2 lines each.
- Present tense for the current role, past tense for prior roles.
- Every bullet opens with a DIFFERENT strong action verb.
- 2–3 quantified results per role (numbers only from the master resume).
- Weave the top-10 keywords from Step 1 naturally — never stuff; mirror exact JD phrases.
- Reorder skills categories and bullets so the most JD-relevant content leads.
- The truthfulness guardrail above applies verbatim.

## STEP 3 — ATS scan

Persona: an ATS engine (deterministic, keyword-driven). Then:

1. Write `<outdir>/keywords.txt` — the top-10 keywords plus secondary JD keywords, one per line.
2. Run the full build once (contract #4 below) to get `<outdir>/ats_report.json`, `resume.pdf`, `resume.tex`.
3. Read `ats_report.json` and write `<outdir>/ats_report.md`: report the overall `score` AND all four `grade_breakdown` categories verbatim — `parse_integrity` /30 (technical parsing), `keyword_coverage` /40, `anti_stuffing` /10, `formatting` /20 (content compliance) — plus the `keywords.missing`/`overused` lists and every failed entry in `checks`. Then add persona commentary: estimated rank vs competing candidates, red flags / disqualifiers, and which sections need stronger optimization to reach 92+.

## STEP 4 — Fix loop

Edit `<outdir>/resume.yaml` per the report's recommendations, rerun contract #4, and repeat until **score >= 92 AND PAGES=1**. Max 4 iterations. If still stuck after 4, report the blocker honestly (e.g. "keyword X is not truthfully claimable") — never fabricate content to raise the score.

## STEP 5 — Export

Final artifacts: `<outdir>/resume.pdf` (local ATS-safe build) and `<outdir>/resume.tex` (Jake's Resume source — tell the user to upload it to overleaf.com for the LaTeX-typeset version; no local LaTeX compiler is required). Send `resume.pdf` to the user if your client supports file delivery. Then summarize: match score before vs after, final ATS score, keywords integrated, and what changed.

## CLI contracts

```
python scripts/render_tex.py RESUME_YAML OUT_TEX
    # Jake's-Resume-style .tex. Exit 0 on success.

python scripts/render_pdf.py RESUME_YAML OUT_PDF
    # ATS-safe PDF via reportlab; auto-shrinks to 1 page.
    # Last line "PAGES=<n>". Exit 0 if 1 page, exit 2 if not (PDF still written).

python scripts/ats_audit.py PDF_PATH --jd JD_TXT --keywords KEYWORDS_TXT --json OUT_JSON
    # Deterministic ATS audit; prints summary, writes JSON. Exit 0 always.

python scripts/build.py RESUME_YAML --jd JD_TXT --keywords KEYWORDS_TXT --outdir DIR
    # Orchestrates all three: DIR/resume.tex, DIR/resume.pdf, DIR/ats_report.json,
    # copies RESUME_YAML to DIR/resume.yaml. Prints "ATS_SCORE=<n>" and "PAGES=<n>".
```

## Resume YAML schema (condensed)

```yaml
name: str
contact: {phone, email, linkedin, location, tagline}   # linkedin without https://; tagline may be ""
summary: str                                           # one paragraph
skills: [{category: str, items: str}]                  # items = ONE comma-separated string
experience: [{company, title, location, start, end, bullets: [str]}]   # end may be "Present"
projects: [{name, tech: str, bullets: [str]}]          # tech = ONE comma-separated string
education: [{school, degree, location, start, end, notes: [str]}]      # start may be ""; notes may be []
certifications: [str]
additional: [{label: str, text: str}]
```

Section render order is fixed: Summary, Skills, Experience, Projects, Education, Certifications, Additional. Do not invent fields.

## Worked example

User pastes a Working Student Compliance JD from "Acme Bank". You then:

```
outdir = output/acme-compliance-werkstudent/
# Step 0: save JD -> jd.txt; read base/resume.yaml
# Step 1: write gap_analysis.md (match score 4/10, top-10 missing keywords, ...)
# Step 2: write resume.yaml (rewritten, truthful)
# Step 3: write keywords.txt, then:
python scripts/build.py output/acme-compliance-werkstudent/resume.yaml --jd output/acme-compliance-werkstudent/jd.txt --keywords output/acme-compliance-werkstudent/keywords.txt --outdir output/acme-compliance-werkstudent
#         write ats_report.md from ats_report.json
# Step 4: edit resume.yaml, rerun build.py until ATS_SCORE>=92 and PAGES=1 (max 4 rounds)
# Step 5: send resume.pdf; point to resume.tex for Overleaf; summarize before/after
```
