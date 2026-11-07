## Paper 3 v0.6 (code-only)

Research full package in [Google Drive](https://drive.google.com/drive/folders/1W7dhLbHXcoYlOCljSeNqBVjf8T5IxEkl). Frozen protected inputs remain in the authorized Drive ZIP, not public GitHub. This release has no expert gold and no authentic pySHACL conformance result.

# ThaiHerb Knowledge Graph — Paper 2 v0.8 & Paper 3 v0.6

**Research release:** 7 November 2026 | DEVELOPMENT / AUTHOR REVIEW | NOT MANUSCRIPT-READY.

This is a controlled continuation of frozen P2 v0.7 and P3 v0.5. The historical original V3 (208 source assertions) remains unchanged; the corrected P2 formula cohort is maintained as a separate data version. See `docs/DATA_LINEAGE.md`.

## What is newly audited

### Paper 2: Evidence provenance and claim-level curation

The 20-herb frozen research panel contains **100 herb–compound occurrence assertions** with 83 internal compound identifiers and 20 cited source records. Classification of all 100 claims (NOT a biological validation):

| Status | Claims | Meaning |
|---|---:|---|
| `PRIMARY_FULLTEXT_MATCH` | 5 | Original experimental article's specific analytical table, Piper retrofractum |
| `PRIMARY_ABSTRACT_ONLY` | 5 | Original experimental abstract; plant/material methods not fully validated |
| `PRIMARY_ABSTRACT_AFTER_HYDROLYSIS` | 5 | After alkaline hydrolysis; **not** intact pod or formula occurrence |
| `SECONDARY_ABSTRACT_NAME_MATCH` | 9 | Name mentioned in review abstract, not original study confirmation |
| `SECONDARY_ONLY` | 10 | Identified in reviewed literature, secondary claims only |
| `NOT_VERIFIED` | 66 | Claim-specific source, material and/or method still require curation |

**Only 5/100 meet the audit's PRIMARY_FULLTEXT_MATCH criterion.** One independent curator with AI assistance did the review, not two independent experts. The historical original 35-class compound map is absent; reconstructed classes are non-equivalent candidates. A PMID, DOI, PubChem CID or title match alone never proves phytochemical occurrence. Exact source-design audit is in `results/P2_SOURCE_TYPE_AUDIT_20.csv` and audit reasons are in `results/P2_CHEM_EVIDENCE_100_v08.csv`.

### Paper 3: Frozen clinical/provenance and representation checks

The immutable historical V3 freeze is **208** assertions (71 formula, 100 chemistry, 30 pharmacology, 7 clinical), SHA-256 `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`. The selected M1/M2/M3 representations contain **207, 1501 and 2733** RDF triples respectively. M1 collapses the SPO pair CLIN005 and CLIN006; this shows representation loss, **not** lower question-answer accuracy, nor a clinically adjudicated contradiction.

There are 45 source IDs in this archived export versus 67 claimed in an older manuscript, with original registry scope unresolved; seven clinical object identifiers are missing and retained as source text; 100 chemistry locator issues are queued. Eight **development** questions and 24 deterministic model outputs exist, but no independent answer gold, actual reviewer scores, true QA accuracy or external generalization result.

### SHACL status

Real `pySHACL` was NOT executed (`NOT_RUN_DEPENDENCY_UNAVAILABLE`) because installation was blocked by environment package-index connectivity. Custom structural tests, synthetic graph fixtures and the included validator cannot substitute for genuine SHACL Core validation on the authentic M3 graph. To attempt in an environment where `pySHACL` is installed:

```bash
python -m pip install -r requirements.txt
python -m pip install 'pyshacl>=0.31,<0.41'
python src/validate_shacl.py
```

## Reproduce code and evaluate integrity

Python 3.11+; dependencies `rdflib`, `pytest`, and optional `pyshacl`. Run from the extracted ZIP root:

```bash
python -m pip install -r requirements.txt
python -m src.stage_v08
python -m src.dashboard_v08
python -m pytest -q tests
```

Windows alternative: `run_next_windows.bat` for the earlier code path, followed by the explicit new commands above. Test `34/34` from the previous stage plus **16 additional tests** (total 50/50), independently rerun after freeze when building this version.

## Reviewer deliverables

- `results/P2_CHEM_EVIDENCE_100_v08.csv`, `results/P2_OPEN_CLAIM_QUEUE_v08.csv`, `results/P2_SOURCE_TYPE_AUDIT_20.csv`
- `results/P3_CLINICAL_OBJECT_7_REMAINING.csv`, `results/P3_CHEMISTRY_LOCATOR_100_QUEUE.csv`, `results/P3_SOURCE_45_REGISTRY_SCOPE.csv`
- `results/P3_SPO_COLLISIONS.csv`, `results/P3_CQ_CANDIDATE_QUEUE.csv`, `results/P3_V06_RDF_QUERY_DIAGNOSTICS_24.csv`
- `dashboard/ThaiHerb_EvidenceIntegrity_v08_RDFv06.html` (offline, exploratory)
- `manuscript/ThaiHerb_P2v08_P3v06_AUTHOR_REVIEW.docx` (author-review working addendum, not a final manuscript)
- `docs/SCIENTIFIC_STATUS_REPORT_TH.md`, `docs/MANUSCRIPT_METHODS_RESULTS_ADDENDUM_EN.md`, `docs/EDITORIAL_OVERLAP_MATRIX.csv`
- `results/TEST_REPORT_V08_V06.json`, `SHA256_MANIFEST.json`, and `docs/RELEASE_GATES_V08_V06.csv`

## Open scientific gates (not misrepresented as complete)

1. Primary compound-specific full-text curation still outstanding for most of 100 claims; source disjointness and medicinal material identity unresolved.
2. Recover original 35 classes *or* declare a new evidence-curated non-equivalent taxonomy.
3. Independent external corpus and **two real blinded domain reviewers** with adjudicated gold needed for scientific generalization and answer-quality benchmarks.
4. Execute real SHACL Core and seeded negative controls on frozen M3, capture detailed RDF validation report.
5. Independently evaluate M1/M2/M3 on same eligible assertions with pre-registered primary endpoint, not synthetic success scores.

Official methodological standards: W3C PROV-O (2013) https://www.w3.org/TR/prov-o/ and W3C SHACL (2017) https://www.w3.org/TR/shacl/. Source-specific study citations are in `docs/MANUSCRIPT_METHODS_RESULTS_ADDENDUM_EN.md`.

**Release safety:** No prior archives or GitHub `main` modified. The GitHub public branch may omit rights-restricted full input data, which are included only in the authorized complete research ZIP kept on Drive. Do not infer clinical interchangeability, regulatory approval, safety or therapeutic efficacy from KG links, embeddings or graph validity tests.
