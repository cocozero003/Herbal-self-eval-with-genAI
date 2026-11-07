# Paper 2 v0.4 — Data dictionary

- `data/paper2_bootstrap_v3_proxy.json`: archived V3-derived historical 71-member baseline; do not edit.
- `data/paper1_formula_reviewed_snapshot.json`: legacy H01–H10 curator-reviewed formula crosswalk.
- `data/paper2_source_reviewed_species_v04.json`: source-checked 74-member species-level snapshot; 174 assertions (74 formula, 100 chemistry). Not proof of equivalence at medicinal-part level.
- `results/NEW_HERBS_SOURCE_REVIEW_100.csv`: 100 H11–H20 cells, official printed-page and PDF-page locators.
- `results/SOURCE_REVIEW_MATRIX_200.csv`: combined inherited 100 cells and newly reviewed 100 cells.
- `results/FORMULA_MEMBERSHIP_CORRECTIONS.csv`: 3 restorations in F09: H11, H15, H17.
- `results/SOURCE_REVIEW_FORMULA_ASSERTIONS_74.csv`: rebuilt formula claims, all marked AI-assisted single-curator.
- `results/BEFORE_AFTER_NPMI_190.csv`: graph-correction impact (190 pairs, plus illustrative part-sensitive H11-F08 variant).
- `results/ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv`: 34,200 new cosine scores, 9 variants x 20 seeds x 190 pairs.
- `results/SEED_REPEATABILITY_20SEEDS.csv`: 20-seed pairwise rank stability, descriptive (190 correlated seed pairs per model).
- `results/MEAN_PAIR_SIMILARITIES.csv`: 9 methods x 190 mean pair similarities.
- `results/PERTURBATION_COMPARISON_20SEEDS.csv`: six perturbation comparisons, not statistical proof of biological validity.
- `results/LOFO_COVERAGE_10.csv`: internal leave-one-formula-out 10 folds, 6 with complete coverage.
- `results/LOFO_STRUCTURAL_BASELINES.csv`: test-document co-occurrence baseline AP/AUROC, not biological truth.
- `results/SOURCE_CORRECTION_IMPACT.json`: source reconciliation metrics.
- `results/RELEASE_MANIFEST.json`: input SHA hashes, software versions and scientific limits.
- `dashboard/Paper2_SourceReview_v0.4.html`: standalone offline browser with tabs, filtering and tabular results.
- `manuscript/Paper2_SourceReviewed_Robustness_v0.4.docx`: technical research report, not full journal-ready paper.

The original 35 compound-class taxonomy does not exist in the accessible project; do not replace it with a guessed ontology.
