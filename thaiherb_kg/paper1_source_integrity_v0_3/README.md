# ThaiHerb Paper 1 — Primary Source Integrity Audit v0.3

**Audit date:** 2026-11-07  
**Scope:** Ten-herb pilot formula projection, Cooc sensitivity, chemistry-input audit.  
**Scientific status:** **PARTIAL SOURCE REVIEW; NOT DATA-FROZEN; NOT A NEW PUBLISHED RESULT.**

## Why this release exists

The previous Paper 1 web/weighting packages reproduced the reported total of 46 herb–formula memberships and 23 positive-NPMI edges **from a later V3-derived projection**. Matching these totals is not proof that 46 inputs match the 2023 official source. This release checks a subset directly against the *DTAM / Thai FDA official Thai traditional formula compendium (B.E. 2566)* and tests the impact of a detected mismatch.

Official source: https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

## Verified review scope

- **10/10 formula labels/pages:** mapped against official table of contents; labels alone do not validate ingredient rows.
- **14/46 projected positive memberships:** row-level checked against displayed source ingredient tables for three formulas.
- **11/46 confirmed present** (F01=3, F04=6, F05=2).
- **3/46 source-contradicted**: F05 `ยาประสะว่านนางคำ` (powder, official printed page 161) has no ginger (`H01`), Java long pepper (`H02`), or black pepper (`H03`) in the complete stated ingredient list, but all three were included in the project projection. The table does contain plai (`H05`) and kaffir lime (`H10`).
- **32/46 still not checked** against original ingredient tables; not silently treated as confirmed.
- **30 chemistry relationships:** available only as later V3-selected subset; original Paper 1 chemical row identities, 19 compound classes, plant-part/analytical context and original full trained vectors remain unresolved.

Other important metadata issue: formula F03 printed in the official TOC as `ยาไฟประสะกัลป์`, while the source body and manuscript use `ยาไฟประลัยกัลป์`. The name should be handled as a source-text spelling variant and not automatically merged without a controlled alias registry.

## Scientific impact (this is a partial correction only)

| Parameter | Old proxy | F05-only partial correction |
|---|---:|---:|
| Formula memberships | 46 | 43 |
| Positive NPMI pairs | 23 | 24 |
| NPMI pair scores changed | — | 24 / 45 |
| Spearman correlation of NPMI pair rankings | 1.0 | 0.9056 |
| NPMI top-five pair overlap | 5 | 3 |

Paired-seed Cooc Word2Vec experiments (60 walks/herb, max 20 nodes, 32-d skip-gram, window 5, negative 5, 15 epochs, 10 seeds) further demonstrate sensitivity to formula corrections:

| Weighting | Original versus partial-correction embedding rank rho mean | Within-seed stability, old projection | Within-seed stability, partially corrected |
|---|---:|---:|---:|
| Original positive NPMI | 0.7675 | 0.9322 | 0.8838 |
| NPMI + support shrinkage | 0.7977 | 0.9557 | 0.8944 |
| NPMI + degree adjustment | 0.8008 | 0.9566 | 0.8810 |
| Combined | 0.8056 | 0.9623 | 0.8704 |

**This does not establish biological validity, superiority of weighting algorithms, or reproducibility of the originally archived manuscript embeddings.** The original Paper 1 manuscript reported Cooc seed-rank rho=0.946, but its original walk corpus and full output vectors are unavailable. The implemented Cooc walk sampler is a documented reimplementation, not byte-for-byte reproduction.

## Reproducible workflow

On Windows PowerShell or Unix:

```bash
python -m pip install -r requirements.txt
python src/audit_paper1.py --data data/paper1_bootstrap_v3_proxy.json --out results
python src/embedding_sensitivity.py --data data/paper1_bootstrap_v3_proxy.json --out results
python -m pytest -q tests
```

Audit script alone needs only the Python standard library; embeddings require NumPy, SciPy and Gensim. Word2Vec is deterministic here given the same single-worker environment but numbers may differ across Python/Gensim versions.

## Outputs

- `results/formula_id_crosswalk.csv`: source formula IDs, titles, forms, printed pages and scope of review.
- `results/formula_membership_review.csv`: all 46 projected memberships, 11 confirmed, 3 contradicted, 32 pending.
- `results/source_contradicted_projection_rows.csv`: three source-contradicted assertions.
- `results/paper1_partial_source_correction.json`: an explicitly labelled **partial scenario**, not a clean gold dataset.
- `results/npmi_original_vs_partially_corrected_45pairs.csv`: exact pair effects.
- `results/weighting_effect_of_source_correction.csv`: ranking sensitivity of four weighted graphs.
- `results/embedding_pair_seed_sensitivity.csv`, `results/embedding_sensitivity_summary.csv`: matched-seed computational sensitivity.
- `results/chemistry_30_source_gaps.csv`: chemistry audit queue.
- `results/audit_summary.json`, `results/embedding_environment.json`: machine-readable run audit.
- `docs/NEXT_GATES_TH.md`, `docs/MANUSCRIPT_IMPLICATIONS_TH.md`: scientific requirements and manuscript impact.

## Data boundaries

- The official PDF is **not bundled**, because retrieving its bytes from the current runtime did not succeed; the official public URL and page labels are supplied for repeat verification.
- The archived manuscript is included as a local audit reference only; do not upload it to a public GitHub repository without explicit rights review.
- A later V3 data proxy is bundled to reproduce this analysis. **Its contents are not certified as the original ten-herb pilot input.**
- GitHub should contain code, methods, review summaries and tests; preserve research snapshots and manuscript files in the authorized Google Drive research folder until publication/licensing is settled.

## Critical publication gate

**Do not freeze the Paper 1 corpus** until every selected formula version is checked across all focal herbs (including absent memberships), 30 original chemistry records and 19 class assignments are restored and primary-source locators are independently verified, and the complete Cooc/Chem/Core pipeline is rerun with recorded environment versions and independent expert or source-holdout validation.
