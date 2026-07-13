#!/usr/bin/env python
"""render_pdf.py -- ATS-safe single-page resume PDF built with reportlab/platypus.

Usage:
    python render_pdf.py RESUME_YAML OUT_PDF

Layout mirrors Jake's Resume: A4 page, Helvetica family only, centered name
header, ruled section headers, two-column (borderless table) entry header
lines so dates/locations right-align while text still extracts left-to-right.

Single-page enforcement: renders to a memory buffer and counts pages; retries
with body font 10 -> 9.5 -> 9pt, then tighter leading/spacing, then 1.1cm
margins. Prints "PAGES=<n>" as the last line. Exit 0 if the resume fits on
one page, exit 2 otherwise (the PDF is still written).
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import argparse
import io
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (HRFlowable, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

EN_DASH = "–"
BULLET = "•"
LINK_HEX = "#1155cc"  # blue so email/LinkedIn read as clickable hyperlinks

SECTION_ORDER = ("Summary", "Skills", "Experience", "Projects",
                 "Education", "Certifications", "Additional")

# Section header labels; overridable per-document via a top-level `labels:`
# mapping in the YAML (e.g. labels: {experience: Berufserfahrung}) so German
# CVs can carry the header strings German ATS parsers recognize.
DEFAULT_LABELS = {
    "summary": "Summary",
    "skills": "Skills",
    "experience": "Experience",
    "projects": "Projects",
    "education": "Education",
    "certifications": "Certifications",
    "additional": "Additional",
}

PHOTO_WIDTH = 2.8  # cm; passport-style header photo (German Lebenslauf option)
PHOTO_MAX_HEIGHT = 3.6  # cm

# Candidate layouts, ordered spacious -> compact. We pick the FIRST that fits
# on one page, i.e. the most spacious layout that still fits. Short resumes land
# near the top (large font, airy spacing -> fills the page, easy for HR to read);
# long resumes fall through to the compact end (shrunk to fit). This both removes
# bottom whitespace on short resumes and keeps long ones on a single page.
CANDIDATES = (
    {"body": 11.0, "lead": 1.30, "space": 2.10, "margin": 1.55 * cm},
    {"body": 10.5, "lead": 1.28, "space": 1.90, "margin": 1.50 * cm},
    {"body": 10.5, "lead": 1.24, "space": 1.60, "margin": 1.45 * cm},
    {"body": 10.0, "lead": 1.24, "space": 1.45, "margin": 1.40 * cm},
    {"body": 10.0, "lead": 1.20, "space": 1.25, "margin": 1.40 * cm},
    {"body": 10.0, "lead": 1.18, "space": 1.05, "margin": 1.40 * cm},
    {"body": 9.5,  "lead": 1.18, "space": 1.00, "margin": 1.35 * cm},
    {"body": 9.5,  "lead": 1.12, "space": 0.85, "margin": 1.30 * cm},
    {"body": 9.0,  "lead": 1.14, "space": 0.85, "margin": 1.30 * cm},
    {"body": 9.0,  "lead": 1.08, "space": 0.72, "margin": 1.20 * cm},
    {"body": 9.0,  "lead": 1.05, "space": 0.62, "margin": 1.10 * cm},
)

# Zero-padding, top-aligned, borderless table style for two-column lines.
PAD0 = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
])


def esc(value):
    """XML-escape a value for use inside reportlab Paragraph markup."""
    if value is None:
        return ""
    return xml_escape(str(value).strip())


def date_range(start, end):
    parts = [p for p in (str(start or "").strip(), str(end or "").strip()) if p]
    return (" %s " % EN_DASH).join(parts)


def contact_chip(kind, value):
    """Render a contact field; email/linkedin/portfolio become clickable
    hyperlinks. Email and LinkedIn keep their address as visible text (ATS
    extracts them as plain text); the portfolio renders as a compact
    "Portfolio" label with the URL only in the link annotation."""
    v = str(value or "").strip()
    if not v:
        return ""
    if kind == "email":
        return '<a href="mailto:%s" color="%s">%s</a>' % (esc(v), LINK_HEX, esc(v))
    if kind in ("linkedin", "portfolio"):
        href = v if v.lower().startswith("http") else "https://" + v
        label = "Portfolio" if kind == "portfolio" else esc(v)
        return '<a href="%s" color="%s">%s</a>' % (esc(href), LINK_HEX, label)
    return esc(v)


def make_styles(cfg):
    body = cfg["body"]
    lead = body * cfg["lead"]
    sp = cfg["space"]
    base = dict(fontName="Helvetica", fontSize=body, leading=lead,
                textColor=colors.black)
    return {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=17,
                               leading=20, alignment=TA_CENTER, spaceAfter=2),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9,
                                  leading=11.5, alignment=TA_CENTER),
        "tagline": ParagraphStyle("tagline", fontName="Helvetica", fontSize=9,
                                  leading=11, alignment=TA_CENTER,
                                  spaceBefore=1.5),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold",
                            fontSize=body + 0.5, leading=(body + 0.5) * 1.15,
                            spaceBefore=7 * sp, alignment=TA_LEFT),
        "body": ParagraphStyle("body", alignment=TA_LEFT, **base),
        "line": ParagraphStyle("line", alignment=TA_LEFT, spaceAfter=1.2 * sp,
                               **base),
        "left": ParagraphStyle("left", alignment=TA_LEFT, **base),
        "right": ParagraphStyle("right", alignment=TA_RIGHT, **base),
        "bullet": ParagraphStyle("bullet", alignment=TA_LEFT, leftIndent=11,
                                 bulletIndent=1, bulletFontName="Helvetica",
                                 bulletFontSize=body, spaceAfter=0.6 * sp,
                                 **base),
    }


def resolve_labels(data):
    """Merge the optional top-level `labels:` mapping over the defaults."""
    overrides = data.get("labels") or {}
    labels = dict(DEFAULT_LABELS)
    for key, value in overrides.items():
        k = str(key or "").strip().lower()
        v = str(value or "").strip()
        if k in labels and v:
            labels[k] = v
    return labels


def build_story(data, cfg, avail_width):
    styles = make_styles(cfg)
    sp = cfg["space"]
    labels = resolve_labels(data)
    story = []

    # ---- Header block --------------------------------------------------
    name = str(data.get("name") or "").strip()
    contact = data.get("contact") or {}
    header = []
    if name:
        header.append(Paragraph(esc(name), styles["name"]))
    contact_parts = [contact_chip(k, contact.get(k)) for k in
                     ("phone", "email", "linkedin", "portfolio", "location")
                     if str(contact.get(k) or "").strip()]
    if contact_parts:
        header.append(Paragraph(" | ".join(contact_parts), styles["contact"]))
    tagline = str(contact.get("tagline") or "").strip()
    if tagline:
        header.append(Paragraph("<i>%s</i>" % esc(tagline), styles["tagline"]))

    # Optional header photo (contact: photo: <path>) for German-style CVs.
    # Placed right of the name/contact block; skipped silently if unset and
    # with a warning if the file is missing.
    photo_path = str(contact.get("photo") or "").strip()
    if photo_path and Path(photo_path).is_file():
        from reportlab.platypus import Image as RLImage
        img = RLImage(photo_path, width=PHOTO_WIDTH * cm,
                      height=PHOTO_MAX_HEIGHT * cm, kind="proportional")
        photo_col = (PHOTO_WIDTH + 0.3) * cm
        table = Table([[header, img]],
                      colWidths=[avail_width - photo_col, photo_col])
        table.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("VALIGN", (0, 0), (0, 0), "MIDDLE"),  # name block centers on photo
            ("VALIGN", (1, 0), (1, 0), "TOP"),
        ]))
        story.append(table)
    else:
        if photo_path:
            print("WARNING: photo file not found, rendering without photo: %s"
                  % photo_path)
        story.extend(header)

    # ---- Helpers --------------------------------------------------------
    def section(title):
        story.append(Paragraph(esc(title), styles["h"]))
        story.append(HRFlowable(width="100%", thickness=0.7,
                                color=colors.black, spaceBefore=1.5,
                                spaceAfter=3 * sp))

    def two_col(left_markup, right_markup):
        row = [[Paragraph(left_markup, styles["left"]),
                Paragraph(right_markup, styles["right"])]]
        table = Table(row, colWidths=[avail_width * 0.72, avail_width * 0.28])
        table.setStyle(PAD0)
        story.append(table)

    def add_bullets(items):
        items = [b for b in (items or []) if str(b or "").strip()]
        if items:
            story.append(Spacer(1, 1 * sp))
        for text in items:
            story.append(Paragraph(esc(text), styles["bullet"],
                                   bulletText=BULLET))

    # ---- Summary ---------------------------------------------------------
    summary = str(data.get("summary") or "").strip()
    if summary:
        section(labels["summary"])
        story.append(Paragraph(esc(summary), styles["body"]))

    # ---- Skills ------------------------------------------------------------
    skills = data.get("skills") or []
    if skills:
        section(labels["skills"])
        for cat in skills:
            category = esc((cat or {}).get("category"))
            items = esc((cat or {}).get("items"))
            story.append(Paragraph("<b>%s:</b> %s" % (category, items),
                                   styles["line"]))

    # ---- Experience ---------------------------------------------------------
    experience = data.get("experience") or []
    if experience:
        section(labels["experience"])
        for i, job in enumerate(experience):
            job = job or {}
            if i:
                story.append(Spacer(1, 3 * sp))
            dates = date_range(job.get("start"), job.get("end"))
            two_col("<b>%s</b>" % esc(job.get("title")),
                    "<b>%s</b>" % esc(dates))
            two_col("<i>%s</i>" % esc(job.get("company")),
                    "<i>%s</i>" % esc(job.get("location")))
            add_bullets(job.get("bullets"))

    # ---- Projects --------------------------------------------------------
    projects = data.get("projects") or []
    if projects:
        section(labels["projects"])
        for i, proj in enumerate(projects):
            proj = proj or {}
            if i:
                story.append(Spacer(1, 2.5 * sp))
            tech = str(proj.get("tech") or "").strip()
            if tech:
                head = "<b>%s</b> | <i>%s</i>" % (esc(proj.get("name")),
                                                  esc(tech))
            else:
                head = "<b>%s</b>" % esc(proj.get("name"))
            story.append(Paragraph(head, styles["left"]))
            add_bullets(proj.get("bullets"))

    # ---- Education ---------------------------------------------------------
    education = data.get("education") or []
    if education:
        section(labels["education"])
        for i, edu in enumerate(education):
            edu = edu or {}
            if i:
                story.append(Spacer(1, 3 * sp))
            dates = date_range(edu.get("start"), edu.get("end"))
            two_col("<b>%s</b>" % esc(edu.get("school")),
                    "<b>%s</b>" % esc(dates))
            two_col("<i>%s</i>" % esc(edu.get("degree")),
                    "<i>%s</i>" % esc(edu.get("location")))
            add_bullets(edu.get("notes"))

    # ---- Certifications ---------------------------------------------------
    certifications = [c for c in (data.get("certifications") or [])
                      if str(c or "").strip()]
    if certifications:
        section(labels["certifications"])
        joined = (" %s " % BULLET).join(esc(c) for c in certifications)
        story.append(Paragraph(joined, styles["body"]))

    # ---- Additional --------------------------------------------------------
    additional = data.get("additional") or []
    if additional:
        section(labels["additional"])
        for item in additional:
            item = item or {}
            story.append(Paragraph("<b>%s:</b> %s" % (esc(item.get("label")),
                                                      esc(item.get("text"))),
                                   styles["line"]))

    return story


def count_pages(pdf_bytes, doc):
    try:
        from pypdf import PdfReader
        return len(PdfReader(io.BytesIO(pdf_bytes)).pages)
    except Exception:
        return int(getattr(doc, "page", 1) or 1)


def render(data, cfg):
    name = str(data.get("name") or "Resume").strip() or "Resume"
    margin = cfg["margin"]
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=margin, rightMargin=margin,
                            topMargin=margin, bottomMargin=margin,
                            title="%s - Resume" % name, author=name)
    avail_width = A4[0] - 2 * margin
    doc.build(build_story(data, cfg, avail_width))
    pdf_bytes = buf.getvalue()
    return pdf_bytes, count_pages(pdf_bytes, doc)


def main():
    parser = argparse.ArgumentParser(
        description="Render an ATS-safe single-page resume PDF from YAML.")
    parser.add_argument("resume_yaml", help="Path to the resume YAML file")
    parser.add_argument("out_pdf", help="Path for the output PDF")
    args = parser.parse_args()

    yaml_path = Path(args.resume_yaml)
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("ERROR: %s did not parse to a mapping" % yaml_path)
        print("PAGES=0")
        return 2

    pdf_bytes, pages = b"", 0
    for n, cfg in enumerate(CANDIDATES, start=1):
        pdf_bytes, pages = render(data, cfg)
        print("try %d: body=%.1fpt lead=x%.2f space=x%.2f margin=%.2fcm -> %d page(s)"
              % (n, cfg["body"], cfg["lead"], cfg["space"], cfg["margin"] / cm, pages))
        if pages <= 1:
            break

    out_path = Path(args.out_pdf)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(pdf_bytes)
    print("wrote %s" % out_path)
    print("PAGES=%d" % pages)
    return 0 if pages == 1 else 2


if __name__ == "__main__":
    sys.exit(main())
