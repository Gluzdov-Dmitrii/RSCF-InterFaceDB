"""Create a hash manifest for local source artifacts without copying them."""

from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".csv", ".xlsx"}
DEFAULT_EXCLUDED_DIRS = {".git", ".dvc", ".venv", "private", "tmp", "__pycache__"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(
    root: Path,
    extensions: set[str] | None = None,
    all_files: bool = False,
) -> list[dict[str, str | int]]:
    allowed = {suffix.lower() for suffix in (extensions or DEFAULT_EXTENSIONS)}
    rows: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or (not all_files and path.suffix.lower() not in allowed):
            continue
        relative = path.relative_to(root)
        if any(part in DEFAULT_EXCLUDED_DIRS for part in relative.parts):
            continue
        stat = path.stat()
        content_hash = sha256_file(path)
        rows.append(
            {
                "artifact_id": f"ART-{content_hash[:12]}",
                "relative_path": relative.as_posix(),
                "suffix": path.suffix.lower(),
                "bytes": stat.st_size,
                "sha256": content_hash,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
                "status": "empty" if stat.st_size == 0 else "present",
            }
        )
    return rows


def write_manifest(rows: list[dict[str, str | int]], output: Path, force: bool = False) -> None:
    if output.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "artifact_id",
        "relative_path",
        "suffix",
        "bytes",
        "sha256",
        "modified_utc",
        "status",
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--extensions", help="Comma-separated suffixes, for example .pdf,.docx")
    parser.add_argument("--all-files", action="store_true", help="Include extensionless artifacts")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    extensions = set(args.extensions.split(",")) if args.extensions else None
    rows = inventory(args.root.resolve(), extensions, args.all_files)
    write_manifest(rows, args.output.resolve(), args.force)
    print(f"Recorded {len(rows)} artifacts in {args.output}")


if __name__ == "__main__":
    main()
