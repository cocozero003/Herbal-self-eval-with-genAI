# Paper 3 v0.9 — Offline constraint-profile validation and independent benchmark lock

**Research status:** Technical validation complete for the supported local constraint subset; W3C SHACL Core via pySHACL **not executed**. Confirmatory M1/M2/M3 answer accuracy **not calculated** due to missing independent gold.

## Scientific objective

Assess reproducible information preservation in three controlled projections of the same 208 fixed source assertions, independently of text-generation effects. Separately, prepare a preregistered paired performance test whose inferential statistics are only released after blinded expert review.

## Fixed source and model parity

The input `data/P3_V3_208_LOCKED.csv` consists of 71 formula assertions, 100 chemistry assertions, 30 pharmacology-target assertions and 7 clinical assertions. It is not an expert-curated gold dataset. The same 208 records were projected into M1 (flat SPO, 207 RDF triples), M2 (assertion-reified + provenance, 1,501 RDF triples), and M3 (evidence/context-qualified assertion reification, 2,733 RDF triples). One pair of distinct clinical assertions with the same flat subject/predicate/object is merged under M1 because RDF graphs do not retain duplicate triples. More triples do not imply better scientific quality.

## Local SHACL constraint-profile method

The project includes a SHACL shapes graph `results/P3_SHACL_CORE_SHAPES_V04.ttl`. A local inspection engine parses this actual graph and evaluates a **restricted constraint-profile**: `sh:targetClass`, simple IRI `sh:path`, `sh:minCount`, `sh:maxCount`, `sh:nodeKind` (IRI and Literal), and `sh:class` using direct `rdf:type` without inference. It emits an RDF ValidationReport-shaped artifact (`P3_V09_SHACL_SUBSET_REPORT.ttl`) but labels it as **incomplete implementation**. This is not full W3C SHACL conformance and is not a substitute for pySHACL.

The 2,733-triple M3 graph generated **zero violations** for these supported constraints. Seven seeded negative controls—removed provenance, subject or identifier; removed source type; duplicate object or provenance; and wrongly typed subject—were **all detected (7/7)**. These are controlled engineering checks, not an external test of scientific correctness.

Attempts to install `pyshacl>=0.31,<0.41` in this runtime were unsuccessful because the available package index exposes no installable distribution. The `pySHACL` **NOT_RUN** gate is preserved; no full Core PASS result is reported. A real pySHACL execution remains required in a dependency-enabled environment.

## Independent paired benchmark protocol and safeguards

There are 32 development-stage competency questions, not blinded gold. Three model outputs per question yield a 96-row assessment template. Reviewer 1 and reviewer 2 must score without seeing each other's ratings or model identifiers; differences require adjudication by an independent moderator. An independent frozen set, explicit inclusion criteria, conflict-of-interest checks, source-disjoint audit, response freeze, and evidence-citation correctness are prerequisites to confirmatory analysis.

The scoring library `src/blind_benchmark_v09.py` includes a fail-closed gate. It returns **BLOCKED** when gold or assessor decisions are absent; it does not impute answers or replace human experts with the language model. For completed data, it supports four paired binary endpoints (answer correctness, citation correctness, evidence completeness, and appropriateness of abstention). Exact two-sided McNemar tests are calculated for all three model pairs, adjusted via Bonferroni for three pairwise comparisons per endpoint. A 1,000-resample paired bootstrap with a fixed seed estimates a difference-of-proportions 95% interval. Pre-specified endpoint multiplicity across the four families must additionally be addressed by the author before manuscript submission.

For the present release, **0/32** independent gold answers and **0/96** blinded model judgments have been supplied. Consequently **no** clinical answer accuracy, superiority p-values, or source-disjoint generalization results are reported. Synthetic fixtures used to test the computational pipeline do not become study results.

## Remaining validity limitations

(1) The original chemical occurrence claims are not fully source-verified and 7 clinical object identifiers remain noncanonical; (2) review-level sources may combine incompatible preparations and taxa; (3) many evidence attributes in M3 are documentary attributes, not verified biological facts; (4) deterministic schema retention cannot establish response correctness; and (5) missing pySHACL and independent review preclude manuscript-ready external validity.

## Reproduce

```bash
python -m src.original_source_screen_v11
python -m src.shacl_profile_check_v09
python -m src.blind_benchmark_v09
python -m src.build_dashboard_v11
python -m pytest -q tests
```

For a full standards-level test in a proper environment:

```bash
python -m pip install "pyshacl>=0.31,<0.41"
python -m src.validate_shacl_v08
```

Do not cite the local subset checker as an implementation of all W3C SHACL Core features.

## References (APA 7th edition)

Knublauch, H., & Kontokostas, D. (2017, July 20). *Shapes Constraint Language (SHACL)* (W3C Recommendation). World Wide Web Consortium. https://www.w3.org/TR/shacl/

Sommer, A. (2026). *pySHACL* [Computer software]. Python Package Index. https://pypi.org/project/pyshacl/

McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika, 12*(2), 153–157. https://doi.org/10.1007/BF02295996

Efron, B., & Tibshirani, R. J. (1993). *An introduction to the bootstrap*. Chapman & Hall.
