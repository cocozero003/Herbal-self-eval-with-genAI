# Paper 2 v0.3 — Scientific gates and handoff

**Release type:** internal research/provenance foundation, not publication-ready research.

## Completed in v0.3

1. Locked and hashed the 20-herb V3-derived proxy and Paper 1 ten-formula crosswalk.
2. Audited 200 formula–focal-herb positions: legacy 100 matched at single-curator level, newly added 100 not yet independently verified.
3. Verified 71 formula memberships, 100 chemistry assertions, 83 compound IDs and 82 positive-NPMI edges.
4. Computed formula holdout sensitivity and fair baselines in six eligible full-coverage folds; four folds explicitly blocked for cold starts.
5. Measured single-source fragility: 20 of 20 chemistry source holdouts invalidate full-190-dyad coverage.
6. Measured rank change after eight randomized 4/5 exact-compound panel ablations.
7. Prepared blinded 190-pair R1/R2 worksheets and a blank adjudication form. None contains fictitious expert labels.
8. Completed ten automated integrity tests and checked DOCX rendering and offline HTML JavaScript syntax.

## Blocking gaps before presenting Paper 2 as external validity research

- Original 35-class chemistry taxonomy and original full 190-pair embeddings have not been recovered.
- Added H11–H20 × ten formulas requires comprehensive full-ingredient-table primary-source review. The original source-ID crosswalk for legacy H01–H10 only proves consistency with the Paper 1 single-curator projection.
- Formula source is one purposively selected compendium. A LOFO internal split cannot certify independent generalization.
- Chemistry source assignment has one source ID per herb, preventing fully supported leave-one-source-out comparisons.
- No human expert has independently rated any 190 pairs; the forms are blank.
- Exact compound IDs in the import do not establish molecular structure equivalence, plant tissue, analytical conditions, detection and preparation.

## Next milestone (v0.4)

1. Validate added 100 formula-herb positions against original official formula tables, with evidence locators and an absence-check protocol.
2. Recover class labels from the genuine source archive, or release a separately dated and reviewed new taxonomy with explicit provenance.
3. Run paired 20-seed Cooc/Chem/Core + class-free baselines and preregister external formula corpus eligibility before opening it.
4. Obtain external-source and human-reviewed herb-pair annotations; track reviewer agreements and coverage blocks.

## Integrity policy

Never substitute Paper 1's v0.8 reconstructed 19-class results for the Paper 2 original 35-class chemistry mapping. Never use data from a held-out formula to build its Cooc training graph. Never count an unrepresented herb as zero chemical similarity without an explicit missingness report. Never assert absent pairing means therapeutic dissimilarity.
