# Thai Herbal Knowledge Graph — P2 v0.9 / P3 v0.7

New **independent corroboration** for four chemical claim IDs without modifying historic primary-source disposition, source overlap/leakage audit, M1/M2/M3 RDF parity recheck, and benchmark eligibility quarantine for unadjudicated competency questions. Input baselines from P2 v0.8 / P3 v0.6 are copied unchanged. This is NOT manuscript-ready.

```bash
python -m pytest -q tests
python -m src.stage_v08
python src/validate_shacl.py
```

The last command requires the optional `pyshacl` package and will emit NOT_RUN with a nonzero exit when missing; do not represent that status as conformance. See `docs/P2_V09_NEW_PRIMARY_CORROBORATION.md`, `docs/P3_V07_EVALUATION_LOCK.md`, and results CSVs.
