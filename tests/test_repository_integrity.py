import csv
import re
from pathlib import Path
from urllib.parse import unquote

MARKDOWN_ROOTS = (
    Path("README.md"),
    Path("AGENTS.md"),
    Path("agents"),
    Path("configs"),
    Path("data"),
    Path("database"),
    Path("docs"),
    Path("literature"),
    Path("manuscripts"),
    Path("metadata"),
    Path("models"),
    Path("notebooks"),
    Path("planning"),
    Path("prompts"),
    Path("reports"),
    Path("simulations"),
    Path("workflows"),
)
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in MARKDOWN_ROOTS:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(root.rglob("*.md"))
    return sorted(files)


def test_relative_markdown_links_resolve() -> None:
    broken: list[str] = []
    for document in markdown_files():
        for raw_target in LINK_PATTERN.findall(document.read_text(encoding="utf-8")):
            target = raw_target.strip().split("#", maxsplit=1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            target = unquote(target.strip("<>"))
            if not (document.parent / target).resolve().exists():
                broken.append(f"{document}: {raw_target}")
    assert broken == []


def test_source_manifest_identifiers_are_unique() -> None:
    with Path("literature/metadata/source_manifest.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    source_ids = [row["source_id"] for row in rows]
    dois = [row["doi"].lower() for row in rows if row["doi"]]
    assert len(source_ids) == len(set(source_ids))
    assert len(dois) == len(set(dois))
    assert all(row["title"] and row["url"] for row in rows)
