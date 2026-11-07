"""Generate reconciliation tables, graphics, and a provenance-aware manuscript.
No clinical interpretation or unverified original replay claims.
"""
from __future__ import annotations
import csv,json,hashlib,os,sys,subprocess,textwrap
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results';M=ROOT/'manuscript';D=ROOT/'docs';S=ROOT/'supplement'
for p in (R,M,D,S):p.mkdir(parents=True,exist_ok=True)

def rows(name):
 with (R/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save(name,values):
 with (R/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(values[0]));w.writeheader();w.writerows(values)
seed=rows('seed_repeatability_13models.csv');sensitivity=rows('perturbation_sensitivity_10comparisons.csv');family=rows('botanical_family_descriptive_3models.csv');walks=rows('core_channel_contributions_by_seed.csv')
sd={x['model']:x for x in seed};sp={x['perturbation']:x for x in sensitivity}
orig={'Cooc-NPMI':.946,'Chem-Candidate19':.977,'Core-Candidate19':.945}
reconc=[]
for k,v in orig.items():
 reconc.append({'original_manuscript_label':k.replace('-Candidate19','').replace('-NPMI',''),
  'comparison':'10-seed mean rank Spearman','archived_manuscript_value':v,
  'fresh_reanalysis_value':sd[k]['rank_rho_mean'],'difference_reanalysis_minus_original':round(float(sd[k]['rank_rho_mean'])-v,6),
  'identity':'NOT_EQUIVALENT_ARCHIVED_DATA_AND_CANDIDATE_CHEMISTRY','implication':'do not substitute; new results are separately labeled'})
for name,old in [('Cooc-thr0p05',.982),('Cooc-thr0p15',.963),('Cooc-thr0p30',.657),('Chem-PruneFirst2',.226),('Core-Cooc25',.969),('Core-Cooc75',.800)]:
 v=float(sp[name]['mean_rank_spearman'])
 reconc.append({'original_manuscript_label':name,'comparison':'mean-ranking perturbation Spearman','archived_manuscript_value':old,
 'fresh_reanalysis_value':round(v,6),'difference_reanalysis_minus_original':round(v-old,6),
 'identity':'NOT_EQUIVALENT_ARCHIVED_DATA_AND_CANDIDATE_CHEMISTRY','implication':'do not substitute; perturbation and source archive differ'})
save('ORIGINAL_MANUSCRIPT_VS_V08_REANALYSIS.csv',reconc)
# Data inventory
chem=rows('../data/CHEMICAL_IDENTITY_TAXONOMY_25.csv') if False else None
p=ROOT/'data/CHEMICAL_IDENTITY_TAXONOMY_25.csv'
with p.open(encoding='utf-8-sig') as f:chem=list(csv.DictReader(f))
# Scientific readiness matrix makes no fictitious review or source equivalence claim.
gates=[
 ('G1','Defined 10-herb feasibility scope','PASS','Explicit closed pilot design; excludes efficacy claims'),
 ('G2','Official formula locator and 10x10 projection','SOURCE_REVIEWED','10 formula tables, single-curator model-assisted, not double reviewed'),
 ('G3','New reproducible Cooc/Chem/Core workflow','PASS','130 fits over 10 paired seeds with frozen V3-derived proxy data'),
 ('G4','Original Paper 1 chemistry table and 19 class identity','NOT_RECOVERED','Candidate 19 class count is not proof of original equality'),
 ('G5','Original Table 2-4 exact replay','NOT_REPRODUCED','Original 10-seed results treated as historical manuscript report only'),
 ('G6','v0.8 reanalysis integrity tests','PASS','10/10 pytest, deterministic rerun verified'),
 ('G7','Herb-compound row-level primary full-text verification','PARTIAL','AI-assisted public abstract/source summaries; material contexts differ'),
 ('G8','Independent pair-wise biological similarity benchmark','NOT_DONE_NOT_REQUIRED_FOR_PROOF_OF_FEASIBILITY','No external model-accuracy claims'),
 ('G9','Manuscript and supplementary analyses aligned with same V3-derived proxy','PASS','Reanalysis manuscript v0.8 uses only reanalysis results'),
 ('G10','Coauthor/publication signoff and target-journal formatting','NOT_DONE','Author names, funding, author contributions and journal selection pending')]
save('PUBLICATION_READINESS_GATES.csv',[{'gate':a,'requirement':b,'status':c,'comment':d} for a,b,c,d in gates])

# Graphics
fig,ax=plt.subplots(figsize=(8,4))
labels=['Cooc','Chem','Core','Cooc + support & degree']
vals=[float(sd[k]['rank_rho_mean']) for k in ['Cooc-NPMI','Chem-Candidate19','Core-Candidate19','Cooc-Combined']]
ax.bar(labels,vals)
ax.set_ylim(0,1);ax.set_ylabel('Mean pairwise-seed Spearman rho');ax.set_title('V3-derived reconstruction: seed repeatability (10 seeds)')
for i,v in enumerate(vals):ax.text(i,min(v+.022,.95),f'{v:.3f}',ha='center',fontsize=10)
ax.tick_params(axis='x',labelrotation=12);fig.tight_layout();fig.savefig(R/'FIG01_seed_rank_stability.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.8))
keys=['Cooc-thr0p05','Cooc-thr0p15','Cooc-thr0p30','Chem-PruneFirst2','Core-Cooc25','Core-Cooc75']
vals=[float(sp[k]['mean_rank_spearman']) for k in keys]
ax.barh(range(len(keys)),vals);ax.set_yticks(range(len(keys)),['NPMI > .05','NPMI > .15','NPMI > .30','Chem: first 2 compounds','Core: 25:75 walks','Core: 75:25 walks']);ax.invert_yaxis();ax.set_xlim(0,1);ax.set_xlabel('Spearman rho vs matched baseline mean pair rankings');ax.set_title('V3-derived reconstruction: perturbation sensitivity');fig.tight_layout();fig.savefig(R/'FIG02_perturbation_sensitivity.png',dpi=180);plt.close(fig)

def mdtable(records,columns):
 header='| '+' | '.join(columns)+' |\n';line='| '+' | '.join(['---']*len(columns))+' |\n'
 return header+line+'\n'.join('| '+' | '.join(str(r.get(k,'')) for k in columns)+' |' for r in records)+'\n'
# Main text keeps original reported results out of its numerical claim base.
main=f'''# Evidence-channel-specific graph embeddings for Thai herbal medicine: A reproducible ten-herb computational feasibility reanalysis

**Manuscript status:** Author-review candidate, reconstructed-data analysis; not a verified reproduction of the earlier pilot.  
**Version:** Paper 1 v0.8, 7 November 2026.  
**Authors:** [To be entered by research team]. **Affiliation, corresponding author, journal:** [To be entered].

## Abstract

**Background:** Traditional herbal knowledge graphs combine heterogeneous documents and phytochemistry, yet seed-repeatable embeddings can be unstable when the underlying evidence changes. We investigated whether formula co-occurrence and constituent information could be represented as distinct computational channels in a fixed Thai herbal pilot without treating the resulting proximity as therapeutic equivalence.

**Methods:** Ten selected botanicals and ten official Thai traditional formulations were represented as 46 focal herb-formula memberships. Positive normalized pointwise mutual information (NPMI) generated a 23-edge herb co-occurrence graph. A V3-derived 30 herb-compound assertion proxy with 25 distinct compound labels and a subsequently curated **candidate** 19-class mapping supplied a separate chemical channel. Heterogeneous typed walks and 32-dimensional skip-gram embeddings were trained in 13 configurations across ten fixed random seeds (130 model fits). Analyses included seed-rank repeatability, NPMI and support/degree variants, deterministic chemistry pruning, and Cooc:Chem walk ratio changes. Internal formula-holdout results from the previous version were retained as exploratory context, not biological validation.

**Results:** Mean between-seed Spearman correlation across 45 unordered herb-pair rankings was **{sd['Cooc-NPMI']['rank_rho_mean']}** for Cooc, **{sd['Chem-Candidate19']['rank_rho_mean']}** for Chem, and **{sd['Core-Candidate19']['rank_rho_mean']}** for Core. The support/degree-adjusted Cooc variant reached **{sd['Cooc-Combined']['rank_rho_mean']}**, but this stability does not establish external predictive validity. Chemical pruning to two curated compounds per herb changed the Chem mean ranking considerably (Spearman **{sp['Chem-PruneFirst2']['mean_rank_spearman']}** relative to the candidate 19-class baseline). Equal walk counts did not ensure equal context contribution: Cooc accounted for approximately **{np.mean([float(r['effective_cooc_token_share']) for r in walks if r['model']=='Core-Candidate19']):.1%}** of tokens at a nominal 50:50 walk ratio.

**Conclusions:** Evidence-channel-specific computational representation was feasible in this fixed pilot, but its geometry depended on source selection, chemical annotations, walk schemas, and embedding initialization. These results establish neither biological similarity nor safety, efficacy, interchangeability, or generalization. The original Paper 1 chemical-class archive and exact model vectors were not recovered; all numerical results here are an explicitly separated **reanalysis**, not a claimed replication of earlier published-manuscript tables.

**Keywords:** Thai herbal medicine; knowledge graph; source provenance; NPMI; metapath walks; graph embedding; phytochemistry; robustness; computational feasibility.

## 1. Introduction

Evidence sources for traditional medicines vary in purpose and epistemic strength. Official formula compendia document recipe membership; phytochemical studies describe compounds observed in specific plants, tissues, extracts or analyses. Neither kind of relation, by itself, establishes shared clinical effects. If these channels are collapsed during graph construction, a high similarity score can become difficult to explain, and any subsequent apparent agreement with traditional categories may simply reflect labels already embedded in the training graph.

Knowledge graphs have become established in traditional Chinese medicine information management. HERB 2.0 integrates experimental and clinical evidence into a comprehensive knowledge resource (Gao et al., 2025), while quality frameworks have distinguished completeness, accuracy and usability (Liu et al., 2024). Heterogeneous network embedding approaches, including metapath2vec, motivate typed random-walk representations that respect different node and edge kinds (Dong et al., 2017). A small Thai herbal pilot provides a tractable setting for testing how such approaches behave when source provenance and channels are controlled.

The earlier ThaiHerb ten-herb manuscript described a source-grounded feasibility experiment and reported high seed-repeatability statistics for three sibling embeddings. However, the accessible project inputs do not contain the original 19-class chemical mapping or the archived vectors and walk corpora required for exact reproduction. The present work therefore has a deliberately narrower, transparent status: it is a reproducible **reanalysis on a versioned later-stage proxy**, designed to substantiate the feasibility argument while preventing historical and reconstructed outcomes from being combined as though computed from the same dataset. The objectives are: (1) construct separated formula and chemical evidence channels; (2) quantify descriptive seed-repeatability under the locked proxy; (3) document fragility under specified perturbations; and (4) isolate what is and is not supported by the resulting similarity rankings.

## 2. Materials and methods

### 2.1 Design and provenance boundary

This is a computational methodological feasibility reanalysis. The fixed sample includes ten focal herbs and ten selected formulas in the official Department of Thai Traditional and Alternative Medicine (DTAM) and Thai Food and Drug Administration (Thai FDA) compendium, B.E. 2566 (DTAM & Thai FDA, 2023). Formula information is a ten-herb **projection** of the complete prescriptions, not a complete pharmaceutical formula with amounts, preparations, or all constituent plants. The formulas were purposively selected and share a single documentary source, so they cannot be treated as an independent random sample of national practice. The source-reviewed projection was checked by one AI-assisted curator; this is not two-person adjudication.

The chemistry source contains 30 selected herb–compound claims (three per focal herb) spanning 25 distinct names. Compound presence is supported by a mixture of primary studies, public abstracts, government monographs, and other summaries; source qualification highlights differences in plant part, cultivar, extraction and compound identity. The 19 classes used in this reanalysis are **candidate assignments** prepared later from the v0.5 evidence review; they reproduce the reported class count but are **not authenticated equivalents** of the unavailable original taxonomy. PubChem candidate identifiers describe possible molecule identities and do not, by themselves, establish compound occurrence in a plant specimen (Kim et al., 2023).

The analytical data freeze is recorded as SHA-256 checksums for the four input files, and the full software and seed specifications are stored in `results/reanalysis_manifest.json`. An independent chemical target-label benchmark does not exist for this corpus.

### 2.2 Formula co-occurrence graph

An undirected pairwise Cooc projection was built from formula membership. For each herb pair (a,b), the population was ten formulas; p(a), p(b) and p(a,b) were estimated from occurrences across those records. We calculated normalized pointwise mutual information (NPMI) as

\\[\\mathrm{{NPMI}}(a,b)=\\frac{{\\log\\left[p(a,b)/(p(a)p(b))\\right]}}{{-\\log p(a,b)}}\\]

and retained only edges with NPMI > 0. For the locked proxy, this produced 23 positive edges among 45 possible undirected herb pairs. The edge weight used for sampling was positive NPMI. Support-aware and degree-corrected sampling were explicitly treated as **alternative computational weights** rather than changes in primary-source truth. For support adjustment, \\(w_{{ab}}=\\max(0,\\mathrm{{NPMI}}_{{ab}})n_{{ab}}/(n_{{ab}}+2)\\). Degree correction divided edge weight by \\((d_a d_b)^{{1/4}}\\); its choice was heuristic and **not tuned to independent biological labels**.

### 2.3 Typed chemical graph and Core mixture

The Chem graph connected herbs (H) to reported compounds (C) and their candidate classes (K). Typed walks used H–C–H and H–C–K–C–H motifs, attempting five sequential motifs per walk in this reconstructed implementation. This is a controlled methodological choice and must **not** be claimed to match every walk generated in the original unavailable archive. Cooc walks sampled up to twenty herb nodes and Chem walks followed the typed schema. The Core model combined walks from both sources by sequence count; a nominal 50:50 mixture was used as baseline. Token counts were separately measured to test whether equal sequence numbers entailed equal computational representation (they did not).

### 2.4 Training and repeatability

For each configuration and seed, sixty walks were initiated from each herb, yielding 600 walk sequences before any Cooc/Chem mixture. A skip-gram Word2Vec model was fitted with 32 dimensions, window 5, negative sampling 5, epochs 15, minimum count 1 and a single worker. Seeds were 11, 23, 37, 41, 53, 67, 79, 83, 97 and 101. The tokenizer included typed compound and class identifiers; herb similarity was calculated only between herb vectors. Every one of 45 unordered herb pairs was assigned cosine similarity. Seed-repeatability was summarized by the mean Spearman correlation among all 45 distinct pairs of seed rankings per model. Those 45 seed comparisons are **dependent** and were not used as independent inferential observations.

### 2.5 Prespecified analyses within this reanalysis

Thirteen configurations were run, comprising three sibling baselines, three alternative Cooc weights, three NPMI edge thresholds, one chemistry-pruning condition, two Core walk ratios, and one 18-class alternative annotation. Perturbation agreement was the Spearman correlation between the **mean similarity vectors across ten seeds** in a perturbed condition and its matched baseline, with supplementary paired-seed correlations and top-five overlap. Chemistry pruning deterministically retained the first two recorded compounds per herb; this is an **order-dependent stress test**, not an unbiased sample of all chemical perturbations. The Core ratios tested 25:75 and 75:25 Cooc:Chem walks in addition to 50:50.

A label-withheld descriptive diagnostic compared within- and between-family herb pairs. Family metadata were not supplied to the embedding trainer. This diagnostic is not external validation because herbs were present during unsupervised training. Separately, version v0.7 employed leave-one-formula-out (LOFO) co-occurrence ranking against simple structural baselines. That experiment is reported only in the Supplement: it evaluates co-occurrence in a withheld document from the same selected corpus, not biological similarity. The complete-model evaluation of one formula was blocked by a previously unseen herb (cold start).

### 2.6 Ethics, reproducibility and claim controls

No human participants, clinical records or identifiable data were analyzed. The project package includes the input data freeze, executable Python pipeline, complete per-seed cosine output, derived tables, source-review caveats, and integrity tests. It does **not** include the original missing pilot study class map, walk corpora, model files, or an independent expert validation study. The manuscript purposely avoids clinical claims and has no author approval, funding declaration, or journal-specific formatting certification.

## 3. Results

### 3.1 Fixed corpus

The source-reviewed ten-formula projection contained 46 herb–formula memberships, 54 absent entries and 100 possible formula × focal-herb cells. The 30 chemistry claims represented 25 unique names; 19 chemical classes were used as later candidate annotations. There were 45 unordered focal herb pairs, of which 23 had positive Cooc NPMI. All counts apply only to the selected pilot.

### 3.2 Seed repeatability of three separated evidence channels

Table 1 presents the full ten-seed reanalysis. The mean seed-pair rank correlations were {sd['Cooc-NPMI']['rank_rho_mean']} (Cooc), {sd['Chem-Candidate19']['rank_rho_mean']} (Chem), and {sd['Core-Candidate19']['rank_rho_mean']} (Core). Importantly, these results differ from the earlier manuscript's reported 0.946/0.977/0.945; the original chemical training archive has not been recovered and the two result sets cannot be considered exact replicates. The positive conclusion supported here is **computational feasibility and descriptive repeatability of a particular reanalysis**, not the reproduction of every historical score.

**Table 1. Seed-repeatability of v0.8 proxy-data reanalysis**

{mdtable([{'Model':n,'Mean rho':sd[k]['rank_rho_mean'],'SD':sd[k]['rank_rho_sd_population'],'Minimum':sd[k]['rank_rho_min']} for n,k in [('Cooc','Cooc-NPMI'),('Chem','Chem-Candidate19'),('Core','Core-Candidate19'),('Cooc combined','Cooc-Combined')]],['Model','Mean rho','SD','Minimum'])}

![Figure 1. Reconstructed seed-repeatability, ten seeds.](../results/FIG01_seed_rank_stability.png)

### 3.3 Structural perturbations and chemical curation dependence

Changing the Cooc NPMI threshold from 0 to .05 or .15 largely preserved the mean rank order, with Spearman correlations {sp['Cooc-thr0p05']['mean_rank_spearman']} and {sp['Cooc-thr0p15']['mean_rank_spearman']}; at .30, correlation decreased to {sp['Cooc-thr0p30']['mean_rank_spearman']}. Cooc support-and-degree correction increased seed repeatability to {sd['Cooc-Combined']['rank_rho_mean']}, but no conclusion about external validity follows. For Chem, deterministic reduction from three to two compounds per herb resulted in mean rank correlation {sp['Chem-PruneFirst2']['mean_rank_spearman']} against its 19-class candidate baseline. This is a demonstration of selection sensitivity and must not be interpreted as statistical evidence about all alternative two-compound subsets. As shown in Figure 2, changing the relative Cooc and Chem walk mixture also altered Core rankings.

**Table 2. Main perturbation comparisons (v0.8)**

{mdtable([{'Perturbation':name,'Rank rho':sp[k]['mean_rank_spearman'],'Top 5 overlap':sp[k]['top5_overlap_mean_vectors']} for name,k in [('Cooc > 0.05','Cooc-thr0p05'),('Cooc > 0.15','Cooc-thr0p15'),('Cooc > 0.30','Cooc-thr0p30'),('Chem 2 per herb','Chem-PruneFirst2'),('Core 25:75','Core-Cooc25'),('Core 75:25','Core-Cooc75')]],['Perturbation','Rank rho','Top 5 overlap'])}

![Figure 2. Mean-rank perturbation sensitivity.](../results/FIG02_perturbation_sensitivity.png)

### 3.4 Effective channel contribution and label-withheld diagnostics

Equal Cooc and Chem walk **counts** did not result in equal token representation. At a 50:50 walk ratio the Cooc channel contributed approximately {np.mean([float(r['effective_cooc_token_share']) for r in walks if r['model']=='Core-Candidate19']):.1%} of all tokens; these are token counts, not necessarily effective negative-sampling context pairs or causal attribution to channel information. Mean within-family cosine exceeded mean between-family cosine by {family[0]['descriptive_difference']} in Cooc, {family[1]['descriptive_difference']} in Chem, and {family[2]['descriptive_difference']} in Core. Only four within-family pairs existed; these differences are descriptive, non-independent and unadjusted.

### 3.5 Internal formula holdout is not a success metric for clinical relevance

In the prior v0.7 LOFO analysis, nine of ten formulas allowed a fair full 45-pair comparison, and PairSupport achieved mean AP 0.419 compared with 0.395 for Cooc-NPMI, 0.275 for Chem-Proxy and 0.292 for Core-Proxy. The blocked fold suffered a previously unseen herb, not missing data imputed using the held-out formula. This was a narrow documentation co-occurrence test rather than a separate chemical truth set. Although embeddings did not outperform the simple structural baseline for this task, this does not negate feasibility of constructing channel-separated representations. It does limit claims of predictive advantage.

## 4. Discussion

The principal positive finding is that it is feasible to construct distinguishable and programmatically reproducible herb representations using two separated evidence channels in a fixed ten-herb pilot. The new results reinforce the methodological caution in the earlier research: seed agreement is not sufficient evidence of robust scientific knowledge. More complicated graph walks and embedding objectives did not consistently improve the internal held-out co-occurrence task beyond basic pair support. Different edge weighting rules modify random-walk sampling, not the epistemic quality of the underlying documentary or laboratory assertion.

The chemical channel presented the greatest evidence-dependence problem. The panel contained only three curated compound associations per herb, selected for demonstration rather than exhaustiveness. Loss of one of these records can change the topology and the learned geometry disproportionately; source-holdout results in v0.6 show that, for many original source IDs, a single removal leaves at least one herb unrepresented. Furthermore, botanical species, cultivar, plant part and preparation can be mismatched in literature citations. A compound detected in distilled oil should not automatically be asserted for fresh tissues, and mixed-species pharmacopoeial materials cannot by themselves authenticate a species-specific occurrence.

Equal numbers of formula and chemical walks did not mean equal data contributions. This observation should inform future work that compares normalized context-pair counts or trains separately normalized channel vectors before fusion. For a small pilot it is more important to make that issue visible than to fit a parameter-rich fusion model whose external performance cannot be evaluated.

**Original-results reconciliation.** The revised research workflow is not an exact reproduction of the pre-existing ten-herb manuscript. The earlier document reported Cooc/Chem/Core seed correlations of 0.946/0.977/0.945 and Chem pruning agreement of 0.226; the new proxy based on candidate chemical classes yields different results. No unpublished archive, source passage or original class map has been invented to explain away those differences. The historical results must be described as reported in the original manuscript and should not appear mixed with new manuscript Tables 1–2 as a single analysis.

### 4.1 Limitations

First, the corpus is purposefully small and selected, inducing support sparsity, dependency between paired herb observations, cold start, and possible preferential selection. Second, co-occurrence is not a proxy for therapeutic mechanism. Third, the chemical claims and nineteen-class taxonomy were reconstructed from later evidence; precise row-level full-text citations and compound isomer identities have not all been independently adjudicated. Fourth, the original 19-class pilot archive and embedding vectors could not be recovered, restricting historical reproducibility. Fifth, Word2Vec cosine rankings have not been validated against independent herb-pair biological annotations. Sixth, stability statistics across seed pairs are descriptive because correlations share seeds. Finally, the LOFO test relies on formulas from a single official source and its non-co-occurrence labels cannot be treated as chemically negative herb pairs.

## 5. Conclusion

A fixed ten-herb Thai herbal pilot supports the computational feasibility of separating formula co-occurrence and phytochemical-context evidence into different graph embeddings. Under the present reconstructed proxy, the representations exhibit nontrivial seed agreement but substantial fragility to chemical evidence selection. A 50:50 number of input walks does not imply a 50:50 amount of model context. This pilot provides a transparent demonstration of provenance-aware, leakage-conscious sensitivity analysis, **not** evidence of therapeutic equivalence or prediction superiority. Scientific generalizability and expert-rated biological validity require a subsequent expanded study.

## Data and code availability

The v0.8 research package includes inputs, parameter/configuration records, checksum manifests, scripts, per-seed cosine output, 13-model comparison tables and exploratory supplement. Source code is available separately in the project's GitHub branch; the full research package is stored in the project's Google Drive research folder. The original experimental chemical class table and raw trained vectors are unavailable in the accessible archive and no exact-match re-run is asserted.

## Declarations

**Ethics:** Public documentary and published chemistry data were used; no patients, participants or animals were studied in this computational pilot.  
**Funding:** [Authors to confirm].  
**Conflicts of interest:** [Authors to confirm].  
**Author contributions:** [Authors to provide].  
**AI assistance:** AI tools were used in evidence triage, code drafting and manuscript editing; numeric results were generated by code on the versioned proxy dataset and checked by automated tests. Authors retain responsibility for the accuracy of references, botanical identity and final claims.  
**Data provenance limitations:** The original archived chemistry classification is not available; the later mapping is explicitly labeled a candidate reconstruction.

## References (APA 7th edition)

Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In C. Chiarcos, R. Eckart de Castilho, & M. Stede (Eds.), *From form to meaning: Processing texts automatically: Proceedings of the Biennial GSCL Conference 2009* (pp. 31–40). Gunter Narr Verlag.

Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง: ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566* [Reference information for herbal products for notification: Thai traditional medicine formulations, B.E. 2566]. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. In *Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 135–144). Association for Computing Machinery. https://doi.org/10.1145/3097983.3098036

Gao, K., Liu, L., Lei, S., Li, Z., Huo, P., Wang, Z., Dong, L., Deng, W., Bu, D., Zeng, X., Li, C., Zhao, Y., Zhang, W., Wang, W., & Wu, Y. (2025). HERB 2.0: An updated database integrating clinical and experimental evidence for traditional Chinese medicine. *Nucleic Acids Research, 53*(D1), D1404–D1414. https://doi.org/10.1093/nar/gkae1037

Kim, S., Chen, J., Cheng, T., Gindulyte, A., He, J., He, S., Li, Q., Shoemaker, B. A., Thiessen, P. A., Yu, B., Zaslavsky, L., Zhang, J., & Bolton, E. E. (2023). PubChem 2023 update. *Nucleic Acids Research, 51*(D1), D1373–D1380. https://doi.org/10.1093/nar/gkac956

Liu, C., Li, Z., Li, J., Qu, Y., Chang, Y., Han, Q., Cao, L., & Lin, S. (2024). Research on traditional Chinese medicine: Domain knowledge graph completion and quality evaluation. *JMIR Medical Informatics, 12*, e55090. https://doi.org/10.2196/55090

Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. *International Conference on Learning Representations*. https://arxiv.org/abs/1301.3781
'''
(M/'Paper1_Feasibility_Reanalysis_v08.md').write_text(main,encoding='utf-8')
# Editorial & supplement note including historical reconciliation.
reports=f'''# Paper 1 v0.8 — Reproducibility and Editorial Decision Record

Date: 2026-11-07. Reviewer: ChatGPT-assisted computational/editorial review (NOT independent specialist review).

## Scientific recommendation

**Feasibility claim: supported within a locked reconstruction.**  
**Exact replication of original manuscript: NOT SUPPORTED.**  
**External biological validation: NOT UNDERTAKEN.**  
**Submission readiness: CONDITIONALLY NOT APPROVED pending author signoff and original vs reconstructed study selection.**

The original manuscript presents results from a 10-herb, 10-formula, 30 chemistry-assertion, 19-class study and describes an archive not accessible in the currently shared project. Reanalysis v0.8 uses a V3-derived proxy and AI-assisted candidate class annotations and therefore **must be treated as a new reanalysis, not a replacement without editorial disclosure**.

## Original versus candidate reanalysis

{mdtable([{'Analysis':r['original_manuscript_label'],'Original':r['archived_manuscript_value'],'v0.8 reanalysis':r['fresh_reanalysis_value']} for r in reconc],['Analysis','Original','v0.8 reanalysis'])}

## Locked method inventory

- 10 herbs, 10 selected documentary formulas, 46 present formula memberships, 100 reviewed cells.
- 30 phytochemical assertions, 25 compounds, 19 **candidate** chemical classes.
- 23 positive NPMI edges among 45 possible herb pairs.
- 13 model/perturbation configurations × 10 paired seeds = 130 fits.
- 32 dimensions, 60 walks per herb, skip-gram, window 5, negative samples 5, epochs 15, one worker.
- Perturbation metrics are descriptive; no independent herb-pair clinical or biological truth labels are supplied.
- Source checks are AI-assisted and contain material/part/cultivar limitations; original wet-lab statements are not validated by this analysis.

## Manuscript integration rules

1. Use **either** the archived original manuscript's results with proper reproducibility evidence **or** the newly regenerated v0.8 results as the main results; never interleave their numbers as if from the same run.
2. Treat v0.7 LOFO as supplementary task-specific evidence; PairSupport mean AP 0.419 exceeded Cooc 0.395 and Chem/Core 0.275/0.292, without implying failed feasibility.
3. Do not use v0.3's erroneous deletion of F05 memberships; the official ingredient table spans printed pages 161–162.
4. Do not describe candidate 19 chemical classes as the original 19.
5. Author review remains mandatory: chemical occurrence primary full-text, original class definitions, author declarations, journal instructions and research reporting policy.
6. Do not convert the blank expert-review sheets into machine-generated positive/negative gold labels.

## Research boundaries

- Not a proof of efficacy, clinical similarity, safety, substitution, or pharmacological equivalence.
- Source count is not evidence quality weight.
- Pairwise seed correlations are not 45 independent samples.
- Formula holdout is single-corpus document validation and is not an independent biological benchmark.
- No matching of original trained vectors is claimed.

## Stop-go gate

**Go** for internal author review of a self-consistent computational feasibility draft. **No-go** for claiming fully reproduced original paper or independent biological validity. The journal submission decision must be signed by actual authors after verifying botanical/chemical references.
'''
(D/'PUBLICATION_FINALIZATION_REPORT_TH.md').write_text(reports,encoding='utf-8')
# Publish a supplementary analysis CSV inventory as a clear data dictionary.
inventory=[
 ('cooc_pair_weights_45.csv','All unordered pair support, NPMI, positive NPMI','45','formula-derived'),
 ('all_reanalysis_scores_13models_10seeds.csv','130 fits x 45 pair cosine values','5850','V3-derived reconstruction'),
 ('seed_repeatability_13models.csv','Descriptive seed-pair correlation of each model','13','reanalysis'),
 ('perturbation_sensitivity_10comparisons.csv','Paired perturbation comparison with baseline','10','reanalysis'),
 ('core_channel_contributions_by_seed.csv','Source walk counts and effective token shares','30','reanalysis'),
 ('botanical_family_descriptive_3models.csv','Family label-withheld descriptive diagnostics','3','not external validation'),
 ('ORIGINAL_MANUSCRIPT_VS_V08_REANALYSIS.csv','Historical/reanalysis reconciliation','9','not exact original replication'),
 ('PUBLICATION_READINESS_GATES.csv','Editorial and scientific release gate tracker','10','reviewer-only'),
 ('model_comparison_cluster_bootstrap.csv','v0.7 heldout formula internal ranking','9','supplementary; not external similarity')]
with (D/'DATA_DICTIONARY.md').open('w') as f:
 f.write('# Data dictionary and evaluation status\n\n| File | Meaning | Rows | Status |\n|---|---|---:|---|\n')
 for a,b,c,d in inventory:f.write(f'| `{a}` | {b} | {c} | {d} |\n')
 f.write('\nAll numerical results labeled reanalysis come from fixed V3-derived proxy inputs, not the missing original class map. Inputs are in `data/`; output hashes are in `SHA256_MANIFEST.json`.\n')
print(json.dumps({'main_chars':len(main),'report_chars':len(reports),'tables':len(reconc),'output_root':str(ROOT)}))