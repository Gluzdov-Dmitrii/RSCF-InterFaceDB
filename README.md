# RSCF InterFaceDB

Research infrastructure for a reproducible database of liquid surface and interfacial properties, physics-aware machine learning, and a focused application to multi-walled carbon nanotube (MWCNT, МУНТ) formulations for drilling and oilfield fluids.

## Research objective

The project will connect liquid composition, phase identity, mineral surface, environmental conditions, measurement or calculation method, uncertainty, and provenance. The resulting database must support three uses:

1. comparison and validation of experimental, MD, QM and continuum results;
2. out-of-domain prediction and inverse design of liquid formulations;
3. mechanistic testing of MWCNT dispersion, interfacial adsorption and drilling-fluid performance.

The immediate plan is in [planning/weeks/2026-W37.md](planning/weeks/2026-W37.md).
The [research program](docs/project_charter/research_program.md),
[hypothesis register](docs/hypotheses/hypothesis_register.md),
[initial evidence landscape](literature/synthesis/landscape_2026-09-05.md) and
[MWCNT program](docs/mwcnt/mwcnt_program.md) define the proposed publication logic.
The repeatable lab-assistant assignment is in
[prompts/literature_search/weekly_literature_laboratory_ru.md](prompts/literature_search/weekly_literature_laboratory_ru.md).

## Repository map

| Path | Purpose | Git policy |
| --- | --- | --- |
| `literature/` | search protocols, screening, evidence extraction and synthesis | metadata and text tables in Git; full texts outside Git |
| `data/` | external, raw, interim, processed and curated datasets | schemas and tiny fixtures in Git; datasets via DVC later |
| `database/` | relational schema, migrations, views and data dictionary | Git |
| `src/interface_db/` | retrieval, extraction, normalization, validation, ML and simulation helpers | Git |
| `docs/` | research charter, methods, hypotheses, decisions and resources | Git |
| `prompts/` and `agents/` | controlled prompts, roles and work templates | Git |
| `manuscripts/` | source text, bibliography and figures for two papers | source in Git; generated binaries outside Git |
| `workflows/` | local, container and HPC workflow definitions | Git; run outputs outside Git |
| `simulations/` and `models/` | reproducible inputs, model definitions and run contracts | definitions in Git; heavy outputs outside Git |
| `reports/`, `planning/` and `notebooks/` | decisions, weekly execution and exploration | lightweight sources in Git |
| `configs/` and `metadata/` | non-secret defaults and release metadata | Git; machine-local values outside Git |

The pre-existing folders with application texts and partner materials remain local and are ignored. Their detailed audit and hash inventories are under ignored `private/`. Do not move, publish or redistribute them until their access status is reviewed.

## First commands

```powershell
# Create a local environment and install the package plus QA tools.
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"

# Run the lightweight test suite with the selected Python environment.
.venv\Scripts\python.exe -m pytest

# Build a private, hash-based inventory of local source files.
.venv\Scripts\python.exe -m interface_db.provenance.source_manifest `
  "Тексты заявки РНФ" private/application_manifest.local.csv `
  --all-files

# Search Crossref and save a reproducible run outside Git by default.
.venv\Scripts\python.exe -m interface_db.retrieval.crossref_search `
  "interfacial tension brine oil molecular dynamics" `
  --rows 20 `
  --output-dir literature/searches/runs/crossref_demo
```

Repeat the private manifest command for the MWCNT source directory. Use
`PYTHONPATH=src` if the package has not been installed in editable mode.

## Data-management decision

Git stores code, schemas, prompts, plans, bibliographic metadata and small verified examples. Large or restricted source files, datasets, trajectories, models and generated documents stay out of Git. DVC will be initialized only after a durable remote is selected; credentials must remain local. See [docs/data_management_plan.md](docs/data_management_plan.md).

## Status

This is the project scaffold and week-zero research design. Scientific claims and candidate journal quartiles remain provisional until the documented scoping review and current journal metrics are checked. No open-source or data license has yet been selected.
