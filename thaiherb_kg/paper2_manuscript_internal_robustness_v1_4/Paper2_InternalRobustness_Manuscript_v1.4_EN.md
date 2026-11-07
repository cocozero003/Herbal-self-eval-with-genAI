# Internal Robustness, Data-Source Sensitivity, and Representation Stability of Herbal Knowledge Embeddings: A Reproducible Study of 20 Thai Medicinal Herbs and 10 Traditional Formulas

*Original research article | Author-review manuscript | 7 November 2026*

**Document status:** Full research article draft for author and journal-format review; scientific scope restricted to internal documentary robustness.

## Abstract
**Background:** Embeddings constructed from herbal formula co-membership and selected phytochemical claims may be sensitive to random initialization, documentary source coverage and representation choices. Their internal stability should be quantified before biological or clinical interpretations.

**Methods:** We analyzed 20 selected herbs, 10 formula documents (74 species-membership assertions), 100 selected chemical claims and 83 distinct compound IDs. Nine embedding configurations were evaluated over 20 seeds (180 fits; 34,200 scores), alongside nine matched perturbations, ten leave-one-formula-out (LOFO) evaluations, twenty chemistry-source holdouts and provisional taxonomy/material sensitivity analyses. Average precision (AP) and AUROC assessed held-out documentary formula co-membership. Formula-cluster bootstrap intervals were exploratory.

**Results:** Cross-seed rank repeatability (mean Spearman ρ) was 0.969 for Cooc-NPMI, 0.758 for Chem-Exact and 0.693 for Core-Exact50. Chemical pruning from five to three and two claims per herb reduced rank correlation to 0.261 and 0.048, respectively. Six complete LOFO folds (190 pairs each) gave mean AP 0.301 for PositiveNPMI, 0.291 for PairSupport, 0.275 for train-only Cooc-NPMI, 0.168 for Core-Exact50 and 0.139 for Chem-Exact. Core minus PairSupport mean AP was −0.1225 (descriptive formula-cluster bootstrap 95% interval −0.2082 to −0.0502). Four cold-start folds were separately evaluated on 171 pairs. Removing any one chemistry source blocked 19/190 pairs (90% coverage).

**Conclusions:** Internal rank stability and documentary retrieval value depend on the information channel and the selected evidence set. Mixed or chemically informed embeddings were not uniformly advantageous for formula co-membership. These findings do not establish biological validity or external generalizability.

**Keywords:** Thai herbal medicine; graph embeddings; robustness; reproducibility; normalized pointwise mutual information; source sensitivity; leave-one-formula-out; herbal knowledge graph

## 1. Introduction

Herbal knowledge graphs integrate heterogeneous evidence channels, including the co-occurrence of plant species in documentary formula sources and published reports of phytochemical constituents. Dense representations of these networks can facilitate exploratory retrieval and ranking. However, a high similarity score is not necessarily stable under changes to the documentary corpus, candidate constituent list, taxonomic scope, or random initialization. Stability should therefore be measured before interpreting embedding neighborhoods as evidence of pharmacological relatedness.

Random-walk embeddings learn vector representations from graph-derived sequences. The conceptual lineage connects skip-gram word embeddings (Mikolov et al., 2013) and graph random walks (Perozzi et al., 2014). For document co-occurrence, normalized pointwise mutual information (NPMI) provides a frequency-sensitive association metric (Bouma, 2009). These techniques are useful computational tools, but their outputs inherit the selection and measurement conditions of the underlying data.

The present study revisits a source-reviewed internal snapshot derived from a Thai traditional-medicine formula reference corpus (Department of Thai Traditional and Alternative Medicine, 2023). Earlier work provided a 20-herb, 10-formula embedding archive with 20 random seeds. Rather than assume that the combination of co-occurrence and chemical channels improves predictive validity, the study evaluates how their rankings change when source and modeling conditions are perturbed. Its endpoint is held-out documentary formula co-membership, which is not a surrogate for biochemical interaction, therapeutic interchangeability, clinical efficacy, or safety.

