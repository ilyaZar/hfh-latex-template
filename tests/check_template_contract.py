#!/usr/bin/env python3
"""Prüft die produktiven Formatdefinitionen gegen den beschlossenen Vertrag."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FORMATTING = ROOT / "hfh-formatierungen.sty"


def require(pattern: str, text: str, message: str) -> None:
    if re.search(pattern, text, re.MULTILINE) is None:
        raise ValueError(message)


def main() -> int:
    text = FORMATTING.read_text(encoding="utf-8")

    forbidden_packages = {
        "chngcntr": "die LaTeX-Kernelbefehle ersetzen chngcntr",
        "inputenc": "UTF-8 ist seit LaTeX 2018 Kernelstandard",
        "natbib": "biblatex mit Biber ersetzt natbib",
    }
    for package, reason in forbidden_packages.items():
        pattern = (
            rf"\\(?:usepackage|RequirePackage)"
            rf"(?:\[[^\]]*\])?\{{{package}\}}"
        )
        if re.search(pattern, text):
            print(
                f"FEHLER: {package} darf nicht geladen werden ({reason})",
                file=sys.stderr,
            )
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
            r"\\newcommand\s*\{\\source\}\[1\]\s*"
            r"\{\\HFHSourceLine\{\\raggedright\}\{#1\}\}",
            "die linksbündige Standard-Quellenzeile fehlt",
        ),
        (
            r"\\newcommand\s*\{\\sourcecentered\}\[1\]\s*"
            r"\{\\HFHSourceLine\{\\centering\}\{#1\}\}",
            "die zentrierte Quellenalternative fehlt",
        ),
        (
            r"\\newcommand\s*\{\\sourceindented\}",
            "die eingerückte Quellenvariante fehlt",
        ),
        (
            r"\\RequirePackage\s*\[[^]]*backend=biber[^]]*\]"
            r"\s*\{biblatex\}",
            "biblatex muss Biber als Backend verwenden",
        ),
        (
            r"sorting=nyt",
            "das Quellenverzeichnis muss nach Name, Jahr und Titel sortieren",
        ),
        (
            r"\\setlength\s*\{\\bibhang\}\s*\{0\.5cm\}",
            "der hängende Einzug muss 0,5 cm betragen",
        ),
        (
            r"\\setlength\s*\{\\bibitemsep\}\s*\{6pt\}",
            "zwischen Literatureinträgen müssen 6 pt liegen",
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
