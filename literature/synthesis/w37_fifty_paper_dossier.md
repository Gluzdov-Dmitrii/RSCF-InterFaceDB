# Week 37 literature dossier (≥50 papers)

Operator: machine lab assistant. Status: `machine_extracted`. Date: 2026-09-05.

This is **not** a PI novelty decision. It is a screening-and-extraction dossier for InterFaceDB week 37.

## What was actually read

| Level | Meaning | Count (this dossier) |
| --- | --- | --- |
| `pdf_extracted_first_pages` | Local PDF, first ≤15 pages text-extracted | 8 named below |
| `oa_html` | Publisher/OA HTML | Energies 2023 (bot-blocked PDF; HTML used earlier) |
| `abstract` | Crossref/OpenAlex/publisher abstract only | majority |
| `metadata_only` | Title/DOI verified; no abstract body | Lysakova 2024 JML and several Elsevier |

**Local PDFs (gitignored):** `literature/fulltext/2026W37-ALL-LIT-B01/` and `.../2026W37-S7-DRILL-B01/`. Download yield: 19/72 Unpaywall+Sci-Hub on 2026-09-05; Sci-Hub retry then failed with SSL EOF. **Lysakova 2024 JML, Ismail 2016 JPSE, Briggs 2015 Langmuir were not obtained as PDF in this session.**

Full-text PDFs successfully extracted: Okoro 2019 JPEPT; Fazelabdolabadi 2014 Appl Nanosci; Briggs 2018 ColSurA (accepted manuscript); Ismail 2017 MJFAS; Alssafar 2019 IJCPE; Ismail 2018 IOP; Aftab 2017 EJPE (W37-P025); Hajiabadi 2019 JPSE (W37-P033); ThermoML IUPAC 2006 (W37-P001).

Screening table: `literature/screening/screening_w37.csv` (**55+** unique records across S1–S7). S7 batch `2026W37-S7-DRILL-B01` remains 43 unique.

Seven search protocols: `literature/searches/runs/2026W37-S{1-6}-*-B01/run.json` plus existing S7 `run.json`.

---

## 1. Short synthesis (all streams)

**S1.** ThermoML (IUPAC 2006, PDF W37-P001) is a schema for experimental/predicted thermophysical data, **not** a substitute for method-aware surface-tension observations. DST-SurfDB (Zenodo 10.5281/zenodo.21118257, CC BY) is the direct dynamic-tension competitor. Water ST MD (Alejandre 1995 abstract: SPC/E γ = 66.0±3.0 mN m⁻¹ at 328 K vs experiment 67) is a baseline, not a petroleum mixture database.

