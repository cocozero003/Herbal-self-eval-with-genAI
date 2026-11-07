# ThaiHerb Paper 1 — LOFO Validation & Expert Benchmark v0.7

**Status:** Internal held-out formula benchmark **completed**, independent external evidence/expert benchmark **not completed**.

This release extends v0.6 with leak-controlled formula holdouts; it does not supersede the original Paper 1 manuscript's published-report values or prove biomedical similarity.

## Run

```bash
python -m pip install -r requirements.txt
python run_v07.py
```

The full research ZIP includes the existing source-reviewed ten-formula snapshot and candidate chemistry proxy. The public GitHub subfolder includes code and a data access readme, not a copy of the full data and copyrighted materials. The program generates (1) 9 eligible LOFO folds, (2) nine benchmark methods, (3) mean AP/AUROC/P@5 and clustered bootstrap CIs, (4) leakage-oracle and label-permutation controls, (5) 45 pairs scored by no one yet in *two genuinely blank, model-blinded forms*, and (6) a standalone HTML dashboard.

## Key results

- PairSupport mean AP **0.419**; Cooc-NPMI **0.395**; Core-Proxy **0.292**; Chem-Proxy **0.275**.
- Inclusion of held-out labels in the **invalid leakage oracle** raises PairSupport AP to **0.543**.
- One of ten folds (F02) fails full 45-pair evaluation because H07 has no co-occurrence observations after holding out its sole formula.
- Candidate taxonomy, original vectors, expert gold and external source independence remain **unverified**.
- Non-cooccurrence in one formula is never used as a biological negative label.

## Files

- `src/validate_heldout_formulas.py`: deterministic formula holdout and baseline/model comparison
- `src/prepare_expert_review.py`: genuinely blank reviewer forms in independently shuffled order
- `src/evaluate_expert_labels.py`: guarded scorer for future filled review records
- `src/create_dashboard.py`: offline visualization
- `results/`: fold summaries, scores, permutation, leakage demonstration, blank gold forms and manifests
- `dashboard/Paper1_Validation_v0.7.html`: browser dashboard
- `docs/PAPER1_V07_RESEARCH_REPORT_TH.md`: manuscript-aligned research report in Thai
- `docs/EXPERT_REVIEW_SOP_TH.md`: blinded review protocol
- `docs/MANUSCRIPT_ADDENDUM_EN.md`: optional supplementary Methods/Results/Limitations in English
- `tests/`: data-leakage and research-integrity tests

## Reproducibility and caution

- Source data are from v0.6 (not recovered byte-identical original Paper 1 training archive).
- All leave-one-formula-out labels are derived from the same official formula collection.
- The fold-cluster bootstrap uses only nine clusters; uncertainty bounds are exploratory.
- Expert labels are intentionally blank; ChatGPT has **not** acted as two human expert reviewers.
- Do not report these numbers as evidence of efficacy, pharmacological mechanism or generalizable external model superiority.
