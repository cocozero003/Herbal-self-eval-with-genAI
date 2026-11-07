# Internal Robustness, Data-Source Sensitivity, and Representation Stability of Herbal Knowledge Embeddings: A Reproducible Study of 20 Thai Medicinal Herbs and 10 Traditional Formulas

**Manuscript type:** Original research — computational methods and internal validation  
**Manuscript stage:** Author-review draft; journal selection, authorship, affiliations, declarations and final editorial verification pending  
**Source snapshot:** ThaiHerb20 Paper 2 v0.4 (source-reviewed species-level projection), with v1.3 robustness analyses; frozen 7 November 2026

## Abstract

**Background:** Herbal knowledge embeddings are often assessed by similarity rankings, although their robustness to sparse formula documentation, incomplete chemical evidence, and stochastic representation learning is rarely made explicit. An embedding that produces plausible rankings may nevertheless change substantially when its underlying source records change. **Objective:** To quantify internal representation stability, formula-source sensitivity and documentary retrieval in co-occurrence, exact-compound and mixed herbal embeddings without interpreting these outputs as biological similarity. **Methods:** We analysed a source-reviewed panel of 20 Thai medicinal herbs, 10 selected traditional-formula documents, 74 botanical-species membership records and 100 selected herb–compound assertions (83 compound identifiers). Nine archived embedding configurations were assessed across 20 random seeds. Nine paired perturbation conditions examined threshold changes, formula removal, chemical-assertion pruning and mixing ratios. In ten leave-one-formula-out (LOFO) evaluations, formula-derived models were trained on nine documents and evaluated using pair co-membership in the withheld document. Six folds retained all 190 unordered herb pairs; four cold-start folds were reported separately with 171 eligible pairs. We performed formula-cluster bootstrap analyses, 20 leave-one-chemical-source-out interventions, and exploratory material/taxonomy sensitivity checks. **Results:** Archived seed-pair ranking Spearman correlations averaged 0.969 (Cooc-NPMI), 0.758 (Chem-Exact) and 0.693 (Core-Exact50). Retaining three and two of five chemical assertions per herb reduced mean paired rank correlation with Chem-Exact to 0.261 and 0.048, respectively. Across six fully covered LOFO folds, mean average precision (AP) was 0.301 for positive NPMI, 0.291 for PairSupport, 0.275 for train-only co-occurrence embeddings, 0.168 for train-only Core-Exact50, and 0.139 for chemical embeddings. The exploratory paired formula-bootstrap AP difference for Core-Exact50 minus PairSupport was −0.123 (95% interval −0.208 to −0.050). Each chemical-source holdout removed the chemical profile of one herb, rendering 19/190 pairs unevaluable. **Conclusions:** In this selected documentary corpus, co-occurrence rankings were more reproducible across stochastic fits and generally better aligned with withheld formula co-membership than the tested mixed and chemical embeddings. Chemical evidence deletion produced marked representation instability. These findings concern **internal computational robustness and formula-document retrieval**, not external validity, pharmacological relatedness or therapeutic effectiveness.

**Keywords:** traditional Thai medicine; herbal knowledge graph; robustness; source sensitivity; random-walk embedding; co-occurrence; leave-one-formula-out; chemical evidence; reproducibility

## 1. Introduction

Traditional medicinal formulas provide relational information about botanical ingredients, whereas phytochemical literature provides a different and frequently incomplete description of the constituents attributed to individual plants. Combining these channels in an embedding model seems attractive: herbs represented close together in a latent space could potentially be linked through shared formula contexts or shared compounds. However, the semantic interpretation of that proximity is not self-evident. Formula co-membership is a statement about documented practice; a plant–compound edge may refer to a particular material, preparation, analytical platform or experimental report. Neither relation alone establishes pharmacological equivalence, clinical efficacy or safety.

Random-walk embeddings translate graph neighborhoods into sequences that can be processed using distributional representation learning (Mikolov et al., 2013; Perozzi et al., 2014). Such methods may encode prominent structural regularities but can also reflect data availability, edge selection, weighting, sampling and stochastic optimization. In a small herbal corpus, a single formula can contribute multiple ingredient pairs, while the decision to include five selected compounds per herb may have a disproportionate effect on a chemistry-derived representation. Reporting only a best-seed embedding or a high pairwise similarity can hide those dependencies.

