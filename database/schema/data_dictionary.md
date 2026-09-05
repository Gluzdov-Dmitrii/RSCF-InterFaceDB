# InterFaceDB data dictionary v0.2

## Scope and authority

The relational schema in `database/schema/001_initial.sql` is the canonical v0.2
storage model. The versioned property vocabulary is maintained in
`metadata/vocabularies/property_terms.csv`; the seed rows in the SQL migration
must match every CSV field, including definitions, units, quantity kinds,
bounds, state flags and coordinate requirements, plus the complete
property-context mappings.

`data/schemas/observation.schema.json` is the v0.2 staging/interchange companion
for generalized contexts, results, source/method assertions and series. The SQL
schema remains authoritative for relational storage. The Python semantic
validator complements both representations with cross-field invariants that are
not safely or completely expressible in JSON Schema or SQLite constraints.

## Primary rule

One `observation` row is exactly one source-reported, measured, simulated,
derived or predicted result for one property, one context, one condition set and
one method run.

MWCNT characterization, dispersion stability, bulk rheology, filtration,
lubricity, porous-medium outcomes and ML predictions use the same observation
table as interfacial properties. They are not nested secondary values and do not
use a reduced application-results table. Observations from the same experiment
are grouped by a common context, method run, condition set, series or application
run.

## Record states

| State | Meaning |
| --- | --- |
| `staging` | Source-native result retained even if normalization or a condition is incomplete. |
| `curated` | Property, context, canonical value/unit and required coordinate have passed review and semantic validation. |
| `model_ready` | Double-reviewed or adjudicated curated result, with reviewer identity and timestamp, eligible for a versioned modelling snapshot. |
| `withdrawn` | Retained for history but excluded from active analysis. |

Missing information is represented explicitly in its relevant table with a
status such as `not_reported`, or by an absent optional row. It must never be
replaced by a convenient default such as 298.15 K, atmospheric pressure or zero
uncertainty. Moving a record between states does not authorize overwriting its
source-native value.

## Entity supertype and subtypes

`entity` supplies stable identifiers for physical and conceptual research
objects. Each subtype table uses the same `entity_id`; insertion triggers reject
an incompatible `entity_type`.

| Subtype | Purpose | Critical fields |
| --- | --- | --- |
| `material_entity` | Reusable identity for a pure substance, polymer, petroleum material, brine, mineral, defined mixture or nanomaterial parent | kind, preferred name, structure when meaningful |
| `material_identifier` | External identity | scheme and value, for example InChIKey, CAS RN, PubChem CID or internal registry |
| `material_lot` | Physical supplier, laboratory or field lot | parent material, supplier, product, catalogue/batch and source-native purity |
| `formulation` | Nominal, measured or equilibrated composition | class, composition stage and completeness |
| `phase_sample` | Run-specific phase | source material/formulation, physical state and composition stage |
| `surface_specimen` | Prepared solid surface | material, crystal face/termination, hydroxylation, roughness metric, cleaning, treatment and aging |
| `nanomaterial_lot` | CNT lot extension of `material_lot` | CNT type, synthesis, functionalization class/groups and product state |
| `dispersion_batch` | Prepared CNT dispersion | formulation, preparation method, sonication/energy, temperature, mixing order and downstream treatment |
| `core_sample` | Porous-medium specimen | rock/mineralogy, origin, orientation and preparation/restoration history |
| `application_run` | Drilling, filtration, lubricity, EOR or core-flow run | formulation/dispersion/core, method, standard/version, baseline and protocol |

Entity subtype identity and measured properties are deliberately separate.
For example, a nanotube lot does not have a timeless scalar diameter, BET area,
Raman ratio or zeta potential. Diameter, length, BET and Raman results are
observations on a `nanomaterial_lot` context. Zeta potential and apparent
aggregate size are observations on a specific `dispersion` context.

## Formulations and composition

`formulation_component` records both the exact source representation and an
optional normalized value:

- `amount_original_text`, `amount_original`, `unit_original` preserve the source;
- `composition_basis` distinguishes mole/mass/volume fraction, molality,
  amount or mass concentration, parts per mass, parts per volume and oilfield
  mass per barrel;
- `amount_canonical`, `unit_canonical`, `conversion_expression` and
  `conversion_version` record a reproducible normalization;
- `active_product_basis` distinguishes dry active MWCNT or reagent from an
  as-received commercial dispersion/product.

