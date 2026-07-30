#!/usr/bin/env python3
"""Prüft die produktiven Formatdefinitionen gegen den beschlossenen Vertrag."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.tex"


def require(pattern: str, text: str, message: str) -> None:
    if re.search(pattern, text, re.MULTILINE) is None:
        raise ValueError(message)


def main() -> int:
    text = MAIN.read_text(encoding="utf-8")

    if re.search(r"\\usepackage(?:\[[^\]]*\])?\{chngcntr\}", text):
        print("FEHLER: chngcntr darf nicht geladen werden", file=sys.stderr)
        return 1

    requirements = (
        (
            r"\\setlength\s*\{\\footnotesep\}\s*\{14pt\}",
            "footnotesep muss 14 pt betragen",
        ),
        (
            r"\\counterwithout\s*\{footnote\}\s*\{chapter\}",
            "Fußnoten müssen global nummeriert werden",
        ),
        (
            r"\\counterwithout\s*\{table\}\s*\{chapter\}",
            "Tabellen müssen global nummeriert werden",
        ),
        (
            r"\\counterwithout\s*\{figure\}\s*\{chapter\}",
            "Abbildungen müssen global nummeriert werden",
        ),
        (
            r"\\newcommand\s*\{\\source\}",
            "die zentrierte Quellenzeile fehlt",
        ),
        (
            r"\\newcommand\s*\{\\sourceleft\}",
            "die linksbündige Quellenvariante fehlt",
        ),
        (
            r"\\newcommand\s*\{\\sourceindented\}",
            "die eingerückte Quellenvariante fehlt",
        ),
    )

    try:
        for pattern, message in requirements:
            require(pattern, text, message)
    except ValueError as error:
        print(f"FEHLER: {error}", file=sys.stderr)
        return 1

    print("Produktive Formatdefinitionen entsprechen dem Vertrag")
    return 0


if __name__ == "__main__":
    sys.exit(main())
