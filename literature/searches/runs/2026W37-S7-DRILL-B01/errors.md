# Errors and unresolved access — 2026W37-S7-DRILL-B01

## Search-method errors

- Crossref `query.bibliographic` and `query` **do not implement Boolean AND**. Reported totals (Q1 212565, Q2 98587, Q3 107631, Q7 624030) are **not** true subject hit counts. OpenAlex Q4 (`n = 93`) is the only defensible restricted count.
- OpenAlex Q5 (`n = 4368`) and Q6 (`n = 1831`) are too broad; title screening of those exports was used only to recover seed interface papers already on the DOI list.
- Scopus and Web of Science: **not used** (no institutional export in this session).
- Sci-Hub: **not used**. No paywalled PDF was stored.

## DOI / Crossref failures

| DOI | Issue | Resolution |
| --- | --- | --- |
| 10.22050/ijogst.2012.2775 | Crossref HTTP 404 | Publisher page [ijogst.put.ac.ir/article_2775.html](https://ijogst.put.ac.ir/article_2775.html) + OpenAlex |
| 10.22078/jpst.2016.662 | Crossref HTTP 404 | Publisher landing + OpenAlex |
| 10.30492/ijcce.2018.28219 | Crossref HTTP 404 | OpenAlex abstract only; authors not recovered from Crossref |

## High-value sources without usable abstract or full text in this run

Mark as **inaccessible_fulltext** / metadata-only; do not invent numbers:

- [10.1016/j.molliq.2024.125448](https://doi.org/10.1016/j.molliq.2024.125448) Lysakova et al. 2024 J. Mol. Liq. — Crossref/OpenAlex/Semantic Scholar returned **no abstract**. ScienceDirect fetch blocked (Cloudflare/406).
- [10.1016/j.colsurfa.2023.132434](https://doi.org/10.1016/j.colsurfa.2023.132434) Lysakova et al. 2023 — no abstract in APIs.
- [10.1007/s10853-024-09492-w](https://doi.org/10.1007/s10853-024-09492-w) Lysakova et al. 2024 J. Mater. Sci. — publisher/S2 elided abstract.
- [10.1016/j.jngse.2019.103082](https://doi.org/10.1016/j.jngse.2019.103082) Ma et al. plugging — no abstract.
- [10.1016/j.petrol.2019.106257](https://doi.org/10.1016/j.petrol.2019.106257) Hajiabadi et al. formation damage — no abstract.
- [10.1016/j.colsurfa.2018.07.058](https://doi.org/10.1016/j.colsurfa.2018.07.058), [10.1016/j.powtec.2018.10.016](https://doi.org/10.1016/j.powtec.2018.10.016) — no abstracts.
- [10.1016/j.colsurfa.2017.10.010](https://doi.org/10.1016/j.colsurfa.2017.10.010) Briggs/Crossley wettability Pickering — no abstract (seed H6).
- ACS/MDPI HTML sometimes returned bot interstitial; Energies 16(19) 6875 was recovered via web-search cached HTML.

## Ambiguities (do not convert)

- `ppb` in Ismail 2016, Ismail 2018 IOP, Aftab 2017, Okoro 2019: **not converted**. May be pounds per barrel.
- Ismail 2016 filtrate 4.5 ml: API vs HPHT **UNKNOWN**.
- Ismail 2016 cake 2/32 inch: converted to metres only as a derived field.
- Materials Science Forum abstract cake **10 inch** at 300 °F: physically implausible; possible unit error; **not extracted as a value**.
- Energies 2023 MWCNT BET clause “higher than 270 m2” missing `/g` in that sentence.
- Fazelabdolabadi 2014 vs Sedaghatzadeh 2016: same 16.67% filtrate reduction near 138 °C / 500 psi / 1 vol% — **possible duplicate campaign**.
- B01-E23 (0.025 wt.% SWCNT, ~45% viscosity): **secondary citation** inside Journal of Mining Institute HTML pointing at ColSurA 2023; not a primary locator on S03.
- Journal of Mining Institute 2025 (https://pmi.spmi.ru/pmi/article/view/16437): **no DOI found** in this run.
- Alssafar 2019 torque: **software**, not lubricity-tester CoF.
- Hybrid additives (CuO/MWCNT, ZnO/MWCNT, MWCNT+GNP, MWCNT/TiO2) must not be read as MWCNT-only effects.

## Q4 OpenAlex records not given a source_id

Several Q4 hits were off-topic (L-DOPA biosensor, SAE50 nano-lubricant, enclosure convection, photo-thermal nanofluid, fluororubber) and were excluded at title screen without a `B01-Sxx` row. They remain in `raw/Q4_openalex_mwcnt_drilling.json`.
