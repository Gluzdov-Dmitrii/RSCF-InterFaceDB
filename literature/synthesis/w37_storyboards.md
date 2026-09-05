# Storyboards (lab drafts, 2026-09-05)

PI owns journal choice and novelty wording. Lab drafts only.

## Paper 1 — one page

**Claim (allowed if H1/H2 hold):** Method-aware, phase-aware interfacial data plus a physical baseline with a learned residual beat measurement-blind QSPR on family- and time-disjoint tests.

**Must not claim:** “We built the first surface-tension database”; ThermoML and DST-SurfDB already exist.

**Evidence needed:** gold-set observations with locators; license map; leakage audit; FeOs or corresponding-states baseline; Kirch-style MD/ML only as IFT analogue, not as ST proof.

**Figures:** (1) taxonomy of ST vs IFT vs dynamic vs CA; (2) PRISMA-style source flow; (3) split comparison; (4) calibration plot.

**Missing:** 30 human-verified observations; DST-SurfDB schema mapping; ThermoML property-code map.

**Go/no-go for first calculation:** **No-go** for large MD. **Go** for a cheap corresponding-states / parachor baseline on a tiny public subset once gold-set QC passes.

## Paper 2 — one page

**Claim (allowed only if experiment exists):** Dispersion and interfacial state explain MWCNT drilling-fluid filtrate/lubricity/rheology better than mass concentration.

**Must not claim:** “MWCNT improves drilling fluids” (Ismail 2016, Okoro 2019 already).

**Evidence this week:** Okoro full text — non-monotonic OBM filtrate vs ppb (lbm/bbl); Briggs 2018 — wettability-tuned Pickering; Alvi abstract — functionalization at fixed mass; **no dynamic IFT on mud**.

**Minimum experiment:** Stage 0–1 in `docs/mwcnt/mwcnt_program.md`; nested models `y ~ mass` vs `y ~ mass + TSI/sedimentation + IFT`.

**Go/no-go:** **No-go** until Stage 0 (batch characterization, energy calibration, safety). EOR Pickering is mechanism only.

Candidate journals remain provisional as in `manuscripts/paper_02_mwcnt_drilling/README.md`.
