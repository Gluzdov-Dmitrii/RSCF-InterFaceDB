"""Extract page-level text from a PDF while retaining provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_pdf(input_path: Path, output_path: Path, force: bool = False) -> int:
    if output_path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    file_hash = sha256_file(input_path)
    reader = PdfReader(input_path)
    extracted_at = datetime.now(UTC).isoformat()
    with output_path.open("w", encoding="utf-8") as target:
        for page_number, page in enumerate(reader.pages, start=1):
            record = {
                "source_file": input_path.name,
                "source_sha256": file_hash,
                "page": page_number,
                "text": page.extract_text() or "",
                "extracted_at_utc": extracted_at,
                "extractor": "pypdf",
            }
            target.write(json.dumps(record, ensure_ascii=False) + "\n")
    return len(reader.pages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    pages = extract_pdf(args.input, args.output, args.force)
    print(f"Extracted {pages} pages to {args.output}")


if __name__ == "__main__":
    main()