The objectives were to (i) quantify cross-seed rank stability for nine representation configurations, (ii) characterize changes after controlled perturbations of formula and chemical inputs, (iii) compare train-only embeddings and simple baselines using leave-one-formula-out (LOFO) documentary evaluation, and (iv) measure missing-information coverage following removal of each chemical source. Provisional chemical-family and medicinal-material scenarios are reported separately as exploratory sensitivity analyses. No inference of externally validated biological generalizability was planned.

## 2. Materials and Methods

### 2.1. Data provenance and analytical unit

The frozen analysis panel comprised 20 selected medicinal-herb identifiers (H01–H20) and 10 selected formula documents (F01–F10). A versioned single-curator, AI-assisted species-level review of official formula tables yielded 74 formula–herb membership assertions. Review locations, identifiers, corrected membership rows, and source-document hashes are retained in the reproducibility archive. The panel is purposively curated and is not a random or nationally representative sample of herbal formulas.

The chemical channel contained five selected herb–compound claims per herb (100 claims total), referring to 83 distinct internal compound identifiers and 20 primary assigned chemistry source identifiers. This is a selective evidence panel, not a complete metabolomic profile. Only five of the original 100 claims had direct primary full-text verification against their originally assigned source in the upstream evidence audit. The other claims retain their documented audit tier; an unobserved compound in the panel must not be interpreted as chemically absent.

The unit of ranking was an unordered pair of different herbs. With 20 herbs, the fixed universe contained 20 choose 2 = 190 pairs. Formula labels are defined as one when both herbs appear in the particular held-out formula; all other pairs are labeled zero for that *documentary task only*. A zero label does not establish absence of joint use elsewhere or biological incompatibility. The source files are frozen by SHA-256 and stored in the complete reproducible package.

### 2.2. Representation construction and archived seed analysis

Nine archived representation configurations were examined: Cooc-NPMI, Cooc-Support, Cooc-Combined, Cooc-Support2, Chem-Exact, Chem-ExactPrune4, and Core-Exact mixtures with 25%, 50% and 75% co-occurrence walk shares. Co-occurrence graphs were formed using formula-document membership statistics; their baseline NPMI channel retained positive associations. Chemical walks traversed observed herb–compound–herb paths based on the selected 100 claims. The Core configurations mixed the two sequence families; their percentage denotes the nominal fraction of co-occurrence walk sequences, not a calibrated evidence strength.

The archived Word2Vec skip-gram configuration used 32 latent dimensions, window = 5, negative samples = 5, epochs = 15, minimum count = 1, one worker, and 60 random walks initialized per herb. Co-occurrence walks had up to 20 nodes; chemical walks alternated herb and compound tokens. The 20 fixed seeds were 11, 23, 37, 41, 53, 67, 79, 83, 97, 101, 109, 127, 137, 149, 163, 173, 181, 191, 199, and 211. Pairwise herb similarity was cosine similarity between learned embeddings.

The archived experiment included 9 configurations × 20 seeds = 180 fitted models and 180 × 190 = 34,200 recorded pair scores. For each configuration, all 20 choose 2 = 190 pairs of seed-specific rankings were compared by Spearman correlation over the same 190 herb pairs. Thus, seed repeatability is a *within-dataset rank-reproducibility* statistic. The seed comparisons are mutually dependent and are not 190 independent experimental replications. A frozen Cooc-NPMI seed-11 reproduction yielded a maximum absolute score difference of approximately 4.99 × 10⁻⁹ relative to the archived rounded CSV.

### 2.3. Matched perturbation and ablation protocol

