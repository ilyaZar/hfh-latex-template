#!/usr/bin/env python3
"""Prüft den öffentlichen Leitfadeninhalt der produktiven Vorlage."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.tex"
FORMATTING = ROOT / "hfh-formatierungen.sty"
DOCS = ROOT / "docs"
INCLUDED_DOCS = (
    "00-frontmatter",
    "01-verwendungshinweis",
    "02-formale-aspekte",
    "03-aufbau-wissenschaftlicher-arbeiten",
    "04-verzeichnisse",
    "05-eigenstaendigkeitserklaerung",
)

REQUIRED_HEADINGS = (
    "Abstract",
    "Abkürzungsverzeichnis",
    "Verwendungshinweis",
    "Formale Aspekte zur Erstellung wissenschaftlicher Arbeiten",
    "Muster für die Gliederung",
    "Gliederungstiefe",
    "Gliederungslogik",
    "Muster für Abbildungen",
    "Muster für Tabellen",
    "Aufbau wissenschaftlicher Arbeiten",
    "Titelblatt",
    "Inhaltsverzeichnis",
    "Abbildungsverzeichnis und Tabellenverzeichnis",
    "Inhaltsteil der wissenschaftlichen Arbeit",
    "Quellenverzeichnis",
    "Rechtsprechungsverzeichnis (bei Bedarf)",
    (
        "Verzeichnis der Verwaltungsanweisungen, Parlamentaria und "
        "Ähnliches (bei Bedarf)"
    ),
    "Verzeichnis der eingesetzten KI-Werkzeuge (bei Bedarf)",
    "Anlagenverzeichnis (bei Bedarf)",
    "Anlagen",
    "Eigenständigkeitserklärung",
)

REQUIRED_GUIDANCE = (
    "wird ein Abstract im Umfang von etwa ein, maximal zwei",
    "Die Nutzung der Vorlage entbindet Sie nicht davon",
    "Eine über drei (bei umfangreicheren Arbeiten vier) Ebenen",
    "wenn „1.1.1“, dann auch „1.1.2“",
    "Alle Abbildungen müssen grundsätzlich für sich „lesbar“ sein",
    "Tabellen werden neben der fortlaufenden Tabellennummer",
    "Dies ist der wesentliche Teil Ihrer Arbeit",
    "Im Quellenverzeichnis werden alle (und \\textit{ausschließlich} die)",
    "Der Anhang ist nicht dahingehend zu „missbrauchen“",
    "Plagiieren, d.\\,h. geistiges Eigentum stehlen",
)

LATEX_ADAPTATIONS = (
    "Overleaf-Kopie",
    "\\texttt{main.tex}",
    "\\texttt{latexmk -pdf main.tex}",
    "\\texttt{biblatex}",
    "Biber",
    "\\texttt{\\string\\parencite",
    "\\texttt{\\string\\textcite",
    "\\texttt{\\string\\printbibliography}",
    "\\texttt{\\string\\caption}",
    "\\texttt{\\string\\label}",
    "\\texttt{\\string\\ref}",
    "\\texttt{\\string\\source}",
)

FORBIDDEN_WORD_INSTRUCTIONS = (
    "Microsoft Word erstellt",
    "Formatvorlagen ändern",
    "Stellen Sie hierfür den Cursor",
    "Taste „F9“",
    "Dokument kopiert und umbenannt",
)


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def main() -> int:
    main_source = MAIN.read_text(encoding="utf-8")
    source_files = (MAIN, FORMATTING, *sorted(DOCS.glob("*.tex")))
    text = compact(
        "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    )
    missing = [
        item
        for item in REQUIRED_HEADINGS + REQUIRED_GUIDANCE + LATEX_ADAPTATIONS
        if compact(item) not in text
    ]
    stale = [item for item in FORBIDDEN_WORD_INSTRUCTIONS if item in text]
    missing.extend(
        f"\\include{{docs/{name}}}"
        for name in INCLUDED_DOCS
        if f"\\include{{docs/{name}}}" not in main_source
    )
    if r"\input{docs/" in main_source:
        stale.append(r"\input{docs/")
    if r"\nocite{*}" in text:
        stale.append(r"\nocite{*}")

    if text.count(r"\includegraphics") != 2:
        missing.append("genau zwei öffentliche Beispielabbildungen")
    if text.count(r"% \sourcecentered") != 3:
        missing.append("drei kommentierte zentrierte Quellenvarianten")
    if text.count(r"% \sourceindented") != 3:
        missing.append("drei kommentierte eingerückte Quellenvarianten")
    if text.count(r"\label{app:material-") != 2:
        missing.append("zwei getrennt referenzierbare Beispielanlagen")

    if missing:
        print("FEHLER: Leitfadeninhalt fehlt:", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
    if stale:
        print("FEHLER: unzulässiger Alt- oder Umgehungspfad:", file=sys.stderr)
        for item in stale:
            print(f"- {item}", file=sys.stderr)
    if missing or stale:
        return 1

    print("Leitfadenkapitel, LaTeX-Anpassungen und Beispiele sind vollständig")
    return 0


if __name__ == "__main__":
    sys.exit(main())
