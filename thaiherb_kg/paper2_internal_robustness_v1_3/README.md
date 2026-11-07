# ThaiHerb20 Paper 2 — Internal Robustness v1.3

**Release:** 2026-11-07  
**Status:** COMPLETED INTERNAL COMPUTATIONAL EXPERIMENTS / NOT INDEPENDENT BIOLOGICAL OR EXTERNAL VALIDATION.

This is a reproducible scientific research archive using the authorized Paper 2 v0.4 source-reviewed snapshot, with 20 herbs, 10 selected formulas, 74 species memberships, 100 fixed chemical assertions, and 83 distinct compound IDs. It includes the original v0.4 20-seed results (180 previously completed model fits) with SHA-256 verification and numerical replay, plus NEW perturbation, formula holdout, chemical source holdout, and provisional taxonomy sensitivity experiments.

## Quick start

```bash
python -m pip install -r requirements.txt
python src/run_robustness.py
python src/run_sensitivity_extensions.py
python src/paired_formula_bootstrap.py
python src/build_publication_assets.py
python src/build_manuscript.py
python -m pytest -q tests
```

Run `run_windows.bat` on Windows. All research input files are included under `input/` inside the **Drive FULL ZIP**; no web access or credentials are needed to reproduce these analysis results.

## Actual new experiments and limitations

- 9 perturbation configurations × 20 seeds = 180 new paired perturbation comparisons (including archived variant comparisons), with 34,200 variant score rows. **Some variants reuse archived fits; 180 comparisons ≠ 180 newly trained fits.**
- 10 leave-one-formula-out (LOFO) folds, 20 Word2Vec seeds for three embedding models, plus five deterministic baselines. **Train-only Cooc and Core** are freshly fit without the withheld formula. One chemical-only model uses the formula-independent archived embedding.
- Full coverage: six folds × 190 unordered herb pairs. Four cold-start folds exclude the 19 pairs involving the herb unseen in formula training, leaving 171 eligible pair scores per fold. No imputation of unseen-herb scores.
- Bootstrap AP and AUROC 95% intervals: 2,000 draws sampled by held-out formula, not by correlated pair or Word2Vec seed. Exploratory paired formula-cluster differences versus PairSupport use 4,000 draws; no confirmatory p-values.
- Leave-one-chemical-source-out: 20 held-out sources × five random seeds. Each source is unique to one herb with five selected chemical edges; removing it blocks 19 of 190 herb pairs (90% coverage).
- Provisional 31 name-based chemical families and a F08/H11 fruit-vs-gall material counterfactual are **explicitly exploratory, not original 35-class replication**.
- The external pilot has 11 positive-only records from three DOI-distinct primary sources, which were selected after development. No independent adjudicated gold or sampled negatives. **External accuracy, AUPRC and generalizability are NOT claimed**.

## What exactly was measured?

The target is **documentary pair co-membership** in the withheld formula; it is not a ground-truth biological, chemical synergy, clinical effectiveness, safety or efficacy label. Strong performance on this label is not direct evidence of medicinal similarity. The original source audit has only five of 100 claims primary full-text verified; the remaining are lower evidence tiers or unresolved, not biological negatives.

## Key files

- `results/P2_RUN_MANIFEST.json`: input hashes and versions
- `results/P2_ARCHIVED_SEED_REPEATABILITY_20SEEDS.csv`
- `results/P2_PERTURBATION_SUMMARY.csv` and `P2_PERTURBATION_ALL_PAIR_SCORES.csv`
- `results/P2_LOFO_MODEL_METRICS_ALL_10_FOLDS.csv` and `P2_LOFO_PREDICTIONS_ALL.csv`
- `results/P2_LOFO_COVERAGE.csv`, `P2_LOFO_SUMMARY_CLUSTER_BOOTSTRAP.csv`
- `results/P2_PAIRED_CLUSTER_BOOTSTRAP_VS_PAIRSUPPORT.csv`
- `results/P2_SOURCE_HOLDOUT_20_SOURCES_5SEEDS.csv`
- `results/P2_PROVISIONAL_CLASS_MATERIAL_SENSITIVITY_20SEEDS.csv`
- `results/P2_EXTERNAL_DOI_DEDUP_AND_ELIGIBILITY.csv`
- `results/P2_BLINDED_EXPERT_R1_190_UNFILLED.csv`, R2 and adjudication blank forms
- `dashboard/ThaiHerb_Paper2_Robustness_v13.html`
- `ThaiHerb_Paper2_v13_AUTHOR_REVIEW_RESULTS.docx`
- `docs/P2_V13_EXPERT_INTERPRETATION_TH.md`
- `docs/P2_V13_AUTHOR_REVIEW_MANUSCRIPT_EN.md`

## Scientific stop conditions

The original historical 83-to-35 class mapping is not in the accessible archive. A new 31-family grouping may only be used as a clearly marked hypothetical sensitivity analysis. No source-disjoint **confirmatory** external test or independent biological similarity labels were available. For a claim of externally validated robustness, acquire a prospectively frozen distinct dataset, define true negatives and non-detection separately, adjudicate material context, ensure no leakage, and perform blinded expert scoring before evaluating model outputs.