The source setting considered here is a selected panel of formulas documented in the Thai governmental reference compendium of traditional medicinal formulas published in 2023 by the Department of Thai Traditional and Alternative Medicine and collaborators. Its ingredient records are projected to botanical-species membership, but distinct medicinal materials of the same species are not necessarily interchangeable. The source-reviewed corpus consequently serves as a useful test bed for *computational reliability*, rather than as a representative sample of all traditional Thai medicine or a biological gold standard.

Earlier ThaiHerb20 work produced a frozen 20-herb, ten-formula corpus and nine archived embedding configurations evaluated with 20 random seeds. The present study examines a more specific question: how stable are the resulting herb-pair rankings, how do they respond to deliberately removed or modified sources, and what happens when a full formula is omitted from training? This is deliberately distinct from establishing whether any embedding captures pharmacological similarity. The separation is particularly important because an independent biological gold standard and a validated historical 35-class chemical mapping were unavailable.

We addressed three aims: (1) quantify seed-to-seed rank reproducibility and sensitivity to controlled edge/parameter perturbations; (2) evaluate formula-level holdout performance against explicitly *documentary* co-membership labels, while identifying cold-start cases; and (3) quantify the loss of chemical coverage caused by source removal and examine two clearly exploratory counterfactual representations. Our interpretation is restricted to a selected corpus and does not treat repeated seeds or overlapping herb pairs as independent experimental observations.

## 2. Materials and Methods

### 2.1 Study design and frozen corpus

This was a retrospective, reproducible computational robustness study of a predefined corpus, **not** a prospectively registered external validation. We used the source-reviewed ThaiHerb20 Paper 2 v0.4 dataset and its archived 20-seed embeddings. Ten selected formula documents were manually mapped to botanical species from the official 2023 reference-formula compendium. The frozen snapshot contains 20 focal herbs (H01–H20), 10 formula documents (F01–F10), 74 species-level herb–formula memberships, 100 selected chemistry assertions (five per herb), 83 distinct compound identifiers, and 190 unordered focal-herb pairs (20 choose 2).

The compendium was the documentary basis for formula memberships, not a substitute for clinical research. Earlier single-curator review and known differences between species-level membership and medicinal materials were retained. Chemical assertions reflect selected literature-backed candidate edges with unequal evidentiary certainty: at the time of this analysis only five original-source assertions had primary full-text analytical confirmation. We froze both the graph input and the archived embedding-score table with SHA-256 hashes, preserving results rather than silently regenerating alternative mappings.

### 2.2 Representation families and deterministic baselines

We evaluated three representation families. **Co-occurrence embeddings (Cooc)** used a weighted herb–herb graph derived from selected formulas. The weight was the nonnegative portion of normalized pointwise mutual information (NPMI), computed from counts of herbs and pairs across the documents, with zero used when the positive association was undefined or absent. Variants used support weighting, combined degree adjustment or a minimum pair-support threshold. **Chemical embeddings (Chem-Exact)** used a bipartite herb–compound graph with the 100 archived exact-identifier assertions. **Mixed embeddings (Core-Exact)** combined formula-walk and chemical-walk sequences, with the 25, 50 and 75 designations denoting the intended proportions of co-occurrence walk sequences before Word2Vec training (not a verified proportion of biomedical evidence).

Co-occurrence random walks started at each of 20 herb nodes, generated 60 walks per herb with up to 19 transitions, and sampled neighbors using nonnegative graph weights. Chemical walks started from each herb, generated 60 walks per herb, and alternated herb–compound–herb hops for up to five compound steps. The two walk sets were mixed and shuffled before training in the Core variants. Embeddings were trained with a single-worker gensim Word2Vec skip-gram model (32 dimensions; context window 5; five negative samples; 15 epochs; minimum count 1; subsampling 0.001). Cosine similarity between each of the 190 unordered herb pairs provided an output score.

We compared five deterministic rankers for formula holdout: pair support in the nine-document training set; product of marginal formula counts (DegreeProduct); positive NPMI; Jaccard similarity of exact-compound sets; and an inverse-document-frequency weighted compound Jaccard score. The three embedding methods compared in LOFO were Cooc-NPMI-TrainOnly, Core-Exact50-TrainOnly and Chem-Exact-FormulaIndependent. The latter used formula-independent chemistry inputs and archived, seed-matched chemical embeddings, whereas Cooc and Core were explicitly reconstructed from training formulas in each fold.

### 2.3 Archived seed repeatability and replay verification