**S2.** Kirch et al. 2020 ([10.1021/acsami.9b22189](https://doi.org/10.1021/acsami.9b22189), **abstract**): MD+ML for oil/brine IFT; GB feature importance on oil attributes and salinity; LR error up to 2% vs MD and 9% vs literature experiment. **FACT from abstract:** they built an MD IFT set at room T,P. **UNKNOWN:** split design (random vs system-disjoint) until full text. Salager 1979 and Huh 1979 are foundational IFT/phase-behavior priors. Kamal 2017 surfactant-flooding review is discovery-only.

**S3.** Eastoe & Dalton 2000 is a mechanisms review for dynamic ST at air–water; DST-SurfDB supplies surface age. **No drilling-mud dynamic IFT with surface age** was found in S7 full texts read this week.

**S4.** Amott 1959, Anderson 1986, Morrow 1990, Hirasaki 1991 define wettability tests vs contact-angle modes. Iglauer 2014: CO2/water/mineral CA data have large uncertainty; CA alone insufficient for capillary pressure. RezaeiDoust 2009: carbonate vs sandstone smart-water mechanisms differ. InterFaceDB must keep static/advancing/receding and three-phase participants separate (ADR 0002).

**S5–S6.** FeOs (2023) is an open EOS/classical-DFT baseline. Kirch 2020 is the closest supplied MD+ML analogue: **random-row accuracy is not a novelty claim**. Lipid-bilayer and drug-discovery MD hits from OpenAlex S6 were **excluded** (`wrong_application`).

**S7 / H7.** Generic “MWCNT improves WBM rheology/filtrate/friction” is already shown. **H7 mediation (IFT/coverage/dispersion vs mass) is not demonstrated** in any full text read this week. Strongest full-text dose finding: Okoro et al. 2019, API RP 13B-1, **ppb = pounds per 350 mL lab barrel** (Table 2: 70.0 ppb barite). OBM HPHT: 0.5 ppb MWCNT → 15 ml filtrate; 2.5 ppb → 7 ml; 3 ppb → 6 ml (abstract + p.1 and later text). WBM API filtrate better than standard at equivalent MWCNT; cake 2 mm WBM / 1 mm OBM. **Non-monotonic OBM filtrate vs mass.** Briggs 2018 full text: amphiphilic MWNT → smallest droplets; hydrophobic → W/O; hydrophilic → O/W at equal oil/water; stability >1 month. That supports H6, not H7 drilling mediation.

---

## 2. Full-text facts (locators)

### Okoro et al. 2020 (online 2019) — [10.1007/s13202-019-0740-8](https://doi.org/10.1007/s13202-019-0740-8)

- **FACT.** Concentration range 0.5–3 ppb MWCNT; WBM tested on **API filter press**, OBM on **HPHT filter press** (API RP 13B-1). Locator: PDF p.2, “Experimental” / filter-press paragraph.
- **FACT.** Table 2 header: “equivalent to 1 barrel of WBM”; “Product conc. for 1 lab bbl (350 mls)” and barite **70.0 lbs** — **ppb here is oilfield pounds per barrel**, not parts per billion. Locator: Table 2, PDF p.2–3.
- **FACT.** OBM 0.5 ppb → 15 ml filter loss; 2.5 ppb → 7 ml (52% from initial); 3 ppb → 6 ml. Locator: Abstract and PDF discussion (~p.5, “6 mls (Fig. 6)”).
- **FACT.** Cake thickness 2 mm (WBM) and 1 mm (OBM) at reported conditions. Locator: Abstract.
- **UNKNOWN.** MWCNT OD/length/purity/BET; IFT; zeta; mixing energy in J; HPHT T,P numbers for OBM in the pages extracted (need remaining pages / Fig. 6).
- **H7.** Mass dose is a strong predictor of filtrate in this design; **no interfacial mediator**.

### Fazelabdolabadi et al. 2015 (online 2014) — [10.1007/s13204-014-0359-5](https://doi.org/10.1007/s13204-014-0359-5)

- **FACT.** Functionalized vs unfunctionalized MWCNT in water- and oil-based templates; SEM for dispersion. Locator: Abstract / PDF p.1.
- **FACT.** Thermal conductivity +23.2% (1 vol% f-CNT, WBM, ambient); +31.8% at 50 °C; OBM +40.3% / +43.1% at 1 vol%. Locator: Abstract.
- **FACT.** OBM filtration 138 °C, 500 psi, 16.67% filtrate reduction at 1 vol% CNT. Locator: Abstract.
- **Overlap:** Sedaghatzadeh JPST 2016 abstract reports the same 16.67% at 280 °F, 500 psi, 1 vol% — treat as **possible duplicate campaign** until tables compared.

### Briggs et al. 2018 ColSurA — [10.1016/j.colsurfa.2017.10.010](https://doi.org/10.1016/j.colsurfa.2017.10.010)

- **FACT (accepted manuscript PDF).** Droplet size vs wettability is **parabolic**: amphiphilic MWNTs → smallest droplets. Hydrophobic → W/O; hydrophilic → O/W at equal oil and water volumes. Locator: Abstract, PDF p.3.
- **FACT.** Emulsions stable >1 month. Locator: Abstract.
- **NOT drilling fluid.** Supports H6.

### Other extracted PDFs

- Ismail 2017 MJFAS [10.11113/mjfas.v12n3.423](https://doi.org/10.11113/mjfas.v12n3.423): Saraline/Sarapar; aging 250/350 °F, 16 h; 10-s gel +33% (Saraline, 250 °F); Sarapar filtrate −19% (abstract; PDF confirms aging protocol).
- Alssafar 2019 [10.31699/ijcpe.2019.3.6](https://doi.org/10.31699/ijcpe.2019.3.6): simulated BHA torque, not tester CoF; polymer mud torque increased.
- Ismail IOP 2018 [10.1088/1757-899X/380/1/012021](https://doi.org/10.1088/1757-899X/380/1/012021): MWCNT 0.01 ppb **and** GNP 0.02 ppb together → 38–59% torque lubricity reduction — **do not attribute to MWCNT alone**.
- Hajiabadi 2019 [10.1016/j.petrol.2019.106257](https://doi.org/10.1016/j.petrol.2019.106257): nano-modified invert emulsion, rheology **and** formation damage with tomography — **CNT identity and numbers require table extraction from remaining pages** (PDF saved as W37-P033).
- ThermoML IUPAC 2006 PDF: standard for capturing experimental/predicted/evaluated thermodynamic data in XML — **schema paper**, not a ST value set.

---

## 3. Abstract-only papers still counted in the 50+ (honest limits)

S7 includes/maybes without PDF: Lysakova 2024 JML, 2023 ColSurA, 2024 JMS; Ismail 2016 JPSE; Alvi 2018 OMAE; Ma 2020 plugging; Abraham 2025 SPE; Lin 2023 Nanomaterials; ACS Omega MWCNT/TiO2; etc. See `screening_w37.csv` and S7 `report.md`.

S1–S6 extras: Amott, Anderson, Morrow, Hirasaki, Iglauer, Alejandre, Dang & Chang, Kamal review, Salager, Kirch, FeOs, DST-SurfDB, Eastoe.

**INFERENCE.** OpenAlex S6 high-cite dump is contaminated by biology MD; future S6 queries must exclude membrane-protein terms.

---

## 4. H7 status after this pass

| Requirement in H7 | Status |
| --- | --- |
| Dynamic IFT + surface age on the same mud | **UNKNOWN / not found** |
| Interfacial coverage | Briggs-type papers only, not drilling |
| Dispersion metric (TSI vs sedimentation vs DLS separated) | Energies 2023 TSI (OA HTML); not co-registered with HPHT filtrate+lubricity in one table we could read |
| HPHT filtrate, lubricity, aged rheology | Present separately (Okoro, Ismail, Fazel) |
| Nested model vs mass-only | **Not reported** |
| `ppb` basis | **Resolved as lbm/bbl in Okoro Table 2**; still unconfirmed in Ismail 2016 until that PDF |

---

## 5. Still blocked (high value)

Sci-Hub SSL failures on retry; MDPI 403; Elsevier 406/Cloudflare:

- 10.1016/j.molliq.2024.125448
- 10.1016/j.petrol.2016.01.036
- 10.1021/acs.langmuir.5b03189
- 10.1016/j.colsurfa.2023.132434
- 10.1007/s10853-024-09492-w
- 10.3390/en16196875 (PDF; HTML used previously)

Campus proxy or a later Sci-Hub mirror is required. Do not invent those tables.