`ppm` is not a basis. It must be resolved to mass/mass, volume/volume or another
explicit definition. In drilling-fluid sources, `ppb` can mean pounds per barrel
rather than parts per billion. Conversion between mass concentration, mass
fraction and molarity requires the supporting density or molar mass at applicable
conditions.

For complete fraction-based formulations, the semantic validator must require
closure to 1 within a documented tolerance. Incomplete source formulations stay
`composition_complete = 0`; missing components are not inferred. Nominal feed
composition, measured pre-contact composition and equilibrium phase composition
are separate formulations/phase samples.

## System contexts and participants

`system_context` defines the scientific subject of an observation.
`context_participant` is its authoritative membership relation. There is no
independent `system_id` plus fixed phase foreign keys, so it is impossible to
attach a phase from another physical system accidentally.

| Context | Required participant shape |
| --- | --- |
| `liquid_gas_interface` | exactly `liquid_phase` and a gas/vapour `gas_phase`; supercritical fluid is excluded |
| `liquid_liquid_interface` | exactly `liquid_phase_a` and `liquid_phase_b` |
| `liquid_solid_interface` | exactly `liquid_phase` and `solid_surface` |
| `three_phase_contact` | exactly `probe_phase`, `ambient_phase` and `solid_surface`, plus `contact_angle_context` |
| `bulk_fluid` | at least one `bulk_fluid` participant |
| `nanomaterial_lot` | a `subject_nanomaterial_lot` participant |
| `dispersion` | a `dispersion` participant |
| `filtration_test`, `lubricity_test` | an `application_run` participant; formulation may also be linked |
| `porous_media_flow` | both `application_run` and `porous_medium`; formulation may also be linked |

Participant subtype and physical-state checks are enforced by SQL triggers.
Contexts and participants become immutable after the first observation uses
them. To correct an incorrectly assembled context, create a new context and a
superseding observation.

For liquid-liquid interfaces, roles A and B are canonical rather than physical
drop/bulk labels. Use a stable composition fingerprint to choose A/B and preserve
reported `drop`, `bulk`, `upper`, `lower`, `displacing` or `displaced` semantics
in `reported_role` or method parameters.

Contact angle is a property of a three-phase contact line, not merely a
liquid-solid pair. `contact_angle_context` therefore records the phase through
which the angle is measured and the geometry. The property ID distinguishes
static, advancing and receding observations.

## Property vocabulary and context rules

`property_term` defines a property, canonical unit, dimension, physical range
and any mandatory primary series coordinate. `property_context_rule` lists every
allowed property-context pair. The observation table contains composite foreign
keys to both the context and the property-context rule, so combinations such as
surface tension on a liquid-liquid context or contact angle on a liquid-gas
interface fail at the database boundary.

Important v0.2 definitions:

- equilibrium and dynamic surface tension are restricted to liquid-gas contexts;
- `supercritical_fluid` is not a gas phase and cannot enter a
  `liquid_gas_interface`; a future fluid-supercritical vocabulary extension must
  define its own context and thermodynamic measurand;
- equilibrium and dynamic interfacial tension are restricted to liquid-liquid
  contexts;
- dynamic tension requires a `surface_age` series with an explicit time origin;
- contact angles use degrees as the domain canonical unit and require a
  three-phase context, non-`unspecified` geometry, baseline-fitting method and a
  non-empty surface-preparation protocol before curation;
- `adsorption_amount_static` is a directly observed equilibrium loading at a
  stated equilibrium adsorbate concentration. Fitted capacity and
  area-normalized surface excess are different future terms;
- `adsorption_retention_dynamic` is deprecated because retention in porous media
  does not establish adsorption. Use the mechanism-neutral
  `porous_media_retained_mass_dynamic` and attribute a mechanism only through
  separate evidence;
- `permeability_impairment` is `(k_before - k_after) / k_before`, so negative
  values indicate improvement;
- `recovery_factor` is a fraction from 0 to 1 and requires its OOIP, ROIP or other
  denominator basis in method/condition metadata.

The SQL seed contains 43 v0.2 properties. The protocol-dependent legacy terms
`dispersion_stability_index`, `aggregate_size_apparent` and `yield_point` may be
curated for source fidelity but are explicitly barred from `model_ready`.
Specific sedimentation, centrifugation, DLS, image-size and rheology terms should
be used instead. The deprecated `adsorption_retention_dynamic` term is inactive
and cannot enter a curated state.

