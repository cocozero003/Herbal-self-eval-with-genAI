# ThaiHerb KG Research Engineering Release

**Paper 2 v1.0: Independent Claim Corroboration**; **Paper 3 v0.8: Structural Representation Fidelity**  
Date: 7 November 2026 | Author-review working release, not completed scientific validation.

## Research facts

- The same 100 original herb–compound assertions are frozen; only 5 have primary full-text original-source matches.
- Five new corroborations from a primary chemical-analysis study of commercial *Coriandrum sativum* fruit essential oil. Four additional claims from prior stage: **9 distinct original claims with independent-source corroborations**. The original citation dispositions remain unchanged.
- Five *Plumbago indica* claims have explicit context-warning queues (original paper introduction vs directly measured Table 1).
- Original Paper 3 V3 has 208 assertions (71 formula, 100 chemistry, 30 pharmacology-target, 7 clinical).
- RDF M1, M2, M3 retain 207, 1,501 and 2,733 triples. Deterministic source/qualifier retention examined across 624 model-assertion pairs. **No question-answer accuracy claimed.**
- SHACL Core **NOT RUN** on this machine because the package index was unreachable. **No independent expert gold available.**

## Reproduce

With Python 3.11+, from the extracted project directory:

```bash
python -m pip install -r requirements.txt
python -m src.stage_v10
python -m src.build_dashboard_v10
python -m pytest -q tests
```

For actual standards-compliant SHACL Core when dependency installation is available:

```bash
python -m pip install "pyshacl>=0.31,<0.41"
python -m src.validate_shacl_v08
```

Do not mistake RDFLib integrity tests for an authentic SHACL Core execution. The validator outputs `NOT_RUN` if pySHACL is unavailable.

## Key outputs

Data freeze: `data/P3_V3_208_LOCKED.csv`, `results/P2_CHEM_EVIDENCE_100_v09.csv`.

Evidence: `results/P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv`, `results/P2_ALL_CLAIMS_AUDIT_LEDGER_100_v10.csv`, `results/P2_SOURCE_CONTEXT_WARNINGS_PLUMBAGO_5_v10.csv`.

KG diagnostics: `results/P3_RDF_ASSERTION_RETENTION_624_v08.csv`, `results/P3_RDF_CAPABILITY_SUMMARY_v08.csv`, `results/P3_SPO_COLLISION_GROUPS_v08.csv`.

Review: `results/P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv`.

Exploration: `dashboard/ThaiHerb_EvidenceAndRepresentation_v10_v08.html` (offline interactive HTML, no network calls).

See `CURRENT_RELEASE.md`, `docs/STATUS_AND_NEXT_GATES_TH.md`, `docs/RELEASE_GATES_V10_V08.csv` and full artifact checksums.
