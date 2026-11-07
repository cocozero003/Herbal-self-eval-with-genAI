# ThaiHerb Knowledge Graph — Paper 2 Current Release

**Release:** Paper 2 Source-Reviewed 20-Seed Reanalysis v0.4  
**Date:** 2026-11-07  
**Scientific status:** AI-assisted, single-curator source review and reproducible exploratory reanalysis, **not** original 35-class Chem/Core replication or independently adjudicated biological validation.

## Canonical release locations

- [Google Drive v0.4 folder](https://drive.google.com/drive/folders/1HzlXnfWErLA2oX1jLKgg9yWPRxiebl6m)
- [Full research ZIP](https://drive.google.com/file/d/1BRDPN-RgEi7sdKmWzkvQxhry7BkQ6XET/view?usp=drivesdk)
- [Public-code ZIP](https://drive.google.com/file/d/1fnxEg_MjU7iitTg8sDbMarXVH1cJBCOR/view?usp=drivesdk)
- [Word research report](https://docs.google.com/document/d/1XqgwAoHkyhyIFWZe_6bvOcnC8AZQxgis/edit?usp=drivesdk)
- [Offline evidence dashboard](https://drive.google.com/file/d/1LfZtHMLhS2wY_ki8WWxiPVv3MtpMqM3y/view?usp=drivesdk)
- [GitHub source code branch](https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p2-source-reviewed-v0.4-20261107/thaiherb_kg/paper2_source_review_v0_4)

## Version highlights

- Official formula-table audit of 100 added-herb cells (H11–H20 × F01–F10), including printed-page locators.
- Formula F09: three previously omitted botanical-species memberships restored (H11, H15, H17), 71 → 74 total memberships.
- Species-level and medicinal-material distinctions documented for *Terminalia chebula* fruit/gall and *Myristica fragrans* seed/aril.
- NPMI scores changed for 37/190 herb pairs; 82 positive-NPMI edges remain.
- 9 models × 20 seeds × 190 pairs = 34,200 embedding similarity scores; Python tests 16/16 passed.
- Mean seed-rank rho: Cooc-NPMI 0.968781, Chem-Exact 0.757706, Core-Exact50 0.692690.
- Corrected-dataset internal LOFO baseline, six eligible of ten folds; no external biological evaluation.

## Scientific provenance and open gates

The source review was performed with AI assistance and is **not independent botanical/pharmacognosy adjudication**. The inherited chemistry panel is V3-derived, and the originally reported 35 chemical classes have not been recovered. **Chem-Exact** uses only exact-compound H–C–H paths, not original class-mediated H–C–K–C–H walks. Original experimental results must not be overwritten or described as exactly replicated. Full source material verification, independent external corpus, and genuinely independent expert labels remain open research gates.

## Integrity

- Full research ZIP SHA-256: `da43125ae2707a4d10e1dac9f5ffd9e002e032f125cf7dd318fec84d76570a87`
- Public code ZIP SHA-256: `ea1bbc062557faea20005306dccc3eeef913bb860075c64b4199b8de84a055e1`
- Version v0.3 remains archived separately; GitHub main is unchanged.

## How to reproduce

Download the **full research ZIP** to obtain the controlled inputs, extract all files, create a clean Python environment, install the pinned requirements, then run `python run.py` from the project root and `python -m pytest -q tests`. The GitHub public code folder intentionally excludes the research input data. Checksums and source-review flags are included in the full ZIP.
