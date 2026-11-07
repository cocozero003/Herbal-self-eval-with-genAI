# Data Dictionary

`CHEMICAL_ASSERTION_EVIDENCE_REVIEW_30.csv`: every row is one V3-derived herb-compound occurrence claim and a candidate documentary locator. `occurrence_evidence_status` is an AI-assisted classification, not expert adjudication. PubChem CID indicates compound identity lookup only, not its occurrence in a herb.

`CHEMICAL_IDENTITY_TAXONOMY_25.csv`: one compound name per row, original v0.4 candidate class vs new v0.5 candidate class. `pubchem_cid_candidate` may be blank when stereoisomer or exact structure is uncertain. `DMPBD` canonical text is resolved from primary research, without PubChem CID.

`CLASS_TAXONOMY_ABLATION_10SEEDS.csv`: 20 paired comparisons (10 each Chem/Core), each involving the same seed and data source with candidate taxonomy changed from 18 to 19 groups.

`HERB_PAIR_EXPLANATION_45.csv`: exploratory explanations of 45 dyads using in-sample formula/co-chemical links; never treat as an independent gold standard.

`INDEPENDENT_DYAD_EXPERT_BLIND_45.csv`: blank human expert labels; leave empty until actual blinded assessment.

`CURATION_AND_ABLATION_SUMMARY.json`: aggregate counts and reanalysis; no publication-readiness assertion.
