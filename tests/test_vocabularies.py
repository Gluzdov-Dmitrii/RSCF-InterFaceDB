import csv
import json
import sqlite3
from pathlib import Path


def property_ids_from_csv() -> set[str]:
    path = Path("metadata/vocabularies/property_terms.csv")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return {row["property_id"] for row in csv.DictReader(stream)}


def nullable_float(value: str) -> float | None:
    return None if value == "" else float(value)


def normalized_csv_rows() -> tuple[str, dict[str, tuple]]:
    path = Path("metadata/vocabularies/property_terms.csv")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    versions = {row["vocabulary_version"] for row in rows}
    assert len(versions) == 1
    normalized = {
        row["property_id"]: (
            row["label"],
            row["definition"],
            row["canonical_unit_code"],
            row["dimension_code"],
            row["required_coordinate_term"] or None,
            nullable_float(row["canonical_min"]),
            int(row["min_inclusive"]),
            nullable_float(row["canonical_max"]),
            int(row["max_inclusive"]),
            int(row["active"]),
            int(row["model_ready_allowed"]),
            row["model_ready_block_reason"] or None,
            tuple(sorted(row["allowed_context_types"].split("|"))),
        )
        for row in rows
    }
    return versions.pop(), normalized


def test_json_schema_property_ids_match_vocabulary() -> None:
    schema = json.loads(Path("data/schemas/observation.schema.json").read_text(encoding="utf-8"))
    assert set(schema["$defs"]["propertyId"]["enum"]) == property_ids_from_csv()


def test_sql_property_ids_match_vocabulary() -> None:
    database = sqlite3.connect(":memory:")
    database.executescript(Path("database/schema/001_initial.sql").read_text(encoding="utf-8"))
    sql_ids = {row[0] for row in database.execute("SELECT property_id FROM property_term")}
    assert sql_ids == property_ids_from_csv()


def test_sql_property_semantics_match_vocabulary() -> None:
    database = sqlite3.connect(":memory:")
    database.executescript(Path("database/schema/001_initial.sql").read_text(encoding="utf-8"))
    csv_version, csv_rows = normalized_csv_rows()
    sql_version = database.execute(
        "SELECT vocabulary_version FROM schema_metadata WHERE schema_version = '0.2.0'"
    ).fetchone()[0]
    context_rows: dict[str, list[str]] = {}
    for property_id, context_type in database.execute(
        "SELECT property_id, context_type FROM property_context_rule"
    ):
        context_rows.setdefault(property_id, []).append(context_type)
    sql_rows = {
        row[0]: (*row[1:], tuple(sorted(context_rows[row[0]])))
        for row in database.execute(
            "SELECT property_id, label, definition, canonical_unit_code, dimension_code, "
            "required_coordinate_term, canonical_min, min_inclusive, canonical_max, "
            "max_inclusive, active, model_ready_allowed, model_ready_block_reason "
            "FROM property_term"
        )
    }

    assert sql_version == csv_version
    assert sql_rows == csv_rows