Nine perturbation comparisons were matched to their corresponding archived baseline by random seed (nine variants × 20 seeds = 180 paired comparisons). Co-occurrence variants used minimum positive-NPMI thresholds of 0.15 and 0.30, omitted formula F08, or applied the archived support-at-least-two formulation. Chemical variants retained four, three, or two of each herb’s five selected constituents; the three- and two-compound variants were resampled reproducibly per seed. Mixed-representation variants changed the nominal co-occurrence walk fraction from the 50% baseline to 25% or 75%.

For each comparison, Spearman rank correlation across the 190 scores quantified whole-ranking stability, and overlap of the top ten ranked pairs was recorded. Mean and standard deviation across the 20 paired seeds summarize stochastic variation, not between-source or population uncertainty. Because the set of five compounds per herb was itself selected, chemical pruning measures *panel sensitivity*, not resilience to random removal from all known phytochemicals.

### 2.4. Leave-one-formula-out documentary evaluation

Each of the ten formulas served once as the test document. All formula-dependent graph statistics, co-occurrence walks, and Core walks were reconstructed using the remaining nine documents, with the test formula withheld from graph fitting. The formula-independent selected chemical channel remained fixed. This design reduces direct test-formula leakage into fitted Cooc and Core representations, but the overall 20-herb panel was defined before fold construction; the task remains an internal, selected-panel study rather than an external unseen-herb test.

Eight methods were evaluated: deterministic PairSupport, PositiveNPMI, DegreeProduct, exact-set chemical Jaccard, inverse-document-frequency-weighted chemical Jaccard, train-only Cooc-NPMI embedding, train-only Core-Exact50 embedding, and the formula-independent Chem-Exact embedding. The three embedding methods used 20 seed fits per fold; deterministic baselines were computed once per fold. Predictions were evaluated against documentary held-out formula co-membership via average precision (AP) and area under the ROC curve (AUROC). AP was preferred as the primary ranking endpoint under varying positive fractions (Saito & Rehmsmeier, 2015). AP was calculated as Σₖ (Rₖ − Rₖ₋₁)Pₖ and was not reported as interpolated trapezoidal PR-AUC.

In six folds, every herb had training occurrence and all 190 pairs could be evaluated. In four folds, one herb was absent from all nine training formulas; its 19 pairs were excluded as cold-start ineligible, leaving 171 evaluable pairs per fold. These four folds are analyzed separately because filtering changes both coverage and potentially the class distribution. No missing scores were imputed. The mean positive-label fraction was 0.124 for both the six complete and four partial folds, providing a descriptive class-balance reference. The formula was the resampling unit; seed fits and herb pairs were not counted as independent sampling clusters.

### 2.5. Uncertainty, source holdouts and additional sensitivity tests

For each fold and method, the 20 embedding-seed metrics were averaged before uncertainty estimation. Percentile intervals for mean fold-level AP and AUROC were generated by 2,000 bootstrap resamples of the formula units within each coverage stratum. Paired method-minus-PairSupport comparisons used 4,000 bootstrap resamples of the same formula clusters (Efron & Tibshirani, 1993). With only six complete and four partial folds, these intervals are descriptive and potentially unstable; no confirmatory hypothesis-test p values were computed.

Each of the 20 chemistry source IDs was withheld in turn, removing the five selected chemistry claims for the single herb associated with that source. The chemical embeddings were refit with five fixed seeds per holdout, and rank Spearman was computed only on the 171 remaining evaluable pairs. The missing 19 pairs were counted as missing, not assigned optimistic scores. This assesses sensitivity to missing source coverage, not prediction on independently labeled unseen literature.

Two exploratory, explicitly non-historical sensitivity tests were conducted over 20 seeds: (i) replacing exact compound identifiers with a newly constructed, unadjudicated 31-family name-based grouping and (ii) deleting the F08/H11 species-level formula edge in a medicinal-material counterfactual motivated by fruit/pericarp versus insect-gall distinctions. The original 83-to-35 chemical-class crosswalk was not available. The 31-family analysis is *not* a reconstruction or replication of that historical method.

### 2.6. Reproducibility and quality safeguards

