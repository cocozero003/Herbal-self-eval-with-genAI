# ThaiHerb Knowledge Graph — Paper 1 Current Release

**Verified on:** 2026-11-07  
**Current controlled release:** Publication Finalization / computational reanalysis **v0.8**  
**Status:** Author-review manuscript and internally reproducible V3-derived feasibility reanalysis; **not confirmed ready for journal submission**.

## Google Drive — research deliverables

- [Paper 1 v0.8 research folder](https://drive.google.com/drive/folders/11ZhI1j3fpmYS9KixG5E_1pw03pqC5fIe)
- [Full research package ZIP](https://drive.google.com/file/d/1HZYlxuI36gbg2d5E_jzanedT3LXJ2sLd/view?usp=drivesdk)
- [Public source code ZIP](https://drive.google.com/file/d/1gASNPanShaRipkSziqVe9emhoD_D1Zus/view?usp=drivesdk)
- [Main manuscript (DOCX)](https://docs.google.com/document/d/12B73v_SNQlF8UBnnzt7oT7xGPtE_xCiE/edit?usp=drivesdk&ouid=108336010316871284918&rtpof=true&sd=true)
- [Main manuscript (PDF)](https://drive.google.com/file/d/1-tQNM0vVywrmRyGfl7TW83kQ0QuXq-Qj/view?usp=drivesdk)
- [Supplementary Methods and Results (DOCX)](https://docs.google.com/document/d/1yiqbDpPT3gY_cwv3IdPkLBFQzkMwxXZd/edit?usp=drivesdk&ouid=108336010316871284918&rtpof=true&sd=true)
- [Research dashboard](https://drive.google.com/file/d/1Wjq-BPaDEmZ2HXy8tJVGbOGOmBf_9J-Q/view?usp=drivesdk)
- [Publication readiness gates](https://drive.google.com/file/d/1pxBCLkrQjIo_fCqAgXR8uqMdo7TRKh3d/view?usp=drivesdk)

## GitHub — public code only

- Repository: [Herbal-self-eval-with-genAI](https://github.com/cocozero003/Herbal-self-eval-with-genAI)
- Controlled branch: `thaiherb-p1-publication-finalization-v0.8-20261107`
- [Paper 1 source folder](https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p1-publication-finalization-v0.8-20261107/thaiherb_kg/paper1_publication_finalization_v0_8)
- The branch is intentionally separate from `main`; the project-specific release does **not** imply a main-branch merge.

## Manifest / checksums

- Full research ZIP SHA-256: `b564bf958d216c0d1bb85bb11650d1ed16390d232d8a67b7cad672eac88a2c48`
- Public code ZIP SHA-256: `0d871851df3f3aa99ce5c6cafeddc16bfd5051300d1a327f4727576ebefa04f1`
- Full ZIP integrity: verified; 53 entries.
- Technical checks reported for v0.8: 10/10 automated tests; 13 variants x 10 seeds = 130 model fits; 45 herb pairs x 130 = 5,850 scores.
- Source data and source papers have **not** undergone independent human expert adjudication.

## Scientific decision boundary

1. **Supported:** A source-separated Cooc/Chem/Core graph embedding pipeline is computationally feasible on the defined fixed ten-herb pilot. It was rerun using a locked V3-derived proxy dataset.
2. **Not supported:** The candidate 19-class chemistry mapping is the original unavailable Paper 1 mapping, or the v0.8 results exactly replicate the historical manuscript's model vectors/metrics.
3. **Not supported:** Therapeutic equivalence, safety/efficacy, general biological similarity or external predictive superiority.
4. **Remaining gates:** Author/coauthor signoff, primary full-text claim-to-source adjudication where incomplete, original taxonomy reconciliation or formal acceptance of the new reconstructed analysis, and final target-journal requirements.
5. **Do not overwrite** Paper 1 v0.3–v0.7; they are historical experimental and audit snapshots. v0.3's erroneous F05 three-edge deletion was corrected in later work.

## How to reproduce

Download the **full** research ZIP from Google Drive, extract it retaining paths and the controlled research data, install the versions in `requirements.txt`, then run `python run_v08.py`. The GitHub folder alone does not include the restricted inputs.

This document is a release locator and status record. It does not replace the scientific manuscript, source files, or author approval.
