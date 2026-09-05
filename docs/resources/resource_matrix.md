# Resource matrix

All compute quantities are planning ranges. Refine them after the system count, molecular size, target precision and convergence protocol are fixed.

## People and responsibilities

| Role | Minimum contribution | Current decision needed |
| --- | --- | --- |
| Principal investigator | scope, hypothesis decisions, conflict resolution and publication narrative | reserve two review checkpoints per week |
| Literature/data curator | searches, deduplication, license checks and source metadata | assign named human owner |
| Lab-assistant models | discovery, first-pass screening and structured extraction | run only with versioned prompts and human QC |
| Interfacial scientist | measurement-method and uncertainty review | identify collaborator or advisor |
| MD/QM specialist | force-field choice, convergence and cluster runs | confirm availability before Gate E |
| Drilling-fluid experimentalist | DOE, HPHT methods and field relevance | confirm equipment and sample access |
| Data/ML engineer | pipeline, schema, baselines and OOD evaluation | can begin after schema freeze |

## Compute and storage

| Activity | Pilot need | Scale-up range | Notes |
| --- | --- | --- | --- |
| metadata and ETL | 8 cores, 32 GB RAM, 50 GB | 16-32 cores, 64 GB, 200 GB | PDF/full-text corpus stays outside Git |
| tree/QSPR models | CPU workstation | one 16-24 GB GPU for deep models | start with strong CPU baselines |
| PC-SAFT/DGT/FeOs | CPU workstation | hundreds to thousands of core-hours | low cost once parameters exist |
| COSMO conformers/profiles | tens of molecules | roughly 10,000-100,000 core-hours for hundreds with conformers | benchmark a small batch before allocation |
| classical MD | 3-5 systems and convergence tests | roughly 1,000-10,000 GPU-hours | use only to close ranked data gaps |
| DFT/AIMD | 1-3 reference configurations | tightly scoped allocation | not a bulk database filler |
| CFD or pore-scale | 2 validation cases | parameter sensitivity ensemble | needs uncertainty from the database |
| durable data storage | 200 GB | 1-5 TB plus backup | separate durable project area from scratch |

Potential open tools include Python, SQLite/DuckDB/PostgreSQL, Parquet, RDKit, scikit-learn, CatBoost/XGBoost, PyTorch, LAMMPS or GROMACS, PLUMED, Packmol, ASE, CP2K or Quantum ESPRESSO, [FeOs](https://github.com/feos-org/feos) and [openCOSMO-RS](https://www.tuhh.de/v8/softwares/opencosmo-rs). Existing Ansys Fluent expertise can support the continuum validation branch.

## Experimental capabilities for the MWCNT line

| Capability | Purpose | Priority |
| --- | --- | --- |
| pendant and spinning-drop tensiometry | equilibrium and low IFT | required |
| maximum-bubble-pressure or equivalent DST method | surface-age dependence | high |
| contact-angle goniometry with controlled surface preparation | mineral and shale wettability | required |
| zeta potential, DLS or complementary size method, UV-Vis | dispersion stability | required, with awareness of CNT measurement limits |
| calibrated sonication or high-shear mixing | reproducible dispersion energy | required |
| HPHT rheometer and aging cells | drilling-fluid rheology and thermal stability | required for Paper 2 |
| HPHT filter press and lubricity tester | filtration, cake and friction outcomes | required for Paper 2 |
| optical microscopy and SEM | droplets, cake and invasion morphology | high |
| Raman, XPS, TGA and BET | nanotube identity and functionalization | high; partner access acceptable |
| core or shale testing and CT | damage and invasion mechanism | stretch |

Dry CNT handling needs a written exposure-control procedure, closed preparation where possible, waste and spill rules, and local occupational-safety review. NIOSH CIB 65 is a useful conservative reference, but local requirements govern the work.

## Inputs that must be confirmed

- cluster scheduler, CPU/GPU types, quotas, scratch retention and permitted software;
- durable project storage and DVC-compatible access;
- access to full-text databases and commercial DDB/DIPPR/REFPROP licenses;
- actual MWCNT grades, purity, diameter/length, functionalization and batch availability;
- drilling-fluid base formulations, brines, oils, minerals or shale samples;
- available tensiometry, HPHT rheology, filtration, microscopy and surface-analysis equipment;
- partner confidentiality and publication restrictions;
- named human validators and weekly time budget.
