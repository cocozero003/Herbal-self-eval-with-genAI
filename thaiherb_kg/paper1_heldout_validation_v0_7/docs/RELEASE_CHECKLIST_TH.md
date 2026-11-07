# Release Checklist — Paper 1 v0.7

| Gate | สถานะ | หลักฐาน |
|---|---|---|
| Data input integrity | COMPLETE FOR v0.7 PROXY ONLY | `results/benchmark_manifest.json` with SHA-256 |
| Formula-level heldout separation | PASS | `results/fold_eligibility_10.csv` |
| Cold-start gating | PASS; F02 blocked | Fold eligibility and tests |
| 9 method comparators | COMPLETE | `results/model_comparison_cluster_bootstrap.csv` |
| Pairwise predictions | COMPLETE | `results/heldout_pair_predictions.csv` |
| Bootstrap, sign-flip, label-permutation | EXPLORATORY COMPLETE | Results + method note |
| Invalid leakage-oracle demonstration | COMPLETE | `results/label_leakage_demonstration.csv` |
| Two model-blind reviewer forms | BLANK FOR REAL USERS | R1/R2 review CSVs |
| Independent reviewers / actual ratings | **NOT COMPLETED** | `results/expert_evaluation_gate.json` |
| External source-disjoint corpus | **NOT COMPLETED** | Not supplied |
| Original Paper 1 chemistry class table and vectors | **NOT RECOVERED** | Earlier v0.6 limitations |
| Automated Python tests | PASS (11/11) | `tests/test_validation_v07.py` |
| HTML interaction QA desktop/mobile | PASS | `qa_dashboard.py` and QA screenshots (internal) |
| Manuscript supplement | WORKING DRAFT | `manuscript/Paper1_v0.7_Validation_Addendum.docx` |
| Publication ready | **NO** | Missing independent external validation and source signoff |

## Data deployment

Full project ZIP contains V3-derived research proxy inputs; do not automatically publish them in a public repository without data governance and license clearance. GitHub should contain code, empty templates, and documentation, and refer authorized users to the full ZIP in project Google Drive.
