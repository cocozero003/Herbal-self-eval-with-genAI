# Paper 3 v0.4: Controlled Graph Projection and Benchmark Preparation

## Study status

**Implementation study only. Not a scored QA experiment.** The 208 frozen legacy V3 assertions (71 formula, 100 chemistry, 30 pharmacology-target, and seven clinical) were projected without reweighting or importing the corrected Paper 2 v0.4 74-membership data. A comparison against an adjudicated gold test set was not performed.

## Methods

We implemented three representations of the *same* historical assertion set with identical identifier and source-universe inclusion:

- **M1:** subject–predicate–object triples; the one-to-many assertion provenance is not represented in the RDF graph. A separate audit CSV preserves the original assertion IDs but is not exposed as evidence by the M1 graph.
- **M2:** each assertion is instantiated as an RDF resource with stable ID, exact subject/relation/object and `prov:wasDerivedFrom` a source entity.
- **M3:** M2 augmented with literature-supplied `evidenceMode`, `directness`, `originalStatus`, `contextText`, `limitationText`, and unresolved-object flags. Text material and assay qualifiers are *not normalized into first-class entities* yet; this is not the full target design.

All RDF is generated deterministically from the same `data/P3_V3_208_LOCKED.csv` and separately versioned from archived graphs. Count differences against historical 5,148 triples or v0.3 2,834 triples are due to newly declared projection scope, not replication results.

## New observation: Loss of two context-distinct clinical assertions in naive SPO

The 208 frozen source assertions yield **207 unique M1 triples** due to a precise collision: `CLIN005` (SRC_CLIN_VERMA1993) and `CLIN006` (SRC_CLIN_BORDIA1997) both share `(H01, platelet aggregation, ADP- and epinephrine-induced platelet aggregation)`. However, their historical dataset specifies different conditions and effect directions: a short-term healthy-volunteer ginger study versus a coronary-disease study of chronic ginger administration with a distinct single-dose qualification. Collapsing their statements into one SPO triple loses assertion identity and attribution. This is a **structural counterexample** from the frozen dataset, not independent verification of the underlying trial results or evidence of superior M3 answer accuracy.

## Programmatic results

| Output | M1 | M2 | M3 |
|---|---:|---:|---:|
| Input assertion records | 208 | 208 | 208 |
| RDF triples generated | 207 | 1,501 | 2,733 |
| Individually traceable assertion nodes | 0 | 208 | 208 |
| Explicit source attribution in graph | No | Yes | Yes |
| Textual qualification in graph | No | No | Yes |
| Material/assay normalization | No | No | No |

These numbers are triples and counts, **not** benchmark accuracy. The 624-row development rendering is for checking preservation of original assertions only.

## Validation and planned benchmark

Structural checks cover missing source edges, extra assertion objects, source node type and missing subject. Four seeded defects are detected by a narrow custom RDFLib checker, which **does not implement the SHACL standard**. A separate `src/validate_shacl.py` uses actual `pyshacl` SHACL Core when installed, writing an RDF report and testing the same four negative controls. `pyshacl` installation was unavailable in this environment; its result is `NOT_RUN_DEPENDENCY_UNAVAILABLE`.

A blank blinded-competency-question kit contains eight domains: taxonomy, plant material/preparation, formula/version, compound occurrence, pharmacology directness, clinical population/regimen, context discordance, and uncertainty. Reviewer ratings and adjudicated expected answers are intentionally blank. No model performance metrics or statistical significance can be calculated yet.

## Limitations

The original 67-record source registry is not recovered, while 45 observed source identifiers remain in the v0.3 audit. Seven clinical object identifiers are missing in legacy V3, preserved as literals without synthetic canonical IDs. Source contexts are historical dataset fields whose scientific correctness is not independently certified by the RDF generator. Three models are presently *representation projections*, not fully equal-capability natural-language QA engines. The standard SHACL, material/assay ontology, expert question gold and source-disjoint validation are outstanding.

## References (APA 7)

World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/

World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/
