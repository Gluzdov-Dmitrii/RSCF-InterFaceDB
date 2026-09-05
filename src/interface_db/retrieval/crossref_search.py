"""Run a small, reproducible Crossref bibliographic search."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://api.crossref.org/works"


def build_url(query: str, rows: int, from_year: int | None = None) -> str:
    params = {
        "query.bibliographic": query,
        "rows": rows,
        "select": "DOI,title,author,published,container-title,URL,type",
    }
    if from_year is not None:
        params["filter"] = f"from-pub-date:{from_year}-01-01"
    return f"{API_URL}?{urlencode(params)}"


def normalize_item(item: dict) -> dict:
    published = item.get("published", {}).get("date-parts", [[]])
    year = published[0][0] if published and published[0] else None
    authors = [
        " ".join(part for part in (author.get("given"), author.get("family")) if part)
        for author in item.get("author", [])
    ]
    return {
        "doi": item.get("DOI"),
        "title": (item.get("title") or [None])[0],
        "authors": authors,
        "year": year,
        "container_title": (item.get("container-title") or [None])[0],
        "url": item.get("URL"),
        "type": item.get("type"),
    }


def write_search(
    query: str,
    rows: int,
    output_dir: Path,
    mailto: str | None,
    from_year: int | None,
    force: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    run_path = output_dir / "run.json"
    results_path = output_dir / "results.jsonl"
    if not force and (run_path.exists() or results_path.exists()):
        raise FileExistsError(f"Refusing to overwrite an existing run in {output_dir}")

    url = build_url(query, rows, from_year)
    agent = "InterFaceDB/0.1 (research metadata retrieval"
    if mailto:
        agent += f"; mailto:{mailto}"
    agent += ")"
    request = Request(url, headers={"User-Agent": agent, "Accept": "application/json"})
    with urlopen(request, timeout=60) as response:  # noqa: S310 - fixed HTTPS endpoint
        payload = json.load(response)

    records = [normalize_item(item) for item in payload["message"]["items"]]
    content = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    results_path.write_text(content, encoding="utf-8")
    run = {
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "provider": "Crossref REST API",
        "query": query,
        "from_year": from_year,
        "requested_rows": rows,
        "returned_rows": len(records),
        "request_url": url,
        "results_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
    }
    run_path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--rows", type=int, default=20, choices=range(1, 101), metavar="1..100")
    parser.add_argument("--from-year", type=int)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mailto", help="Contact email for Crossref polite-pool identification")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    write_search(args.query, args.rows, args.output_dir, args.mailto, args.from_year, args.force)


if __name__ == "__main__":
    main()
