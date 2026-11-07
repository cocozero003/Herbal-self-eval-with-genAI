# ThaiHerb Paper 2 — Robustness Foundation v0.3

**Scientific status: SOURCE-INTEGRITY AND INTERNAL BASELINE BENCHMARK COMPLETE ON V3-DERIVED PROXY. The original Paper 2 35-class chemistry table and original 20-seed 190-pair vectors are NOT recovered.**

## Scope and why Paper 1 is not a blocker

Paper 1 demonstrated computational feasibility. Paper 2 investigates whether that representation is robust to a larger selected herb panel, formula/source removal, chemistry panel pruning, and independent benchmark design. It can start without expert confirmation of Paper 1's biological similarity, but no new claim of biological generalizability follows from these internal tests.

- Dataset: 20 herbs, 10 selected official formulas, 71 formula membership assertions, 100 compound occurrence assertions, 83 compound IDs, and 190 herb dyads.
- Formula-derived positive NPMI edges: 82.
- Ten legacy herb formula projections match Paper 1's single-curator source audit. The new ten herbs' formula members are not independently verified.
- All 20 source-held-out chemistry conditions isolate at least one herb because the original selected chemistry panel has only one source ID per herb.
- LOFO full-190-pair evaluation: 6 eligible folds, 4 cold-start folds. Held-out labels are documentary formula-cooccurrence labels, **not biological negative/positive gold**.
- 5 simple baselines include formula PairSupport, DegreeProduct, PositiveNPMI, exact-compound Jaccard and IDF Jaccard.
- 8 randomized 4-of-5 chemical panel deletions; exact compound similarities only, **no invented 35 chemical classes**.
- Two blinded forms for 190 pairs with **empty labels**; reviewer independence cannot be manufactured by AI.

## Run

```bash
python -m pip install -r requirements.txt
python src/paper2_foundation.py
python src/make_release.py
python -m pytest -q tests
```

For a local Windows machine, the same commands work under PowerShell. Open `dashboard/Paper2_Robustness_v0.3.html` offline.

## Output files

- `results/formula_herb_200_matrix.csv` and `results/formula_id_crosswalk_10.csv`: provenance and review status.
- `results/cooc_pair_weights_190.csv`: support and NPMI on all pairs.
- `results/exact_compound_pairs_190.csv`: exact molecular labels only (not inferred structures/classes).
- `results/lofo_graph_sensitivity_20rows.csv`: leave-one-formula-out graph-rank sensitivity.
- `results/lofo_baseline_metrics.csv` and `results/lofo_baseline_summary.csv`: task-specific internal comparisons.
- `results/leave_one_source_out_20.csv`: full chemical-coverage source fragility.
- `results/exact_chemistry_panel_pruning_8.csv`: chemistry-panel sensitivity.
- `results/BLINDED_EXPERT_*.csv`: blank score-blinded templates for **independent humans**.
- `docs/PAPER2_V03_RESEARCH_REPORT_TH.md`: detailed interpretation and next-stage gates.
- `manuscript/Paper2_Research_Starting_Report_v0.3.docx`: author-review summary, not a submission-ready paper.
- `dashboard/Paper2_Robustness_v0.3.html`: single-file offline dashboard.

## Data sharing and attribution

The complete dataset snapshot is held in the authorized project Google Drive archive. Only analysis scripts, tests, methods and README should be pushed to a public GitHub branch until the original dataset distribution rights and original citations are checked.

The formula source is the official DTAM/Thai FDA B.E. 2566 compendium. The study-design warning about leakage follows Brière et al. (2026), *Bioinformatics*, 42(8), btag608, https://doi.org/10.1093/bioinformatics/btag608.

## Critical warning

The reported Paper 2 manuscript results (Cooc 0.973, Chem 0.842, Core 0.902, 35 compound classes) are historical manuscript assertions and **not** newly verified in this v0.3 pipeline. Do not copy them into new results tables and call them reproduced. Current results are not independent external validation.
