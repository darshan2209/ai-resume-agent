#!/usr/bin/env python3
"""build.py -- Contract 4 of the resume-agent pipeline (orchestrator).

Usage:
    python scripts/build.py RESUME_YAML \
        --jd JD_TXT --keywords KEYWORDS_TXT --outdir DIR

Steps:
  1. render_tex.py  RESUME_YAML DIR/resume.tex     (contract 1)
  2. render_pdf.py  RESUME_YAML DIR/resume.pdf     (contract 2; exit 2 = >1 page)
  3. ats_audit.py   DIR/resume.pdf --jd JD_TXT --keywords KEYWORDS_TXT
                    --json DIR/ats_report.json     (contract 3)
  4. copy RESUME_YAML -> DIR/resume.yaml (unless it already is that file)

Prints each step's output, then a summary whose final lines are:
    ATS_SCORE=<n>
    PAGES=<n>

Exit codes: 0 = success and PDF fits on one page;
            2 = pipeline completed but the PDF is more than one page;
            1 = a step failed outright.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def run_step(label, cmd):
    """Run a pipeline step, echo its output, return (exit_code, stdout)."""
    print("== {0}: {1}".format(label, " ".join(str(c) for c in cmd)))
    proc = subprocess.run(
        [str(c) for c in cmd],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.stdout:
        print(proc.stdout.rstrip("\n"))
    if proc.stderr:
        print(proc.stderr.rstrip("\n"), file=sys.stderr)
    return proc.returncode, proc.stdout or ""


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Orchestrate the resume pipeline: LaTeX render, "
                    "ATS-safe PDF render, deterministic ATS audit.")
    parser.add_argument("resume_yaml", help="tailored resume YAML (canonical schema)")
    parser.add_argument("--jd", required=True, help="job description .txt")
    parser.add_argument("--keywords", required=True,
                        help="keywords .txt, one keyword/phrase per line")
    parser.add_argument("--outdir", required=True, help="output directory")
    args = parser.parse_args(argv)

    resume_yaml = Path(args.resume_yaml)
    if not resume_yaml.is_file():
        print("ERROR: resume YAML not found: {0}".format(resume_yaml),
              file=sys.stderr)
        return 1

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    tex_path = outdir / "resume.tex"
    pdf_path = outdir / "resume.pdf"
    report_path = outdir / "ats_report.json"

    # -- Step 1: LaTeX (contract 1) -------------------------------------
    code, _ = run_step("render_tex", [
        sys.executable, SCRIPTS_DIR / "render_tex.py", resume_yaml, tex_path])
    if code != 0 or not tex_path.is_file():
        print("ERROR: render_tex.py failed (exit {0})".format(code),
              file=sys.stderr)
        return 1

    # -- Step 2: PDF (contract 2) ---------------------------------------
    # exit 0 = one page; exit 2 = could not fit but PDF still written.
    code, pdf_out = run_step("render_pdf", [
        sys.executable, SCRIPTS_DIR / "render_pdf.py", resume_yaml, pdf_path])
    if code not in (0, 2) or not pdf_path.is_file():
        print("ERROR: render_pdf.py failed (exit {0})".format(code),
              file=sys.stderr)
        return 1
    pdf_exit = code

    pages = None
    for line in reversed(pdf_out.splitlines()):
        match = re.fullmatch(r"PAGES=(\d+)", line.strip())
        if match:
            pages = int(match.group(1))
            break
    if pages is None:
        print("WARNING: could not parse PAGES= from render_pdf.py output",
              file=sys.stderr)

    # -- Step 3: ATS audit (contract 3) ----------------------------------
    code, _ = run_step("ats_audit", [
        sys.executable, SCRIPTS_DIR / "ats_audit.py", pdf_path,
        "--jd", args.jd, "--keywords", args.keywords, "--json", report_path])
    if code != 0 or not report_path.is_file():
        print("ERROR: ats_audit.py failed (exit {0})".format(code),
              file=sys.stderr)
        return 1

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        score = report["score"]
        if pages is None:
            pages = report.get("page_count")
    except (OSError, ValueError, KeyError) as exc:
        print("ERROR: could not read score from {0}: {1}".format(
            report_path, exc), file=sys.stderr)
        return 1

    # -- Step 4: copy the YAML alongside the artifacts -------------------
    target_yaml = outdir / "resume.yaml"
    if resume_yaml.resolve() != target_yaml.resolve():
        shutil.copyfile(resume_yaml, target_yaml)

    # -- Summary ----------------------------------------------------------
    print()
    print("== build summary ==")
    print("tex:    {0}".format(tex_path))
    print("pdf:    {0}".format(pdf_path))
    print("report: {0}".format(report_path))
    print("yaml:   {0}".format(target_yaml))
    print("ATS_SCORE={0}".format(score))
    print("PAGES={0}".format(pages if pages is not None else "?"))
    return 0 if pdf_exit == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
