#!/usr/bin/env python3
"""Meldet offensichtliche Verstöße gegen inhaltliche V-Regeln aus Tabelle 1."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Command:
    name: str
    argument: str
    start: int
    end: int


@dataclass(frozen=True)
class Environment:
    name: str
    body: str
    start: int
    end: int


@dataclass(frozen=True)
class Issue:
    code: str
    line: int
    message: str


FLOAT_RULES = {
    "hfhtable": ("F.1", "F.4", "Tabelle", "tab:"),
    "table": ("F.1", "F.4", "Tabelle", "tab:"),
    "hfhfigure": ("G.1", "G.5", "Abbildung", "fig:"),
    "figure": ("G.1", "G.5", "Abbildung", "fig:"),
}


def strip_comments(text: str) -> str:
    """Entfernt LaTeX-Kommentare und erhält Zeilennummern."""

    clean_lines = []
    for line in text.splitlines(keepends=True):
        cut = None
        for index, character in enumerate(line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        if cut is None:
            clean_lines.append(line)
        else:
            newline = "\n" if line.endswith("\n") else ""
            clean_lines.append(line[:cut] + newline)
    return "".join(clean_lines)


def matching_brace(text: str, opening: int) -> int | None:
    depth = 0
    for index in range(opening, len(text)):
        character = text[index]
        if character not in "{}":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and text[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2:
            continue
        if character == "{":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return index
    return None


def commands(text: str, names: Iterable[str]) -> list[Command]:
    found = []
    alternatives = "|".join(re.escape(name) for name in names)
    pattern = re.compile(
        rf"\\(?P<name>{alternatives})\*?\s*(?:\[[^\]]*\]\s*)?\{{"
    )
    for match in pattern.finditer(text):
        opening = match.end() - 1
        closing = matching_brace(text, opening)
        if closing is None:
            continue
        found.append(
            Command(
                name=match.group("name"),
                argument=text[opening + 1 : closing],
                start=match.start(),
                end=closing + 1,
            )
        )
    return found


def environments(text: str, names: Iterable[str]) -> list[Environment]:
    found = []
    alternatives = "|".join(re.escape(name) for name in names)
    token = re.compile(
        rf"\\(?P<kind>begin|end)\s*\{{(?P<name>{alternatives})\}}"
    )
    matches = list(token.finditer(text))
    for position, match in enumerate(matches):
        if match.group("kind") != "begin":
            continue
        name = match.group("name")
        depth = 1
        closing = None
        for candidate in matches[position + 1 :]:
            if candidate.group("name") != name:
                continue
            depth += 1 if candidate.group("kind") == "begin" else -1
            if depth == 0:
                closing = candidate
                break
        if closing is None:
            continue
        found.append(
            Environment(
                name=name,
                body=text[match.end() : closing.start()],
                start=match.start(),
                end=closing.end(),
            )
        )
    return found


def mask_environment_definitions(text: str) -> str:
    """Blendet begin/end-Tokens in newenvironment-Definitionen aus."""

    pattern = re.compile(
        r"\\(?:re)?newenvironment\*?\s*\{[^{}]+\}"
        r"\s*(?:\[[^\]]*\]\s*)*"
    )
    spans = []
    for match in pattern.finditer(text):
        cursor = match.end()
        complete = True
        for _ in range(2):
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if cursor >= len(text) or text[cursor] != "{":
                complete = False
                break
            closing = matching_brace(text, cursor)
            if closing is None:
                complete = False
                break
            cursor = closing + 1
        if complete:
            spans.append((match.start(), cursor))

    if not spans:
        return text
    characters = list(text)
    for start, end in spans:
        for index in range(start, end):
            if characters[index] != "\n":
                characters[index] = " "
    return "".join(characters)


def mask_spans(text: str, spans: Iterable[tuple[int, int]]) -> str:
    characters = list(text)
    for start, end in spans:
        for index in range(start, end):
            if characters[index] != "\n":
                characters[index] = " "
    return "".join(characters)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def plain_text(value: str) -> str:
    value = re.sub(r"\\(?:[A-Za-z@]+|.)\*?", " ", value)
    value = value.replace("{", " ").replace("}", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def sorting_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", plain_text(value))
    return "".join(
        character for character in normalized if not unicodedata.combining(character)
    ).casefold()


def has_counter_without(text: str, counter: str) -> bool:
    pattern = re.compile(
        rf"\\counterwithout\s*\{{\s*{re.escape(counter)}\s*\}}"
        r"\s*\{\s*chapter\s*\}"
    )
    return bool(pattern.search(text))


def audit_text(text: str) -> list[Issue]:
    clean = strip_comments(text)
    content = mask_environment_definitions(clean)
    issues: list[Issue] = []

    if not has_counter_without(clean, "footnote"):
        issues.append(
            Issue(
                "E.5",
                1,
                "Fortlaufende Fußnoten benötigen "
                "\\counterwithout{footnote}{chapter}.",
            )
        )
    if not has_counter_without(clean, "table"):
        issues.append(
            Issue(
                "F.1",
                1,
                "Globale Tabellennummerierung benötigt "
                "\\counterwithout{table}{chapter}.",
            )
        )
    if not has_counter_without(clean, "figure"):
        issues.append(
            Issue(
                "G.1",
                1,
                "Globale Abbildungsnummerierung benötigt "
                "\\counterwithout{figure}{chapter}.",
            )
        )

    for footnote in commands(content, ["footnote"]):
        visible = plain_text(footnote.argument)
        first_letter = next(
            (character for character in visible if character.isalpha()), None
        )
        if first_letter is None or not first_letter.isupper():
            issues.append(
                Issue(
                    "E.6",
                    line_number(content, footnote.start),
                    "Fußnote beginnt nicht erkennbar mit einem Großbuchstaben.",
                )
            )
        if not visible.endswith("."):
            issues.append(
                Issue(
                    "E.7",
                    line_number(content, footnote.start),
                    "Fußnote endet nicht mit einem Punkt.",
                )
            )

    all_labels = commands(content, ["label"])
    label_counts: dict[str, int] = {}
    for label in all_labels:
        label_counts[label.argument] = label_counts.get(label.argument, 0) + 1
    for label, count in label_counts.items():
        if count > 1:
            first = next(item for item in all_labels if item.argument == label)
            issues.append(
                Issue(
                    "LABEL",
                    line_number(content, first.start),
                    f"Label {label!r} ist {count}-mal vergeben.",
                )
            )

    float_environments = environments(content, FLOAT_RULES)
    prose = mask_spans(
        content,
        ((environment.start, environment.end) for environment in float_environments),
    )
    reference_names = ["ref", "autoref", "cref", "Cref", "vref"]
    references = {
        item.argument for item in commands(prose, reference_names)
    }

    for environment in float_environments:
        object_rule, reference_rule, label_name, prefix = FLOAT_RULES[
            environment.name
        ]
        at_line = line_number(content, environment.start)
        captions = commands(environment.body, ["caption"])
        sources = commands(environment.body, ["source"])
        labels = commands(environment.body, ["label"])

        if not captions or not captions[0].argument.strip():
            issues.append(
                Issue(
                    object_rule,
                    at_line,
                    f"{label_name} besitzt keine eindeutige Beschriftung.",
                )
            )
        if not sources or not sources[0].argument.strip():
            issues.append(
                Issue(
                    object_rule,
                    at_line,
                    f"{label_name} besitzt keine Quellenangabe.",
                )
            )
        if not labels:
            issues.append(
                Issue(
                    object_rule,
                    at_line,
                    f"{label_name} besitzt kein Label.",
                )
            )
            issues.append(
                Issue(
                    reference_rule,
                    at_line,
                    f"{label_name} kann ohne Label nicht referenziert werden.",
                )
            )
            continue

        for label in labels:
            if not label.argument.startswith(prefix):
                issues.append(
                    Issue(
                        object_rule,
                        at_line,
                        f"Label {label.argument!r} sollte mit {prefix!r} beginnen.",
                    )
                )
            if label.argument not in references:
                issues.append(
                    Issue(
                        reference_rule,
                        at_line,
                        f"Label {label.argument!r} wird im Text nicht referenziert.",
                    )
                )

    for environment in environments(content, ["hfhsourceentries"]):
        entries = commands(environment.body, ["hfhsourceentry"])
        keys = [sorting_key(entry.argument) for entry in entries]
        if keys != sorted(keys):
            issues.append(
                Issue(
                    "I.4",
                    line_number(content, environment.start),
                    "Manuelle Quellenangaben sind nicht alphabetisch sortiert.",
                )
            )

    return sorted(issues, key=lambda issue: (issue.line, issue.code))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_files", type=Path, nargs="+")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = "\n".join(
        tex_file.read_text(encoding="utf-8")
        for tex_file in args.tex_files
    )
    issues = audit_text(text)
    source_label = ", ".join(str(path) for path in args.tex_files)
    if issues:
        for issue in issues:
            print(
                f"{source_label}:{issue.line}: "
                f"{issue.code}: {issue.message}"
            )
        return 1
    print(f"{source_label}: alle geprüften inhaltlichen V-Regeln erfüllt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
