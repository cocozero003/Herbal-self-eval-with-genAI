# Controlled input data for Paper 1 v0.7

This GitHub folder contains **source code and documentation only**. It does not include the ten-formula V3-derived research proxy, the original source PDF or any privately archived manuscripts. To rerun, download the complete authorized project ZIP from Google Drive:

https://drive.google.com/drive/folders/1xz1syi5K3B7vhnEqZdmaXbAablVRQZEF

The full ZIP contains these inputs:

- `data/paper1_bootstrap_v3_proxy.json`
- `data/formula_reviewed_snapshot.json`
- `data/CHEMICAL_IDENTITY_TAXONOMY_25.csv`
- `data/CHEMICAL_ASSERTION_EVIDENCE_REVIEW_30.csv`

Copy `data/` into this directory, install dependencies from `requirements.txt`, then run `python run_v07.py`. It generates outputs under `results/` and the standalone dashboard under `dashboard/`.

No independent human expert labels have been supplied. The blinded CSVs in the **Drive full ZIP** are empty by design. The 19 compound classes are a candidate reconstruction, not the recovered original Paper 1 taxonomy. Formula holdout tests whether two herbs occur in the heldout formula, not biological or clinical similarity. The special leaked oracle in the results is intentionally invalid and must never be used as a candidate model.
