## Paper 3 v0.4 source-parity milestone

Same frozen V3 **208** source assertions projected to **M1=207 RDF triples**, **M2=1501 triples**, **M3=2733 triples**. M1 collapses contextual distinction for CLIN005/CLIN006; this is not a QA accuracy benchmark.

[Complete versioned ZIP on Google Drive](https://drive.google.com/file/d/14xLYZO7SD2rzJVXOnMgd_1pLr5imYIsI/view)

[Interactive M1/M2/M3 explorer](https://drive.google.com/file/d/1yYbrCUStcoRoA8IUGVyNDx3OQqvtyA-o/view)

```bash
python run_p3.py
python -m pip install 'pyshacl>=0.31,<0.41'
python src/validate_shacl.py
```

Important: pySHACL did not run in the authoring environment; four custom structural controls are not SHACL Core conformance. No human expert gold and no M1/M2/M3 accuracy result. Full runnable code is in the ZIP.

# Thai Herbal Knowledge Graph — Evidence Gate and Controlled Projection Release

**Release date:** 2026-11-07  
**Paper 2:** v0.6 chemical source-verification pilot (continuation of frozen v0.5).  
**Paper 3:** v0.4 M1/M2/M3 controlled projection development (continuation of frozen v0.3).  
**Status:** DEVELOPMENT / NOT MANUSCRIPT-READY.

## What has actually been done

- The immutable input extracts are `data/P2_CHEM_EVIDENCE_100_v05_LOCKED.csv`, `data/P2_SOURCE_REGISTRY_v05_LOCKED.csv`, and `data/P3_V3_208_LOCKED.csv`.
- Five *Piper retrofractum* chemical occurrence assertions (CA006–CA010) were checked individually against Luca et al. (2021), Section 3.1, Table 3, final species column. This is an AI-assisted single-curator source audit **not independent expert adjudication**.
- No other chemical occurrence assertion was promoted to `PRIMARY_FULLTEXT_MATCH`; **95 remain NOT_VERIFIED**. Original 83 canonical compound structures and 35-class mapping remain unverified.
- The frozen **208** Paper 3 V3 assertions were projected identically to M1 naive SPO, M2 provenance-aware assertion nodes, and M3 evidence-qualified assertion nodes. M3 retains **text** qualifiers and does not yet normalize material, dose, or assay entities.
- M1 contains **207 distinct SPO triples**, because CLIN005 and CLIN006 share the same SPO but have distinct sources and study contexts. M2 and M3 each preserve all 208 assertion nodes.
- A development-only render table contains 624 rows (208 per model). This is NOT an independently benchmarked question-answer evaluation.
- Four custom structural negative-control checks passed. `pyshacl` could not be installed in this runtime, so actual SHACL Core status is **NOT_RUN_DEPENDENCY_UNAVAILABLE**.

## Run on Windows

1. Install Python 3.11–3.13 and make sure Python is on PATH.
2. `python -m pip install -r requirements.txt`
3. `python build_all.py`
4. `python -m pytest -q tests`
5. Install `pyshacl`: `python -m pip install "pyshacl>=0.31,<0.41"` (internet or a local wheelhouse required).
6. `python src/validate_shacl.py` runs actual SHACL Core and four negative controls when installed.
7. Open `dashboard/Paper2_ClaimAudit_v0.6.html` or `dashboard/Paper3_M1M2M3_v0.4.html` offline.

`run_windows.bat` automates these tasks. SHACL will exit with code 2 if its dependency is absent; do not treat this as passing validation.

## Unresolved scientific gates

- 95/100 compound-level claims not verified against exact source tables/pages; available 5 are source/claim checks, not human adjudication.
- Original 35 chemical classes cannot be reproduced with the available archive.
- Cross-source external corpus and two blinded experts are unavailable.
- 67 vs 45 Paper 3 full source-registry reconciliation and original 5,148-RDF triple recreation are unresolved.
- Clinical canonical object IDs (7 rows) and chemistry source locators require audit.
- No actual comparative study answers or accuracy, recall, citation precision, p-values or confidence intervals are reported.
- M3 context contains unnormalized source text and cannot be considered complete material/assay ontology.

## Source and integrity documents

Read `docs/P2_PRIMARY_EVIDENCE_REVIEW_TH.md`, `docs/P3_METHODS_UPGRADE_EN.md`, `docs/RELEASE_GATES.csv`, and `SHA256_MANIFEST.json`.

**Do not append corrected P2 74 formula assertions to the original P3 V3 208 rows and call them the same release.** Versioned reconciliation is required.