import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ats_audit.py - deterministic ATS simulation scorer (no AI calls).
#
# Contract:
#   python ats_audit.py PDF_PATH --jd JD_TXT --keywords KEYWORDS_TXT --json OUT_JSON
#
# Rubric (0-100):
#   A. Parse integrity (30)
#   B. Keyword coverage (40)
#   C. Anti-stuffing   (10)
#   D. Formatting      (20)
#
# Prints a human-readable summary, writes the full JSON report, exits 0
# whenever the audit itself completes (the score is data, not failure).

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader

# ---------------------------------------------------------------- constants

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# Candidate phone runs: digits mixed with spaces/dashes/dots/parens/slashes,
# optionally starting with "+" (e.g. +49 30 1234 5678). Validated by digit count.
PHONE_CAND_RE = re.compile(r"\+?\(?\d[\d\s\-()./]{5,}\d")
PHONE_MIN_DIGITS = 9
PHONE_MAX_DIGITS = 16
# Digit runs that are really dates, not phones (e.g. "05/2018 - 03/2019").
PHONE_DATEISH_RE = re.compile(
    r"\d{1,2}[./](?:19|20)\d{2}|(?:19|20)\d{2}\s*[-–—]\s*(?:19|20)\d{2}"
)

# Canonical sections with the header strings CV parsers recognize; a section
# counts as found when ANY of its variants (English or German) appears.
STANDARD_HEADERS = {
    "Summary": ["Summary", "Profile", "Profil", "Kurzprofil"],
    "Skills": ["Skills", "Kenntnisse", "Fähigkeiten", "Kompetenzen"],
    "Experience": ["Experience", "Berufserfahrung", "Praktische Erfahrung"],
    "Projects": ["Projects", "Projekte"],
    "Education": ["Education", "Ausbildung", "Bildungsweg", "Studium"],
    "Certifications": ["Certifications", "Zertifikate", "Zertifizierungen"],
    "Additional": ["Additional", "Weitere Angaben", "Sonstiges"],
}

MONTH = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)"
)
DASH = r"[-–—]"  # hyphen, en dash, em dash

# Accepted range styles:
#   English CVs: "Mon YYYY - Mon YYYY" or "Mon YYYY - Present"
#   German CVs (numeric): "MM/YYYY - MM/YYYY" or "MM/YYYY - heute"
STRICT_RANGE_RE = re.compile(
    rf"^{MONTH}\.?\s+\d{{4}}\s*{DASH}\s*(?:{MONTH}\.?\s+\d{{4}}|Present)$",
    re.IGNORECASE,
)
STRICT_RANGE_NUM_RE = re.compile(
    rf"^\d{{2}}[./]\d{{4}}\s*{DASH}\s*(?:\d{{2}}[./]\d{{4}}|heute|Present)$",
    re.IGNORECASE,
)
EXPECTED_RE = re.compile(rf"^Expected\s+{MONTH}\.?\s+\d{{4}}$", re.IGNORECASE)

# Anything that looks like a date range at all (word-month, numeric, bare-year forms).
LOOSE_RANGE_RE = re.compile(
    rf"(?:[A-Za-z]{{3,9}}\.?\s+(?:19|20)\d{{2}}|\d{{1,2}}[./](?:19|20)\d{{2}}|(?:19|20)\d{{2}})"
    rf"\s*(?:{DASH}|\bto\b|\buntil\b|\bbis\b)\s*"
    rf"(?:[A-Za-z]{{3,9}}\.?\s+(?:19|20)\d{{2}}|\d{{1,2}}[./](?:19|20)\d{{2}}|(?:19|20)\d{{2}}"
    rf"|Present|Current|Now|Ongoing|heute|laufend)",
    re.IGNORECASE,
)

BULLET_LINE_RE = re.compile(r"^\s*(?:[•▪◦●‣·∙*]\s*|[-–]\s+)\S")

