# Paper 1 v0.8 — Reproducibility and Editorial Decision Record

Date: 2026-11-07. Reviewer: ChatGPT-assisted computational/editorial review (NOT independent specialist review).

## Scientific recommendation

**Feasibility claim: supported within a locked reconstruction.**  
**Exact replication of original manuscript: NOT SUPPORTED.**  
**External biological validation: NOT UNDERTAKEN.**  
**Submission readiness: CONDITIONALLY NOT APPROVED pending author signoff and original vs reconstructed study selection.**

The original manuscript presents results from a 10-herb, 10-formula, 30 chemistry-assertion, 19-class study and describes an archive not accessible in the currently shared project. Reanalysis v0.8 uses a V3-derived proxy and AI-assisted candidate class annotations and therefore **must be treated as a new reanalysis, not a replacement without editorial disclosure**.

## Original versus candidate reanalysis

| Analysis | Original | v0.8 reanalysis |
| --- | --- | --- |
| Cooc | 0.946 | 0.932159 |
| Chem | 0.977 | 0.90917 |
| Core | 0.945 | 0.739359 |
| Cooc-thr0p05 | 0.982 | 0.994466 |
| Cooc-thr0p15 | 0.963 | 0.977734 |
| Cooc-thr0p30 | 0.657 | 0.695652 |
| Chem-PruneFirst2 | 0.226 | 0.036495 |
| Core-Cooc25 | 0.969 | 0.947563 |
| Core-Cooc75 | 0.8 | 0.822793 |


## Locked method inventory

- 10 herbs, 10 selected documentary formulas, 46 present formula memberships, 100 reviewed cells.
- 30 phytochemical assertions, 25 compounds, 19 **candidate** chemical classes.
- 23 positive NPMI edges among 45 possible herb pairs.
- 13 model/perturbation configurations × 10 paired seeds = 130 fits.
- 32 dimensions, 60 walks per herb, skip-gram, window 5, negative samples 5, epochs 15, one worker.
- Perturbation metrics are descriptive; no independent herb-pair clinical or biological truth labels are supplied.
- Source checks are AI-assisted and contain material/part/cultivar limitations; original wet-lab statements are not validated by this analysis.

## Manuscript integration rules

1. Use **either** the archived original manuscript's results with proper reproducibility evidence **or** the newly regenerated v0.8 results as the main results; never interleave their numbers as if from the same run.
2. Treat v0.7 LOFO as supplementary task-specific evidence; PairSupport mean AP 0.419 exceeded Cooc 0.395 and Chem/Core 0.275/0.292, without implying failed feasibility.
3. Do not use v0.3's erroneous deletion of F05 memberships; the official ingredient table spans printed pages 161–162.
4. Do not describe candidate 19 chemical classes as the original 19.
5. Author review remains mandatory: chemical occurrence primary full-text, original class definitions, author declarations, journal instructions and research reporting policy.
6. Do not convert the blank expert-review sheets into machine-generated positive/negative gold labels.

## Research boundaries

- Not a proof of efficacy, clinical similarity, safety, substitution, or pharmacological equivalence.
- Source count is not evidence quality weight.
- Pairwise seed correlations are not 45 independent samples.
- Formula holdout is single-corpus document validation and is not an independent biological benchmark.
- No matching of original trained vectors is claimed.

## Stop-go gate

**Go** for internal author review of a self-consistent computational feasibility draft. **No-go** for claiming fully reproduced original paper or independent biological validity. The journal submission decision must be signed by actual authors after verifying botanical/chemical references.
