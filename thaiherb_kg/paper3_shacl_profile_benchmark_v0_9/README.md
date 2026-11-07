# ThaiHerb Knowledge Graph | Paper 2 v1.1 & Paper 3 v0.9

Date: 2026-11-07. Author-review / reproducible research-engineering release.

## Achievements

- Kept frozen Paper 2 chemical 100 assertions and Paper 3 V3 208 assertions.
- Screened 20 original source document types and assigned 100 **conservative** claim-specific grades: 5 original primary full-text, 15 primary abstracts (including 5 hydrolysis-dependent), 19 review-level mentions, 61 unresolved locators. Source metadata is not an independent clinical gold.
- Established two Kew-verified botanical synonym crosswalks (H12/H19) and quantified preservation of taxon, material and processing context.
- Executed a local subset evaluator of the **actual SHACL shape graph**: 0 violations for the original M3 graph and 7/7 seeded negative controls detected. **Full SHACL Core via pySHACL NOT RUN** because unavailable.
- Built a fail-closed paired blinded benchmark harness for 32 proposed competency questions x 3 model outputs. No expert answers available, therefore no confirmatory model accuracy claimed. Synthetic unit test labels remain inside tests only.
- Added offline interactive evidence dashboard with search, filters and CSV export.

## Run

```bash
python -m src.original_source_screen_v11
python -m src.shacl_profile_check_v09
python -m src.blind_benchmark_v09
python -m src.build_dashboard_v11
python -m pytest -q tests
```

To perform *genuine* SHACL Core in an environment that has the dependency:

```bash
python -m pip install 'pyshacl>=0.31,<0.41'
python -m src.validate_shacl_v08
```

The local subset implementation is **not a full SHACL Core validator**; it supports only the constraints used by this project and does not replace pySHACL.

## Key files

- `results/P2_ORIGINAL_SOURCE_TRACE_100_v11.csv`
- `results/P2_SOURCE_TYPE_AUDIT_20_v11.csv`
- `results/P2_TAXON_SYNONYM_2_v11.csv`
- `results/P2_V11_AUDIT_SUMMARY.json`
- `results/P3_V09_SHACL_SUBSET_REPORT.ttl`
- `results/P3_V09_SHACL_PROFILE_STATUS.json`
- `results/P3_V09_NEGATIVE_CONTROLS_7.csv`
- `results/P3_V09_BLINDED_SCORING_TEMPLATE_96.csv`
- `results/P3_V09_BENCHMARK_GATE_REPORT.json`
- `dashboard/ThaiHerb_SourceAndValidation_v11_v09.html`
- `docs/P2_V11_METHODS_RESULTS_APA7.md`
- `docs/P3_V09_SHACL_BENCHMARK_METHODS_APA7.md`
- `docs/EXPERT_REVIEW_SOP_V09_TH.md`

## Validation status

Technical checks and reproducibility are in scope. Human adjudicated gold, complete original full-text verification of chemistry, complete SHACL Core conformance, original 35-class taxonomy, clinically accurate response testing, and independent external generalizability are **not** complete; do not present this package as a final scientific validation.
