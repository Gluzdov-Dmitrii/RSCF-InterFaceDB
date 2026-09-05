import copy
import json
from pathlib import Path

from interface_db.validation.validate_observations import (
    load_property_terms,
    semantic_errors,
    validate_file,
)

SCHEMA = Path("data/schemas/observation.schema.json")
VOCABULARY = Path("metadata/vocabularies/property_terms.csv")


def component(material_id: str, name: str, amount: float = 1.0) -> dict:
    return {
        "material_id": material_id,
        "material_kind": "substance",
        "name": name,
        "amount_original": amount,
        "unit_original": "1",
        "basis": "mole_fraction",
        "amount_canonical": amount,
        "unit_canonical": "1",
        "conversion_rule": "identity",
        "active_product_basis": "not_applicable",
    }


def phase(participant_id: str, role: str, name: str, state: str) -> dict:
    return {
        "participant_id": participant_id,
        "role": role,
        "entity": {
            "entity_id": f"MAT-{participant_id}",
            "entity_type": "phase_sample",
            "name": name,
        },
        "phase_state": state,
        "composition": {
            "stage": "equilibrated",
            "completeness": "complete",
            "components": [component(f"MAT-{participant_id}", name)],
        },
    }


def minimal_observation() -> dict:
    return {
        "schema_version": "0.2.0",
        "observation_id": "OBS-test-001",
        "property_id": "surface_tension_equilibrium",
        "context": {
            "context_id": "CTX-water-air",
            "type": "liquid_gas_interface",
            "participants": [
                phase("water", "liquid_phase", "water", "liquid"),
                phase("air", "gas_phase", "air", "gas"),
            ],
        },
        "result": {
            "value_status": "reported",
            "raw_value_text": "72.0 mN/m",
            "value_kind": "point",
            "qualifier": "exact",
            "value_original": 72.0,
            "unit_original": "mN/m",
            "value_canonical": 0.072,
            "unit_canonical": "N/m",
            "conversion_rule": "x / 1000",
            "conversion_version": "units-v0.1",
            "statistic_kind": "mean",
        },
        "source_assertion": {
            "source_id": "SRC0001",
            "doi": None,
            "url": "https://example.org/record/1",
            "ingestion_route": "primary_publication",
            "exact_locator": "Table 1, row 2",
            "reported_property_label": "surface tension",
            "extraction_mode": "human",
            "verification_status": "human_checked",
            "accessed_on": "2026-09-05",
            "redistribution_status": "metadata_only",
        },
        "method_run": {
            "method_run_id": "RUN-method-001",
            "origin_kind": "experiment",
            "method_term": "Wilhelmy plate",
            "run_label": "Example Wilhelmy measurement",
            "replicate_count": 3,
            "parameters": [],
        },
        "conditions": [
            {
                "condition_id": "COND-temperature",
                "kind": "temperature",
                "status": "reported",
                "raw_value_text": "25 °C",
                "value_original": 25.0,
                "unit_original": "°C",
                "value_canonical": 298.15,
                "unit_canonical": "K",
                "conversion_rule": "x + 273.15",
                "conversion_version": "units-v0.1",
            }
        ],
        "uncertainties": [
            {
                "component_type": "source_reported",
                "status": "not_reported",
                "missing_reason": "The source reports no uncertainty",
            }
        ],
        "relations": [],
        "quality": {
            "data_level": "staging",
            "review_status": "single_review",
            "flags": ["missing_uncertainty"],
        },
    }


def messages_for(tmp_path: Path, record: dict) -> list[str]:
    path = tmp_path / "observation.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    return validate_file(path, SCHEMA, VOCABULARY)


def test_equilibrium_surface_tension_validates(tmp_path: Path) -> None:
    assert messages_for(tmp_path, minimal_observation()) == []


def test_versioned_example_validates() -> None:
    assert validate_file(
        Path("data/examples/observation_water_air.json"),
        SCHEMA,
        VOCABULARY,
    ) == []


def test_surface_tension_rejects_liquid_liquid_context(tmp_path: Path) -> None:
    record = minimal_observation()
    record["context"]["type"] = "liquid_liquid_interface"
    assert messages_for(tmp_path, record)


def test_reported_uncertainty_requires_value(tmp_path: Path) -> None:
    record = minimal_observation()
    record["uncertainties"] = [
        {
            "component_type": "source_reported",
            "status": "reported",
            "representation": "standard_uncertainty",
            "unit": "N/m",
        }
    ]
    assert any("value" in message for message in messages_for(tmp_path, record))


def test_complete_fraction_composition_must_close(tmp_path: Path) -> None:
    record = minimal_observation()
    record["context"]["participants"][0]["composition"]["components"] = [
        component("MAT-water", "water", 0.9),
        component("MAT-ethanol", "ethanol", 0.9),
    ]
    assert any("COMPOSITION_CLOSURE" in message for message in messages_for(tmp_path, record))