We retained 20 specified random seeds (11, 23, 37, 41, 53, 67, 79, 83, 97, 101, 109, 127, 137, 149, 163, 173, 181, 191, 199 and 211). The earlier dataset contains nine model configurations × 20 seeds = 180 archived fits and 34,200 pairwise scores. These were **not** counted as newly fitted models in the present analysis. Seed repeatability was assessed by Spearman correlation of the 190 pair rankings across 190 unique seed combinations. To verify numerical reproducibility, the Cooc-NPMI seed-11 configuration was rerun using its original code and inputs; the maximum absolute difference from the archived eight-decimal scores was below 5 × 10⁻⁹.

### 2.4 Predefined perturbations and ablations

Nine within-seed comparisons measured changes in pairwise ranking relative to their corresponding archived model: (i–ii) positive NPMI edge thresholds of 0.15 and 0.30; (iii) omission of formula F08; (iv–vi) retaining four, three or two of five selected chemical assertions per herb; (vii) a support-at-least-two co-occurrence graph; and (viii–ix) mixing 25% or 75% co-occurrence walks rather than the 50% Core baseline. For chemical three-of-five and two-of-five ablations, assertions were subsampled by seed; the four-of-five variant and other archived configurations reused frozen scores where appropriate. Thus nine variants × 20 seeds = 180 *paired comparisons*, not 180 newly trained models. Outcomes were rank Spearman correlation and the overlap between the top ten herb pairs; seed-level means and standard deviations were descriptive.

### 2.5 Leave-one-formula-out documentary retrieval

For each of ten folds, one formula was held out and the remaining nine formed the training corpus. All formula-derived co-occurrence features, Cooc walks and Core walks were recalculated from training documents only. Chemical inputs were fixed independent of formula membership. Evaluation labels were assigned **one** if both herbs appeared in the withheld formula and **zero** otherwise; a zero denotes only *absence of joint documentation in that particular formula*, not tested biological dissimilarity.

We scored average precision (AP) and area under the receiver-operating-characteristic curve (AUROC) for each formula. Both metrics assess the relative ranking for the held-out documentary label; AP is particularly informative when positive pairs are sparse (Saito & Rehmsmeier, 2015). The eight methods were evaluated on the same eligible pairs within each fold, with 20 seeds for stochastic models and one evaluation for deterministic rankers. Each fold was summarized first over its seeds and then given equal weight in across-formula summaries.

An herb appearing only in the held-out formula has no formula-trained embedding neighborhood and was treated as a **cold-start herb**, not assigned an invented score. Six folds allowed all 190 pair scores; four had exactly one cold-start herb and therefore 171 evaluable pairs after excluding 19 incident pairs. Results were stratified into these full and partial strata rather than pooled across different evaluation populations. Complete-case performance is not an unbiased estimate for cold-start situations.

### 2.6 Uncertainty estimation and paired comparisons

We estimated descriptive 95% percentile intervals using 2,000 resamples of **formula folds** within each coverage stratum. We computed paired differences relative to PairSupport using 4,000 formula-cluster resamples, retaining fold pairing between methods. Pair scores and random seeds were **not** treated as independent sampling units. Because only six fully covered formulas and four partial formulas were available, these intervals were exploratory and no multiplicity-adjusted confirmatory hypothesis tests or p values were claimed. Small-sample uncertainty in cross-validation is well recognized (Varoquaux, 2018).

### 2.7 Chemical-source holdout and provisional context sensitivity

Each herb had five selected chemistry edges assigned to one archived source ID. In 20 holdout interventions, we removed all five edges from one chemical source at a time, refit chemical walks across five seeds, and examined coverage and the rank correlation restricted to still-evaluable pairs. This is an **internal data-availability stress test**: removing a source also removes the entire chemical profile of its corresponding herb. It cannot identify source-independent chemical validity.

Two additional sensitivity analyses were separated from the main evaluation: an unadjudicated name-based classification of 83 compounds into 31 provisional chemical families (the unrecovered original 35-class mapping was not replicated), and a single formula–herb material counterfactual involving F08/H11, where species-level membership and distinct plant materials may diverge. Neither exploratory intervention supplied an independent biological label.

### 2.8 External data, source integrity, and software

