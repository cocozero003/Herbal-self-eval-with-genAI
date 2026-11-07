# ThaiHerb Paper 1 — v0.6 Evidence Qualification and Source-Independence Audit

Date: 2026-11-07  
Scientific status: **AI-assisted research review and reproducible exploratory source-deletion experiment; NOT independent expert review or original Paper 1 embedding replication.**

This release extends **v0.5** without modifying the original manuscript, code baseline or selected 30 herb–compound assertions. The official 10-formula projection remains 46 memberships and 23 positive-NPMI edges; the deprecated v0.3 three-edge deletion is explicitly invalid.

## What is actually new

- New 30-row literature qualification and context-caution ledger, preserving the previous provenance fields.
- 12 publicly retrievable additional study/monograph URLs identified as candidate corroboration for 23 of 30 assertions; some address species but not cultivar, and some address processed oil rather than unprocessed material.
- Independence audit: 8/10 focal herbs have just one original source ID in the selected chemistry ledger.
- Source holdout coverage gate: 8/12 original source deletions remove **all** chemical evidence for at least one focal herb and are blocked for full 45-pair ranking.
- Paired Chem/Core 10-seed sensitivity analysis for the **four remaining valid source holdouts**, totaling 80 paired model/seed comparisons.
- Offline HTML dashboard and manuscript-ready supplemental report, all labeled exploratory.

## Run

```bash
python -m pip install -r requirements.txt
python audit_v06/evidence_qualification.py
python audit_v06/source_holdout_embedding.py
python audit_v06/generate_dashboard.py
python -m pytest -q tests
```

Run from the project root. `results/19_class_candidate/embedding_cosine_45pairs_10seeds.csv` is the locked v0.5 exploratory baseline for paired comparison; `data/paper1_bootstrap_v3_proxy.json` is **not the original Paper 1 chemistry data archive**. No web access is needed to rerun. The additional URLs are literature review metadata, not downloaded source full texts.

## Scientific guardrails

- Source citation counts are not edge truth scores, pharmacological effectiveness weights, or independent gold labels.
- PubChem identifies chemical structures, not presence in a particular plant or plant part.
- Original Paper 1 class taxonomy (19 published classes), model vectors, and training walks are not recovered.
- New 19-class candidate taxonomy is post-hoc and does not match the original merely because the class count is 19.
- Claims backed by abstracts/reviews are not the same as primary full-text row-level evidence verification.
- No independent humans have reviewed the 45 blinded herb-pair labels (template remains blank).

## Main files

| Path | Contents |
|---|---|
| `audit_v06/evidence_qualification.py` | Deterministic review ledger + original source stress test |
| `audit_v06/source_holdout_embedding.py` | Coverage-gated paired Chem/Core exploratory reruns |
| `audit_v06/generate_dashboard.py` | Standalone offline HTML builder |
| `results/v06/` | CSVs and machine-readable study manifests |
| `dashboard/Paper1_Source_Independence_v0.6.html` | Interactive evidence explorer |
| `docs/PAPER1_V06_RESEARCH_REPORT_TH.md` | Detailed research interpretation with references |
| `docs/MANUSCRIPT_INTEGRATION_NOTES_v06.md` | Suggested non-destructive manuscript edits |
| `manuscript/Paper1_v0.6_Evidence_Qualification_Addendum.docx` | Research addendum for manuscript handoff |
| `tests/test_v06_quality.py` | Scientific integrity checks |

Drive location: `Paper 1 - ThaiHerb10 Feasibility / Evidence_Qualification_v0.6_2026-11-07`.
