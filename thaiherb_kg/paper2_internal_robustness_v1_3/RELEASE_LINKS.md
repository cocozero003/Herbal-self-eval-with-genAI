# Paper 2 v1.3 — 20-herb internal robustness experiment

**Version:** 2026-11-07. **Claim scope:** internal computational robustness of source-reviewed selected formula/co-occurrence data, NOT independently externally validated phytochemistry or biology.

## Verified full research package

- [Google Drive release folder](https://drive.google.com/drive/folders/17KMremKf0Iv9icZaWaxz127TQjl2BZ10)
- [Full versioned ZIP with original v0.4 frozen data, 20-seed results, new experiments, manuscript, figures and offline dashboard](https://drive.google.com/file/d/1CLSvyUsF_8GEDgRhtYlVLMAAD3PWdXmE/view)
- [Word results supplement](https://drive.google.com/file/d/1VjbVHJChuioU5-45xILWBgFA1BJRm6XU/view)
- [Interactive dashboard](https://drive.google.com/file/d/1OiC_dMHiP6zQDXXyFeRV1Qp1CKKC3eSv/view)
- [Actual clean ZIP rerun proof](https://drive.google.com/file/d/1kt0sKyWcf7LfTfSMHGLUY1kQLN7tAlRf/view)

ZIP SHA-256: `15c94317001f9b10d3788a51fa75daea1d7350e8e81ad9d7a3371ab8c76a61ef`. Google Drive file was downloaded back into the runtime; **87/87 inner manifest hashes match**, and the returned ZIP SHA-256 is identical.

## Actual results

- 20 herbs, 10 curated formula documents, 74 botanical species membership assertions; 100 fixed herb-chemical claims, 83 internal compound identifiers; 190 unordered pairs.
- Archived v0.4: nine configurations × 20 seeds = 180 fits and 34,200 similarity scores. Seed-11 Cooc replay maximum error: `4.99e-9`.
- New: nine paired perturbation comparisons × 20 seeds, ten LOFO folds, eight model baselines and embeddings, twenty source holdouts × five seeds, provisional 31-family sensitivity, and material counterfactual.
- **6 complete LOFO folds (190 pairs):** PositiveNPMI mean AP 0.301, PairSupport 0.291, Cooc-NPMI train-only 0.275, Core-Exact50 train-only 0.168, Chem-Exact 0.139. The binary label is held-out formula co-membership, not biological efficacy.
- **4 cold-start LOFO folds** score only 171 pairs each; missing-herb pairs are not imputed.
- 20 chemical source holdouts each block 19 of 190 pair scores; 90% coverage.
- Paired formula-cluster bootstrap: Core-Exact50 mean AP minus PairSupport = -0.123 (exploratory interval [-0.208, -0.050]; only six complete formula clusters).
- **Clean rerun:** All original source files, code, and outputs extracted from full ZIP and the analysis run again. Five principal result CSVs match byte-for-byte; 23/23 pytest checks and browser interaction smoke passed.

## Integrity constraints

The original 35-class chemical mapping was not recovered; a name-based 31-family sensitivity is not original replication. Only five of 100 archived chemistry claims have primary full-text confirmation. Eleven positive candidate observations from three DOI-distinct new papers were selected post hoc and lack negative labels and independent adjudicated gold. No external AUPRC/AUROC or biological generalizability is asserted. Source data are supplied in the authorized Drive ZIP rather than in this code-only GitHub branch.

### GitHub Actions

[Manual full replay workflow](https://github.com/cocozero003/Herbal-self-eval-with-genAI/blob/thaiherb-p2-internal-robustness-v1.3-20261107/.github/workflows/thaiherb_paper2_v13_replay.yml) verifies the immutable ZIP SHA-256 and runs all experiments if the user authorizes access to the specified Google Drive archive. **This GitHub Actions workflow has not been presented as executed**; the completed full rerun was performed inside ChatGPT using the verified ZIP.
