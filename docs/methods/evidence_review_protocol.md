# Evidence review protocol v0.1

## Review type and purpose

Week 37 uses a scoping review to map data sources, property definitions, measurement methods, predictive models, simulation workflows and the MWCNT drilling-fluid evidence base. It follows the reporting logic of [PRISMA-ScR](https://www.prisma-statement.org/scoping) and logs searches in the spirit of [PRISMA-S](https://doi.org/10.1186/s13643-020-01542-z). This is not yet a registered systematic review.

## Review questions

1. Which open, licensed or computable sources contain usable surface, interfacial, contact-angle or adsorption data?
2. Which metadata control comparability and uncertainty for each property mode?
3. Which physical, ML, MD, QM and CAE approaches have credible baselines and open implementations?
4. Which novelty claims survive comparison with recent databases and OOD modeling studies?
5. Which MWCNT interface mechanisms connect to measurable drilling-fluid outcomes?

## Search streams

- S1: liquid-vapor surface tension and mixtures;
- S2: liquid-liquid IFT, oil/brine and surfactants;
- S3: dynamic tension and adsorption kinetics;
- S4: mineral wettability, contact angle and adsorption;
- S5: datasets, QSPR/ML, physical baselines and uncertainty;
- S6: MD/QM/DFT, EOS/DGT, COSMO-RS and pore-scale/CFD transfer;
- S7: MWCNT dispersion, Pickering interfaces, drilling fluids, EOR and formation damage.

Exact seed queries are versioned in `literature/searches/strategies/initial_scoping_queries.yaml`.

## Information sources

Use Crossref and OpenAlex for broad bibliographic discovery, then publisher pages and DOI records for verification. Search Scopus and Web of Science when institutional access permits reproducible export. Search NIST ThermoML, ILThermo, Chemistry WebBook, NOAA ADIOS, IAPWS, Zenodo and relevant domain repositories directly. Patents are a separate evidence type and do not replace peer-reviewed mechanistic evidence.

## Eligibility

Include a source when it provides at least one of the following:

- extractable interfacial measurements with sufficient conditions;
- a reusable data source, schema or validated correlation;
- a computational protocol with verification or convergence evidence;
- a predictive model with enough information to assess splits and leakage;
- mechanistic or application evidence for CNT/MWCNT formulations.

Exclude or quarantine:

- records with no traceable primary source;
- reviews used as if they were primary measurements;
- values with irrecoverable property mode, phase identity or units;
- inaccessible claims whose abstract does not support the asserted detail;
- duplicates, conference summaries superseded by full papers, or retracted work;
- application claims that lack a comparable control or defined formulation.

Language scope is English and Russian. No publication-year cutoff is applied to foundational methods. Discovery prioritizes the most recent five years plus cited foundational work.

## Search-run record

Every run records:

- `search_run_id`, platform and endpoint;
- exact query, filters and coverage date;
- UTC timestamp and operator;
- script and prompt version or Git commit;
- returned count and exported count;
- raw output path and SHA-256;
- deduplication method and errors.

## Screening

Perform title/abstract screening first, followed by full-text screening. Record one decision per source and stage with a controlled reason. A second human reviews all lead-hypothesis sources and a random sample of at least 10% of other inclusions and exclusions.

## Evidence extraction

Each quantitative item needs source ID, exact locator, property and interface type, both phases, composition basis, conditions, original value/unit, normalized value/unit, method, uncertainty, evidence type and verification status. Dynamic data require surface age. Liquid-liquid IFT should retain both equilibrium phase compositions when reported.

For MWCNT records also capture grade, wall type, diameter/length, purity, BET, defect metric, functionalization and degree, concentration basis, dispersant/polymer, order of addition, mixing energy/time, aging, zeta potential, size/stability measure, full formulation and application outcome.

## Quality control

1. Validate DOI/URL and bibliographic identity.
2. Confirm the value against the exact table, figure, text or dataset record.
3. Preserve original notation before conversion.
4. Run schema, unit, range and referential-integrity checks.
5. Group likely duplicates but never delete them silently.
6. Compare extracted values with source-level sample size and uncertainty.
7. Mark conflicts for adjudication by the principal investigator.

The initial extraction gold set should contain at least 30 observations double-checked by a human across all four property domains and at least five MWCNT application records. Automation is not scaled until field-level precision is acceptable and all critical errors are understood.

## Synthesis outputs

- source-license matrix;
- evidence and gap map by property, chemical family, phase, condition and method;
- method benchmark matrix;
- competitor and novelty table;
- hypothesis scorecard with support and falsifiers;
- ranked list of experiments or calculations by expected information gain;
- PRISMA-style flow counts.