def test_second_application_result_is_not_allowed(tmp_path: Path) -> None:
    record = minimal_observation()
    record["application_test"] = {"endpoint": "rheology", "value": 10}
    assert any("application_test" in message for message in messages_for(tmp_path, record))


def test_dynamic_surface_tension_allows_zero_with_time_origin(tmp_path: Path) -> None:
    record = minimal_observation()
    record["property_id"] = "surface_tension_dynamic"
    record["series"] = {
        "series_id": "SERIES-dst-001",
        "point_index": 0,
        "coordinates": [
            {
                "coordinate_id": "COORD-surface-age",
                "kind": "surface_age",
                "raw_value_text": "0 s",
                "value_original": 0,
                "unit_original": "s",
                "value_canonical": 0,
                "unit_canonical": "s",
                "conversion_rule": "identity",
                "conversion_version": "units-v0.1",
                "time_origin": "new interface formation",
            }
        ],
    }
    assert messages_for(tmp_path, record) == []


def test_dynamic_surface_tension_requires_series(tmp_path: Path) -> None:
    record = minimal_observation()
    record["property_id"] = "surface_tension_dynamic"
    assert any("series" in message for message in messages_for(tmp_path, record))


def test_contact_angle_requires_three_phase_context(tmp_path: Path) -> None:
    record = minimal_observation()
    record["property_id"] = "contact_angle_static"
    record["result"]["unit_original"] = "deg"
    record["result"]["unit_canonical"] = "deg"
    record["result"]["value_original"] = 72
    record["result"]["value_canonical"] = 72
    assert messages_for(tmp_path, record)


def test_unit_conversion_mismatch_is_rejected(tmp_path: Path) -> None:
    record = minimal_observation()
    record["conditions"][0]["value_canonical"] = 25.0
    assert any("UNIT_CONVERSION_MISMATCH" in message for message in messages_for(tmp_path, record))


def test_not_reported_result_cannot_have_numeric_value(tmp_path: Path) -> None:
    record = minimal_observation()
    record["result"] = {
        "value_status": "not_reported",
        "missing_reason": "unavailable",
        "value_original": 0,
    }
    assert messages_for(tmp_path, record)


def test_measured_through_participant_must_exist() -> None:
    record = minimal_observation()
    record["context"]["measured_through_participant_id"] = "missing"
    assert "UNKNOWN_MEASURED_THROUGH_PARTICIPANT" in semantic_errors(record, {})


def test_model_ready_requires_review_and_uncertainty() -> None:
    record = copy.deepcopy(minimal_observation())
    record["quality"]["data_level"] = "model_ready"
    errors = semantic_errors(record, {})
    assert "MODEL_READY_NOT_HUMAN_VERIFIED" in errors
    assert "MODEL_READY_MISSING_UNCERTAINTY" in errors


def test_generic_property_is_blocked_from_model_ready() -> None:
    record = minimal_observation()
    record["property_id"] = "yield_point"
    record["context"]["type"] = "bulk_fluid"
    record["quality"] = {
        "data_level": "model_ready",
        "review_status": "double_review",
        "flags": [],
    }
    record["source_assertion"]["verification_status"] = "human_verified"
    terms = load_property_terms(VOCABULARY)
    assert "PROPERTY_NOT_MODEL_READY" in semantic_errors(record, terms)


def test_vocabulary_required_coordinate_is_enforced() -> None:
    record = minimal_observation()
    record["property_id"] = "sedimentation_supernatant_mass_fraction"
    record["context"]["type"] = "dispersion"
    terms = load_property_terms(VOCABULARY)
    assert "REQUIRED_COORDINATE_MISSING" in semantic_errors(record, terms)


def test_loose_censored_threshold_intersects_property_domain() -> None:
    record = minimal_observation()
    record["property_id"] = "recovery_factor"
    record["result"].update(
        {
            "raw_value_text": "< 1.2",
            "value_kind": "censored",
            "qualifier": "less_than",
            "value_original": 1.2,
            "unit_original": "1",
            "value_canonical": 1.2,
            "unit_canonical": "1",
            "conversion_rule": "identity",
        }
    )
    terms = load_property_terms(VOCABULARY)
    assert "CENSORED_RANGE_EMPTY" not in semantic_errors(record, terms)


def test_censored_threshold_with_empty_domain_is_rejected() -> None:
    record = minimal_observation()
    record["property_id"] = "recovery_factor"
    record["result"].update(
        {
            "raw_value_text": "< 0",
            "value_kind": "censored",
            "qualifier": "less_than",
            "value_original": 0,
            "unit_original": "1",
            "value_canonical": 0,
            "unit_canonical": "1",
            "conversion_rule": "identity",
        }
    )
    terms = load_property_terms(VOCABULARY)
    assert "CENSORED_RANGE_EMPTY" in semantic_errors(record, terms)
