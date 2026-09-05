# Initial research landscape

Date: 2026-09-05

This is a rapid, evidence-backed map for planning. It is not a completed systematic review and should not be cited as proof of novelty.

## Main conclusion

Two simple claims are already weak: “we created a surface-tension database” and “MWCNT improves drilling-fluid rheology or filtration”. Stronger novelty comes from joining method- and phase-aware data, honest out-of-domain validation and a mechanistic MWCNT application.

The leading program is:

1. build a FAIR database that preserves property mode, both phases, method, uncertainty and provenance;
2. benchmark physics-guided prediction on unseen substances, systems, families and publication time;
3. use the database to choose liquid phase, surfactant and MWCNT functionalization by dispersion and interfacial descriptors, then test drilling outcomes.

## High-value data sources

| Source | Value | Main constraint |
| --- | --- | --- |
| [NIST ThermoML](https://www.nist.gov/mml/acmd/trc/thermoml) | machine-readable thermophysical records for pure substances and mixtures | not every record is critically evaluated; map property codes and licenses |
| [NIST ILThermo](https://www.nist.gov/mml/acmd/trc/ionic-liquids-database) | ionic-liquid pure, binary and ternary data with method, purity and uncertainty | best for a focused ionic-liquid branch, not the whole petroleum domain |
| [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry/fluid/) | reference curves for pure fluids | surface tension only along the saturation curve |
| [NOAA ADIOS](https://response.restoration.noaa.gov/adios-oil-database) and [JSON data](https://github.com/NOAA-ORR-ERD/noaa-oil-data) | petroleum assays, physical properties and some interfacial context | NOAA warns that record completeness varies and users must assess fitness |
| [DST-SurfDB](https://zenodo.org/records/21118257) | 979 dynamic-tension series for 233 surfactants, including surface age and method | direct 2026 competitor; examine license and retained-series bias |
| [IAPWS water reference](https://iapws.org/technical-guidance/release/Surf-H2O) | unit and correlation validation | water-vapor only |
| DDB, DIPPR and REFPROP | high-value reference or correlation baselines | licensed; do not assume redistribution rights |

Crossref provides open bibliographic metadata through its [REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/). Chemical identity should be reconciled with PubChem, InChI/InChIKey and, where useful, OPSIN. Metadata retrieval is separate from permission to copy full text.

## Data semantics that determine validity

- Liquid-vapor surface tension, liquid-liquid IFT and dynamic tension are different targets.
- Liquid-liquid IFT needs both phases and ideally both equilibrium phase compositions.
- Dynamic surfactant data need surface age, not just a concentration and one tension value.
- Contact angle needs static/advancing/receding mode, surrounding phases, surface preparation, roughness and history.
- Multiple points from one curve or paper must stay in the same ML split group.
- Experimental and computed values can coexist but require explicit evidence type and method fidelity.

## Modeling ladder

| Level | Methods | Role |
| --- | --- | --- |
| 0 | Eötvös/Guggenheim-Katayama, corresponding states, parachor and simple composition rules | non-negotiable baselines |
| 1 | RDKit descriptors or fingerprints with linear, GPR, CatBoost/XGBoost and mixture-aware models | scalable prediction and ablation |
| 2 | PC-SAFT or related EOS with DGT, COSMO-RS and classical DFT | physical baseline and residual learning |
| 3 | classical MD with pressure-tensor or test-area estimators | selected gaps, mechanisms and benchmark systems |
| 4 | DFT/AIMD or learned potentials | targeted force-field uncertainty, not bulk filling |
| 5 | CFD, LBM or pore-scale models | transfer of database uncertainty into engineering outputs |

[FeOs](https://github.com/feos-org/feos) is a practical open framework for EOS, classical DFT, surface tension and adsorption calculations. [openCOSMO-RS](https://www.tuhh.de/v8/softwares/opencosmo-rs) provides an open COSMO-RS and conformer pipeline. The closest supplied MD/ML precedent is [Kirch et al.](https://doi.org/10.1021/acsami.9b22189), which makes random-row accuracy an insufficient novelty claim.

The benchmark should compare random splits with component-, system-, family- and time-disjoint tests. A promising architecture is `prediction = physical baseline + learned residual` with calibrated uncertainty.

## MWCNT and drilling fluids

Prior work already reports MWCNT effects on water-based drilling-fluid rheology, torque and filtration, including [Ismail et al.](https://doi.org/10.1016/j.petrol.2016.01.036). A close 2024 competitor found that preparation method controls colloidal stability and that CNTs strongly influence rheology but may weakly influence filtration in a realistic water-based formulation: [Lysakova et al.](https://doi.org/10.1016/j.molliq.2024.125448).

The scientific bridge to InterFaceDB is stronger at the interface:

- nanotube dispersibility follows a multicomponent solvent-compatibility space rather than one surface-tension value: [Hansen-parameter study](https://doi.org/10.1021/nn900493u);
- MWCNT network thickness at an oil-water interface correlates with emulsion stability and changes with surfactant: [Langmuir study](https://doi.org/10.1021/acs.langmuir.5b03189);
- controlled functionalization produces a nonlinear relationship between MWCNT wettability, droplet size and emulsion type: [Pickering study](https://doi.org/10.1016/j.colsurfa.2017.10.010);
- MWCNT/silica hybrids provide supporting EOR evidence but should not substitute for drilling-fluid controls: [hybrid study](https://doi.org/10.1016/j.jssc.2016.10.017).

Non-public MWCNT materials were used only to identify questions for an internal audit. No partner-specific technical assertion is treated as public evidence here. A publishable experiment plan must be derived from open prior art and from protocols, rights and raw data that the owner has explicitly cleared.

In drilling literature, `ppb` can mean pounds per barrel rather than parts per billion. Always preserve the original term and resolve its basis before conversion.

## Prioritized gaps

1. Source-level rights and exact ThermoML/DST property mappings.
2. A gold set that measures extraction error by field, not only by record.
3. Duplicate and split-group rules for curves, repeated experiments and reused datasets.
4. External validation data for oil/brine IFT and mineral contact angle.
5. Method-aware uncertainty and physical-baseline residual learning.
6. MWCNT experiments that fix dispersion energy and characterize functionalization.
7. A mechanistic link from dynamic IFT and interfacial coverage to HPHT filtration, lubricity and formation damage.
8. Legal separation between public grant outputs and confidential partner data.

## Immediate recommendation

Spend the first week on taxonomy, rights, the extraction gold set, prior-art falsification and the MWCNT pilot definition. Do not start bulk AIMD or a large parameter sweep. The first cluster allocation should answer one ranked uncertainty that a cheaper model cannot resolve.