The archived analysis used Gensim 4.4.0; the final run manifest records Python 3.13.5, NumPy 2.3.5, and pandas 2.2.3. Scripts use fixed seeds and single-worker embedding training. Frozen input checksums, detailed per-pair predictions, all fold and seed metrics, pairing identifiers, rank correlations, bootstrap replicates, figure source CSVs, and run instructions are provided in the accompanying versioned research package. A clean-extraction replay reproduced five principal result CSVs byte-for-byte and passed 23 automated regression tests. This documents computational repeatability on the retained environment; it does not validate the scientific source claims.

## 3. Results

### 3.1. Reproducibility and cross-seed stability

Across nine archived configurations, rank stability differed markedly by information channel (Table 1). The seed-mean Spearman correlation was 0.969 for Cooc-NPMI, 0.758 for Chem-Exact, and 0.693 for Core-Exact50. Cooc-Support and Cooc-Combined were slightly more stable (both approximately 0.974). Core-Exact75 had the lowest observed mean cross-seed correlation among these archived configurations (0.637). The stable orderings for formula-derived channels reflect repeatability conditional on the ten selected documents and do not imply external scientific accuracy.

Among the 190 within-model seed-to-seed ranking comparisons, the reported standard deviations summarize descriptive variability across dependent pairs of seeds. They must not be used as if they were independently sampled observations for confidence intervals or formal between-model significance tests.

### 3.2. Controlled perturbation sensitivity

Cooc-NPMI was relatively stable under positive-NPMI thresholds of 0.15 (mean ρ = 0.963) and 0.30 (ρ = 0.914). Omitting F08 changed ranks more substantially (ρ = 0.870), and the support-at-least-two criterion produced a larger shift (ρ = 0.391). In the chemical channel, retaining four of five compounds produced mean ρ = 0.606; retaining three and two produced ρ = 0.261 and 0.048, respectively (Table 2; Figure 2). These changes highlight the dependence of exact-compound embeddings on the selected constituent subset.

Changing the relative mixture of walk sequences also affected Core rankings: the 25% and 75% co-occurrence variants correlated 0.713 and 0.641, respectively, with Core-Exact50. High seed reproducibility therefore does not guarantee invariance to the source or design choices defining the graph.

### 3.3. Held-out documentary formula ranking

Among six complete LOFO folds, PositiveNPMI had the highest mean AP (0.301), while PairSupport had the highest mean AUROC (0.743). Cooc-NPMI train-only achieved mean AP 0.275; Core-Exact50 achieved 0.168 and Chem-Exact 0.139. The mean positive fraction in these folds was 0.124 (Table 3; Figure 1). Although several methods exceeded that class-fraction reference, this is not an independent biological evaluation.

On a paired fold basis, Core-Exact50 AP was lower than PairSupport by −0.1225, with a descriptive 95% formula-cluster bootstrap percentile interval of −0.2082 to −0.0502 based on 4,000 draws. This interval is not a confirmatory proof of inferiority because there were only six complete formula units and no external validation cohort. PositiveNPMI minus PairSupport had a mean AP difference of +0.0099 with an interval spanning zero, so the small difference between their mean APs is not presented as a superiority claim.

Four additional LOFO folds each had one cold-start herb, resulting in only 171 eligible pairs; those results are provided in Table 4 and the supplementary CSV rather than pooled with the six 190-pair folds. The partial-fold results do not support conclusions about the withheld herb itself. Mean AP rankings changed across coverage strata, underscoring that exclusion rules alter the target population being evaluated.

### 3.4. Chemistry-source and medicinal-material sensitivity

The source-withholding experiment was deterministic with respect to coverage: removing the sole assigned chemistry source for a herb removed five selected claims and made that herb’s 19 pair comparisons unavailable, yielding exactly 171/190 = 90% evaluable pairs in every source holdout. Across those 20 source IDs, mean rank Spearman among known pairs was 0.755 (range 0.621–0.810), averaged over five refits per source. The observed 90% coverage is a property of the study’s one-source-per-herb evidence design, not an externally estimated source-failure rate.

