# Research program

## What the project must produce

The local application defines a two-year program. Its detailed administrative audit is
kept outside public Git until the PI clears it. The research-facing deliverables are:

- a structured and validated database linking liquid composition, surface, conditions and interfacial properties;
- reproducible protocols for obtaining missing values with molecular dynamics and, where justified, CFD, QM or machine learning;
- quantitative composition-property relationships with uncertainty and applicability limits;
- a first-year database version, pilot calculations and material for the first article;
- a final database, predictive models, multiscale demonstrations and a second article;
- registration of a database intellectual-property result, subject to the signed
  agreement and formal publication rules.

Two Q1-Q2 papers and a citable database release are the scientific minimum. Maintain a
reserve manuscript story until the signed agreement confirms the formal counting of
publications and registered results; do not infer that one substitutes for another.

## Scope for version 1

The database should not attempt to cover every interfacial phenomenon at once. Version 1 will prioritize four linked evidence domains:

1. equilibrium liquid-vapor surface tension of pure liquids and mixtures;
2. equilibrium liquid-liquid interfacial tension, especially oil/brine and surfactant systems;
3. dynamic surface or interfacial tension of surfactant solutions with surface age;
4. liquid-solid behavior: contact angle, wettability alteration and adsorption on mineral surfaces.

MWCNT formulations form a dedicated application layer. It adds nanomaterial identity, functionalization, dispersion protocol, colloidal stability, interfacial coverage, emulsion behavior, rheology, filtration, lubricity and formation-damage outcomes. EOR data can inform mechanisms, but the primary commercial demonstration is drilling-fluid design.

## Central scientific argument

A database by itself is infrastructure, not sufficient novelty. The research claim will be tested at three levels:

1. **Measurement-aware data:** explicitly representing method, phase state, uncertainty and provenance changes conclusions and model calibration.
2. **Physics-aware prediction:** a model of the residual relative to a physical baseline should transfer to new chemical families and systems better than an end-to-end model trained on random rows.
3. **Mechanistic application:** interfacial and dispersion descriptors should explain MWCNT drilling-fluid performance better than nanotube mass concentration alone.

This argument links the application text to a publishable sequence: trustworthy data, robust prediction, then a mechanism-driven industrial case.

## Workstreams

| ID | Workstream | Near-term output | Final output |
| --- | --- | --- | --- |
| WS1 | Evidence and licensing | reproducible scoping review and source-license matrix | maintained evidence map and bibliography |
| WS2 | Data model and quality | observation schema, controlled vocabularies, gold extraction set | versioned database with provenance and QC |
| WS3 | Retrieval and extraction | Crossref/PDF pilots with human validation | reproducible ingestion and review pipeline |
| WS4 | Physical and ML baselines | benchmark design and small feasibility dataset | calibrated OOD models and applicability domain |
| WS5 | MD/QM/CAE | ranked systems and convergence protocols | targeted gap-filling and multiscale examples |
| WS6 | MWCNT drilling fluids | mechanism map and minimal pilot design | validated multiobjective formulation study |
| WS7 | Publications and release | paper storyboards and evidence requirements | two submissions and citable database release |

## Publication strategy

### Paper 1: database and benchmark

Working title: *A method- and uncertainty-aware database and out-of-domain benchmark for liquid surface and interfacial tension*.

Minimum publishable package:

- a public schema and provenance model;
- a redistribution-safe dataset release plus metadata for restricted sources;
- a manually verified extraction gold set;
- classical and physical baselines, QSPR/tree models and at least one mixture-aware model;
- random, component-disjoint, system-disjoint, family-disjoint and temporal evaluation;
- calibrated uncertainty and explicit applicability-domain analysis.

Candidate journals depend on the final emphasis: *Scientific Data*, *Journal of Chemical Information and Modeling*, *Journal of Chemical & Engineering Data* or *Fluid Phase Equilibria*. Current quartiles and scope must be checked immediately before selecting a target.

### Paper 2: MWCNT application

Working title: *Interfacial-descriptor-guided multiobjective design of MWCNT-enhanced drilling fluids under saline and high-temperature conditions*.

The paper must go beyond “MWCNT improves rheology”. The publishable mechanism is:

`composition and processing -> dispersion and interfacial state -> rheology, filtration, lubricity and damage`.

Minimum evidence should include matched controls, fixed dispersion energy, functionalization characterization, dynamic/equilibrium interfacial measurements, aging, rheology, HPHT filtration and a mechanism-level analysis. Candidate journals include *Langmuir*, *Colloids and Surfaces A*, *Journal of Molecular Liquids*, *Geoenergy Science and Engineering* and *SPE Journal*. Target selection again requires a current quartile and scope check.

## Computation strategy

Use a cascade rather than committing early to the most expensive method:

1. correlations and corresponding-states or parachor baselines;
2. PC-SAFT or related EOS plus density-gradient theory where parameters exist;
3. COSMO-RS descriptors and QSPR/ML;
4. classical MD for selected gaps and mechanism checks;
5. DFT/AIMD or learned potentials only when force-field uncertainty controls the conclusion;
6. CFD or pore-scale models only after the interfacial parameter and uncertainty are defined.

Every expensive run needs a hypothesis, cheaper baseline, convergence test, expected information gain and stop rule.

## Decision gates

- **Gate A, scope:** property taxonomy and minimum metadata accepted.
- **Gate B, evidence:** at least 30 key papers screened and a source-license matrix completed.
- **Gate C, extraction:** a manually checked gold set shows acceptable field-level error and every value has a locator.
- **Gate D, novelty:** at least two lead hypotheses survive explicit prior-art falsification.
- **Gate E, computation:** a ranked gap map justifies the first MD/QM/CAE campaign.
- **Gate F, MWCNT:** equipment, materials, safety and partner access support a credible pilot; otherwise Paper 2 remains a data/computation study.

The first week closes Gates A and part of B-D. It deliberately avoids a large simulation campaign.
