# Paper 3 v0.7: prospective evaluation lock and leakage rules

**Freeze:** Historical V3 208 assertions remain immutable and identical across M1/M2/M3. All source-discovered documents post baseline freeze are held out of the knowledge graph; direct/functional pharmacology and clinical contexts must not be inferred from missing metadata. M1/M2/M3 comparison across development cases is a *representation engineering diagnostic* only.

## Confirmatory benchmark stop gates

1. Publish independent source inclusion/exclusion rules and question categories before reading outcomes.
2. Two genuinely independent blinded reviewers adjudicate answer correctness and justified abstention. Unfilled ratings remain empty; generative model ratings cannot substitute.
3. Train/tune and test partitions must be disjoint by source publication and answer-relevant claim family where applicable.
4. Save timestamped predictions for all three frozen engines **before** revealing gold labels.
5. Score semantic correctness on common-answerable cases, answer rate/coverage, unsupported overclaim, provenance citation correctness, qualifier fidelity and latency separately.
6. Report paired uncertainty grouped by case/source rather than treating 3 model outputs as 3 independent observations.
7. Do not treat SHACL conformance as evidence of scientific or clinical truth.

`P3_V07_BENCHMARK_ELIGIBILITY.csv` is an actual, unfilled expert review queue, not artificial labels; no numerical comparisons are authorized at this release.