`property_condition_requirement`, `property_method_parameter_requirement` and
`property_result_basis_rule` are the authoritative machine-readable
property-to-metadata mappings. `model_ready_allowed` provides a fail-closed gate
for a generic term that cannot yet be made commensurate. Vocabulary additions
require a stable ID, definition, canonical unit, quantity kind, allowed context,
requirements, bounds, migration note and version bump. SQL/CSV synchronization
must compare normalized full rows and context sets, not IDs alone.

## Conditions

`condition_set` groups run conditions; each `condition_value` has a controlled
term, optional target entity (`applies_to_entity_id`), source-native
representation, normalized representation, status, conversion and source
assertion. When that entity is a direct system participant, its participant role
is resolved through the observation's own `context_id`; a component nested in a
formulation may instead be targeted directly by entity ID.

The initial terms cover temperature, absolute and confining pressure, pH, ionic
strength, salinity, component concentration, relative centrifugal force and
centrifugation time,
surface/equilibration/sample/storage/rest/filtration time, shear rate, frequency,
strain, flow rate, superficial/interstitial velocity, injected pore volumes and
humidity. `component_concentration` has no universal canonical unit: its target
entity, `basis_or_scale` and the series-specific canonical unit are mandatory.
Thus `kg/m3`, `mol/m3`, `kg/kg` and oilfield `lb/bbl` are never treated as
interchangeable coordinates merely because all are called “concentration”.
Condition sets and their values become immutable as soon as an observation uses
them; a correction requires a new set and a superseding observation.

Rules outside simple SQL constraints remain mandatory:

- pH requires phase, scale/method and temperature; do not impose a universal
  0-14 hard bound;
- gauge pressure is retained as reported and converted to
  `pressure_absolute` only with the reference pressure;
- TDS, equivalent NaCl salinity, mass fraction, molality and ionic strength are
  not interchangeable;
- surface age, sample age, equilibration time and storage/thermal-aging time are
  distinct terms.

## Method runs and evidence origin

`method_run.origin_kind` identifies how the scientific result was generated:
`experiment`, `molecular_dynamics`, `dft_qm`, `cfd_lbm`, `correlation`,
`ml_prediction` or `derived`. Database import and secondary reporting are
ingestion routes on `source_assertion`, not evidence origins.

`method_run` captures the instrument/software and versions, protocol and profile
versions, force field/model, content hashes and optional structured parameters.
Searchable parameters are rows in `method_parameter`. Terms are controlled by
`method_parameter_term`; categorical values such as population statistic and
rheological model use `method_parameter_value_term`. Property-level required
qualifiers are enforced before curation or model readiness. Method-specific
profiles must additionally be validated outside SQL, at minimum:

- experiment: instrument, calibration, acquisition and replicate/statistical
  protocol;
- MD: code/version, force fields, ensemble, box/interface count, timestep,
  equilibration/production, cutoffs/electrostatics, estimator, replicas and
  convergence/finite-size checks;
- DFT/QM: functional, dispersion correction, basis/pseudopotential, slab and
  termination, k-grid/cutoff, solvation and convergence;
- CFD/LBM: equations/model, geometry, mesh-independence, boundary/initial
  conditions, solver convergence and links to input IFT/contact-angle
  observations;
- ML: data snapshot/split, features/preprocessing, seed, environment, calibration
  and applicability-domain rule.

A method run and its parameters become immutable when an observation, series,
dispersion preparation or application run uses them. Corrections create a new
versioned method run.

## Sources, assertions and provenance

`source` stores bibliographic or internal artifact identity, access rights,
license and optional content hash. `source_assertion` stores the exact page,
table, figure, dataset row or artifact-record locator and separates extraction
mode from human verification.

Each observation has one source assertion and one method run. Internal
calculations use a source record of type `simulation_artifact` or
`laboratory_record` with an exact output locator.

The provenance graph follows the Entity-Activity-Agent pattern:

- `agent` identifies people, organizations, software and model agents;
- `provenance_activity` records extraction, normalization, conversion,
  digitization, simulation, training, prediction, derivation, review or migration;
- `provenance_input` identifies exactly one input object per row and may store an
  artifact hash;
- `provenance_generated_observation` links outputs;
- `observation_relation` records derivation, replicate, control, baseline,
  conflict, digitization and supersession relationships.

