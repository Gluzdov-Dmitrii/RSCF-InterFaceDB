from pathlib import Path

from interface_db.provenance.source_manifest import inventory


def test_inventory_hashes_allowed_files_and_marks_empty(tmp_path: Path) -> None:
    (tmp_path / "paper.pdf").write_bytes(b"example")
    (tmp_path / "empty.docx").write_bytes(b"")
    (tmp_path / "ignore.txt").write_text("ignore", encoding="utf-8")
    rows = inventory(tmp_path)
    assert len(rows) == 2
    statuses = {row["relative_path"]: row["status"] for row in rows}
    assert statuses == {"empty.docx": "empty", "paper.pdf": "present"}
    assert all(len(str(row["sha256"])) == 64 for row in rows)


def test_inventory_can_include_extensionless_files(tmp_path: Path) -> None:
    (tmp_path / "artifact").write_bytes(b"")
    rows = inventory(tmp_path, all_files=True)
    assert rows[0]["relative_path"] == "artifact"
    assert rows[0]["status"] == "empty"
