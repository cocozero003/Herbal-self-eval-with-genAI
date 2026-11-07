# ThaiHerb Paper 2 — Source-Reviewed Robustness v0.4

**2026-11-07 — internal reproducible research package.** Not original Paper 2 replication, not biological validation.

## What's new from v0.3

- An AI-assisted, single-curator audit of all 100 H11–H20 × F01–F10 cells against complete official ingredient tables with printed-page locators.
- Three source-verified F09 memberships restored: H11, H15, H17. Species-level formula total: 71 → **74**; V3 raw data preserved.
- Special handling of species-versus-medicinal material, especially *Terminalia chebula* gall vs fruit and *Myristica fragrans* aril vs seed.
- New **class-free** Cooc, Chem-Exact (H–C–H), Core-Exact 20-seed reanalysis; 9 configurations × 20 seeds = 180 model fits.
- Before/after NPMI audit, 190-pair mean embeddings, six perturbation comparisons, and LOFO structural baselines.
- No artificial recovery of the original 35 chemical classes, no fabricated independent expert scores.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run.py
```

Data required under `data/` in **the authorized full ZIP**: `paper2_bootstrap_v3_proxy.json`, `paper1_formula_reviewed_snapshot.json`. The script regenerates `paper2_source_reviewed_species_v04.json`, result CSVs and integrity tests. Public GitHub contains code and documentation, not these research data archives.

## Main outputs

- `results/NEW_HERBS_SOURCE_REVIEW_100.csv`
- `results/FORMULA_MEMBERSHIP_CORRECTIONS.csv`
- `results/SOURCE_REVIEW_FORMULA_ASSERTIONS_74.csv`
- `results/ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv` (34,200 rows)
- `results/SEED_REPEATABILITY_20SEEDS.csv`
- `results/BEFORE_AFTER_NPMI_190.csv`
- `results/SOURCE_CORRECTION_IMPACT.json`
- `results/RELEASE_MANIFEST.json`
- `dashboard/Paper2_SourceReview_v0.4.html`
- `manuscript/PAPER2_V04_METHODS_RESULTS_ADDENDUM_EN.md`
- `docs/PAPER2_V04_SOURCE_REVIEW_REPORT_TH.md`

## Research boundary

- Original 35 classes and archived original model vectors are NOT available; Chem-Exact and Core-Exact are different algorithms with different information channels from original Chem/Core.
- No independent external formula set and no expert biological similarity gold labels.
- Do not use v0.3's 71-membership data and v0.4's 74-membership metrics in a single figure without explicitly labeling cohorts.
- The species projection is NOT a preparation/part-specific ingredient graph. Special-material notes require expert review.
- Official source: https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf
