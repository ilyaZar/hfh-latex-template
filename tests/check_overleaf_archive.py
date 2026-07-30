#!/usr/bin/env python3
"""Prüft Datenschutz und Inhalt des von GitHub erzeugten Overleaf-Archivs."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_ARCHIVE_FILES = {
    "LICENSE",
    "README.md",
    "main.tex",
    "references.bib",
}
PUBLIC_PREFIX = "images/"
PRIVATE_SUFFIXES = {".docx"}
RESTRICTED_MEDIA_SUFFIXES = {".jpeg", ".jpg", ".pdf", ".png"}
METADATA_MARKERS = {
    b"Exif\x00\x00": "EXIF",
    b"Photoshop 3.0": "Photoshop/IPTC",
    b"http://ns.adobe.com": "Adobe XMP",
    b"<x:xmpmeta": "XMP",
    b"<?xpacket": "XMP",
}


def run(*command: str) -> bytes:
    process = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", errors="replace"))
    return process.stdout


def tracked_files() -> list[PurePosixPath]:
    output = run("git", "ls-files", "-z")
    return [
        PurePosixPath(item.decode("utf-8"))
        for item in output.split(b"\0")
        if item
    ]


def check_repository_privacy(paths: list[PurePosixPath]) -> None:
    violations = []
    for path in paths:
        path_text = path.as_posix()
        suffix = path.suffix.casefold()
        if suffix in PRIVATE_SUFFIXES:
            violations.append(f"privates Quelldokument: {path_text}")
        if suffix in RESTRICTED_MEDIA_SUFFIXES and not path_text.startswith(
            PUBLIC_PREFIX
        ):
            violations.append(f"Medienartefakt außerhalb images/: {path_text}")
        if path_text.startswith("assets/private/"):
            violations.append(f"privater Asset-Pfad: {path_text}")
        if path_text.startswith("tests/screenshots/"):
            violations.append(f"Screenshot-Testartefakt: {path_text}")
    if violations:
        raise ValueError("\n".join(violations))


def check_public_image_metadata(paths: list[PurePosixPath]) -> None:
    violations = []
    for path in paths:
        path_text = path.as_posix()
        if not path_text.startswith(PUBLIC_PREFIX):
            continue
        payload = (ROOT / path_text).read_bytes()
        for marker, label in METADATA_MARKERS.items():
            if marker in payload:
                violations.append(f"{label}-Metadaten in {path_text}")
    if violations:
        raise ValueError("\n".join(violations))


def check_archive() -> list[str]:
    with tempfile.TemporaryDirectory(prefix="hfh-overleaf-") as directory:
        archive = Path(directory) / "template.zip"
        run(
            "git",
            "archive",
            "--format=zip",
            f"--output={archive}",
            "HEAD",
        )
        with zipfile.ZipFile(archive) as zipped:
            names = sorted(
                name for name in zipped.namelist() if not name.endswith("/")
            )

    missing = sorted(REQUIRED_ARCHIVE_FILES - set(names))
    unexpected = sorted(
        name
        for name in names
        if name not in REQUIRED_ARCHIVE_FILES
        and not name.startswith(PUBLIC_PREFIX)
    )
    if missing:
        raise ValueError(f"Pflichtdateien fehlen im Archiv: {missing}")
    if unexpected:
        raise ValueError(f"Unerwartete Dateien im Archiv: {unexpected}")
    return names


def main() -> int:
    try:
        paths = tracked_files()
        check_repository_privacy(paths)
        check_public_image_metadata(paths)
        names = check_archive()
    except (RuntimeError, ValueError, zipfile.BadZipFile) as error:
        print(f"FEHLER: {error}", file=sys.stderr)
        return 1

    print("Overleaf-Archiv enthält ausschließlich freigegebene Dateien:")
    for name in names:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