The exploratory 31-family chemical aggregation had mean rank ρ = 0.502 relative to exact-compound Chem-Exact, and a corresponding 50% Core-family variant had ρ = 0.446. The F08/H11 medicinal-material counterfactual yielded mean ρ = 0.958 relative to Cooc-NPMI. These are analytical sensitivity probes with incomplete chemical and material adjudication; they cannot substitute for the missing original 35-class taxonomy or verified part/preparation-specific evidence.

## 4. Discussion

### 4.1. Internal stability is not the same as representation validity

This reproducible experiment supports an important methodological distinction: repeatability under random initialization, resilience to changes in input evidence, and usefulness for a defined prediction endpoint are separate properties. Co-occurrence-derived rankings were highly repeatable across random seeds, yet their order could shift under document exclusion and graph construction thresholds. Chemistry-derived rankings were less seed-stable and especially sensitive to removing constituents from a five-claim-per-herb panel. The Core representation inherited sensitivities of both channels and did not outperform the simplest formula-support baseline on the chosen documentary LOFO endpoint.

The finding does not mean that chemical or integrated representations are intrinsically inferior in all herbal knowledge applications. The chosen label tests recovery of formula co-membership, which is conceptually closer to the source used to build the co-occurrence graph than to a chemical similarity objective. A different, expert-adjudicated endpoint (e.g., part- and preparation-specific chemistry or clinically justified substitution) may produce a different ranking. No such gold labels were available here.

### 4.2. Source dependence and the design of missing-information stress tests

The chemical-source holdout clarifies an operational issue: with one assigned chemistry source per herb, withholding any source creates complete chemical cold-start for that herb. Reporting a rank correlation only over still-covered pairs without also reporting 19 blocked pairs would overstate robustness. The study therefore treats abstention/coverage as a first-class outcome. The 90% figure is exact for the selected 20-herb structure; future evidence graphs should incorporate multiple independently verified chemical measurements for the same taxon, part, and preparation to test resilience to *source substitution* rather than solely source deletion.

The provisional family ablation further shows that broad chemical class choices can substantially change neighborhood structure. However, the original historical 35-class map is unavailable, and 31 newly assigned name-based families have not been independently checked. These results can guide future experiments, not support claims that a 35-class biological ontology was reconstructed.

### 4.3. Statistical interpretation and strengths

An important strength is that LOFO graph construction excluded the target formula, and statistics were summarized at the held-out formula rather than treating thousands of correlated pair/seed rows as independent samples. The original 180-fit archive was linked to a numerical seed-level replay; paired perturbations and exact-source holdouts were regenerated; a clean archive extraction reproduced the result files. These measures improve auditability and reproducibility.

Nevertheless, percentile intervals from six formula clusters are imprecise and must be interpreted descriptively. Different herbs recur across formulas, making formula units non-independent in a strict population-sampling sense. No confirmatory family-wise test was performed, and hyperparameter selection and cohort selection were not prospectively registered. The observational nature of the selected documentary panel precludes causal claims about constituent loss or plant physiology.

### 4.4. Limitations and publication boundary

The primary limitations are the small, nonrandom sample (10 formula documents); single-curator, AI-assisted source review with no independent reviewer adjudication; species-level collapsing of plant material differences; a selected five-compound chemical panel with original-source full-text confirmation for only five of 100 source claims; loss of the historical 35-class mapping; and four LOFO folds with systematic cold-start exclusions. Model comparisons were not externally validated on a genuinely prespecified source-disjoint sample with positive and negative adjudicated labels. Eleven additional analytical observations from three DOI-distinct studies exist as a post-hoc positive-only pilot but do not support confirmatory AP or AUROC. The internal results cannot be generalized to Thai herbal practice, phytochemical equivalence, safety, or therapeutic outcomes.

