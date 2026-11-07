# Paper 2 — Robustness foundation (v0.3): author-review addendum

**Scientific status:** An exploratory V3-derived proxy-data analysis; not a replication of the archived 35-class Chem/Core model. Results must be distinguished from the earlier 20-herb manuscript.

**Aim:** To establish source-integrity boundaries and leakage-aware structural baselines before extending the 20-herb knowledge graph. This work does not require biological validation of the preceding 10-herb feasibility paper.

**Methods:** We audited 20 herbs, ten formula codes, 71 formula membership assertions, and 100 curated herb–compound assertions. A 20×10 membership matrix was cross-checked against a single-curator ten-herb source review. Leave-one-source-out audit tracked chemistry coverage. For internal leave-one-formula-out benchmarking, each of ten formulas was completely omitted from training and full 190-pair evaluation was restricted to folds with all herbs represented by the remaining nine formulas. We tested PairSupport, DegreeProduct, PositiveNPMI, exact-compound Jaccard and IDF-weighted exact-compound Jaccard. Outcome labels indicate co-occurrence in withheld formulas, not independently graded biological similarity. Eight seed-locked 4-of-5 compound-panel deletion experiments assessed exact-compound rank sensitivity.

**Results:** Twenty distinct chemical source IDs each exclusively supported one focal herb; removing any one source isolated that herb. Four of ten formula-holdout folds exhibited previously unseen herbs. In the six eligible folds, PairSupport achieved mean AP 0.253147 (mean AUROC 0.728453). Exact-compound-only Jaccard was inferior on the held-out formula-cooccurrence task; this does not test chemical accuracy. Mean Spearman rank agreement across eight 4/5 chemistry panels was 0.792. Positive NPMI edges were 82/190, with 38 edges supported by only one formula.

**Interpretation:** This analysis identifies source concentration and cold-start risks in the preselected small formula corpus. No independent external validation or recovery of the original 35-class chemistry ontology has occurred. The reported 20-seed Cooc/Chem/Core values from the original manuscript should not be replaced with these descriptive baseline results.

**Conclusion:** Proceed to source-verifying expanded formulas, recovering class mappings, and preregistering an independent corpus benchmark. Author review and independent adjudication are outstanding.
