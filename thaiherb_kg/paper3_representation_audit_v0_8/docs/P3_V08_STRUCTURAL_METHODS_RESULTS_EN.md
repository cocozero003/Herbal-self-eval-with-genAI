# Paper 3 v0.8: Comparative representation integrity (author-review methods/results)

## Research question and scope

We assessed whether three representational models preserve recoverable evidence properties when projecting precisely the same frozen 208 source assertions. **This is a representation capability and lineage engineering analysis**, not an experiment on human question-answer correctness, scientific fact validity, biomedical safety, or therapeutic interchangeability.

The immutable V3 input contained 71 formula memberships, 100 chemistry assertions, 30 pharmacology-target assertions and seven clinical assertions. Its SHA-256 is `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`. The three RDF projections, pre-existing at the selected freeze, contain 207 (M1), 1,501 (M2) and 2,733 (M3) unique triples, respectively. M1 is a naive subject-predicate-object materialization; M2 has reified assertion identities and PROV source links; M3 also stores contextual and interpretation qualifiers.

## Reproducible audit

`src/stage_v10.py` reads all models using RDFLib and traverses all 208 original assertions, checking existence of the corresponding M1 triple and the M2/M3 assertion identifiers, source lineage, evidence mode, directness and context fields. The resulting matrix contains 624 rows (208 × three models). The source IDs and assertion identities are recoverable for 0/208 M1, 208/208 M2 and 208/208 M3 assertions. Evidence mode, directness and context text are recoverable for 0/208 M1, 0/208 M2, and 208/208 M3 assertions. These are expected differences in data model design. They are not independent predictive outcomes and should not be assigned inferential *p* values or compared as evidence of scientific answer quality.

One M1 SPO combines CLIN005 and CLIN006, whereas M2 and M3 preserve their separate assertion IDs and source relations. This is a structural collapse, not a human-adjudicated biological contradiction. Seven clinical records lack original canonical object identifiers: M3 retains source-grounded context and flags these objects rather than fabricating a canonical medical concept.

The study's prospective benchmark kit contains 32 development competency questions with all expert-gold fields blank. A fully independent confirmatory evaluation requires two real blinded reviewers, adjudication, fixed eligibility, prespecified endpoints and saved predictions prior to scoring. Neither accuracy nor M3 superiority can be claimed here. Source lineage does not imply experimental causal proof.

## SHACL Core boundary

The previous v0.4 shapes are retained. A runnable validator with five mutated copies of the actual M3 graph is packaged at `src/validate_shacl_v08.py`. Attempts to install `pyshacl` on the authoring system failed because the configured package source could not be resolved. Thus the actual SHACL Core run is **NOT_RUN**, not conforming by assumption. The included structural regression checks rely on RDFLib and are not a substitute for a standard SHACL engine. On a system with working package access, run `python -m pip install 'pyshacl>=0.31,<0.41'` followed by `python -m src.validate_shacl_v08`, and inspect both the authentic graph report and five negative-control results. Passing SHACL detects only ontology/constraint conformance, not scientific truth.

## References (APA 7)

World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/

World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/
