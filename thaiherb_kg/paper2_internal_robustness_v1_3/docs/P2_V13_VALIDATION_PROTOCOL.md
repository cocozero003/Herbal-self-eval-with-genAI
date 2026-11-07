# Paper 2 Internal Robustness Protocol and Generalizability Boundary

**Design version:** 2026-11-07. This report is a transparent analysis protocol documented with the outputs; it is **not** prospectively preregistered.

## Primary internal task

The fixed evaluation universe is 20 focal herbs and 190 unordered pairs. Ten selected official formula documents supply the documentary membership labels. For each fold, all formula-derived walks are fitted from nine formula documents. Herb pair labels in the held-out formula are used only for scoring. Chemical claims are independent of formula labels and remain fixed. Full 190-pair folds (six) are reported separately from cold-start partial 171-pair folds (four).

## Model comparison

Deterministic baselines: PairSupport, DegreeProduct, Positive NPMI, exact compound Jaccard, IDF compound Jaccard. Train-only models: Cooc-NPMI, Core-Exact50; formula-independent chemical embeddings: Chem-Exact. All embeddings use the original `input/v04/src/reanalyse.py` algorithm and 20 recorded seeds. No test labels are used for tuning and no hyperparameter search is conducted on these ten held-out formulas.

## Repeated seed stability and perturbations

The exact archived 9-configuration/20-seed scores are retained; a single seed from the archived Cooc-NPMI is directly replayed to verify byte-level numerical concordance to eight decimals. Nine paired perturbation variants include thresholding, formula removal, chemical deletion and Core mixture ratio changes. An additional exploratory 31-family hypothesis and botanical material counterfactual are kept separately.

## Outcomes and inference

Mean AP, AUROC and formula-cluster bootstrap 95% intervals are descriptive of documentary held-out co-membership in a small, selected dataset. Every fold contributes equal weight after averaging its model seeds. The paired difference to PairSupport resamples folds as paired clusters (4,000 draws). There are only six complete-case formula clusters; consequently intervals are weak and p-values are deliberately omitted. Seed replicates and 190 overlapping pairs are not treated as independent units.

## Chemical evidence and cold-start

The fixed chemical panel is five selected assertions per herb. Single-source-per-herb selection makes leave-one-source-out inherently a cold-start intervention: exact profile unavailable for one herb and 19 of 190 pairs not scored. This is a data-availability robustness measure, not an external validation. The 31 provisional chemical families do not equate to the historical unrecovered 35 classes.

## External generalizability stop gate

The 11 currently available DOI-disjoint primary analytical observations were post-hoc selected positives from three publications with different extraction and plant-part contexts. The corpus has no sampled negatives, independent experimental non-detection adjudication or prospective preregistration. Accordingly, no confirmatory external AUROC, AUPRC or biological accuracy is calculable. A future source-disjoint test must be locked before results, include matched material/preparation/protocol contexts, derive both positive and tested non-detection outcomes without confusing absence in archive with true negative, and be reviewed blind by at least two real experts.
