# ThaiHerb KG Methods Upgrade — v0.2 (2026-11-07)

This is a **methodology and data-integrity upgrade** for three related but **distinct** manuscripts. It adds reproducible source-locked audits and review artifacts without overwriting earlier studies.

## Execute

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest -q tests
```

The core analysis is standard library + RDFLib. `pyshacl` is needed for a real SHACL validation run; if unavailable, no SHACL pass is claimed.

## Papers and scientific boundaries

| Paper | Dataset in this package | Verified computations in this release | NOT established |
|---|---|---|---|
| P1 | V3-derived ten-herb projection; 10 formulas | 23 NPMI edges; edge weighting and leave-one-formula-out sensitivity | Exact identity to original 10-herb source corpus; original trained vectors; independent biological validity |
| P2 | V3-derived 20-herb projection; 10 formulas | 82 NPMI edges; support/degree edge ablation; IDF/Jaccard compound overlap | Independent reference-standard, chemical structure Tanimoto, full 20-seed embedding rerun |
| P3 | V3 assertion CSV/UI subset | 208 assertions inventory; evidence provenance RDF export where IDs exist; contradiction review queue; blank expert benchmark | Full SHACL conformance; original-paper verification at locator level; expert agreement or superiority over M1/M2 |

**Primary assertion layer remains intact.** Degree and support adjustments apply only to computational projections, not to evidence truth, strength, or therapeutic claims. No clinical extrapolation is authorized by these outputs.

## Important flags

- Formula identifiers and compound choices originate from later-stage project projections; source-document-to-row equivalence is not yet independently audited for Paper 1 and Paper 2.
- The 7 clinical V3 assertions have empty canonical object identifiers and are omitted from the IRI-only RDF projection; they appear in `paper3/curation_issues.csv`.
- The chemistry source locators are not uniformly compound-specific. Reviewer work is required before claiming item-level verification.
- Independent blinded experts and conflict adjudication have **not** been performed; templates are intentionally empty.
- The RDF `example.org` vocabulary is a prototype namespace; do not publish it as an authoritative biomedical ontology.

## Source reference and standards

- World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/
- World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/
- Biolink Model. *Understanding the Biolink Model*. https://biolink.github.io/biolink-model/
- Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. *Proceedings of KDD*. https://doi.org/10.1145/3097983.3098036

## Next verified gates

1. Audit original records, source locators, source license and copyright status; freeze Paper 1, Paper 2, Paper 3 separately.
2. For P1, restore original chemistry class table / vectors; compare weight schemes using biological expert gold, not just seed stability.
3. For P2, curate external formula-first and compound structure validation, blinded pairwise similarity labels; add metapath2vec baseline only after data freeze.
4. For P3, obtain canonical context IDs, run pySHACL and negative controls, create an independent adjudicated benchmark with M1/M2/M3 evidence parity.

See `docs/CHANGELOG_TH.md` and the per-paper output files.