Source-native observation fields are immutable by trigger. The evidentiary
fields of a referenced `source_assertion` (source, locator, reported value and
extraction identity) are immutable as well; verification status may advance.
The cited source identity/version/hash is locked after its first assertion;
access and redistribution metadata may still be updated. Corrections create a
new assertion and a new observation with
`supersedes_observation_id` and provenance.

## Result and uncertainty representation

An observation result is one of:

- `point`: one numeric value with `exact` or `approximate` qualifier;
- `interval`: lower and upper bounds;
- `censored`: a numeric threshold with `<`, `<=`, `>` or `>=` semantics.

A censored threshold is not a point estimate. SQL accepts a loose bound outside
the physical range when its feasible set still intersects the property domain
(for example `recovery_factor < 1.2`) and rejects only an empty intersection
(for example `recovery_factor > 1.2`). Strict versus inclusive qualifiers are
handled at an inclusive or exclusive property boundary.

`raw_value_text` and original unit are mandatory. Curated/model-ready records
also require the property canonical unit and corresponding canonical value or
bounds. Point/censored results cannot also carry canonical interval bounds, and
interval results cannot carry a canonical point value. Physical ranges and
canonical units are enforced from `property_term`. If the original and canonical
units differ, a non-empty conversion expression and version are mandatory.

`statistic_kind` distinguishes a single value, mean, median, fitted value,
simulation average, digitized estimate and model prediction. Individual
replicates can be stored as separate observations under `replicate_group_id`;
an aggregate mean is another observation linked to its inputs.

`uncertainty_component` is one-to-many because experimental repeatability,
instrument uncertainty, digitization error, correlated simulation sampling and
ML predictive uncertainty are not interchangeable. Confidence intervals require
bounds and confidence level; expanded uncertainties require a coverage factor.
`not_reported` is stored with kind `none`, not with a zero value.

## Series

`observation_series` defines only a logical curve and its primary independent
coordinate; it deliberately has no context foreign key. Every point remains a
scalar `observation` and owns its context and condition set. This permits a
temperature or concentration series in which formulation, phase sample or other
context identity changes between points without attaching a point to the wrong
system.

For every series point, `coordinate_condition_value_id` identifies the matching
row in that observation's condition set. SQL checks that its term, original and
canonical values and units agree with the series and observation coordinate. For
a `component_concentration` series that condition row also supplies the target
component entity and explicit basis. Series coordinate semantics and referenced
coordinate-condition rows become immutable once used; corrections require new
rows and provenance.

Other fixed or secondary coordinates remain ordinary rows in the point's
condition set.

Mandatory examples:

- dynamic surface/IFT: `surface_age`, with a defined interface-creation time;
- apparent viscosity: `shear_rate`;
- gel strength: `rest_time`;
- HPHT filtrate volume: `filtration_time`;
- dispersion stability index: `storage_time`.

Zero surface age is valid if the operational time origin is defined. A complete
curve must never be stored as an array-valued observation.

## MWCNT and application layer

MWCNT concentration is a formulation-component amount, not an intrinsic field of
the nanotube identity. The component must identify the physical lot and whether
concentration refers to dry active nanotube or as-received product.

`dispersion_batch` stores the preparation history. Rated sonicator power,
delivered energy, energy density, amplitude, duty cycle, maximum temperature,
cooling, mixing order and centrifugation/filtration are distinct metadata and
must not be silently substituted for one another.

Paper-2/H5-H7 application results are ordinary observations with specific
measurands:

- dispersion: sedimentation supernatant mass fraction, centrifugation
  supernatant mass fraction, zeta potential, DLS z-average and image-derived
  equivalent aggregate diameter;
- interface/emulsion: interfacial coverage fraction, Sauter mean droplet
  diameter and separated-volume fraction;
- bulk rheology: apparent/plastic viscosity, Herschel-Bulkley yield stress,
  API oilfield yield point, gel strength and oscillatory storage/loss moduli;
- filtration: HPHT filtrate volume and filter-cake thickness;
- drilling: lubricity coefficient;
- porous media: mechanism-neutral retained mass, permeability impairment and
  recovery factor;
- CNT lot: purity, ash, surface oxygen atomic fraction, identified
  functional-group amount and aspect ratio in addition to BET/Raman/size.

`application_step` preserves injection or treatment order, time, pore volume and
flow rate. Relative improvement claims must link treatment and baseline
observations rather than store an unqualified percentage.

