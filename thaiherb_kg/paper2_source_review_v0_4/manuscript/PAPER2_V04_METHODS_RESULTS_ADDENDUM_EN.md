# Paper 2 — v0.4 source-audited robustness and 20-seed model reconstruction

## Editorial status
Reanalysis of 20-herb selected pilot, NOT replication of unavailable 35-class archive. Source review on 100 added-herb/formula cells is single-curator, ChatGPT-assisted. Human-independent adjudication and an external source-disjoint validation set are not available.

## Methods
An official 2023 compendium was consulted for all ten selected formulas, reading complete ingredient-table continuations. Formula memberships were projected to the botanical-species level, while documented variation in medicinal material (e.g., *Terminalia chebula* fruit/pericarp versus gall; *Myristica fragrans* seed versus aril) was recorded rather than merged at medicinal-material level. Three omitted herb–formula memberships were restored to F09 and a frozen 74-membership species snapshot was prepared. All 100 H11–H20 membership cells carry official printed-page locators.

Nine embedding variants were compared over 20 preselected random seeds with Word2Vec skip-gram, dimension 32, window five, negative samples five, 15 epochs and one worker. Cooc walks used NPMI weights with support and degree alternatives; Chem walks used H–C–H exact compound paths, and Core variants mixed them at 25/75, 50/50 and 75/25 walk counts. No compound class labels were supplied or inferred. Each model yielded 190 unordered herb-pair cosine scores per seed. Computational repeatability was the mean of 190 dependent seed-pair Spearman correlations; edge perturbation compared mean cosine ranking and top-ten overlap. Held-out formula co-occurrence was evaluated by structural baselines on folds with all herbs represented in training.

## Main findings

- Formula memberships: 71 V3-derived vs 74 source-reviewed species-level. Source correction: F09 + H11, H15, H17.
- Mean original-versus-source-corrected NPMI rank correlation: 0.973895; 37/190 pairs changed score.
- Cooc-NPMI stability: 0.968781; Chem-Exact: 0.757706; Core-Exact50: 0.69269.
- Eligible full 190-pair LOFO folds: 6/10; expert biological labels and external source-disjoint tests absent.

## Interpretation
The expanded panel exposes substantive data-selection and medicinal-part normalization risks. Source-corrected Cooc paths and class-free exact-chemistry paths are trainable and repeatable, but the new chemical channel is not comparable to the original manuscript's compound-class walks. No claims of predictive superiority, pharmacological relevance, therapeutic interchangeability, efficacy or safety are supported.

## Citations
Official Thai herbal formula compendium (2023): https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf. metapath2vec (Dong et al., 2017), DOI:10.1145/3097983.3098036.
