# ThaiHerb KG v0.2 — source-only GitHub staging branch

**Status:** An isolated staging branch in an existing herbal-related repository. This is **not** the official ThaiHerb project repository and was not merged into `main`.

## Install data locally

The code in `thaiherb_kg/` is uploaded to GitHub; source-derived scientific data and full test output stay in Google Drive pending source-license checks.

1. Download [ThaiHerb KG Methods Upgrade v0.2 ZIP](https://drive.google.com/file/d/16Ovt_hBIgjyCr-lCSI__LK4LmGJbf8Yx/view) from the project Drive.
2. Extract it, preserving its `data/` directory and the other paths.
3. Use the extracted package to run `python run_all.py` and `python -m pytest -q tests`. The GitHub copy can be diffed against that frozen release.
4. If running the GitHub source directly, copy the ZIP's `data/` directory to `thaiherb_kg/data/` before executing `python run_all.py`.

## Scope and limitations

- Paper 1: 10 herbs, 23 positive-NPMI edges, leave-one-formula-out **edge-rank** ablation.
- Paper 2: 20 herbs, 82 positive-NPMI edges; compound-ID Jaccard and IDF-weighted Jaccard.
- Paper 3: 208 assertion records, 201 prototype RDF assertion records, 4 contradiction review candidates and blank independent benchmark templates.
- 8 local Python tests passed in the packaged environment. This is not a GitHub Actions result.
- No original source-equivalence audit, expert gold-standard study, clinical validation, or full pySHACL confirmation has yet been completed.
- Source datasets should not be committed to this public branch until publication permissions and source-level verification are established.

**Google Drive paper folders**

- [Paper 1 upgrade](https://drive.google.com/drive/folders/14OjUl6lTTadQSiP9gLWa2N2j8ugvqH5T)
- [Paper 2 upgrade](https://drive.google.com/drive/folders/1llMXv_pYFKgQ5z2r7AVFMKIdGy92FdVq)
- [Paper 3 upgrade](https://drive.google.com/drive/folders/1n8MxQXm8OwtXlcGyTjpI_VrLes2It3u0)