An earlier evidence workstream selected 11 positive analytical records from three primary publications with DOI strings distinct from those of the 20 archived chemical sources. The records were selected **after model development**, lack sampled non-detections, use heterogeneous botanical materials and were not independently adjudicated. We therefore did not compute external AP, AUROC, accuracy or biological generalization claims from them. The complete archive includes input fingerprints, results, source-holdout logs, seed-level outcomes and analysis scripts. The original computation used Python 3.13.5, NumPy 2.3.5, pandas 2.2.3 and gensim 4.4.0. We validated release integrity and a clean extracted replay separately from empirical validity.

## 3. Results

### 3.1 Corpus, model outputs and internal replay

The frozen corpus comprised 20 focal herbs across ten selected formula documents and 74 species-level membership records; five selected chemistry assertions were associated with each herb. The representation comparison universe contained 190 unordered focal-herb pairs. The archived nine-configuration experiment preserved 180 seed-specific fits and 34,200 pair scores. The exact Cooc-NPMI seed-11 replay differed from its archived scores by at most 4.99 × 10⁻⁹, supporting numerical consistency of that reconstruction.

### 3.2 Random-seed stability

Across archived 20-seed configurations, mean between-seed rank correlations were high for Cooc-NPMI (0.969; SD 0.006), Cooc-Support (0.974; SD 0.005) and Cooc-Combined (0.974; SD 0.005). Chemical and mixed embeddings were less stable: Chem-Exact yielded 0.758 (SD 0.031), Core-Exact50 0.693 (SD 0.036), and Core-Exact75 0.637 (SD 0.075). These values represent internal agreement of pair rankings across random seeds; they do not assess whether those rankings agree with independent expert judgments.

![Figure 1. Archived seed-to-seed ranking reproducibility across embedding configurations. The source figure displays 20-seed summary statistics; the plotted correlations are not biological accuracy scores.](figures/Figure3_Archived_20seed_stability.png){width=5.8in}

### 3.3 Perturbation sensitivity

Chemical embeddings showed substantial ranking changes under progressive removal of selected compound assertions. Chem-ExactPrune4 retained mean rank correlation 0.606 (SD 0.039) with the full five-of-five Chem-Exact baseline. Retaining only three and two compounds per herb reduced mean rank correlation to 0.261 (SD 0.131) and 0.048 (SD 0.126), respectively. The average top-ten overlap in the two-of-five analysis was 1.9 pairs out of ten. By contrast, moderate NPMI edge thresholds gave correlations of 0.963 and 0.914, while removal of one selected formula F08 gave 0.870. The co-occurrence minimum-support-two variant was more disruptive (0.391). Changing the Core mixture from 50% to 25% and 75% co-occurrence walks resulted in correlations of 0.713 and 0.641, respectively.

**Table 1. Paired within-seed rank changes under nine perturbations**

| Intervention | Comparison baseline | Mean Spearman rho | SD across seeds | Mean top-10 overlap |
|:---|:---|---:|---:|---:|
| Chem: retain 4/5 assertions | Chem-Exact | 0.606 | 0.039 | 4.10 |
| Chem: retain 3/5 assertions | Chem-Exact | 0.261 | 0.131 | 4.00 |
| Chem: retain 2/5 assertions | Chem-Exact | 0.048 | 0.126 | 1.90 |
| Cooc: NPMI threshold 0.15 | Cooc-NPMI | 0.963 | 0.008 | 6.45 |
| Cooc: NPMI threshold 0.30 | Cooc-NPMI | 0.914 | 0.015 | 6.90 |
| Cooc: omit formula F08 | Cooc-NPMI | 0.870 | 0.023 | 5.40 |
| Cooc: pair support ≥ 2 | Cooc-NPMI | 0.391 | 0.038 | 5.40 |
| Core: cooc walk share 25% | Core-Exact50 | 0.713 | 0.038 | 7.30 |
| Core: cooc walk share 75% | Core-Exact50 | 0.641 | 0.038 | 5.50 |

*Note.* All estimates are means across 20 paired seeds on 190 unordered herb pairs. Top-ten overlap and Spearman rho reflect two different aspects of stability; neither is a quality-of-care endpoint. Differences across scenarios also reflect how each perturbation is implemented.

![Figure 2. Rank Spearman correlation between each perturbed configuration and its matched-seed baseline; higher scores indicate more stable pair orderings.](figures/Figure2_Perturbation_Rank_Stability.png){width=5.8in}

### 3.4 Formula-level held-out retrieval