Finally, the three embedding channels represent different computational views of the same limited source-derived universe. They do not encode concentration, assay specificity, biological target, dose, preparation, adverse effects, or causal therapeutic synergy. Similarity metrics must therefore be presented as *descriptive internal ranks* rather than scientific evidence of clinical interchangeability.

### 4.5. Research implications

Future validation should freeze a new external formula corpus before modeling; include part/preparation identity and chemical measurement provenance; recruit independent domain experts for source adjudication and pair-level gold labels; report unknown/abstained outcomes; and compare performance on both documentary co-membership and scientifically meaningful out-of-source labels. The seed-stability and source-deletion framework is reusable, but the current paper should be positioned as an internal robustness and representation-sensitivity study, distinct from subsequent evidence-centric knowledge-graph validation.

## 5. Conclusion

Across 20 selected Thai medicinal herbs and 10 curated formula documents, source- and model-dependent herbal embeddings showed substantial differences in rank reproducibility and sensitivity. Co-occurrence embeddings were comparatively stable under random seeds, whereas exact-compound embeddings were markedly disrupted by pruning a sparse chemical evidence panel. In six complete held-out formula tests, simple co-occurrence baselines performed as well as or better than mixed Core embeddings for the explicitly documentary co-membership task. Source deletion exposed immediate chemical cold-start and 10% pair-level coverage loss. The study establishes an auditable internal sensitivity benchmark and delineates the conditions under which richer evidence integration requires further external and expert-led validation.

## Declarations

Author names and affiliations: To be supplied and approved by the research team.

Ethics: This computational study uses documentary formula references and literature-derived chemical claims; no individual patient data or human-subject observations were processed. The authors should confirm local institutional ethics requirements before submission.

Data and code availability: Frozen data and auditable scripts are archived in the versioned ThaiHerb Paper 2 v1.3 full research ZIP. The source/code-only GitHub branch and Google Drive release links are provided in the accompanying submission checklist. Access and reuse remain subject to the source documents’ licensing terms.

Funding, competing interests, author contributions, and acknowledgments: To be completed by the responsible authors. No funding statement or contribution history has been invented in this draft.

### Table 1. Archived cross-seed rank repeatability

| Model | Mean Spearman ρ | SD | Min | Max |
| --- | --- | --- | --- | --- |
| Cooc-NPMI | 0.969 | 0.006 | 0.948 | 0.985 |
| Cooc-Support | 0.974 | 0.005 | 0.955 | 0.985 |
| Cooc-Combined | 0.974 | 0.005 | 0.961 | 0.986 |
| Cooc-Support2 | 0.935 | 0.020 | 0.873 | 0.981 |
| Chem-Exact | 0.758 | 0.031 | 0.665 | 0.845 |
| Chem-ExactPrune4 | 0.735 | 0.033 | 0.631 | 0.817 |
| Core-Exact50 | 0.693 | 0.036 | 0.605 | 0.791 |
| Core-Exact25 | 0.701 | 0.032 | 0.596 | 0.781 |
| Core-Exact75 | 0.637 | 0.075 | 0.447 | 0.792 |

### Table 2. Matched-seed perturbations

| Perturbation | Comparator | Mean ρ | Seed SD | Top-10 overlap | Seeds |
| --- | --- | --- | --- | --- | --- |
| Cooc-NPMI-Threshold0.15 | Cooc-NPMI | 0.963 | 0.008 | 6.5 | 20 |
| Cooc-NPMI-Threshold0.30 | Cooc-NPMI | 0.914 | 0.015 | 6.9 | 20 |
| Cooc-Remove-F08 | Cooc-NPMI | 0.870 | 0.023 | 5.4 | 20 |
| Cooc-Support2 | Cooc-NPMI | 0.391 | 0.038 | 5.4 | 20 |
| Chem-ExactPrune4 | Chem-Exact | 0.606 | 0.039 | 4.1 | 20 |
| Chem-Prune3 | Chem-Exact | 0.261 | 0.131 | 4.0 | 20 |
| Chem-Prune2 | Chem-Exact | 0.048 | 0.126 | 1.9 | 20 |
| Core-Exact25 | Core-Exact50 | 0.713 | 0.038 | 7.3 | 20 |
| Core-Exact75 | Core-Exact50 | 0.641 | 0.038 | 5.5 | 20 |

