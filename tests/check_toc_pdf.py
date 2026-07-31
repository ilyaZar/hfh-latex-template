#!/usr/bin/env python3
"""Prüft die Word-nahe Darstellung des produktiven Inhaltsverzeichnisses."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "main.pdf"
XHTML = "http://www.w3.org/1999/xhtml"
X = f"{{{XHTML}}}"


class CheckError(RuntimeError):
    pass


def run(*command: str) -> str:
    process = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise CheckError(
            f"{' '.join(command)} fehlgeschlagen: {process.stderr.strip()}"
        )
    return process.stdout


def parse_lines() -> list[list[tuple[str, float, float]]]:
    xml = run("pdftotext", "-bbox-layout", str(PDF), "-")
    root = ElementTree.fromstring(xml)
    pages = []
    for page in root.iter(f"{X}page"):
        lines = []
        for line in page.iter(f"{X}line"):
            words = line.findall(f"{X}word")
            if not words:
                continue
            text = " ".join("".join(word.itertext()) for word in words)
            lines.append(
                (
                    text,
                    float(words[0].get("xMin")),
                    float(words[0].get("yMin")),
                )
            )
        pages.append(lines)
    return pages


def find_line(
    page: list[tuple[str, float, float]],
    prefix: str,
) -> tuple[str, float, float]:
    for line in page:
        if line[0].startswith(prefix):
            return line
    raise CheckError(f"Inhaltsverzeichniszeile {prefix!r} fehlt")


def between(value: float, lower: float, upper: float, label: str) -> None:
    if not lower <= value <= upper:
        raise CheckError(
            f"{label}: {value:.2f} liegt nicht zwischen "
            f"{lower:.2f} und {upper:.2f}"
        )


def check() -> None:
    if not PDF.exists():
        raise CheckError("main.pdf fehlt; Vorlage vor dem Test kompilieren")

    pages = parse_lines()
    toc_pages = [
        index
        for index, page in enumerate(pages)
        if any(
            text == "Inhaltsverzeichnis" and x < 100
            for text, x, _ in page
        )
    ]
    if len(toc_pages) != 1:
        raise CheckError("Das Inhaltsverzeichnis muss genau eine Seite belegen")

    toc_index = toc_pages[0]
    toc = pages[toc_index]
    if toc_index + 1 >= len(pages):
        raise CheckError("Auf das Inhaltsverzeichnis folgt keine weitere Seite")
    next_page = pages[toc_index + 1]
    if not any(
        text == "Abbildungsverzeichnis" and x < 100
        for text, x, _ in next_page
    ):
        raise CheckError(
            "Das Abbildungsverzeichnis muss direkt auf das einseitige "
            "Inhaltsverzeichnis folgen"
        )

    usage = find_line(toc, "Verwendungshinweis")
    chapter = find_line(toc, "Formale Aspekte")
    section = find_line(toc, "Muster für die Gliederung")
    subsection = find_line(toc, "Gliederungstiefe")
    second_chapter = find_line(toc, "Aufbau wissenschaftlicher Arbeiten")
    find_line(toc, "Bezeichnung der Anlage")

    chapter_gap = chapter[2] - usage[2]
    normal_gap = subsection[2] - section[2]
    between(chapter_gap, 20.0, 20.8, "Abstand vor Haupteintrag")
    between(normal_gap, 17.0, 17.8, "Abstand normaler Einträge")

    title_positions = (
        chapter[1],
        section[1],
        subsection[1],
        second_chapter[1],
    )
    for position in title_positions:
        between(position, 133.5, 135.5, "Beginn der Textspalte")

    print(
        "Inhaltsverzeichnis: eine Seite, "
        f"Abstände {normal_gap:.2f}/{chapter_gap:.2f} pt, "
        f"Textspalte {chapter[1]:.2f} pt"
    )


def main() -> int:
    try:
        check()
    except CheckError as error:
        print(f"FEHLER: {error}", file=sys.stderr)
        return 1
    print("Gerenderte Inhaltsverzeichnis-Prüfung bestanden")
    return 0


if __name__ == "__main__":
    sys.exit(main())
