# Data management plan

## Design principles

The repository follows the `external -> raw -> interim -> processed -> curated` separation used in established data-science project structures. FAIR principles guide identifiers, metadata, access conditions, interoperability and provenance. FAIR does not mean every source can be redistributed.

Authoritative references:

- [Cookiecutter Data Science directory structure](https://cookiecutter-data-science.drivendata.org/)
- [FAIR Guiding Principles](https://www.gofair.foundation/fair-principles)
- [DVC pipeline files](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files)
- [DVC configuration and secret handling](https://dvc.org/doc/user-guide/project-structure/configuration)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html)
- [Frictionless Table Schema](https://specs.frictionlessdata.io/table-schema/)

## Storage classes

| Class | Examples | Location | Versioning |
| --- | --- | --- | --- |
| source metadata | DOI, citation, license, hash, locator | `literature/metadata/` | Git |
| restricted full text | publisher PDF, partner report, application document | local `literature/fulltext/` or approved private storage | never public Git; private DVC only if authorized |
| raw machine data | API JSON, XML, OCR and extracted text | `data/raw/` | DVC after remote approval |
| transformed data | normalized tables and deduplicated records | `data/interim/`, `data/processed/` | DVC |
| release data | SQLite, Parquet, CSV release bundle | `data/curated/` | DVC plus DOI repository when licensed |
| code and definitions | schema, migration, prompt, workflow, tests | `database/`, `src/`, `prompts/`, `workflows/` | Git |
| large computation | trajectories, wavefunctions, checkpoints and logs | cluster project storage and `simulations/runs/` | DVC or archive policy, not Git |
| manuscript source | Markdown, LaTeX, BibTeX and small diagrams | `manuscripts/` | Git |

The current application PDFs and MWCNT partner materials remain in their original local folders. Both folders are ignored before the first commit. A detailed hash inventory goes in `private/source_manifest.local.csv`, which is also ignored. Only public bibliographic metadata should enter `literature/metadata/source_manifest.csv`.

## Git and DVC policy

GitHub recommends small objects, with 1 MB as a practical recommendation and 100 MB as an enforced single-object limit. Generated files should live outside Git. The project therefore blocks common document, dataset, model and simulation formats in `.gitignore`.

DVC is the planned data layer because it can connect retrieval, parsing, normalization, validation, features, training and release while Git keeps the lightweight definitions. Do not initialize a remote until these questions are answered:

1. Is the storage durable project space rather than cluster scratch?
2. Can access be restricted by dataset or project?
3. Are backup, retention and quota documented?
4. Can restricted publisher and partner files be stored there legally?
5. Who controls credentials after personnel changes?

Track the remote address without secrets in `.dvc/config`. Store tokens, passwords and private keys only in `.dvc/config.local` or the user's credential system.

## Identifiers and provenance

- `source_id`: stable local ID for a publication, dataset, patent or report.
- `observation_id`: stable ID for one property value at one defined state.
- `system_id`: composition and phase system, independent of a particular measurement.
- `method_run_id`: one execution of an experimental, correlation, simulation or
  prediction method that produced an observation.
- `search_run_id`, `qc_run_id` and model-run identifiers: one traceable retrieval,
  review or modeling execution in the corresponding workflow.

Every derived artifact records input hashes, code commit, parameters, time in UTC, responsible agent, tool or model version, and output hash. Observation review uses `machine_extracted -> single_review -> double_review | adjudicated`. Invalid candidates remain in the extraction audit or quarantine area and are not promoted into a release; a corrected accepted observation can explicitly `supersede` an earlier one.

## Licensing and publication

- Record source license and redistribution status separately.
- A DOI does not grant permission to publish the full text or extracted tables.
- Public releases contain only records that pass a documented rights check.
- Restricted records may contribute to internal analysis only when the license permits it; public artifacts can retain citation-level metadata without copied content.
- Partner documents default to confidential until the owner confirms otherwise.
- No project-wide software or data license has been selected yet. Choose them before the first public release.

## Quality and release

Release candidates must pass schema validation, unit checks, duplicate grouping, range checks, referential integrity and a manual audit sample. Release versions use semantic tags such as `data-v0.1.0`. Each public snapshot should include a data dictionary, changelog, citation metadata, license statement and RO-Crate metadata.

## Retention and recovery

- Raw data are immutable; corrections create a new derived record.
- Keep at least two durable copies of released data and code.
- Cluster scratch is disposable and never the only copy.
- Store checksums for every source and release artifact.
- Document recovery tests at least once per release cycle.