LOFO was feasible in all ten formula folds but exposed two distinct coverage situations. In six folds (F01, F04, F06, F08, F09 and F10), every focal herb appeared in the remaining nine formulas and all 190 pairs were scored. In four folds (F02, F03, F05 and F07), holding out the formula left one focal herb unseen in the remaining formula graph, requiring exclusion of the 19 corresponding pairs; these folds retained 171 pairs each. The number of positive documentary co-membership pairs in a fully covered formula ranged from three to 36. The positive fractions were consequently highly heterogeneous.

In the six full-coverage folds, the largest mean AP was obtained with PositiveNPMI (0.301), followed closely by PairSupport (0.291) and Cooc-NPMI-TrainOnly (0.275). PairSupport had the largest mean AUROC (0.743). Core-Exact50-TrainOnly achieved mean AP 0.168 and AUROC 0.561, and Chem-Exact-FormulaIndependent achieved 0.139 and 0.478. This indicates that under the *documentary pair co-membership endpoint*, adding chemistry to the train-only embedding was not accompanied by a retrieval advantage over direct formula-based baselines. It does not imply that chemical information lacks potential biological value.

**Table 2. Leave-one-formula-out evaluation stratified by observable pair coverage**

| Scoring approach | Full 6 folds: mean AP [95% interval] | Full mean AUROC | Partial 4 folds: mean AP | Partial mean AUROC |
|:---|:---|---:|---:|---:|
| PositiveNPMI | 0.301 [0.139, 0.452] | 0.675 | 0.147 | 0.554 |
| PairSupport | 0.291 [0.181, 0.391] | 0.743 | 0.300 | 0.693 |
| Cooc-NPMI-TrainOnly | 0.275 [0.165, 0.375] | 0.679 | 0.184 | 0.583 |
| DegreeProduct | 0.261 [0.145, 0.402] | 0.685 | 0.349 | 0.720 |
| Core-Exact50-TrainOnly | 0.168 [0.104, 0.223] | 0.561 | 0.195 | 0.522 |
| ChemIDFJaccard | 0.140 [0.081, 0.182] | 0.477 | 0.172 | 0.531 |
| Chem-Exact-FormulaIndependent | 0.139 [0.081, 0.184] | 0.478 | 0.174 | 0.518 |
| ChemJaccard | 0.133 [0.077, 0.177] | 0.475 | 0.157 | 0.528 |

*Note.* Intervals in the full coverage stratum use 2,000 formula-cluster percentile bootstrap draws. Seed-specific scores were averaged within formula before across-formula summaries. Partial folds exclude exactly 19 herb pairs involving the cold-start herb, changing the evaluated population; the two strata should not be interpreted as an unbiased head-to-head performance trend. AP is average precision, not the area estimated by another numerical PR integration rule.

![Figure 3. Mean average precision (AP) and exploratory formula-cluster bootstrap intervals for the six fully covered LOFO folds.](figures/Figure1_LOFO_AP_6_complete_formulas.png){width=5.8in}

### 3.5 Paired differences relative to the formula-support baseline

For six full folds, the estimated formula-cluster paired mean difference in AP between Core-Exact50 and PairSupport was −0.1225 (95% exploratory percentile interval −0.2082 to −0.0502; 4,000 draws). For train-only Cooc-NPMI relative to PairSupport, the difference was −0.0154 (interval −0.1431 to 0.1017), and for PositiveNPMI it was 0.0099 (interval −0.1825 to 0.1903). The wide intervals for the two co-occurrence comparisons and the small number of independent formula clusters rule out stronger confirmatory statements. No significance claims or p-values were derived from seed-level pseudo-replicates.

### 3.6 Chemical-source loss and exploratory botanical-material sensitivity

For each of the 20 source holdouts, five chemical assertions were removed and one herb lost its entire selected chemical profile. Only 171 of 190 pairs remained evaluable (90% coverage); the rank correlation on these available pairs averaged 0.755 across source-specific five-seed summaries (range 0.621–0.810). The predictable loss of 19 pairs per intervention is a consequence of the one-source-per-herb design, not evidence that a model generalizes beyond its data.

The provisional 31-family regrouping gave a mean rank correlation of 0.502 (SD 0.037) relative to Chem-Exact; the provisional Core family variant yielded 0.446 (SD 0.049) relative to Core-Exact50. The F08/H11 material counterfactual yielded 0.958 (SD 0.006) relative to the species-level Cooc-NPMI ranking. These comparisons demonstrate sensitivity to *representation choices* but cannot reproduce the missing original 35-class ontology or validate material equivalence.

