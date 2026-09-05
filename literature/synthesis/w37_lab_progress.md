# Week 37 lab progress vs Sunday gates

Date: 2026-09-05. Operator: machine lab. This does **not** close PI-owned items.

| Gate | Required | Lab status |
| --- | --- | --- |
| Formal application audit | Signed agreement, publication counters | **Blocked.** `docs/compliance/application_obligations.md` already states agreement is not in repo. PI-owned. |
| ADR 0002 / vocabulary | Approve or correct | **Draft exists** (`docs/decisions/0002_property_taxonomy.md` v0.2 proposed). Lab did not change it. PI-owned. |
| Seven search streams | Saved protocols | **Done.** S1–S6 `run.json` + S7 `2026W37-S7-DRILL-B01/run.json`. OpenAlex counts: S1 3269, S2 14920, S3 1292, S4 19846, S5 647, S6 16107 (exported 50 each). S7 Q4 n=93. |
| Screen ≥50 unique; ≥20 MWCNT | | **Done for unique count.** `screening_w37.csv` has 55+ rows; S7 alone 43 unique with ≥20 MWCNT/drilling/interface. |
| License map ≥25 | | **Done at metadata level.** `source_manifest.csv` already 27 SRC rows; this week adds OA tags in S7 `sources.csv` and dossier. |
| 30 human-checked observations | | **Not done.** All extractions remain `machine_extracted`. Gold-set human QC is **blocked** until a human reviewer. |
| Gap map + H1–H9 scores | | **Lab draft:** `w37_hypothesis_scorecard.md` + dossier. Not PI-approved. |
| Two + two/three lead hypotheses | | **Lab suggestion only:** Paper1 H1/H2; Paper2 H6/H7 (+H5). PI-owned. |
| Resource matrix | | File exists `docs/resources/resource_matrix.md`. No new cluster numbers invented. |
| Storyboards + go/no-go | | Drafts in `manuscripts/paper_01_interfacedb/` and `paper_02_mwcnt_drilling/` if present; see `w37_storyboards.md`. **No-go** for large MD/DFT. **Conditional go** for cheapest distinguishing mud screen **after** Stage 0 governance. |

## Downloads

- Attempted 72 DOIs: 19 PDFs via Unpaywall or Sci-Hub (local only, gitignored).
- Sci-Hub retry (20 priority): **0/20** (SSL EOF). Lysakova 2024 and Ismail 2016 still closed.
- Do not treat Sci-Hub as reliable this session.

## Honest deficit

The 50-paper **dossier** mixes full-text and abstract analysis. Human gold-set of 30 observations and PI novelty workshop are still open. That is why Sunday “release v0.1” cannot be claimed complete by the lab alone.
