"""Validate observation syntax and cross-field scientific invariants."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections.abc import Iterable
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

FRACTION_BASES = {"mole_fraction", "mass_fraction", "volume_fraction"}
TENSION_PROPERTIES = {
    "surface_tension_equilibrium",
    "surface_tension_dynamic",
    "interfacial_tension_equilibrium",
    "interfacial_tension_dynamic",
}
CONTACT_ANGLE_PROPERTIES = {
    "contact_angle_static",
    "contact_angle_advancing",
    "contact_angle_receding",
}
MODEL_READY_BLOCKING_FLAGS = {
    "ambiguous_context",
    "ambiguous_unit",
    "ambiguous_concentration_basis",
    "composition_incomplete",
    "method_incomplete",
    "quarantine",
}


def load_records(path: Path) -> Iterable[tuple[str, dict]]:
    if path.suffix.lower() == ".jsonl":
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if line.strip():
                yield f"line {line_number}", json.loads(line)
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        for index, record in enumerate(payload):
            yield f"item {index}", record
    else:
        yield "root", payload


def load_property_terms(path: Path) -> dict[str, dict[str, str | set[str]]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        return {
            row["property_id"]: {
                **row,
                "canonical_unit": row.get("canonical_unit_code", row.get("canonical_unit", "")),
                "allowed_contexts": set(
                    row.get("allowed_context_types", row.get("allowed_contexts", "")).split("|")
                ),
            }
            for row in rows
        }


def _normalized_unit(value: str) -> str:
    return value.strip().lower().replace("·", "").replace(" ", "")


def _conversion_error(
    original: float,
    original_unit: str,
    canonical: float,
    canonical_unit: str,
) -> bool:
    source_unit = _normalized_unit(original_unit)
    target_unit = _normalized_unit(canonical_unit)
    expected: float | None = None
    if source_unit in {"mn/m", "dyn/cm"} and target_unit == "n/m":
        expected = original / 1000
    elif source_unit == "n/m" and target_unit == "n/m":
        expected = original
    elif source_unit in {"°c", "degc", "c"} and target_unit == "k":
        expected = original + 273.15
    elif source_unit == "k" and target_unit == "k":
        expected = original
    elif source_unit in {"°", "deg", "degree", "degrees"} and target_unit in {
        "°",
        "deg",
        "degree",
        "degrees",
    }:
        expected = original
    return expected is not None and not math.isclose(
        expected,
        canonical,
        rel_tol=1e-9,
        abs_tol=1e-12,
    )


def _optional_float(value: object) -> float | None:
    if value in {None, ""}:
        return None
    return float(value)


def _inside_property_domain(value: float, term: dict[str, str | set[str]]) -> bool:
    lower = _optional_float(term.get("canonical_min"))
    upper = _optional_float(term.get("canonical_max"))
    min_inclusive = term.get("min_inclusive") == "1"
    max_inclusive = term.get("max_inclusive") == "1"
    if lower is not None and (value < lower or (value == lower and not min_inclusive)):
        return False
    return not (upper is not None and (value > upper or (value == upper and not max_inclusive)))


def _censored_domain_intersects(
    threshold: float,
    qualifier: str,
    term: dict[str, str | set[str]],
) -> bool:
    lower = _optional_float(term.get("canonical_min"))
    upper = _optional_float(term.get("canonical_max"))
    min_inclusive = term.get("min_inclusive") == "1"
    max_inclusive = term.get("max_inclusive") == "1"
    if qualifier == "less_than":
        return lower is None or threshold > lower
    if qualifier == "less_or_equal":
        return lower is None or threshold > lower or (threshold == lower and min_inclusive)
    if qualifier == "greater_than":
        return upper is None or threshold < upper
    if qualifier == "greater_or_equal":
        return upper is None or threshold < upper or (threshold == upper and max_inclusive)
    return False


def semantic_errors(
    record: dict,
    property_terms: dict[str, dict[str, str | set[str]]],
    fraction_tolerance: float = 0.01,
) -> list[str]:
    """Return stable error codes for invariants outside JSON Schema's scope."""
    errors: list[str] = []
    property_id = record.get("property_id")
    context = record.get("context", {})
    context_type = context.get("type")
    term = property_terms.get(property_id)
    if term and context_type not in term["allowed_contexts"]:
        errors.append("PROPERTY_CONTEXT_MISMATCH")

    series = record.get("series", {})
    coordinate_kinds = {
        item.get("kind") for item in series.get("coordinates", []) if item.get("kind")
    }
    required_coordinate = term.get("required_coordinate_term") if term else None
    if required_coordinate and required_coordinate not in coordinate_kinds:
        errors.append("REQUIRED_COORDINATE_MISSING")

    participants = context.get("participants", [])
    participant_ids = [item.get("participant_id") for item in participants]
    if len(participant_ids) != len(set(participant_ids)):
        errors.append("DUPLICATE_PARTICIPANT_ID")
    measured_through = context.get("measured_through_participant_id")
    if measured_through and measured_through not in participant_ids:
        errors.append("UNKNOWN_MEASURED_THROUGH_PARTICIPANT")

    for participant in participants:
        composition = participant.get("composition")
        if not composition:
            continue
        components = composition.get("components", [])
        material_ids = [component.get("material_id") for component in components]
        if len(material_ids) != len(set(material_ids)):
            errors.append("DUPLICATE_COMPOSITION_COMPONENT")

        bases = {component.get("basis") for component in components}
        fraction_bases = bases & FRACTION_BASES
        if fraction_bases and len(bases) > 1:
            errors.append("MIXED_COMPOSITION_BASIS")
        if composition.get("completeness") == "complete" and len(fraction_bases) == 1:
            canonical_amounts = [component.get("amount_canonical") for component in components]
            if any(value is None for value in canonical_amounts):
                errors.append("MISSING_CANONICAL_COMPOSITION")
            elif not math.isclose(
                sum(canonical_amounts),
                1.0,
                rel_tol=0,
                abs_tol=fraction_tolerance,
            ):
                errors.append("COMPOSITION_CLOSURE")

        for component in components:
            if component.get("material_kind") != "nanomaterial_lot":
                continue
            if component.get("basis") == "reported_other":
                errors.append("AMBIGUOUS_NANOMATERIAL_CONCENTRATION")
            if (
                record.get("quality", {}).get("data_level") != "staging"
                and component.get("active_product_basis") == "unknown"
            ):
                errors.append("AMBIGUOUS_ACTIVE_PRODUCT_BASIS")

    result = record.get("result", {})
    if result.get("value_status") == "reported":
        canonical_unit = result.get("unit_canonical")
        if term and canonical_unit != term["canonical_unit"]:
            errors.append("CANONICAL_UNIT_MISMATCH")
        if result.get("value_kind") == "interval":
            if result.get("lower_canonical", 0) > result.get("upper_canonical", 0):
                errors.append("INVALID_RESULT_INTERVAL")
        if "value_original" in result and "value_canonical" in result:
            if _conversion_error(
                result["value_original"],
                result["unit_original"],
                result["value_canonical"],
                result["unit_canonical"],
            ):
                errors.append("UNIT_CONVERSION_MISMATCH")
        values = [
            result[key]
            for key in ("value_canonical", "lower_canonical", "upper_canonical")
            if key in result
        ]
        if any(not math.isfinite(value) for value in values):
            errors.append("NONFINITE_CANONICAL_VALUE")
        elif term:
            value_kind = result.get("value_kind")
            if value_kind in {"point", "interval"} and any(
                not _inside_property_domain(value, term) for value in values
            ):
                errors.append("PROPERTY_RANGE_MISMATCH")
            elif value_kind == "censored" and not _censored_domain_intersects(
                result["value_canonical"], result.get("qualifier", ""), term
            ):
                errors.append("CENSORED_RANGE_EMPTY")
        if property_id in TENSION_PROPERTIES and any(value < 0 for value in values):
            errors.append("NEGATIVE_TENSION")
        if property_id in CONTACT_ANGLE_PROPERTIES and any(
            value < 0 or value > 180 for value in values
        ):
            errors.append("CONTACT_ANGLE_OUT_OF_RANGE")

    for condition in record.get("conditions", []):
        if condition.get("status") != "reported":
            continue
        if _conversion_error(
            condition["value_original"],
            condition["unit_original"],
            condition["value_canonical"],
            condition["unit_canonical"],
        ):
            errors.append("UNIT_CONVERSION_MISMATCH")

    for uncertainty in record.get("uncertainties", []):
        if "lower" in uncertainty and "upper" in uncertainty:
            if uncertainty["lower"] > uncertainty["upper"]:
                errors.append("INVALID_UNCERTAINTY_INTERVAL")
            point = result.get("value_canonical")
            if (
                uncertainty.get("representation") == "confidence_interval"
                and point is not None
                and not uncertainty["lower"] <= point <= uncertainty["upper"]
            ):
                errors.append("RESULT_OUTSIDE_CONFIDENCE_INTERVAL")

    coordinate_ids = [item.get("coordinate_id") for item in series.get("coordinates", [])]
    if len(coordinate_ids) != len(set(coordinate_ids)):
        errors.append("DUPLICATE_SERIES_COORDINATE")

    quality = record.get("quality", {})
    if quality.get("data_level") in {"curated", "model_ready"}:
        if term and term.get("active") != "1":
            errors.append("INACTIVE_PROPERTY_NOT_CURATABLE")
    if quality.get("data_level") == "model_ready":
        if term and term.get("model_ready_allowed") != "1":
            errors.append("PROPERTY_NOT_MODEL_READY")
        if quality.get("review_status") not in {"double_review", "adjudicated"}:
            errors.append("MODEL_READY_NOT_HUMAN_VERIFIED")
        if record.get("source_assertion", {}).get("verification_status") not in {
            "human_verified",
            "adjudicated",
        }:
            errors.append("MODEL_READY_SOURCE_NOT_HUMAN_VERIFIED")
        if set(quality.get("flags", [])) & MODEL_READY_BLOCKING_FLAGS:
            errors.append("MODEL_READY_HAS_BLOCKING_FLAG")
        if any(item.get("status") == "not_reported" for item in record.get("uncertainties", [])):
            errors.append("MODEL_READY_MISSING_UNCERTAINTY")
        if property_id in CONTACT_ANGLE_PROPERTIES:
            surfaces = [
                participant.get("surface_specimen", {})
                for participant in participants
                if participant.get("role") == "solid_surface"
            ]
            if not surfaces or any(
                surface.get("preparation_status") != "reported"
                or not str(surface.get("preparation") or "").strip()
                for surface in surfaces
            ):
                errors.append("MODEL_READY_SURFACE_PREPARATION_INCOMPLETE")

    return sorted(set(errors))


def validate_file(
    data_path: Path,
    schema_path: Path,
    vocabulary_path: Path = Path("metadata/vocabularies/property_terms.csv"),
) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    terms = load_property_terms(vocabulary_path)
    messages: list[str] = []
    for locator, record in load_records(data_path):
        schema_errors = sorted(
            validator.iter_errors(record), key=lambda item: list(item.absolute_path)
        )
        for error in schema_errors:
            path = ".".join(str(part) for part in error.absolute_path) or "<record>"
            messages.append(f"{locator}: {path}: {error.message}")
        if not schema_errors:
            messages.extend(f"{locator}: {code}" for code in semantic_errors(record, terms))
    return messages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("data/schemas/observation.schema.json"),
    )
    parser.add_argument(
        "--vocabulary",
        type=Path,
        default=Path("metadata/vocabularies/property_terms.csv"),
    )
    args = parser.parse_args()
    messages = validate_file(args.data, args.schema, args.vocabulary)
    if messages:
        print("\n".join(messages))
        raise SystemExit(1)
    print(f"Validated {args.data}")


if __name__ == "__main__":
    main()