![Figure 4. Held-out formula coverage and cold-start counts. The six complete-case folds should be distinguished from the four partial-coverage folds.](figures/Figure4_LOFO_Coverage_and_ColdStart.png){width=5.8in}

### 3.7 Evidence eligibility and reproducibility

The source audit retained 100 chemical assertions, but primary full-text confirmation within their **original cited publications** was available for only five. An additional external pilot contained 11 post-hoc positive observations from three DOI-disjoint sources with heterogeneous material context and no negative cases; it was excluded from confirmatory performance evaluation. The archived 83-to-35 original class mapping was not recovered. A clean extraction of the complete research ZIP reran the core analyses, matching five principal summary CSVs byte-for-byte; 23 regression tests passed. These reproducibility checks support the ability to repeat *this analysis*, not independent validation of the underlying evidence corpus.

## 4. Discussion

### 4.1 Main interpretation

Three findings deserve emphasis. First, the relative ordering of herb pairs produced by co-occurrence random-walk embeddings was more consistent across stochastic seeds than the tested chemical-only and mixed embeddings within the selected dataset. Second, removing only part of a deliberately sparse chemical profile caused pronounced rank rearrangement, illustrating a dependence on chemical-edge availability that can be masked by reporting a single best model. Third, in the held-out formula co-membership task, simple formula-derived rankings matched or exceeded the mixed and chemical embeddings on mean AP, demonstrating that increased representation complexity is not automatically advantageous for every chosen endpoint.

These are **negative or qualified findings about engineering reliability**, not a failure of the herbal knowledge-graph concept. A model can be computationally unstable while potentially encoding valuable relationships under a different, independently validated target. Conversely, a formula co-membership score can look favorable while remaining clinically uninterpretable. Our design intentionally exposes this distinction rather than allowing documentary labels to stand in for pharmacological gold standards.

### 4.2 Why formula-based baselines are strong in a documentary test

The outcome itself is defined from whether a pair of herbs appears in a formula record. PairSupport and positive NPMI summarize nearly the same documentary source channel, albeit from the nine training formulas; they therefore have an inherently close relationship with this endpoint. A mixed embedding is asked to preserve both formula and chemical contexts in a finite latent dimension, and its cosine similarities need not optimize the withheld co-membership ranking. This explanation is consistent with the data but was not isolated through an independent causal experiment. The fair conclusion is task-specific: in ten selected documents, source-aligned deterministic baselines were difficult to improve upon.

### 4.3 Chemical sparsity, botanical materials and source dependence

The chemistry graph deliberately encodes five selected assertions per herb, not a comprehensive set of measured constituents. Evidence types differ across sources, and plant part, extraction and detection conditions matter. Trimming three of five edges per herb can therefore remove much of the selected representation, making the rank changes plausible without implying the plant lacks those compounds. The source holdout is even more restrictive: because each herb's entire selected profile comes from one source ID, source deletion is functionally an herb-level chemical cold start. Reporting 90% pair coverage as though it were a model robustness score would overstate the finding; it is better interpreted as a direct measure of missing-information burden.

The F08/H11 case also illustrates the semantic gap between botanical species membership and medicinal material identity. A species may contribute distinct medicinal materials to traditional practice; retaining only its species identifier can create a misleading impression of material equivalence. The single counterfactual is a sensitivity illustration, not a complete plant-part ontology evaluation.

### 4.4 Statistical reliability and limitations of the evaluation population

The independent documentary units here are only ten selected formulas, with six in the complete-case stratum. Although each formula yields many herb pairs and the stochastic models use 20 seeds, those repeated outputs do not create hundreds of independent empirical formula observations. We therefore resampled formulas, not overlapping pairs or seeds. Bootstrap intervals should still be regarded as exploratory with so few clusters (Varoquaux, 2018). Cold-start exclusions in four folds introduce a different and non-random pair population; their estimates are informative operationally but not directly exchangeable with full-coverage folds. Furthermore, the AP task includes *negative documentary pairs*, not analytically proven absent chemical associations or medically unrelated herbs.

### 4.5 Comparison with existing graph representation research

Random-walk-based representation learning was designed to preserve structural neighborhoods (Mikolov et al., 2013; Perozzi et al., 2014; Grover & Leskovec, 2016), not to establish truth outside the input graph. This study extends that methodological lesson to a particular herbal dataset: reproducibility and source perturbation must be evaluated alongside any claimed use of latent similarity. The principal contribution is a traceable test procedure with explicit missing-data, cold-start and chemical-source gates, rather than a new algorithm claiming superior general predictive performance.