## Dataset snapshots, OOD splits and ML predictions

`dataset_snapshot` is a content-addressed set of observation IDs with selection
query, schema/vocabulary versions and license. It is assembled in `draft` state
from `model_ready` observations, then moved once to `frozen` with
`finalized_at`. A frozen row and its `dataset_member` rows are immutable. Splits
can only be created from a frozen snapshot. Member observation values and their
uncertainty rows are also locked; scientific corrections are represented by a
new observation and a new snapshot, never by rewriting a released member.

`split_definition` records the strategy and group axes. `split_assignment`
requires every assigned observation to belong to the same snapshot. A trigger
rejects a repeated `group_key` across train, validation and test, including on
updates. Supported strategies include series-, source-, component-, system-,
mineral-family-, laboratory-, time-, MWCNT-lot- and functionalization-disjoint
splits. `random_row` is retained only as a diagnostic baseline and is not an OOD
claim.

`ml_model_run` records the data snapshot/split, feature schema, preprocessing,
code/environment hashes, seed, hyperparameters and model artifact. Its method run
must have origin `ml_prediction`. Once predictions or applicability-domain rules
refer to a run, the run and its split assignments are immutable.

A predicted value is first staged as a normal observation with `statistic_kind =
model_prediction`; `ml_prediction_detail` links it to the exact same ML method
run before the observation can become curated/model-ready.

`domain_rule` defines the named metric, feature space, version, threshold and
direction. `domain_assessment` stores score, decision, nearest-training evidence
and reasons. A trigger rejects an in/out-domain decision that contradicts its
threshold rule. Predictive intervals remain uncertainty components on the
observation.

## Database-enforced versus semantic QC

SQLite enforces:

- subtype identity;
- property-context compatibility;
- required interface/contact participant shapes;
- participant physical-state classes;
- exclusion of supercritical fluids from liquid-gas surface-tension contexts;
- context immutability after use;
- result shape, canonical unit and property range;
- feasible-domain logic for censored thresholds;
- controlled property condition, method-qualifier and result-basis requirements;
- fail-closed model-ready policy for generic non-commensurate property terms;
- contact-angle geometry, baseline-fit and surface-preparation completeness;
- required primary series coordinate for curated results;
- agreement between a series point and its referenced coordinate condition,
  including target and basis for component-concentration series;
- uncertainty shape;
- snapshot/split membership and group-key leakage;
- ML prediction origin and OOD threshold consistency;
- source-native observation immutability;
- immutable referenced source assertions, frozen dataset snapshots, used splits,
  ML runs and assessed domain rules;
- strict SQLite typing for central numeric result, condition, composition,
  dispersion, split/model and OOD tables.

The external semantic validator must additionally check:

- UCUM/QUDT unit parsing and numerical conversion;
- fraction closure, charge balance where applicable and conversion prerequisites;
- each targeted condition entity is a participant in the observation context or
  is traceably nested in a participating formulation/phase sample;
- duplicate fingerprints and contradictory values;
- property-specific method-profile completeness;
- temperature, pressure and other plausibility ranges as warnings where they are
  not universal physical invariants;
- complete provenance chains and content hashes;
- series monotonicity/duplicate coordinates;
- source-, component-, mineral-, lot- and time-level split leakage beyond the
  stored primary group key;
- model-ready eligibility and unresolved QC errors.

`qc_run` and `qc_issue` retain versioned validator output. QC issues are not
silently deleted or replaced by a manually chosen quality score.

`PRAGMA foreign_keys = ON` is connection-local in SQLite. Every application,
ETL job and test connection must enable it and immediately assert
`PRAGMA foreign_keys = 1`; running the migration once is not sufficient. The
reference deployment requires SQLite 3.37 or newer because central scientific
tables use `STRICT` typing.

## Recommended insertion order

1. Create agents, sources and source assertions.
2. Create material identities, lots, formulations and phase/surface specimens.
3. Create method runs, required controlled method parameters, condition sets and
   their condition values.
4. Create dispersion/application subtypes when applicable.
5. Create a system context, then all required participants and any contact-angle
   geometry.
6. Create a context-independent series if the property or study design requires
   a coordinate.
7. Insert the scalar observation and uncertainty components.
8. Record provenance, relations and QC results.
9. After double review/adjudication, assemble a draft dataset snapshot, freeze
   it, then create splits and model runs.
