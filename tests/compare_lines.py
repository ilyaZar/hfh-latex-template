#!/usr/bin/env python3
"""Compare visible line breaks between the source and the test PDF."""

from difflib import SequenceMatcher
from pathlib import Path
import re
import subprocess


TEST_DIR = Path(__file__).resolve().parent
ROOT_DIR = TEST_DIR.parent
SOURCE_PDF = ROOT_DIR / "1127501_WB00-BAC-PB1-260630.pdf"
TEST_PDF = TEST_DIR / "bachelor-layout-comparison.pdf"
PAGE_PAIRS = (
    (6, 1),
    (7, 2),
    (18, 3),
    (19, 4),
    (20, 5),
    (21, 6),
    (34, 7),
    (35, 8),
)
SCENARIO_PAIRS = (
    ((6, 7), (1, 2)),
    ((18, 19), (3, 4)),
    ((20, 21), (5, 6)),
    ((34, 35), (7, 8)),
)


def visible_lines(pdf_path: Path, page: int) -> list[str]:
    """Return visible lines without the varying header and footer."""
    command = [
        "pdftotext",
        "-f",
        str(page),
        "-l",
        str(page),
        "-layout",
        str(pdf_path),
        "-",
    ]
    output = subprocess.check_output(command, text=True)
    lines = []

    for raw_line in output.splitlines():
        line = " ".join(raw_line.split())
        if not line:
            continue
        if "Marc-William Wagner" in line and "1127501" in line:
            continue
        if re.fullmatch(r"Seite \d+ von \d+", line):
            continue
        lines.append(line)

    return lines


def matching_line_count(source: list[str], test: list[str]) -> int:
    """Count equal lines in their longest order-preserving alignment."""
    matcher = SequenceMatcher(None, source, test, autojunk=False)
    return sum(block.size for block in matcher.get_matching_blocks())


def main() -> None:
    print("Original  Test  gleiche Zeilen  Originalzeilen")
    for source_page, test_page in PAGE_PAIRS:
        source_lines = visible_lines(SOURCE_PDF, source_page)
        test_lines = visible_lines(TEST_PDF, test_page)
        matching = matching_line_count(source_lines, test_lines)
        print(
            f"{source_page:>8}  {test_page:>4}  "
            f"{matching:>14}  {len(source_lines):>14}"
        )

    total_matching = 0
    total_source = 0
    for source_pages, test_pages in SCENARIO_PAIRS:
        source_lines = []
        test_lines = []
        for page in source_pages:
            source_lines.extend(visible_lines(SOURCE_PDF, page))
        for page in test_pages:
            test_lines.extend(visible_lines(TEST_PDF, page))
        total_matching += matching_line_count(source_lines, test_lines)
        total_source += len(source_lines)

    ratio = total_matching / total_source
    print(f"Passagen gesamt: {total_matching}/{total_source} ({ratio:.1%})")


if __name__ == "__main__":
    main()
