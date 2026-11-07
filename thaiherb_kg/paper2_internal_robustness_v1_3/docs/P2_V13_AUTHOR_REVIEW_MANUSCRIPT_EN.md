# Source-Sensitive Stability of Formula- and Chemistry-Derived Embeddings in a Curated Thai Herbal Panel: A Reproducible 20-Seed Internal Robustness Study

**Author-review draft — methods/results supplement; not a final externally validated manuscript.**

## Abstract

**Background.** Graph embedding models for herbal knowledge representations may be sensitive to selected formula documents, source-specific chemical evidence and random initialization. The original historical 35-class chemical map was unavailable in the accessible archive.

**Methods.** The frozen source-reviewed 20-herb dataset comprised 10 curated formulas, 74 species-level formula memberships, 100 selected herb–compound claims and 83 distinct compound identifiers. Nine archived embedding configurations were evaluated across 20 seeds (180 fits, 34,200 scores), with one seed numerically replayed. Nine paired perturbation variants were analyzed across 20 seeds. Ten leave-one-formula-out folds refit Cooc and Core without the target formula. Six folds supported a complete 190-pair universe; four had one cold-start herb and were analyzed separately using 171 pairs. Baselines were formula PairSupport, Positive NPMI, DegreeProduct and exact/IDF-weighted chemical Jaccard. Average precision (AP) and AUROC were calculated against *documentary held-out formula co-membership*, not biological outcomes. Formula-level bootstrap intervals (2,000 iterations) and paired formula-cluster bootstrap differences (4,000 iterations) were descriptive only. Twenty chemical-source holdouts were tested with five seeds each.

**Results.** In six complete LOFO folds, mean AP was 0.301 for Positive NPMI, 0.291 for PairSupport, 0.275 for Cooc-NPMI, 0.168 for Core-Exact50 and 0.139 for Chem-Exact. Core-Exact50 AP was lower than PairSupport (paired mean difference -0.122). Stochastic random retention of three and two of five compounds per herb yielded mean Spearman rank correlations of 0.261 and 0.048 relative to the full chemical baseline. Every source-level chemical holdout eliminated direct coverage for one herb, yielding 171/190 remaining pair scores (90%). A separately labeled provisional 31-family ablation and botanical material counterfactual were also completed.

**Conclusion.** On this selected documentary target, co-occurrence measures performed better on average than chemical-only or mixed embeddings. The findings demonstrate model and source sensitivity rather than clinical validity or external generalizability. Independent biological gold ratings and source-disjoint prospective tests remain unavailable.

## 1. Data, provenance and target

The unit was an unordered pair of herbs from a panel of 20 herbs (190 pairs). The 10 selected official formula documents provided 74 source-reviewed species-level membership assertions. The fixed chemical panel comprised five selected compounds per herb (100 claims), 83 distinct internal compound identifiers, and one main chemistry source ID per herb. Source audit and material-specific caveats were carried from versioned releases. Herb–compound absence from the selected panel is not chemical non-occurrence. Taxonomic species co-membership cannot imply equivalence of dried plant part, gall, seed or aril.

## 2. Reproducible embeddings and perturbations

We used archived Gensim 4.4.0 Word2Vec skip-gram (vector size 32, window 5, negative sampling 5, epochs 15, min_count 1, workers 1, 60 random walks per herb). The twenty seeds were 11, 23, 37, 41, 53, 67, 79, 83, 97, 101, 109, 127, 137, 149, 163, 173, 181, 191, 199 and 211. Cooc-NPMI used positive normalized pointwise mutual information weights on the ten formula documents; Chem-Exact used herb–compound–herb paths. Core-Exact mixed co-occurrence and chemical sequences. Fixed complete archive code and configuration hashes are included. Numerical replay for Cooc-NPMI, seed 11 differed from the archived value by less than 5e-9 (rounding at eight decimal places).

Perturbations included Cooc threshold 0.15 and 0.30, Cooc with F08 document omitted, random retention of three or two chemical claims per herb, the archived four-of-five subset, support>=2 co-occurrence, and Core 25:75 versus 75:25 mixing. In addition, an explicitly provisional name-based 31-family aggregation and the F08/H11 material-specific removal counterfactual were tested across 20 seeds. These do not recover the original missing 35 chemical classes.

## 3. Leave-one-formula-out protocol and leakage safeguards

For each fold, all Cooc and Core walks were reconstructed using the remaining nine formula documents; held-out co-membership labels were used only for evaluation. Formula-independent chemical data were held fixed. We measured average precision and AUROC over 190 herb pairs in six full folds and 171 eligible pairs for each of four cold-start folds; results were reported separately. Excluding cold-start pairs removes some positive labels and may change the estimand. The output is a documentary retrieval task; non-co-occurring pairs are not validated biological negatives. Random seed repeats were not treated as independent cases for inferential intervals.

## 4. Main results

### Table 1. Complete-fold LOFO model comparison

