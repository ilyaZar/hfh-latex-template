#!/usr/bin/env python3
"""Prüft die gerenderten PDFs der Vorlage und der Compliance-Fixture."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree


XHTML = "http://www.w3.org/1999/xhtml"
X = f"{{{XHTML}}}"
ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"


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


def parse_bbox(pdf: Path) -> list[list[tuple[str, float, float]]]:
    xml = run("pdftotext", "-bbox-layout", str(pdf), "-")
    root = ElementTree.fromstring(xml)
    pages = []
    for page in root.iter(f"{X}page"):
        lines = []
        for line in page.iter(f"{X}line"):
            words = ["".join(word.itertext()) for word in line.findall(f"{X}word")]
            lines.append(
                (
                    " ".join(words),
                    float(line.get("xMin")),
                    float(line.get("yMin")),
                )
            )
        pages.append(lines)
    return pages


def find_line(
    pages: list[list[tuple[str, float, float]]],
    page_number: int,
    prefix: str,
) -> tuple[str, float, float]:
    for line in pages[page_number - 1]:
        if line[0].startswith(prefix):
            return line
    raise CheckError(
        f"Seite {page_number}: Zeile mit Präfix {prefix!r} fehlt"
    )


def find_page_line(
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


def check_fixture(pdf: Path, log: Path) -> None:
    info = run("pdfinfo", str(pdf))
    pages_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    size_match = re.search(
        r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts",
        info,
        re.MULTILINE,
    )
    if pages_match is None or int(pages_match.group(1)) != 8:
        raise CheckError("Die Compliance-PDF muss genau acht Seiten haben")
    if size_match is None:
        raise CheckError("Seitenformat konnte nicht gelesen werden")
    width, height = map(float, size_match.groups())
    between(width, 594.5, 596.0, "A4-Breite")
    between(height, 841.0, 843.0, "A4-Höhe")

    log_text = log.read_text(encoding="utf-8", errors="replace")
    forbidden_log_patterns = (
        r"LaTeX Warning",
        r"Package .* Warning",
        r"Overfull",
        r"Underfull",
        r"undefined",
    )
    for pattern in forbidden_log_patterns:
        if re.search(pattern, log_text):
            raise CheckError(f"Log enthält unerlaubtes Muster {pattern!r}")
    for legacy_package in (
        "chngcntr.sty",
        "inputenc.sty",
        "mathptmx.sty",
        "natbib.sty",
        "times.sty",
        "txfonts.sty",
    ):
        if legacy_package in log_text:
            raise CheckError(
                f"Test lädt das redundante oder veraltete Paket "
                f"{legacy_package}"
            )

    fonts = run("pdffonts", str(pdf))
    font_rows = [
        line
        for line in fonts.splitlines()[2:]
        if line.strip() and not line.startswith("-")
    ]
    if not font_rows:
        raise CheckError("Keine eingebetteten PDF-Schriften gefunden")
    for row in font_rows:
        flags = re.search(
            r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$",
            row,
        )
        if flags is None or flags.groups() != ("yes", "yes", "yes"):
            raise CheckError("Nicht alle PDF-Schriften sind eingebettet")
        if "TeXGyreTermesX" not in row.split()[0]:
            raise CheckError("Unerwartete Schrift außerhalb TeX Gyre Termes X")

    text = run("pdftotext", "-layout", str(pdf), "-")
    required_fragments = (
        "Tabelle 1 und Abbildung 1",
        "Tabelle 2 und Abbildung 2",
        "Diese vierte Fußnote",
        "Diese fünfte Fußnote",
    )
    for fragment in required_fragments:
        if fragment not in text:
            raise CheckError(f"Erwarteter PDF-Text fehlt: {fragment!r}")
    if "??" in text:
        raise CheckError("PDF enthält eine ungelöste Referenz")

    bibliography = ("Adler, Beate", "Becker, Clara", "Zimmer, Anton")
    positions = [text.find(name) for name in bibliography]
    if any(position < 0 for position in positions):
        raise CheckError("Mindestens ein Literatureintrag fehlt")
    if positions != sorted(positions):
        raise CheckError("Literatur ist nicht alphabetisch sortiert")

    legal_sources = (
        "Arbeitsgericht Berlin",
        "Bundesgerichtshof",
        "Verwaltungsgericht Hamburg",
    )
    positions = [text.find(name) for name in legal_sources]
    if any(position < 0 for position in positions):
        raise CheckError("Mindestens ein Rechtsprechungseintrag fehlt")
    if positions != sorted(positions):
        raise CheckError(
            "Rechtsprechungsverzeichnis ist nicht alphabetisch sortiert"
        )

    bbox = parse_bbox(pdf)
    first_note = find_line(bbox, 2, "Diese erste Fußnote")
    first_note_last = find_line(bbox, 2, "dem vorgeschriebenen")
    second_note = find_line(bbox, 2, "Diese zweite Fußnote")
    second_note_last = find_line(bbox, 2, "Grundlinienabstand")
    third_note = find_line(bbox, 2, "Diese dritte Fußnote")

    note_line_spacing = first_note_last[2] - first_note[2]
    note_gap_one = second_note[2] - first_note_last[2]
    note_gap_two = third_note[2] - second_note_last[2]
    between(note_line_spacing, 11.5, 12.5, "Fußnoten-Grundlinienabstand")
    between(note_gap_one, 17.0, 18.5, "Abstand Fußnote 1 zu 2")
    between(note_gap_two, 17.0, 18.5, "Abstand Fußnote 2 zu 3")

    table_caption = find_line(bbox, 4, "Tabelle 1:")
    table_header = find_line(bbox, 4, "Prüfmerkmal")
    caption_to_table = table_header[2] - table_caption[2]
    between(caption_to_table, 16.0, 18.5, "Beschriftung zu Tabelle")

    source_lines = [
        line
        for line in bbox[3]
        if line[0].startswith("Quelle: Eigene Darstellung.")
    ]
    if len(source_lines) != 2:
        raise CheckError("Seite 4 muss zwei Quellenzeilen enthalten")
    figure_caption = find_line(bbox, 4, "Abbildung 1:")
    source_alignments = (
        source_lines[0][1] - table_caption[1],
        source_lines[1][1] - figure_caption[1],
    )
    for index, alignment in enumerate(source_alignments, start=1):
        between(
            abs(alignment),
            0,
            0.5,
            f"Quellenzeile {index} muss linksbündig zur Beschriftung sein",
        )
    source_line = source_lines[-1]
    following_text = find_line(bbox, 4, "Der Text nach der Abbildung")
    source_to_text = following_text[2] - source_line[2]
    if source_to_text < 24:
        raise CheckError(
            "Nach der Abbildungsquelle fehlen ungefähr 12 pt Abstand"
        )

    first_bib_line = find_line(bbox, 7, "Adler, Beate")
    first_bib_continuation = find_line(bbox, 7, "senschaftlichen")
    first_bib_last_line = find_line(bbox, 7, "119.")
    second_bib_line = find_line(bbox, 7, "Becker, Clara")
    hanging_indent = first_bib_continuation[1] - first_bib_line[1]
    bibliography_line_spacing = (
        first_bib_continuation[2] - first_bib_line[2]
    )
    bibliography_gap = second_bib_line[2] - first_bib_last_line[2]
    between(hanging_indent, 13.8, 14.6, "Hängender Einzug")
    between(
        bibliography_line_spacing,
        14.0,
        15.0,
        "Grundlinienabstand innerhalb einer Quelle",
    )
    between(bibliography_gap, 19.8, 21.0, "Abstand zwischen Quellen")

    print(f"PDF-Seiten: 8, Format: {width:.2f} x {height:.2f} pt")
    print(
        "Fußnoten:"
        f" innen {note_line_spacing:.2f} pt,"
        f" zwischen {note_gap_one:.2f}/{note_gap_two:.2f} pt"
    )
    print(
        "Tabelle:"
        f" Beschriftungs-Grundlinie zu Kopfzeile {caption_to_table:.2f} pt"
    )
    print(
        "Quellenzeilen: linksbündig zu Tabellen- und Abbildungsbeschriftung"
    )
    print(
        "Quellen:"
        f" Hängeeinzug {hanging_indent / 28.346:.2f} cm,"
        f" Abstand {bibliography_gap - bibliography_line_spacing:.2f} pt"
    )
    print("Schriften eingebettet, Nummerierung und Sortierung korrekt")


def check_template(pdf: Path) -> None:
    if not pdf.exists():
        raise CheckError("main.pdf fehlt; Vorlage vor dem Test kompilieren")

    pages = parse_bbox(pdf)
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

    usage = find_page_line(toc, "Verwendungshinweis")
    chapter = find_page_line(toc, "Formale Aspekte")
    section = find_page_line(toc, "Muster für die Gliederung")
    subsection = find_page_line(toc, "Gliederungstiefe")
    second_chapter = find_page_line(toc, "Aufbau wissenschaftlicher Arbeiten")
    find_page_line(toc, "Bezeichnung der Anlage")

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture-pdf",
        type=Path,
        default=TESTS / "table1-compliance.pdf",
    )
    parser.add_argument(
        "--fixture-log",
        type=Path,
        default=TESTS / "table1-compliance.log",
    )
    parser.add_argument(
        "--template-pdf",
        type=Path,
        default=ROOT / "main.pdf",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        check_fixture(args.fixture_pdf, args.fixture_log)
        check_template(args.template_pdf)
    except CheckError as error:
        print(f"FEHLER: {error}", file=sys.stderr)
        return 1
    print("Gerenderte PDF-Prüfungen bestanden")
    return 0


if __name__ == "__main__":
    sys.exit(main())
