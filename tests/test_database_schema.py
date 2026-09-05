import sqlite3
from pathlib import Path

import pytest


def database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        Path("database/schema/001_initial.sql").read_text(encoding="utf-8")
    )
    return connection


def test_schema_inventory_and_foreign_keys() -> None:
    connection = database()
    tables = connection.execute(
        "SELECT count(*) FROM sqlite_schema "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    ).fetchone()[0]
    triggers = connection.execute(
        "SELECT count(*) FROM sqlite_schema WHERE type = 'trigger'"
    ).fetchone()[0]

    assert tables == 56
    assert triggers == 77
    assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert connection.execute("PRAGMA foreign_key_check").fetchall() == []


def test_critical_numeric_tables_are_strict() -> None:
    connection = database()
    strict_tables = {
        row[1] for row in connection.execute("PRAGMA table_list") if row[5] == 1
    }
    assert {
        "observation",
        "condition_value",
        "uncertainty_component",
        "formulation_component",
        "method_parameter",
        "dataset_snapshot",
        "ml_model_run",
        "domain_rule",
        "domain_assessment",
    } <= strict_tables

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "UPDATE property_term SET canonical_min = 'not-a-number' "
            "WHERE property_id = 'surface_tension_equilibrium'"
        )
