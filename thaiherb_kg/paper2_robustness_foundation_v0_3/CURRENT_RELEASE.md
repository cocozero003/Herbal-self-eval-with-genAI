# ThaiHerb Paper 2 — Current Release (v0.3)

**Verified:** 2026-11-07  
**State:** INTERNAL SOURCE-INTEGRITY & BASELINE ROBUSTNESS STARTED / COMPLETED FOR v0.3  
**Do not confuse with:** original 20-herb manuscript embedding results or Paper 1 v0.8.

## Google Drive

- Paper 2 v0.3 folder: https://drive.google.com/drive/folders/1gIS1U36D7q8fbfSgD-kTO0OYS11peq5E
- Full research ZIP: https://drive.google.com/file/d/1Oz9AZZar7ROJZPUZrdoXbrIUWX2wTvzA/view
- Public code only ZIP: https://drive.google.com/file/d/1TugKtYOUuygzh-wLc2ZGxzpS0MqwyLSf/view
- Interactive HTML and manuscript start report are stored in the same folder.

## GitHub

- Repository: https://github.com/cocozero003/Herbal-self-eval-with-genAI
- Controlled branch: `thaiherb-p2-robustness-foundation-v0.3-20261107`
- Paper 2 code: https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p2-robustness-foundation-v0.3-20261107/thaiherb_kg/paper2_robustness_foundation_v0_3
- `main` untouched. The branch contains source code and methods only; the full data snapshot is retained in authorized Drive.

## Release SHA-256

- Full research ZIP: `5e40ecf96e367d013ea488fb27fb49636964f2e6e284530a8f0801c24b93f1ec`
- Public code ZIP: `5befd8ca7eb4ffbbdecfda559ce2038148c994b24403c71ee5f033880531f947`

## Research inventory / results

- 20 herbs, 10 selected official formulas, 71 formula memberships, 100 herb–compound assertions, 83 distinct compounds.
- 190 herb-pairs and 82 positive-NPMI edges; 38/82 have support from only one formula.
- Chemistry source-holdout: 20/20 source removals leave one herb with no chemistry evidence; do not compute all-pair similarity in those conditions.
- 6/10 complete-coverage formula holdouts (4 cold starts).
- Baseline PairSupport Mean AP 0.253147, AUROC 0.728453 across six eligible within-corpus folds. **Not external biological validity.**
- Random chemistry 4-of-5 exact compound Jaccard panel pruning: mean rank rho 0.791694 over eight panels. **Not original Chem embedding.**
- Automated tests: 10/10 passed. Local DOCX rendered to one-page PNG and reviewed. Offline HTML JavaScript syntax passed.

## Key blockers / next v0.4 milestone

1. Independently verify added-herb F01–F10 formula rows for H11–H20 (all 100 cells).
2. Recover original 35 chemistry classes and complete original vectors, or explicitly design and lock a new reviewed taxonomy.
3. Develop full 20-seed Cooc/Chem/Core comparison without leakage, report source coverage failure and simple baseline comparators.
4. Obtain a genuinely external formula corpus and two independent human expert ratings; labels in v0.3 blinded sheets are empty.

**Paper 1 independent biological validation does NOT block Paper 2 startup.**
