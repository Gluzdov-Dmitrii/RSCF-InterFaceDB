# ADR 0002 Property and interface taxonomy

Date: 2026-09-05

Status: v0.2 proposed for validation in Week 37

## Decision

The database will not use a single generic “surface tension” target. One observation stores one result and links it to a controlled property term, physical context, method run, source assertion and optional series.

### Context types

- `liquid_gas_interface`
- `liquid_liquid_interface`
- `three_phase_contact`
- `liquid_solid_interface`
- `bulk_fluid`
- `dispersion`
- `nanomaterial_lot`
- `filtration_test`
- `lubricity_test`
- `porous_media_flow`

### Initial property types

- `surface_tension_equilibrium`
- `surface_tension_dynamic`
- `interfacial_tension_equilibrium`
- `interfacial_tension_dynamic`
- `contact_angle_static`
- `contact_angle_advancing`
- `contact_angle_receding`
- `adsorption_amount_static`
- `porous_media_retained_mass_dynamic`
- `interfacial_layer_thickness`

Application metrics such as dispersion stability, bulk rheology, filtration, lubricity and permeability damage use their own property IDs and contexts. They remain linked observations rather than extra results embedded into an interfacial observation. The authoritative vocabulary is `metadata/vocabularies/property_terms.csv`.

Method-ambiguous legacy IDs such as `dispersion_stability_index`,
`aggregate_size_apparent`, `yield_point` and `adsorption_retention_dynamic` may preserve
source-native staging records, but cannot enter model-ready snapshots. Specific terms
separate sedimentation from centrifugation, DLS from image sizing, fitted yield stress
from an oilfield-standard yield point, and mechanism-neutral retention from adsorption.

## Required distinctions

- Liquid-liquid records identify two distinct liquid participants and, when reported, both equilibrium phase compositions.
- A supercritical fluid is not silently treated as a gas-phase participant in a
  liquid-gas surface-tension record; such data stay quarantined until a dedicated
  interface context is approved.
- Dynamic tension requires a series coordinate for surface age and a defined time origin; zero is valid at interface creation.
- Contact angle requires droplet, ambient and solid-surface participants, measured-through phase, geometry and preparation status.
- Surfactant concentration records its basis and relation to CMC only when the source supports it.
- Original value text and units are immutable; canonical values are derived fields. Canonical does not always mean SI: contact angle remains in degrees.
- Scientific origin (`experiment`, MD, QM, continuum, correlation, ML or derived) is separate from ingestion route (publication, database, secondary source or internal run).
- Unknown conditions are explicit missing values and quarantine flags, never assumed defaults.
- Complete fraction compositions must close to one within the documented tolerance.

## Why this matters

Mixing these targets creates false duplicates, data leakage and scientifically meaningless models. The taxonomy also enables method-aware uncertainty analysis and a defensible out-of-domain benchmark.
