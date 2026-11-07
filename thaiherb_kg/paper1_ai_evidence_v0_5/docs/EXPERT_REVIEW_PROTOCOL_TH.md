# Blinded independent expert adjudication protocol — NOT YET COMPLETED

Purpose: independently evaluate the scientific and source-specific meaning of ThaiHerb Paper 1 results rather than its seed-to-seed repeatability.

## Eligibility
At least two distinct human experts with expertise in pharmacognosy/botanical taxonomy or phytochemistry. Reviewers cannot see similarity scores, model names, training co-occurrence edges, or the suggested labels of other experts until lock.

## Procedure
1. Check species identity, plant part and appropriate preparation for each of the 30 herb-compound pairs against the primary source and mark `supported`, `contradicted`, or `insufficient evidence`; record exact DOI/URL and table or page locator.
2. Each expert independently labels the 45 herb dyads for a pre-specified task: *phytochemical similarity*, not traditional therapeutic interchangeability. Labels 0=low, 1=intermediate, 2=high, or NA=insufficient data. Raters see a pre-curated external evidence dossier, not inputs reused to train the KG.
3. Compare independent ratings with weighted Cohen kappa (categorical ordinal) and observed agreement. Disagreements are adjudicated by a third person; only then lock gold labels.
4. Report nDCG@5, precision@5, pairwise Spearman, bootstrap confidence intervals over dyads with caution (dyads share herbs, so use herb-block bootstrap sensitivity), and permutation-based uncertainty against baselines.
5. Keep expert-assessed labels entirely separate from AI-assisted curation and from the original input sources to reduce leakage and circular validation.

No claims about achieved agreement, relevance, independent validation, accuracy, or superior biological performance are possible until this process is completed.
