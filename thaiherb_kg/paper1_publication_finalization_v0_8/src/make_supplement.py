from pathlib import Path
import json,csv,hashlib,platform,os,sys
import numpy as np
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results';DOC=ROOT/'supplement'
def readcsv(p):
 with Path(p).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def mdtable(rows,keys):
 return '| '+' | '.join(keys)+' |\n| '+' | '.join(['---']*len(keys))+' |\n'+'\n'.join('| '+' | '.join(str(r.get(k,'')) for k in keys)+' |' for r in rows)+'\n'
seeds=readcsv(R/'seed_repeatability_13models.csv');pert=readcsv(R/'perturbation_sensitivity_10comparisons.csv')
family=readcsv(R/'botanical_family_descriptive_3models.csv');v07=readcsv(R/'model_comparison_cluster_bootstrap.csv')
rec=readcsv(R/'ORIGINAL_MANUSCRIPT_VS_V08_REANALYSIS.csv')
folds=readcsv(R/'fold_eligibility_10.csv')
readiness=readcsv(R/'PUBLICATION_READINESS_GATES.csv')
doc=f'''# Supplementary Methods and Results — ThaiHerb Paper 1 v0.8

**Scientific boundary:** These numerical results belong to the V3-derived, source-reviewed reconstruction. The historical Paper 1 corpus and original 19-class mapping are not authenticated. All validation outcomes are descriptive and selected-corpus dependent.

## S1. Input and provenance

The reconstructed input contains 10 herbs, 10 purposively selected official formula records with 46 focal ingredient memberships, 30 herb–compound assertions, 25 names and a candidate 19-class chemical mapping. The 10 × 10 formula matrix was reviewed with source page ranges by an AI-assisted single curator. Original training archive equivalence is not demonstrated. The user-held full ZIP carries the data inputs, while the GitHub code folder does not expose the research inputs.

Source documentation: Department of Thai Traditional and Alternative Medicine/Thai Food and Drug Administration, *Reference information for herbal products for notification: Thai traditional medicine formulations, B.E. 2566*. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

## S2. Reproducibility parameters

The same ten random seeds were used for thirteen variants. Skip-gram dimension 32, context window 5, 5 negative samples, 15 epochs, workers 1, minimum count 1, sample 0.001; Python and library versions are frozen in `results/reanalysis_manifest.json`. Every cosine score for every herb pair and seed is available in `results/all_reanalysis_scores_13models_10seeds.csv` (5,850 rows).

## S3. Full seed-repeatability

{mdtable([{'Model':r['model'].replace('Candidate19','19').replace('Candidate18','18').replace('Cooc-','C-').replace('Core-','Core-'),'Mean rho':r['rank_rho_mean'],'SD':r['rank_rho_sd_population'],'Min':r['rank_rho_min']} for r in seeds],['Model','Mean rho','SD','Min'])}

Values are mean pairwise comparisons of 10 seed-rank vectors. These 45 seed-pair correlations per model share seeds and should not be treated as independent replicates for inferential significance testing.

## S4. Full perturbation sensitivity

{mdtable([{'Variant':r['perturbation'].replace('Cooc-','C-').replace('Core-','Core-').replace('Candidate19','19'),'Rank rho':r['mean_rank_spearman'],'Top-5 shared':r['top5_overlap_mean_vectors']} for r in pert],['Variant','Rank rho','Top-5 shared'])}

The chemical-pruning condition retains the first 2 of 3 recorded compounds per herb. Because order is curated, this is a **stress test** and not an unbiased randomized chemistry deletion. The Cooc support shrinkage uses k=2 and degree correction uses exponent -1/4. Neither was optimized against biological labels.

## S5. Effective source-token mixture

At nominal Cooc:Chem 50:50 by walk count, the mean Cooc token share was about **{np.mean([float(x['effective_cooc_token_share']) for x in readcsv(R/'core_channel_contributions_by_seed.csv') if x['model']=='Core-Candidate19']):.4f}**; this descriptive figure does not adjust for the effective context-pair sampling rate, repeated co-occurrence tokens, or channel-specific word frequency.

## S6. Label-withheld botanical-family diagnostic

{mdtable([{'Model':r['model'].replace('Candidate19','19'),'Same family':r['same_family_mean'],'Other families':r['different_family_mean'],'Difference':r['descriptive_difference']} for r in family],['Model','Same family','Other families','Difference'])}

Only 4 of 45 dyads share a family. No family edges were used in training, but the entities themselves were, so this is not independent external validation.

## S7. Internal held-out formula benchmark (v0.7, supplementary only)

**Evaluation question:** In a selected 10-formula document collection, do two herbs co-occur in the formula withheld from Cooc training? This is not biological similarity.

{mdtable([{'Model':r['method'],'Mean AP':round(float(r['mean_average_precision']),3),'AUROC':round(float(r['mean_auroc']),3)} for r in v07],['Model','Mean AP','AUROC'])}

Eight out of nine non-PairSupport methods did not exceed PairSupport's mean AP of 0.419 on this task. One fold (F02) was excluded from the full 45-dyad comparison because herb H07 had zero Cooc training occurrences; the chemistry panel was fixed and selected earlier. Label leakage was demonstrated by deliberately including held-out membership, increasing PairSupport AP to 0.543, and the invalid oracle was excluded from all comparison rankings. None of these scores are chemical, clinical or pharmacological relevance metrics.

## S8. Original historical results versus new reconstructed calculations

{mdtable([{'Analysis':r['original_manuscript_label'],'Original':r['archived_manuscript_value'],'Reanalysis':r['fresh_reanalysis_value']} for r in rec],['Analysis','Original','Reanalysis'])}

The original pilot's 19-class chemistry mapping, walk corpus and model vectors have not been located. The new 19-class mapping is candidate; matching its **number of classes** to the historical number cannot establish row-wise equality or reproduce the historical results.

## S9. Scientific readiness and release gates

{mdtable([{'Gate':r['gate'],'Status':r['status'],'Requirement':r['requirement']} for r in readiness],['Gate','Status','Requirement'])}

## S10. Instructions to reproduce

1. Install Python and the versions in `requirements.txt` within a clean environment.
2. From the root of the full v0.8 package run `python run_v08.py`.
3. The pipeline regenerates the full 13 × 10 embedding results, source-token shares, sensitivity tables, and tests.
4. Compare its outputs to the included CSVs or recorded SHA-256 values. Binary-equivalent results across distinct numerical architectures are not guaranteed; rank/cosine tolerance is defined in automated tests.
5. Do not call the output independent expert gold or a reproduction of the missing original class taxonomy.

## S11. Reporting caveats

The original publication project used a selected rather than comprehensive formula corpus. There is no inference about therapeutic interchangeability, pharmacological efficacy, clinical outcomes, safety or regulatory classification. The official recipe compendium is the source for formula context; the phytochemical papers and monographs are distinct, heterogeneous evidence; their citations do not establish an independent herb-pair similarity truth set. The included 2017 typed-walk and NPMI references justify a computational design, not biological truth.
'''
(DOC/'Paper1_Supplementary_Methods_Results_v08.md').write_text(doc,encoding='utf8')
print('written',len(doc),'chars')