# Mojibake / icon glyphs: gender signs, frown, pilcrow, section sign, and the
# U+F000-U+F8FF private-use block (FontAwesome-style icon fonts).
MOJIBAKE_CHARS = {"♂", "♀", "⌢", "¶", "§"}
PUA_LO, PUA_HI = 0xF000, 0xF8FF

JD_TITLE_STOPWORDS = {
    "and", "the", "for", "with", "you", "our", "are", "all", "job", "role",
    "position", "vacancy", "remote", "hybrid", "onsite", "full", "time",
    "part", "mwd", "wmd", "fmd",
}

MAX_KEYWORD_OCCURRENCES = 5

# ------------------------------------------------------------ normalization


def normalize_text(s: str) -> str:
    """Lowercase, treat hyphens/slashes as spaces, collapse whitespace."""
    s = s.lower()
    s = re.sub(r"[-/‐‑‒–—]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def keyword_pattern(keyword: str) -> re.Pattern:
    """Compile a matcher for a normalized keyword, tolerating a trailing
    's' plural on the last word."""
    words = normalize_text(keyword).split()
    if not words:
        return re.compile(r"(?!x)x")  # never matches
    parts = [re.escape(w) for w in words]
    last = words[-1]
    if len(last) >= 4 and last.endswith("s"):
        last_pat = f"(?:{re.escape(last)}|{re.escape(last[:-1])})"
    else:
        last_pat = re.escape(last)
    parts[-1] = last_pat + "s?"
    body = r"\s+".join(parts)
    return re.compile(r"(?<!\w)" + body + r"(?!\w)")


# ----------------------------------------------------------------- loading


def find_phone(text: str):
    """First plausible phone number (9-16 digits, tolerating +49/spaces/dashes),
    skipping digit runs that look like dates."""
    for m in PHONE_CAND_RE.finditer(text):
        cand = m.group(0)
        if PHONE_DATEISH_RE.search(cand):
            continue
        digits = sum(1 for c in cand if c.isdigit())
        if PHONE_MIN_DIGITS <= digits <= PHONE_MAX_DIGITS:
            return re.sub(r"\s+", " ", cand).strip()
    return None


def pdf_has_images(pdf_path: Path):
    """True if any page carries an embedded image XObject (e.g. a header photo).
    German ATS guidance: portal-submitted CVs should be photo-free."""
    try:
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            resources = page.get("/Resources") or {}
            xobjects = resources.get("/XObject")
            if not xobjects:
                continue
            for obj in xobjects.get_object().values():
                try:
                    if obj.get_object().get("/Subtype") == "/Image":
                        return True
                except Exception:
                    continue
        return False
    except Exception:
        return False


def extract_pdf_text(pdf_path: Path):
    """Return (text, page_count). Degrades to ('', 0) on extraction failure."""
    try:
        reader = PdfReader(str(pdf_path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                return "", len(reader.pages)
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages), len(reader.pages)
    except Exception:
        return "", 0


def load_keywords(path: Path):
    """One keyword/phrase per line; skip blanks and #-comments; dedupe on
    normalized form, preserving order and original spelling."""
    keywords = []
    seen = set()
    for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        norm = normalize_text(line)
        if norm and norm not in seen:
            seen.add(norm)
            keywords.append(line)
    return keywords


def jd_title_words(jd_text: str):
    """Deterministic: words (len >= 3) from the first non-blank JD line."""
    title = ""
    for line in jd_text.splitlines():
        if line.strip():
            title = line.strip()
            break
    if not title:
        return []
    words = re.findall(r"[A-Za-z][A-Za-z+#]{2,}", title)
    out = []
    for w in words:
        if w.lower() not in JD_TITLE_STOPWORDS and w.lower() not in {x.lower() for x in out}:
            out.append(w)
    return out


# ------------------------------------------------------------------- audit


def audit(text: str, page_count: int, keywords, jd_text: str, has_images: bool = False):
    checks = []
    recommendations = []
    norm_text = normalize_text(text)

    # Informational (never affects the score): a photo is acceptable in email
    # applications but should be absent from ATS-portal submissions.
    checks.append({
        "name": "no_embedded_image",
        "passed": not has_images,
        "detail": ("no embedded images" if not has_images else
                   "embedded image found (header photo?)"),
    })
    if has_images:
        recommendations.append(
            "PDF contains an embedded image (photo?). Fine for direct email "
            "applications; for ATS-portal submissions rebuild without "
            "contact.photo — German ATS guidance is to keep portal CVs photo-free."
        )

    # Informational: em-dashes in prose are a recognized AI-writing tell and are
    # banned in generated output (en dashes in date ranges are fine).
    em_dashes = text.count("—")
    checks.append({
        "name": "no_em_dashes",
        "passed": em_dashes == 0,
        "detail": ("no em-dashes" if em_dashes == 0
                   else f"{em_dashes} em-dash(es) found"),
    })
    if em_dashes:
        recommendations.append(
            f"Text contains {em_dashes} em-dash(es) (—) - rephrase with commas, "
            "periods, or parentheses; em-dashes read as AI-generated prose."
        )

    # ---- A. Parse integrity (30)
    parse_pts = 0

    text_ok = len(text.strip()) > 800
    if text_ok:
        parse_pts += 10
    else:
        recommendations.append(
            "PDF text extraction yielded {} characters (need > 800) - export a "
            "text-based PDF (no scans/images) with full content.".format(len(text.strip()))
        )
    checks.append({
        "name": "text_extractable",
        "passed": text_ok,
        "detail": f"{len(text.strip())} characters extracted from {page_count} page(s)",
    })

    one_page = page_count == 1
    if one_page:
        parse_pts += 5
    else:
        recommendations.append(
            f"Resume is {page_count} page(s) - condense content to exactly one page."
        )
    checks.append({
        "name": "one_page",
        "passed": one_page,
        "detail": f"page_count = {page_count}",
    })

    email_m = EMAIL_RE.search(text)
    if email_m:
        parse_pts += 5
    else:
        recommendations.append("Add an email address in plain text near the top of the resume.")
    checks.append({
        "name": "email_present",
        "passed": bool(email_m),
        "detail": email_m.group(0) if email_m else "no email address found",
    })

    phone_found = find_phone(text)
    if phone_found:
        parse_pts += 5
    else:
        recommendations.append(
            "Add a phone number in plain text (e.g. +49 30 1234 5678) near the top of the resume."
        )
    checks.append({
        "name": "phone_present",
        "passed": bool(phone_found),
        "detail": phone_found if phone_found else "no phone number found",
    })

    headers_found = []
    for canonical, variants in STANDARD_HEADERS.items():
        for variant in variants:
            base = variant[:-1] if variant.endswith("s") else variant
            if re.search(rf"\b{re.escape(base)}s?\b", text, re.IGNORECASE):
                headers_found.append(canonical)
                break
    headers_ok = len(headers_found) >= 4
    if headers_ok:
        parse_pts += 5
    else:
        missing_headers = [h for h in STANDARD_HEADERS if h not in headers_found]
        recommendations.append(
            "Only {} standard section header(s) found ({}). Use at least 4 of: {} "
            "(English or German variants).".format(
                len(headers_found),
                ", ".join(headers_found) if headers_found else "none",
                ", ".join(missing_headers),
            )
        )
    checks.append({
        "name": "standard_headers",
        "passed": headers_ok,
        "detail": "found {}/7: {}".format(
            len(headers_found), ", ".join(headers_found) if headers_found else "none"
        ),
    })

    # ---- B. Keyword coverage (40) and C. Anti-stuffing (10)
    found_kw, missing_kw, overused_kw = [], [], []
    counts = {}
    for kw in keywords:
        pat = keyword_pattern(kw)
        n = len(pat.findall(norm_text))
        counts[kw] = n
        if n > 0:
            found_kw.append(kw)
        else:
            missing_kw.append(kw)
        if n > MAX_KEYWORD_OCCURRENCES:
            overused_kw.append(kw)

    if keywords:
        keyword_pts = round(40 * len(found_kw) / len(keywords))
    else:
        keyword_pts = 0
        recommendations.append(
            "Keyword list is empty - provide target keywords (one per line) to score coverage."
        )
    checks.append({
        "name": "keyword_coverage",
        "passed": bool(keywords) and not missing_kw,
        "detail": f"{len(found_kw)}/{len(keywords)} keywords found",
    })
    for kw in missing_kw:
        recommendations.append(f"Add missing keyword '{kw}' to Skills or a bullet.")

    stuffing_pts = max(0, 10 - 2 * len(overused_kw))
    checks.append({
        "name": "anti_stuffing",
        "passed": not overused_kw,
        "detail": (
            "no keyword exceeds {} occurrences".format(MAX_KEYWORD_OCCURRENCES)
            if not overused_kw
            else ", ".join(f"'{kw}' x{counts[kw]}" for kw in overused_kw)
        ),
    })
    for kw in overused_kw:
        recommendations.append(
            f"Keyword '{kw}' appears {counts[kw]} times - reduce to "
            f"{MAX_KEYWORD_OCCURRENCES} or fewer mentions to avoid stuffing filters."
        )

    # ---- D. Formatting (20)
    fmt_pts = 0

    # Scan per logical line so a range cannot greedily absorb a date token
    # from the following line (e.g. "Apr 2025 - Present\n2018 - 2019").
    bad_ranges = []
    n_strict = 0
    for line in text.splitlines():
        for m in LOOSE_RANGE_RE.finditer(line):
            snippet = re.sub(r"\s+", " ", m.group(0)).strip()
            if STRICT_RANGE_RE.match(snippet) or STRICT_RANGE_NUM_RE.match(snippet):
                n_strict += 1
            else:
                bad_ranges.append(snippet)
    dates_ok = not bad_ranges
    if dates_ok:
        fmt_pts += 5
    else:
        recommendations.append(
            "Inconsistent date format(s): {}. Use 'Mon YYYY - Mon YYYY' / "
            "'Mon YYYY - Present' / 'Expected Mon YYYY' (English CV) or "
            "'MM/YYYY - MM/YYYY' / 'MM/YYYY - heute' (German CV) everywhere.".format(
                "; ".join(f"'{b}'" for b in bad_ranges[:3])
            )
        )
    checks.append({
        "name": "date_style_consistent",
        "passed": dates_ok,
        "detail": (
            f"{n_strict} compliant range(s), 0 inconsistent"
            if dates_ok
            else f"inconsistent: {'; '.join(bad_ranges[:5])}"
        ),
    })

    bad_glyphs = sorted({
        ch for ch in text
        if ch in MOJIBAKE_CHARS or PUA_LO <= ord(ch) <= PUA_HI
    })
    glyphs_ok = not bad_glyphs
    if glyphs_ok:
        fmt_pts += 5
    else:
        codes = ", ".join(f"U+{ord(c):04X}" for c in bad_glyphs[:8])
        recommendations.append(
            f"Remove icon/mojibake glyphs ({codes}) - replace icon fonts "
            "(FontAwesome etc.) with plain text labels."
        )
    checks.append({
        "name": "no_mojibake",
        "passed": glyphs_ok,
        "detail": (
            "no icon/private-use glyphs"
            if glyphs_ok
            else "found " + ", ".join(f"U+{ord(c):04X}" for c in bad_glyphs[:8])
        ),
    })

    bullet_lines = [ln.strip() for ln in text.splitlines() if BULLET_LINE_RE.match(ln)]
    if bullet_lines:
        avg_len = sum(len(ln) for ln in bullet_lines) / len(bullet_lines)
    else:
        avg_len = 0.0
    bullets_ok = avg_len <= 220
    if bullets_ok:
        fmt_pts += 5
    else:
        recommendations.append(
            f"Average bullet line length is {avg_len:.0f} characters (max 220) - "
            "split long bullets into shorter, single-achievement lines."
        )
    checks.append({
        "name": "bullet_length",
        "passed": bullets_ok,
        "detail": f"{len(bullet_lines)} bullet line(s), average {avg_len:.0f} chars",
    })

    head = text[:300]
    contact_top = bool(EMAIL_RE.search(head) or find_phone(head))
    if contact_top:
        fmt_pts += 5
    else:
        recommendations.append(
            "Contact info (email/phone) not found in the first 300 characters - "
            "move it to the very top of the resume."
        )
    checks.append({
        "name": "contact_at_top",
        "passed": contact_top,
        "detail": (
            "email/phone within first 300 chars"
            if contact_top
            else "no email/phone in first 300 chars"
        ),
    })

    # ---- JD title alignment (recommendations only; never affects the score)
    if jd_text:
        for w in jd_title_words(jd_text):
            w_norm = normalize_text(w)
            if w_norm and not re.search(r"(?<!\w)" + re.escape(w_norm) + r"(?!\w)", norm_text):
                recommendations.append(
                    f"JD title word '{w}' is missing from the resume - consider "
                    "mirroring the target role title in the summary or headline."
                )

    score = parse_pts + keyword_pts + stuffing_pts + fmt_pts
    score = max(0, min(100, int(score)))

    return {
        "score": score,
        "page_count": page_count,
        "grade_breakdown": {
            "parse_integrity": parse_pts,
            "keyword_coverage": keyword_pts,
            "anti_stuffing": stuffing_pts,
            "formatting": fmt_pts,
        },
        "keywords": {
            "found": found_kw,
            "missing": missing_kw,
            "overused": overused_kw,
        },
        "checks": checks,
        "recommendations": recommendations,
    }


# -------------------------------------------------------------------- main


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Deterministic ATS audit of a resume PDF (no AI calls)."
    )
    parser.add_argument("pdf_path", help="Resume PDF to audit")
    parser.add_argument("--jd", help="Job description text file (used for "
                        "recommendations only)")
    parser.add_argument("--keywords", required=True,
                        help="Keywords file, one keyword/phrase per line")
    parser.add_argument("--json", dest="json_out", required=True,
                        help="Path for the full JSON report")
    args = parser.parse_args(argv)

    pdf_path = Path(args.pdf_path)
    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    kw_path = Path(args.keywords)
    if not kw_path.is_file():
        print(f"ERROR: keywords file not found: {kw_path}", file=sys.stderr)
        return 1
    keywords = load_keywords(kw_path)

    jd_text = ""
    if args.jd:
        jd_path = Path(args.jd)
        if jd_path.is_file():
            jd_text = jd_path.read_text(encoding="utf-8", errors="replace")
        else:
            print(f"WARNING: JD file not found, skipping JD checks: {jd_path}",
                  file=sys.stderr)

    text, page_count = extract_pdf_text(pdf_path)
    report = audit(text, page_count, keywords, jd_text,
                   has_images=pdf_has_images(pdf_path))

    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Human-readable summary
    gb = report["grade_breakdown"]
    print(f"ATS AUDIT: {pdf_path}")
    print(f"Score: {report['score']}/100   Pages: {report['page_count']}")
    print(f"  Parse integrity  : {gb['parse_integrity']:>2}/30")
    print(f"  Keyword coverage : {gb['keyword_coverage']:>2}/40 "
          f"({len(report['keywords']['found'])}/{len(keywords)} keywords found)")
    print(f"  Anti-stuffing    : {gb['anti_stuffing']:>2}/10")
    print(f"  Formatting       : {gb['formatting']:>2}/20")
    if report["keywords"]["missing"]:
        print("Missing keywords : " + ", ".join(report["keywords"]["missing"]))
    if report["keywords"]["overused"]:
        print("Overused keywords: " + ", ".join(report["keywords"]["overused"]))
    failed = [c["name"] for c in report["checks"] if not c["passed"]]
    if failed:
        print("Failed checks    : " + ", ".join(failed))
    if report["recommendations"]:
        print("Recommendations:")
        for r in report["recommendations"]:
            print(f"  - {r}")
    print(f"Report written   : {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
