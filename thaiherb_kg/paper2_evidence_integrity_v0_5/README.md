# ThaiHerb Paper 2 v0.5 — evidence-integrity audit

Source baseline: immutable v0.4, 20 herbs, 10 formula projections, 74 formula memberships, 100 archived chemistry assertions, 83 internal compound IDs.

Status: **AUDIT-ONLY**. The 100 chemistry claims are catalogued for source-specific review and remain **NOT_VERIFIED** unless exact plant-part, compound, method and source locator are independently established. Original 35-class map not recovered. Candidate external monographs are not an external gold set. No independent biology-gold performance claim.

Artifacts created and tested locally:
- P2_CHEM_EVIDENCE_100.csv
- P2_COMPOUND_CANONICAL_MAP.csv
- P2_171_TO_174_CROSSWALK.csv
- P2_MATERIAL_CONTEXT_CROSSWALK.csv
- P2_EXTERNAL_CORPUS_CANDIDATES.csv
- SHA256_MANIFEST.json, RELEASE_GATES.csv, offline HTML and ZIP.

QA: 36/36 SHA-256 entries in prior v0.4, v0.4 regression 16/16, new P2/P3 test batch 17/17. SHA test only confirms local archive byte identity, not chemical truth.

The full local release ZIP and combined reproducibility package were generated; upload to the target Drive folder is not yet verified. See the delivered downloadable ZIP for the actual dataset and generator. Do not describe this code-only branch as an archive of the chemistry evidence table.

Run `python src/verify_release.py /path/to/extracted/Paper2_Evidence_Integrity_v0.5_2026-11-07`.
