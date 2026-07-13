#!/usr/bin/env python
"""render_cover_letter.py -- Contract 5 of the resume-agent pipeline.

Usage:
    python render_cover_letter.py COVER_YAML OUT_PDF

ATS-safe one-page cover letter PDF (reportlab, Helvetica only). Layout follows
German Anschreiben conventions (DIN 5008-informed): sender block, recipient
block, right-aligned city+date line, bold subject line (without a "Betreff:"
prefix), salutation, body paragraphs, closing formula, typed name, optional
enclosures ("Anlagen") line. The same layout doubles as a clean international
English letter -- content decides the register, not the renderer.

Single-page enforcement mirrors render_pdf.py: candidate layouts are tried
from spacious to compact and the first that fits is kept. Prints "WORDS=<n>"
and "PAGES=<n>". Exit 0 if the letter fits on one page, exit 2 otherwise
(the PDF is still written).

Cover letter YAML schema:
    lang: en | de                  # optional, default en (Anlagen line label)
    sender: {name, location, phone, email, linkedin}   # linkedin optional
    recipient: {company, contact, location}            # contact/location optional
    date: "Berlin, 12.07.2026"     # full pre-formatted city+date line
    subject: str                   # bold subject line
    salutation: str                # e.g. "Sehr geehrte Frau Schneider,"
    paragraphs: [str, ...]         # body, 3-5 paragraphs
    closing: str                   # e.g. "Mit freundlichen Grüßen"
    signature: str                 # typed full name
    enclosures: str                # optional, e.g. "Lebenslauf, Zeugnisse"
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import argparse
import io
import re
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Candidate layouts, spacious -> compact (same strategy as render_pdf.py).
CANDIDATES = (
    {"body": 11.0, "lead": 1.42, "gap": 9.0, "margin": 2.20 * cm},
    {"body": 10.5, "lead": 1.40, "gap": 8.0, "margin": 2.00 * cm},
    {"body": 10.5, "lead": 1.32, "gap": 7.0, "margin": 1.90 * cm},
    {"body": 10.0, "lead": 1.30, "gap": 6.0, "margin": 1.80 * cm},
    {"body": 10.0, "lead": 1.24, "gap": 5.0, "margin": 1.70 * cm},
    {"body": 9.5,  "lead": 1.22, "gap": 4.5, "margin": 1.60 * cm},
)

ANLAGEN_LABEL = {"de": "Anlagen", "en": "Enclosures"}


def esc(value):
    if value is None:
        return ""
    return xml_escape(str(value).strip())


def _s(value):
    if value is None:
        return ""
    return str(value).strip()


def make_styles(cfg):
    body = cfg["body"]
    lead = body * cfg["lead"]
    base = dict(fontName="Helvetica", fontSize=body, leading=lead,
                textColor=colors.black)
    return {
        "sender_name": ParagraphStyle("sender_name", fontName="Helvetica-Bold",
                                      fontSize=body + 2, leading=(body + 2) * 1.2,
                                      alignment=TA_LEFT, spaceAfter=1),
        "block": ParagraphStyle("block", alignment=TA_LEFT, **base),
        "date": ParagraphStyle("date", alignment=TA_RIGHT, **base),
        "subject": ParagraphStyle("subject", fontName="Helvetica-Bold",
                                  fontSize=body, leading=lead, alignment=TA_LEFT),
        "para": ParagraphStyle("para", alignment=TA_LEFT,
                               spaceAfter=cfg["gap"], **base),
    }


def build_story(data, cfg):
    styles = make_styles(cfg)
    gap = cfg["gap"]
    story = []

    sender = data.get("sender") or {}
    recipient = data.get("recipient") or {}

    # ---- Sender block -----------------------------------------------------
    name = _s(sender.get("name"))
    if name:
        story.append(Paragraph(esc(name), styles["sender_name"]))
    contact_bits = [esc(sender.get(k)) for k in
                    ("location", "phone", "email", "linkedin")
                    if _s(sender.get(k))]
    if contact_bits:
        story.append(Paragraph(" &middot; ".join(contact_bits), styles["block"]))
    story.append(Spacer(1, 2.2 * gap))

    # ---- Recipient block ---------------------------------------------------
    recipient_lines = [esc(recipient.get(k)) for k in
                       ("company", "contact", "location")
                       if _s(recipient.get(k))]
    if recipient_lines:
        story.append(Paragraph("<br/>".join(recipient_lines), styles["block"]))
        story.append(Spacer(1, 1.5 * gap))

    # ---- Date line (right-aligned, DIN style) ------------------------------
    date_line = _s(data.get("date"))
    if date_line:
        story.append(Paragraph(esc(date_line), styles["date"]))
        story.append(Spacer(1, 2.0 * gap))

    # ---- Subject ------------------------------------------------------------
    subject = _s(data.get("subject"))
    if subject:
        story.append(Paragraph(esc(subject), styles["subject"]))
        story.append(Spacer(1, 1.8 * gap))

    # ---- Salutation ----------------------------------------------------------
    salutation = _s(data.get("salutation"))
    if salutation:
        story.append(Paragraph(esc(salutation), styles["para"]))

    # ---- Body ---------------------------------------------------------------
    for p in data.get("paragraphs") or []:
        if _s(p):
            story.append(Paragraph(esc(p), styles["para"]))

    # ---- Closing + signature -------------------------------------------------
    closing = _s(data.get("closing"))
    signature = _s(data.get("signature"))
    if closing:
        story.append(Spacer(1, 0.5 * gap))
        story.append(Paragraph(esc(closing), styles["block"]))
    if signature:
        story.append(Spacer(1, 1.5 * gap))
        story.append(Paragraph(esc(signature), styles["block"]))

    # ---- Enclosures ------------------------------------------------------------
    enclosures = _s(data.get("enclosures"))
    if enclosures:
        lang = (_s(data.get("lang")) or "en").lower()
        label = ANLAGEN_LABEL.get(lang, ANLAGEN_LABEL["en"])
        story.append(Spacer(1, 2.0 * gap))
        story.append(Paragraph("<b>%s:</b> %s" % (label, esc(enclosures)),
                               styles["block"]))

    return story


def count_pages(pdf_bytes, doc):
    try:
        from pypdf import PdfReader
        return len(PdfReader(io.BytesIO(pdf_bytes)).pages)
    except Exception:
        return int(getattr(doc, "page", 1) or 1)


def render(data, cfg):
    sender = data.get("sender") or {}
    name = _s(sender.get("name")) or "Cover Letter"
    margin = cfg["margin"]
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=margin, rightMargin=margin,
                            topMargin=margin * 0.8, bottomMargin=margin * 0.8,
                            title="%s - Cover Letter" % name, author=name)
    doc.build(build_story(data, cfg))
    pdf_bytes = buf.getvalue()
    return pdf_bytes, count_pages(pdf_bytes, doc)


def word_count(data):
    words = 0
    for p in data.get("paragraphs") or []:
        words += len(re.findall(r"\S+", _s(p)))
    return words


def main():
    parser = argparse.ArgumentParser(
        description="Render an ATS-safe one-page cover letter PDF from YAML.")
    parser.add_argument("cover_yaml", help="Path to the cover letter YAML file")
    parser.add_argument("out_pdf", help="Path for the output PDF")
    args = parser.parse_args()

    yaml_path = Path(args.cover_yaml)
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("ERROR: %s did not parse to a mapping" % yaml_path)
        print("PAGES=0")
        return 2

    pdf_bytes, pages = b"", 0
    for n, cfg in enumerate(CANDIDATES, start=1):
        pdf_bytes, pages = render(data, cfg)
        print("try %d: body=%.1fpt lead=x%.2f margin=%.2fcm -> %d page(s)"
              % (n, cfg["body"], cfg["lead"], cfg["margin"] / cm, pages))
        if pages <= 1:
            break

    out_path = Path(args.out_pdf)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(pdf_bytes)
    print("wrote %s" % out_path)
    print("WORDS=%d" % word_count(data))
    print("PAGES=%d" % pages)
    return 0 if pages == 1 else 2


if __name__ == "__main__":
    sys.exit(main())
