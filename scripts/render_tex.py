#!/usr/bin/env python3
"""render_tex.py -- Contract 1 of the resume-agent pipeline.

Usage:
    python scripts/render_tex.py RESUME_YAML OUT_TEX

Renders a resume YAML (canonical schema) into a complete Jake's-Resume-style
LaTeX document via templates/jakes_resume.tex.j2. The .tex is intended for
Overleaf compilation (no local LaTeX toolchain required).

ATS adaptations vs. stock Jake's Resume:
  * no FontAwesome / marvosym icons -- plain-text contact line
  * fixed section order: Summary, Skills, Experience, Projects, Education,
    Certifications, Additional
  * machine-readability preamble kept (pdfgentounicode, glyphtounicode,
    hyperref hidelinks)

Jinja2 uses custom delimiters so LaTeX braces never collide:
  variables << >>, blocks <% %>, comments <# #>.

Exit codes: 0 on success, 1 on input/usage errors.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import argparse
import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
TEMPLATE_NAME = "jakes_resume.tex.j2"

# Single-pass replacement table: keys are matched simultaneously by one regex,
# so replacement text (which itself contains specials) is never re-escaped.
_LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
_LATEX_RE = re.compile("|".join(re.escape(ch) for ch in _LATEX_SPECIALS))


def latex_escape(value):
    """Escape every LaTeX special character in a string (single pass)."""
    if value is None:
        return ""
    return _LATEX_RE.sub(lambda m: _LATEX_SPECIALS[m.group()], str(value))


def url_escape(value):
    r"""Minimal escaping for the URL argument of \href (% and # break it;
    everything else is read more or less verbatim by hyperref)."""
    if value is None:
        return ""
    return str(value).replace("%", r"\%").replace("#", r"\#")


def _s(value):
    """Coerce to stripped string; None becomes ''."""
    if value is None:
        return ""
    return str(value).strip()


def date_range(start, end):
    """'Apr 2025 -- Present', or just one side if the other is empty."""
    if start and end:
        return "{0} -- {1}".format(start, end)
    return start or end


def build_context(data):
    """Normalise the canonical resume schema into a fully-escaped template
    context. Every string that came from the YAML is latex_escape()d here,
    so the template can interpolate values directly."""
    if not isinstance(data, dict):
        raise ValueError("resume YAML must be a mapping at the top level")

    contact = data.get("contact") or {}
    phone = _s(contact.get("phone"))
    email = _s(contact.get("email"))
    linkedin = _s(contact.get("linkedin"))
    location = _s(contact.get("location"))
    tagline = _s(contact.get("tagline"))

    parts = []
    if phone:
        parts.append(latex_escape(phone))
    if email:
        parts.append(r"\href{mailto:%s}{%s}" % (url_escape(email), latex_escape(email)))
    if linkedin:
        if linkedin.lower().startswith(("http://", "https://")):
            url = linkedin
        else:
            url = "https://" + linkedin
        parts.append(r"\href{%s}{%s}" % (url_escape(url), latex_escape(linkedin)))
    if location:
        parts.append(latex_escape(location))

    skills = []
    for entry in data.get("skills") or []:
        entry = entry or {}
        category = latex_escape(_s(entry.get("category")))
        items = latex_escape(_s(entry.get("items")))
        if category or items:
            skills.append({"category": category, "items": items})

    experience = []
    for job in data.get("experience") or []:
        job = job or {}
        experience.append({
            "company": latex_escape(_s(job.get("company"))),
            "title": latex_escape(_s(job.get("title"))),
            "location": latex_escape(_s(job.get("location"))),
            "dates": date_range(latex_escape(_s(job.get("start"))),
                                latex_escape(_s(job.get("end")))),
            "bullets": [latex_escape(_s(b))
                        for b in (job.get("bullets") or []) if _s(b)],
        })

    projects = []
    for proj in data.get("projects") or []:
        proj = proj or {}
        projects.append({
            "name": latex_escape(_s(proj.get("name"))),
            "tech": latex_escape(_s(proj.get("tech"))),
            "bullets": [latex_escape(_s(b))
                        for b in (proj.get("bullets") or []) if _s(b)],
        })

    education = []
    for edu in data.get("education") or []:
        edu = edu or {}
        education.append({
            "school": latex_escape(_s(edu.get("school"))),
            "degree": latex_escape(_s(edu.get("degree"))),
            "location": latex_escape(_s(edu.get("location"))),
            "dates": date_range(latex_escape(_s(edu.get("start"))),
                                latex_escape(_s(edu.get("end")))),
            "notes": [latex_escape(_s(n))
                      for n in (edu.get("notes") or []) if _s(n)],
        })

    certifications = [latex_escape(_s(c))
                      for c in (data.get("certifications") or []) if _s(c)]

    additional = []
    for extra in data.get("additional") or []:
        extra = extra or {}
        label = latex_escape(_s(extra.get("label")))
        text = latex_escape(_s(extra.get("text")))
        if label or text:
            additional.append({"label": label, "text": text})

    return {
        "name": latex_escape(_s(data.get("name"))),
        "contact_line": " $|$ ".join(parts),
        "tagline": latex_escape(tagline),
        "summary": latex_escape(_s(data.get("summary"))),
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "education": education,
        "certifications": certifications,
        "additional": additional,
    }


def make_env():
    """Jinja2 environment with LaTeX-safe delimiters and the latex_escape
    filter registered (values are pre-escaped by build_context; the filter is
    available for ad-hoc template use)."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        comment_start_string="<#",
        comment_end_string="#>",
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,
        undefined=StrictUndefined,
    )
    env.filters["latex_escape"] = latex_escape
    return env


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render resume YAML to Jake's-Resume-style LaTeX "
                    "(ATS-safe, icon-free, for Overleaf compilation).")
    parser.add_argument("resume_yaml", help="path to resume YAML (canonical schema)")
    parser.add_argument("out_tex", help="path for the generated .tex file")
    args = parser.parse_args(argv)

    yaml_path = Path(args.resume_yaml)
    out_path = Path(args.out_tex)

    try:
        raw = yaml_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("ERROR: resume YAML not found: {0}".format(yaml_path), file=sys.stderr)
        return 1
    except OSError as exc:
        print("ERROR: could not read {0}: {1}".format(yaml_path, exc), file=sys.stderr)
        return 1

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        print("ERROR: could not parse YAML: {0}".format(exc), file=sys.stderr)
        return 1

    try:
        context = build_context(data)
    except ValueError as exc:
        print("ERROR: {0}".format(exc), file=sys.stderr)
        return 1

    env = make_env()
    tex = env.get_template(TEMPLATE_NAME).render(**context)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(tex, encoding="utf-8", newline="\n")
    print("Wrote {0}".format(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