### 4.6 Implications for further research and responsible application

A follow-up validation should first obtain independently confirmed plant–compound relations matching species, plant part, preparation, and analytical method; then define held-out negative or non-detection outcomes separately from missing documentation. The test set should be frozen before model selection and evaluated by independent reviewers using the same eligibility rules across representations. The historical 35-class mapping would need to be retrieved or explicitly abandoned in favor of a new, adjudicated chemical ontology. A broader panel of formulas and prespecified out-of-source or out-of-time holdouts could then quantify external transportability. These steps are needed before proposing medicinal similarity inference or decision-support uses.

### 4.7 Strengths and limitations

Strengths include a frozen source-reviewed panel, archived 20-seed results and numerical replay, train-only formula embedding reconstruction in LOFO, transparent separation of six full and four partial folds, formula-level uncertainty estimation and full results release. Limitations include targeted selection of ten formulas, dependence among ingredients within the same formula, incomplete and unevenly verified chemistry claims, one chemical source per herb, unavailable original 35-class mapping, an exploratory rather than confirmatory statistical design and lack of independent biological gold. The 11-record external positive pilot does not overcome these weaknesses and was not used to calculate generalizability scores.

## 5. Conclusions

In a selected 20-herb, ten-formula Thai traditional medicine corpus, co-occurrence-based embeddings displayed relatively high random-seed rank stability, whereas exact-compound and mixed representations were more sensitive to random initialization and removal of chemical evidence. Direct formula-based baselines achieved higher mean AP than the studied Core and chemical embeddings when evaluated against withheld *documentary* co-membership in six fully covered formula folds. Removing a chemical source caused one-herb cold start and made 10% of focal herb pairs unevaluable. These findings support a narrow conclusion about **internal reproducibility, data-source dependence, and representation stability**. They do not establish external generalizability, independent chemical correctness, pharmacological relatedness, clinical benefit or safety.

## Statements and research transparency

**Ethics:** This computational analysis used documentary and public literature-derived herbal evidence; no individual-level human participant data were analyzed. Whether a formal institutional exemption or approval statement is required should be confirmed with the authors' institution and target journal.

**Data and code availability:** The author-review research archive includes the frozen v0.4 input, full v1.3 score tables, 20-seed configurations, 10-fold predictions, uncertainty draws, figures and reproducibility scripts. Complete source-reviewed research files were released in a versioned Google Drive package; publication-facing scripts and validation protocol reside on a separate GitHub branch. Links and the checksum should be included in the submission after repository and access-policy review.

**Funding, conflicts of interest, author contributions, consent, acknowledgements:** To be completed and confirmed by the actual authors. No statements are imputed.

**Use of AI tools:** This manuscript was assembled with assistance from ChatGPT based on frozen computational outputs and literature metadata. All numerical statements, source-to-claim correspondences and authorship declarations require author verification before submission, consistent with journal policy.

## References

Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In *From form to meaning: Processing texts automatically: Proceedings of the Biennial GSCL Conference 2009* (pp. 31–40). https://svn.spraakdata.gu.se/repos/gerlof/pub/www/Docs/npmi-pfd.pdf

Department of Thai Traditional and Alternative Medicine, Thai Food and Drug Administration, & Thai Traditional Medicine Wisdom Fund. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพร ประเภท ตำรับยาแผนไทย ฉบับ พ.ศ. 2566* [Reference information on herbal products: Thai traditional medicine formulas, 2023 edition]. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

Grover, A., & Leskovec, J. (2016). node2vec: Scalable feature learning for networks. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 855–864). https://doi.org/10.1145/2939672.2939754

Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). *Efficient estimation of word representations in vector space*. International Conference on Learning Representations. https://arxiv.org/abs/1301.3781

Perozzi, B., Al-Rfou, R., & Skiena, S. (2014). DeepWalk: Online learning of social representations. In *Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 701–710). https://doi.org/10.1145/2623330.2623732

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432. https://doi.org/10.1371/journal.pone.0118432

Varoquaux, G. (2018). Cross-validation failure: Small sample sizes lead to large error bars. *NeuroImage, 180*, 68–77. https://doi.org/10.1016/j.neuroimage.2017.06.061