### Table 3. Six complete LOFO folds

| Method | Mean AP | 95% bootstrap interval | Mean AUROC |
| --- | --- | --- | --- |
| PositiveNPMI | 0.301 | [0.139, 0.452] | 0.675 |
| PairSupport | 0.291 | [0.181, 0.391] | 0.743 |
| Cooc-NPMI-TrainOnly | 0.275 | [0.165, 0.375] | 0.679 |
| DegreeProduct | 0.261 | [0.145, 0.402] | 0.685 |
| Core-Exact50-TrainOnly | 0.168 | [0.104, 0.223] | 0.561 |
| ChemIDFJaccard | 0.140 | [0.081, 0.182] | 0.477 |
| Chem-Exact-FormulaIndependent | 0.139 | [0.081, 0.184] | 0.478 |
| ChemJaccard | 0.133 | [0.077, 0.177] | 0.475 |

### Table 4. Four cold-start LOFO folds (171 eligible pairs each)

| Method | Mean AP | Mean AUROC |
| --- | --- | --- |
| PositiveNPMI | 0.147 | 0.554 |
| PairSupport | 0.300 | 0.693 |
| Cooc-NPMI-TrainOnly | 0.184 | 0.583 |
| DegreeProduct | 0.349 | 0.720 |
| Core-Exact50-TrainOnly | 0.195 | 0.522 |
| ChemIDFJaccard | 0.172 | 0.531 |
| Chem-Exact-FormulaIndependent | 0.174 | 0.518 |
| ChemJaccard | 0.157 | 0.528 |

## Figures

Figure 1. Mean AP across six complete held-out formulas, with formula-cluster bootstrap percentile intervals.

Figure 2. Mean rank Spearman after matched-seed perturbations (SD across seeds).

Figure 3. Archived 20-seed cross-run rank stability across embedding configurations.

Figure 4. Coverage across all ten LOFO folds (four affected by cold-start).

## References (APA 7)

Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In From form to meaning: Processing texts automatically (pp. 31–40). https://svn.spraakdata.gu.se/repos/gerlof/pub/www/Docs/npmi-pfd.pdf

Department of Thai Traditional and Alternative Medicine. (2023). ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพร ประเภทตำรับยา [Herbal product reference information: Traditional-medicine formulations]. Ministry of Public Health. https://www.dtam.moph.go.th/publications/3712/

Efron, B., & Tibshirani, R. J. (1993). An introduction to the bootstrap. Chapman & Hall.

Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. In International Conference on Learning Representations. https://arxiv.org/abs/1301.3781

Perozzi, B., Al-Rfou, R., & Skiena, S. (2014). DeepWalk: Online learning of social representations. In Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 701–710). Association for Computing Machinery. https://doi.org/10.1145/2623330.2623732

Řehůřek, R., & Sojka, P. (2010). Software framework for topic modelling with large corpora. In Proceedings of the LREC 2010 Workshop on New Challenges for NLP Frameworks. https://www.muni.cz/en/research/publications/884893

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLOS ONE, 10(3), e0118432. https://doi.org/10.1371/journal.pone.0118432

## Reproducibility statement

Source snapshot: v0.4 20-herb species projection; this article reports the v1.3 robustness experiment. Original selected 100 chemical claims are not 100 independently verified primary literature claims. The historical 35-class mapping is unavailable. No biological expert gold or prospective external source-disjoint confirmatory validation is reported. Reproducibility script hashes, complete per-seed results, ten LOFO folds, 20 source holdouts, and original input hashes are bundled with the versioned release.
