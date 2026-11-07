# Paper 1 manuscript integration recommendations (v0.6)

## Placement

This work is a **post-hoc supplemental source-dependence analysis**. Do not retroactively rewrite the original Cooc/Chem/Core methodology or report the exploratory Chem/Core proxy as an exact reproduction of the archived study.

### Suggested Methods paragraph

To assess the susceptibility of the exploratory chemistry evidence projection to source dependence, we grouped its 30 herb–compound assertions by their 12 originally cited source identifiers. Each source was removed in turn. A source-deletion scenario was considered evaluable for full ten-herb similarity rankings only when every focal herb retained at least one chemistry assertion. In eligible scenarios, the candidate 19-class exploratory Chem and Core Word2Vec models were rerun under the same ten paired random seeds. We calculated Spearman rank correlations across the 45 unordered herb pairs and top-five overlap against the unperturbed model. This analysis evaluated source sensitivity and did not constitute external biological validation.

### Suggested Results paragraph

Eight of the ten focal herbs had all three selected chemistry assertions supported by only one original source identifier. Removing one of the 12 original sources eliminated all chemistry assertions for at least one herb in eight source-deletion scenarios. The remaining four scenarios supported matched-seed model comparisons. Removal of the DMSC source for *Piper retrofractum* produced mean rank correlations of 0.721 (Chem) and 0.656 (Core) across ten seeds relative to the unperturbed proxy model. This illustrates dependence on the chosen source set; it does not establish predictive accuracy.

### Suggested Limitations paragraph

The chemistry projection was reconstructed from a later-stage V3 dataset. The archived original Paper 1 compound-class mapping and trained embedding artifacts were unavailable. Additional literature was retrieved after selection of the 30 representative compounds; it therefore served as corroboration, not an independent test set. Some evidence pertains to extracts, specific plant parts, or broadly identified taxonomic materials rather than the exact herbal material. No expert-adjudicated biological similarity reference standard has been completed.

## Editorial gate

Maintain manuscript's original results unchanged unless original primary input artifacts are recovered or a clearly labeled independent new study is approved. The erroneous v0.3 claim that three F05 formula ingredients were absent is retracted: the official table continues onto its second page.
