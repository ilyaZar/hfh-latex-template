#!/usr/bin/env python3
"""Baut und prüft den isolierten Tabelle-1-Compliance-Test."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


TESTS = Path(__file__).resolve().parent


def run(*command: str) -> None:
    print("+", " ".join(command), flush=True)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(
        command,
        cwd=TESTS,
        env=environment,
        check=True,
    )


def main() -> int:
    try:
        run(
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "table1-compliance.tex",
        )
        run(
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "test_compliance_checker.py",
        )
        run(sys.executable, "check_template_contract.py")
        run(sys.executable, "check_guidance_content.py")
        run(sys.executable, "check_toc_pdf.py")
        run(
            sys.executable,
            "check_compliance.py",
            "../main.tex",
            "../hfh-formatierungen.sty",
            "../docs/00-frontmatter.tex",
            "../docs/01-verwendungshinweis.tex",
            "../docs/02-formale-aspekte.tex",
            "../docs/03-aufbau-wissenschaftlicher-arbeiten.tex",
            "../docs/04-verzeichnisse.tex",
            "../docs/05-eigenstaendigkeitserklaerung.tex",
        )
        run(
            sys.executable,
            "check_compliance.py",
            "table1-compliance.tex",
        )
        run(sys.executable, "check_compliance_pdf.py")
        run(sys.executable, "check_overleaf_archive.py")
    except subprocess.CalledProcessError as error:
        return error.returncode
    print("Alle isolierten Tabelle-1-Compliance-Tests bestanden")
    return 0


if __name__ == "__main__":
    sys.exit(main())
