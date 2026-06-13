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

SECTION_ORDER = ("Summary", "Skills", "Experience", "Projects",
                 "Education", "Certifications", "Additional")

# Shrink ladder: body font first, then leading/spacing, then margins.
ATTEMPTS = (
    {"body": 10.0, "lead": 1.18, "space": 1.00, "margin": 1.4 * cm},
    {"body": 9.5,  "lead": 1.18, "space": 1.00, "margin": 1.4 * cm},
    {"body": 9.0,  "lead": 1.18, "space": 1.00, "margin": 1.4 * cm},
    {"body": 9.0,  "lead": 1.06, "space": 0.75, "margin": 1.4 * cm},
    {"body": 9.0,  "lead": 1.06, "space": 0.70, "margin": 1.1 * cm},
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


def build_story(data, cfg, avail_width):
    styles = make_styles(cfg)
    sp = cfg["space"]
    story = []

    # ---- Header block --------------------------------------------------
    name = str(data.get("name") or "").strip()
    contact = data.get("contact") or {}
    if name:
        story.append(Paragraph(esc(name), styles["name"]))
    contact_parts = [esc(contact.get(k)) for k in
                     ("phone", "email", "linkedin", "location")
                     if str(contact.get(k) or "").strip()]
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), styles["contact"]))
    tagline = str(contact.get("tagline") or "").strip()
    if tagline:
        story.append(Paragraph("<i>%s</i>" % esc(tagline), styles["tagline"]))

    # ---- Helpers --------------------------------------------------------
    def section(title):
        story.append(Paragraph(title, styles["h"]))
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
        section("Summary")
        story.append(Paragraph(esc(summary), styles["body"]))

    # ---- Skills ------------------------------------------------------------
    skills = data.get("skills") or []
    if skills:
        section("Skills")
        for cat in skills:
            category = esc((cat or {}).get("category"))
            items = esc((cat or {}).get("items"))
            story.append(Paragraph("<b>%s:</b> %s" % (category, items),
                                   styles["line"]))

    # ---- Experience ---------------------------------------------------------
    experience = data.get("experience") or []
    if experience:
        section("Experience")
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
        section("Projects")
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
        section("Education")
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
        section("Certifications")
        joined = (" %s " % BULLET).join(esc(c) for c in certifications)
        story.append(Paragraph(joined, styles["body"]))

    # ---- Additional --------------------------------------------------------
    additional = data.get("additional") or []
    if additional:
        section("Additional")
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
    for n, cfg in enumerate(ATTEMPTS, start=1):
        pdf_bytes, pages = render(data, cfg)
        print("attempt %d: body=%.1fpt lead=x%.2f margin=%.2fcm -> %d page(s)"
              % (n, cfg["body"], cfg["lead"], cfg["margin"] / cm, pages))
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
