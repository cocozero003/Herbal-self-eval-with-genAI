# Supplementary methodological note — Paper 1 (working draft)

**Title:** Task-specific leave-one-formula-out validation of graph-derived herbal similarity rankings

## Methods

To evaluate a narrow out-of-sample task while maintaining a clean distinction between model stability and predictive validity, we conducted a post hoc leave-one-formula-out (LOFO) benchmark on ten source-reviewed Thai herbal formulas. Each fold omitted one complete formula from all formula-derived model inputs. The nine remaining formulas were used to construct association weights and train co-occurrence graph embeddings under ten preselected random seeds. The pairwise outcome was defined as whether a focal herb pair jointly appeared in the held-out formula, and **must not be interpreted as biomedical or therapeutic similarity**. We compared Cooc-NPMI, support-adjusted and degree-corrected variations, and exploratory candidate Chem/Core representations against non-embedding baselines (formula PairSupport and marginal-degree product). A compound-class Jaccard similarity served as a chemistry baseline. Chemistry inputs were derived from a subsequent proxy dataset and a candidate 19-class mapping; they were not claimed as recovered original Paper 1 embedding inputs.

Full 45-pair cross-model comparisons were blocked for folds with an unrepresented focal herb in co-occurrence training data. One formula (F02) was thus excluded due to the cold-start of H07, leaving nine evaluable folds. We report macro-average precision, AUROC, precision at five and nDCG at five, with cluster bootstrap intervals resampling entire held-out formula units. Paired sign-flip comparisons and within-fold label permutations were exploratory only. An intentionally invalid label-leakage oracle, created by retaining the held-out formula in pair-support counts, was evaluated exclusively to quantify potential inflation from data leakage.

## Results

Of ten formulas, nine allowed full ten-herb prediction, whereas F02 was blocked due to cold-start. The strongest tested method was PairSupport (mean AP 0.419, mean AUROC 0.690), compared with Cooc-NPMI (AP 0.395), Cooc-Combined (AP 0.349), Chem-Proxy (AP 0.275), and Core-Proxy (AP 0.292). The average fraction of positive dyads in eligible formula folds was 0.183. The deliberately invalid leakage oracle increased PairSupport mean AP from 0.419 to 0.543. These findings indicate that the embedding methods examined did not outperform the parsimonious PairSupport baseline for the held-out formula co-occurrence task, and they reinforce the need to report baseline models and explicit leakage safeguards.

## Limitations

Formula test instances originate from a single official compendium and a selected ten-formula sample, not an independent external corpus. Negative labels indicate absence of joint membership within a particular formula, not biological dissimilarity. The chemistry representation relies on a later candidate class taxonomy, and the source-verification process has not been independently adjudicated. Only nine formula units were eligible for the full paired comparison, yielding wide uncertainty intervals. The manuscript's reported original embedding results remain distinct from this exploratory reconstruction. Model-blinded human expert rating forms have been prepared but have not been completed; expert-based external validation is therefore not claimed.

## References

Brière, G., Stosskopf, T., Loire, B., & Baudot, A. (2026). Benchmarking the impact of data leakage on the performance of knowledge graph embedding models for biomedical link prediction. *Bioinformatics, 42*(8), btag608. https://doi.org/10.1093/bioinformatics/btag608
