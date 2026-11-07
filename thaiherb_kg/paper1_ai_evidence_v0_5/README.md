# ThaiHerb Paper 1 — AI-Assisted Evidence & Chemical Taxonomy Review v0.5

Date: 2026-11-07. The parent manuscript remains a ten-herb computational feasibility pilot.

## Scientific status: SOURCE-REVIEWED RESEARCH PROTOTYPE, NOT INDEPENDENTLY ADJUDICATED OR EXACTLY REPLICATED

- Formula layer: 10 selected official formula tables reviewed by model-assisted single curator, 46 positive focal herb–formula memberships, 54 explicitly absent focal herb/formula cells, 23 positive-NPMI edges. The F05 three-edge deletion in the deprecated v0.3 was an error; the formula continues to printed page 162.
- Chemistry: 30 V3-proxy occurrence assertions, 25 unique compound strings. AI-assisted source ledger links each row to a public evidence URL, source type and locator. There are 23 candidate PubChem CID crosswalks and two entries without specific CID (DMPBD and limonene). DMPBD full name is documented in the literature; limonene stereochemistry is unspecified.
- A NEW candidate 19-class taxonomy separates piperlongumine (cinnamamide lactam) from piperine (piperidine alkaloid). This is not recovery of the original unpublished 19-class curation table.
- Reanalysis compares the v0.4 exploratory 18-class candidate graph with the v0.5 19-class candidate on 10 matched seeds. No independent gold labels were created or filled in, no outside human reviewer was impersonated.
- Published/archived Top-15 results are retained only as background, not as an independent benchmark. No new clinical efficacy, drug substitution or biological performance inference is justified.

## Research tasks supplied

1. `results/CHEMICAL_ASSERTION_EVIDENCE_REVIEW_30.csv` — 30 linked candidate evidential associations and review statuses.
2. `results/CHEMICAL_IDENTITY_TAXONOMY_25.csv` — standardized identities, candidate PubChem CIDs, structural ambiguity and separate v0.4/v0.5 classes.
3. `results/HERB_PAIR_EXPLANATION_45.csv` — all 45 dyads, exact formula support, chemical overlap and explanatory classes; **not gold-standard predictions**.
4. `results/CLASS_TAXONOMY_ABLATION_10SEEDS.csv` — paired sensitivity to chemical class revision.
5. `results/19_class_candidate/` — complete re-computed exploratory Cooc/Chem/Core outputs for 10 seeds; do not claim archived vector replication.
6. `results/OPEN_EVIDENCE_ISSUES_30.csv` — actionable review queue for primary-paper verification and source locators.
7. `results/INDEPENDENT_DYAD_EXPERT_BLIND_45.csv` — intentionally blank adjudication labels; required for external validation.
8. `docs/RESEARCH_REPORT_TH.md`, `docs/EXPERT_REVIEW_PROTOCOL_TH.md`, `docs/MANUSCRIPT_REVISION_TH.md` — research methods, publication guardrails and manuscript handoff.
9. `manuscript/Paper1_Reviewed_AI_Assisted_Draft_v0.5.docx` — annotated manuscript with separate post-hoc appendix; NOT publication-ready.
10. `dashboard/Paper1_Evidence_Review_v0.5.html` — offline interactive inspection.

## Local reproduction

Extract the package without changing paths, then run:

```bash
python -m pip install -r requirements.txt
python run_all_v05.py
python -m pytest -q tests
```

The scripts keep archived v0.4 results separate from v0.5. Source evidence URLs are not downloaded during computation; human primary-source review must check the real text and appropriate plant part.

## Non-negotiable limitations

- No original Paper 1 archived compound-class mapping or trained Word2Vec vectors has been recovered. This cannot be substituted by an AI-generated 19-group version and called identical.
- PubChem is used to check chemical identity, not to prove presence in a plant. Different isomers and extraction contexts must not be conflated.
- Some compound occurrence entries have secondary-review support, not primary isolation; some still require row-specific primary confirmation.
- Independent expert review and expert agreement (kappa/ICC) have NOT been performed. An LLM cannot legitimately be counted as independent human experts.
- The sample size of 10 medicinal herbs and 10 deliberately selected formulas makes stability descriptive, not evidence of biological validity.

## Public resources

Official formula compendium: https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf
PubChem: https://pubchem.ncbi.nlm.nih.gov/
DMSC Thai Herbal Pharmacopoeia: https://bdn-thp.dmsc.moph.go.th/

## Version status

- v0.3 deprecated: erroneous partial source correction removing F05 entries.
- v0.4 retained: source-reviewed formula projection + 18-class exploratory chemical taxonomy.
- v0.5 current: per-assertion AI-assisted evidence review and a structurally clarified 19-class exploratory alternative.