| Model | Mean AP | 95% cluster bootstrap CI | Mean AUROC |
|---|---:|---:|---:|
| PositiveNPMI | 0.301 | [0.139, 0.452] | 0.675 |
| PairSupport | 0.291 | [0.181, 0.391] | 0.743 |
| Cooc-NPMI-TrainOnly | 0.275 | [0.165, 0.375] | 0.679 |
| DegreeProduct | 0.261 | [0.145, 0.402] | 0.685 |
| Core-Exact50-TrainOnly | 0.168 | [0.104, 0.223] | 0.561 |
| ChemIDFJaccard | 0.140 | [0.081, 0.182] | 0.477 |
| Chem-Exact-FormulaIndependent | 0.139 | [0.081, 0.184] | 0.478 |
| ChemJaccard | 0.133 | [0.077, 0.177] | 0.475 |

### Table 2. Perturbation sensitivity (mean paired-seed rank Spearman)

| Perturbation | Baseline | Mean rho | SD across seeds |
|---|---|---:|---:|
| Chem-ExactPrune4 | Chem-Exact | 0.606 | 0.039 |
| Chem-Prune2 | Chem-Exact | 0.048 | 0.126 |
| Chem-Prune3 | Chem-Exact | 0.261 | 0.131 |
| Cooc-NPMI-Threshold0.15 | Cooc-NPMI | 0.963 | 0.008 |
| Cooc-NPMI-Threshold0.30 | Cooc-NPMI | 0.914 | 0.015 |
| Cooc-Remove-F08 | Cooc-NPMI | 0.870 | 0.023 |
| Cooc-Support2 | Cooc-NPMI | 0.391 | 0.038 |
| Core-Exact25 | Core-Exact50 | 0.713 | 0.038 |
| Core-Exact75 | Core-Exact50 | 0.641 | 0.038 |

### Source-holdout and material sensitivity

Removing any one of the 20 chemical source IDs removed all five selected chemical links for one herb. In all 20 holdout settings, 19 of the 190 total pairs were not chemically evaluable. The 171 remaining pairs were used to describe ranking stability across five seeds. This is a source-availability stress test, not an independent external-sample study.

The new provisional 31-family aggregation yielded a 20-seed average rank correlation of 0.502 with exact chemical embeddings. Removing the species-level F08/H11 edge to represent a strict fruit-versus-insect-gall material counterfactual yielded a mean rank correlation of 0.958 relative to Cooc-NPMI. These are hypothesis-generating analyses only.

## 5. Evidence and external-study eligibility

The archived 100 chemistry claims have only five original-source primary full-text confirmations; other claims have lower tiers of source traceability. A post-hoc pilot included 11 positive analytical observations from three DOI-distinct publications. Their DOI strings did not overlap those of the 20 archived chemical sources, but the examples were selected after model development and lack blinded independent adjudication and sampled negatives. External AP/AUROC was deliberately not computed. The 83-to-35 historical class mapping was not recovered. The new 31-family mapping is a separate, unadjudicated sensitivity analysis, not original class-level replication.

## 6. Limitations and implications

The corpus was selected, small (ten formula documents), source-specific and sparsely annotated chemically. Selected co-membership is not medicinal interaction or clinical efficacy. The six complete folds yield wide uncertainty intervals, while four other folds have nonrandom cold-start exclusions. Formula-cluster bootstrap intervals reflect variation across the few selected formulas, not independent biological replication. These findings justify a revised, narrower manuscript claim restricted to *internal computational sensitivity and documentary retrieval*, with future prespecified studies requiring independent expert-reviewed biological and material-level labels and a genuinely held-out external corpus.

## References (APA 7)

Albaqami, J. J., Hamdi, H., Narayanankutty, A., Visakh, N. U., Sasidharan, A., Kuttithodi, A. M., Famurewa, A. C., & Pathrose, B. (2022). Chemical composition and biological activities of the leaf essential oils of *Curcuma longa, Curcuma aromatica* and *Curcuma angustifolia*. *Antibiotics, 11*(11), 1547. https://doi.org/10.3390/antibiotics11111547

Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In *From form to meaning: Processing texts automatically* (pp. 31–40). https://svn.spraakdata.gu.se/repos/gerlof/pub/www/Docs/npmi-pfd.pdf

Long, D. M., Quoc, L. P. T., Nhung, T. T. P., Thy, V. B., & Nhu, N. L. Q. (2023). Chemical profiles and biological activities of essential oil of *Citrus hystrix* DC. peels. *Korean Journal of Food Preservation, 30*(3), 395–404. https://doi.org/10.11002/kjfp.2023.30.3.395

Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. *International Conference on Learning Representations*. https://arxiv.org/abs/1301.3781

Sytykiewicz, H., Łukasik, I., & Goławska, S. (2026). GC-MS profiling, antioxidant and enzyme inhibitory activities of basil (*Ocimum basilicum* L.) and clove (*Syzygium aromaticum* L.) essential oils and their binary mixtures. *Molecules, 31*(18), 3292. https://doi.org/10.3390/molecules31183292

Department of Thai Traditional and Alternative Medicine. (2023). *Official herbal reference-formula compendium* [Thai-language source]. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf
