# Hypothesis register

Status values: `lead`, `supporting`, `high_risk`, `rejected`, `needs_prior_art`.

| ID | Testable hypothesis | Primary test | Success criterion for continuation | Status | Paper |
| --- | --- | --- | --- | --- | --- |
| H1 | Method, purity, provenance and reported uncertainty improve prediction calibration on later or unseen systems compared with a measurement-blind dataset. | Same model family with and without metadata; temporal and system-disjoint tests. | Lower error with better 90/95% interval coverage without wider trivial intervals. | lead | 1 |
| H2 | A learned residual over a physical baseline transfers to unseen chemical families better than end-to-end QSPR at the same training size. | Corresponding-states, PC-SAFT/DGT or COSMO-RS baseline plus delta model versus direct model. | Consistent improvement on family-disjoint test and no degradation on in-domain test. | lead | 1 |
| H3 | Uncertainty-guided selection of new MD or experimental points reduces OOD error per added point faster than random gap filling. | Simulated or prospective active-learning loop. | Better learning curve over at least three acquisition rounds. | supporting | 1 |
| H4 | Joint prediction of tension with density, viscosity or vaporization descriptors improves low-data-family accuracy. | Multitask versus single-task ablation with family holdout. | Improvement survives bootstrap uncertainty and leakage audit. | needs_prior_art | 1 |
| H5 | Hansen/COSMO descriptors, dynamic tension and viscosity predict MWCNT dispersion stability better than total surface tension alone. | Fixed-energy dispersion experiment and nested model comparison. | Out-of-sample improvement for sedimentation or centrifugation yield and zeta-potential class. | lead | 2 |
| H6 | Intermediate MWCNT wettability or functionalization maximizes interfacial coverage and emulsion stability; very hydrophilic and very hydrophobic states perform worse. | Functionalization gradient with contact angle, IFT, droplet size and interface imaging. | Reproducible nonlinear optimum with matched size and processing controls. | lead | 2 |
| H7 | Dynamic IFT, interfacial coverage and dispersion stability mediate HPHT filtration, lubricity and rheological stability better than MWCNT mass concentration alone. | Causal or mediation model with held-out formulations. | Mediator model improves predictive performance and coefficients remain stable under sensitivity analysis. | lead | 2 |
| H8 | Apparent MWCNT/SWCNT performance differences shrink after normalizing dose by accessible surface area and aspect ratio. | Matched formulation and processing comparison. | Surface-area-normalized model explains outcomes better than mass-only model. | supporting | 2 |
| H9 | Ionic-liquid or ionic-surfactant descriptors from ILThermo/COSMO can identify stabilizers for saline MWCNT dispersions. | Small high-risk screen against conventional nonionic or anionic dispersants. | At least one candidate remains stable after thermal and salinity aging without unacceptable rheology. | high_risk | 2 |

## Priority decision for the first week

The first paper should test H1 and H2. The second paper should be designed around H5-H7. H9 remains a reserve route, not the default experimental program. H3 determines where cluster calculations add information rather than simply increasing dataset size.

## Falsification questions

Before promoting a hypothesis, the review must answer:

- Has the same claim already been demonstrated with the same property domain and split design?
- Can a simpler confounder, such as method, laboratory, concentration range or duplicate publication, explain the result?
- Is the endpoint measurable with available equipment and realistic uncertainty?
- Would a negative result still create a useful dataset or scientific conclusion?
- Does the claim support the application objectives and one of the two paper stories?
