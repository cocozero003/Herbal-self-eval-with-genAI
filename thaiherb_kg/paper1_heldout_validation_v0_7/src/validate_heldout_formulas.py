"""Locked, per-formula out-of-sample proxy validation for the ThaiHerb ten-herb pilot.

Do not interpret held-out formula co-occurrence as clinical, pharmacological or
independently adjudicated similarity. All predictions are computed after removal
of the entire test formula from the formula-derived training data.
"""
from __future__ import annotations
import csv, hashlib, itertools, json, math, random, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, ndcg_score
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import model_reanalysis as model
from formula_audit import npmi
OUT=ROOT/'results';DATA=ROOT/'data'
SEEDS=[11,23,37,41,53,67,79,83,97,101]
PAIR_NAMES=['DegreeProduct','PairSupport','ClassJaccard','Cooc-NPMI','Cooc-Support','Cooc-Degree','Cooc-Combined','Chem-Proxy','Core-Proxy']
MODEL_NAMES=['Cooc-NPMI','Cooc-Support','Cooc-Degree','Cooc-Combined','Chem-Proxy','Core-Proxy']

def readcsv(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows):
 if not rows:raise ValueError('no rows')
 p.parent.mkdir(parents=True,exist_ok=True)
 with open(p,'w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def mscore(y,s):
 y=np.asarray(y,dtype=int);s=np.asarray(s,dtype=float)
 if len(np.unique(y))!=2:raise ValueError('Need both classes')
 if not np.isfinite(s).all():raise ValueError('nonfinite predictions')
 order=np.lexsort((np.arange(len(s)), -s))
 k=min(5,len(s))
 return {'auroc':float(roc_auc_score(y,s)),
         'average_precision':float(average_precision_score(y,s)),
         'precision_at_5':float(np.mean(y[order[:k]])),
         'ndcg_at_5':float(ndcg_score([y],[s],k=k))}

def training_formula_scores(formulas,ids,pairs):
 counts=Counter(h for f in formulas for h in f['herbs']);joint=Counter()
 for f in formulas:
  for a,b in itertools.combinations(sorted(f['herbs']),2):joint[a,b]+=1
 deg=np.array([counts[a]*counts[b] for a,b in pairs],float)
 pair=np.array([joint[a,b] for a,b in pairs],float)
 return deg,pair

def class_scores(chem,tax,pairs):
 classes=defaultdict(set)
 for a in chem:classes[a['subject_id']].add(tax[a['object_label']])
 return np.array([len(classes[a]&classes[b])/max(1,len(classes[a]|classes[b])) for a,b in pairs],float)

def candidate_models(formulas,chem,ids,seeds):
 bymodel=defaultdict(list)
 for seed in seeds:
  c1=model.generate_cooc(formulas,ids,seed,'npmi')
  chemseq=model.generate_chem(chem,ids,seed)
  for key in ('Cooc-NPMI','Cooc-Support','Cooc-Degree','Cooc-Combined','Chem-Proxy','Core-Proxy'):
   if key=='Cooc-NPMI':seq=c1
   elif key.startswith('Cooc-'):seq=model.generate_cooc(formulas,ids,seed,key.split('-')[1].lower())
   elif key=='Chem-Proxy':seq=chemseq
   else:
    seq=c1[:len(c1)//2]+chemseq[:len(chemseq)//2]
    random.Random(seed).shuffle(seq)
   bymodel[key].append(model.cos_vectors(seq,ids,seed))
 return {name:np.mean(vals,axis=0) for name,vals in bymodel.items()},bymodel

def bootstrap_fold_means(rows,field='average_precision',B=3000,seed=42):
 rng=np.random.default_rng(seed)
 vals=np.array([float(r[field]) for r in rows],float)
 n=len(vals)
 draws=rng.integers(0,n,(B,n))
 d=vals[draws].mean(axis=1)
 return float(np.quantile(d,.025)),float(np.quantile(d,.975))

def fast_average_precision(y,score):
 y=np.asarray(y,dtype=int);score=np.asarray(score,dtype=float)
 # Exact step-wise average precision with tied score groups, consistent with sklearn.
 order=np.argsort(-score,kind='stable');yy=y[order];ss=score[order]
 pos=int(yy.sum());cum_pos=0;seen=0;ap=0.0
 for _,group in itertools.groupby(zip(ss,yy),key=lambda z:z[0]):
  batch=list(group);seen+=len(batch);p=sum(int(z[1]) for z in batch);cum_pos+=p
  ap+=(cum_pos/seen)*(p/pos)
 return ap

def permutation_exact_signflip(delta):
 v=np.asarray(delta,float)
 obs=abs(float(v.mean()))
 perm=[abs(float(np.mean(v*np.array(signs)))) for signs in itertools.product((-1,1),repeat=len(v))]
 return float(sum(z>=obs-1e-12 for z in perm)/len(perm))

def run():
 OUT.mkdir(parents=True,exist_ok=True)
 source=DATA/'paper1_bootstrap_v3_proxy.json'
 d=json.loads(source.read_text(encoding='utf-8'))
 official=json.loads((DATA/'formula_reviewed_snapshot.json').read_text(encoding='utf-8'))
 assert len(official['formulas'])==10 and len(d['herbs'])==10
 ids=[h['id'] for h in d['herbs']]
 pairs=list(itertools.combinations(ids,2))
 assert len(pairs)==45
 # Formulas are from model-assisted single-curator source review, not independent adjudication.
 formulas=official['formulas']
 chem=[a for a in d['assertions'] if a['assertion_type']=='ChemistryOccurrenceAssertion']
 tax={r['name']:r['class_v05'] for r in readcsv(DATA/'CHEMICAL_IDENTITY_TAXONOMY_25.csv')}
 assert len(chem)==30 and len(tax)==25 and len(set(tax.values()))==19
 model.CLASS.clear();model.CLASS.update(tax)
 cscore=class_scores(chem,tax,pairs)
 all_fold=[];foldscores=[];predictions=[];seed_detail=[];leakage_checks=[]
 for heldout in formulas:
  fid=heldout['id'];train=[f for f in formulas if f['id']!=fid]
  assert len(train)==9 and all(f['id']!=fid for f in train)
  counts=Counter(h for f in train for h in f['herbs'])
  unseen=[h for h in ids if counts[h]==0]
  eligibility=not unseen
  y=np.array([int(a in heldout['herbs'] and b in heldout['herbs']) for a,b in pairs],int)
  assert 0<y.sum()<45
  all_fold.append({'heldout_formula_id':fid,'training_formulas':len(train),
   'train_formula_ids':';'.join(f['id'] for f in train),'test_formula_id_absent_from_training':int(fid not in [f['id'] for f in train]),
   'test_focal_herbs':len(heldout['herbs']),'positive_pair_labels':int(y.sum()),
   'negative_pair_labels':int((1-y).sum()),'label_prevalence':float(y.mean()),
   'unseen_herbs_in_train':';'.join(unseen),'full_45_pair_comparison_eligible':int(eligibility),
   'ineligibility_reason':'COLD_START_UNREPRESENTED_HERB' if unseen else ''})
  deg,supp=training_formula_scores(train,ids,pairs)
  if not eligibility:continue
  # Deliberate invalid oracle: include the held-out formula to quantify how label leakage can inflate the same PairSupport score.
  _,leaked_supp=training_formula_scores(formulas,ids,pairs)
  _,proper_supp=training_formula_scores(train,ids,pairs)
  leakage_checks.append({'heldout_formula_id':fid,
    'proper_pair_support_AP':float(average_precision_score(y,proper_supp)),
    'invalid_leaked_pair_support_AP':float(average_precision_score(y,leaked_supp)),
    'leakage_delta_AP':float(average_precision_score(y,leaked_supp)-average_precision_score(y,proper_supp)),
    'invalid_oracle_is_for_diagnostic_only':1})
  preds,per_seed=candidate_models(train,chem,ids,SEEDS)
  preds.update({'DegreeProduct':deg,'PairSupport':supp,'ClassJaccard':cscore})
  for name in PAIR_NAMES:
   s=np.asarray(preds[name],float)
   assert s.shape==(45,)
   metric=mscore(y,s)
   foldscores.append({'heldout_formula_id':fid,'method':name,'seeds_averaged':10 if name in MODEL_NAMES else 0,
     'positives':int(y.sum()),'chance_prevalence':float(y.mean()),**metric})
   for i,(a,b) in enumerate(pairs):predictions.append({'heldout_formula_id':fid,'herb_a':a,'herb_b':b,
     'pair_label_is_cooccurrence_in_heldout_formula':int(y[i]),'method':name,
     'prediction_score_without_heldout_formula':float(s[i]),'training_formula_count':len(train),
     'not_biological_ground_truth':1})
  for name,vectors in per_seed.items():
   for seed,score in zip(SEEDS,vectors):
    ss=mscore(y,score)
    seed_detail.append({'heldout_formula_id':fid,'method':name,'seed':seed,**ss})
 writecsv(OUT/'fold_eligibility_10.csv',all_fold)
 writecsv(OUT/'heldout_pair_predictions.csv',predictions)
 writecsv(OUT/'per_fold_metrics.csv',foldscores)
 writecsv(OUT/'seed_variance_diagnostics.csv',seed_detail)
 writecsv(OUT/'label_leakage_demonstration.csv',leakage_checks)
 summary=[]
 for name in PAIR_NAMES:
  rows=[r for r in foldscores if r['method']==name]
  low,high=bootstrap_fold_means(rows)
  summary.append({'method':name,'eligible_folds':len(rows),'distinct_formulas_total':len(formulas),
      'mean_auroc':round(float(np.mean([r['auroc'] for r in rows])),6),
      'mean_average_precision':round(float(np.mean([r['average_precision'] for r in rows])),6),
      'ap_cluster_bootstrap_95ci_low':round(low,6),'ap_cluster_bootstrap_95ci_high':round(high,6),
      'mean_precision_at_5':round(float(np.mean([r['precision_at_5'] for r in rows])),6),
      'mean_ndcg_at_5':round(float(np.mean([r['ndcg_at_5'] for r in rows])),6),
      'mean_positive_prevalence':round(float(np.mean([r['chance_prevalence'] for r in rows])),6),
      'independent_expert_gold_available':0,'scientific_status':'INTERNAL_HELDOUT_FORMULA_PROXY_ONLY'})
 writecsv(OUT/'model_comparison_cluster_bootstrap.csv',summary)
 # Exact fold-level sign flip vs a structural, label-blind baseline. Exploratory only.
 ref={r['heldout_formula_id']:r['average_precision'] for r in foldscores if r['method']=='PairSupport'}
 comparisons=[]
 for name in PAIR_NAMES:
  if name=='PairSupport':continue
  rr=[r for r in foldscores if r['method']==name]
  delta=[r['average_precision']-ref[r['heldout_formula_id']] for r in rr]
  comparisons.append({'method':name,'reference':'PairSupport','paired_folds':len(delta),
         'mean_AP_delta':round(float(np.mean(delta)),7),
         'exact_signflip_p_exploratory':round(permutation_exact_signflip(delta),7),
         'multiple_testing_corrected':0,'confirmatory_significance_claim':0})
 writecsv(OUT/'paired_signflip_exploratory.csv',comparisons)
 # Label permutation sanity check, shuffle labels strictly within each held-out formula.
 rng=np.random.default_rng(20261107)
 fold_ids=sorted({r['heldout_formula_id'] for r in foldscores})
 empirical=np.mean([r['average_precision'] for r in foldscores if r['method']=='PairSupport'])
 baseline={fid:(np.array([int(r['pair_label_is_cooccurrence_in_heldout_formula']) for r in predictions if r['heldout_formula_id']==fid and r['method']=='PairSupport'],int),
               np.array([float(r['prediction_score_without_heldout_formula']) for r in predictions if r['heldout_formula_id']==fid and r['method']=='PairSupport'],float)) for fid in fold_ids}
 perm_means=[]
 for _ in range(2000):
  perm_means.append(float(np.mean([fast_average_precision(rng.permutation(baseline[fid][0]),baseline[fid][1]) for fid in fold_ids])))
 permutation={'observed_pair_support_mean_AP':round(float(empirical),6),
              'label_permuted_mean_AP_mean':round(float(np.mean(perm_means)),6),
              'label_permuted_AP_95pct_quantiles':[round(float(z),6) for z in np.quantile(perm_means,[.025,.975])],
              'one_sided_permutation_p_exploratory':round((1+sum(z>=empirical for z in perm_means))/(1+len(perm_means)),7),
              'repetitions':2000,'within_fold_label_shuffle':True,'not_independent_external_validation':True}
 (OUT/'null_permutation_summary.json').write_text(json.dumps(permutation,ensure_ascii=False,indent=2),encoding='utf-8')
 manifest={
  'version':'v0.7','task':'within-corpus held-out-formula pair-cooccurrence ranking (NOT expert similarity)',
  'formula_count_total':10,'eligible_full_45pair_folds':sum(f['full_45_pair_comparison_eligible'] for f in all_fold),
  'ineligible_full_45pair_folds':[f['heldout_formula_id'] for f in all_fold if not f['full_45_pair_comparison_eligible']],
  'heldout_prediction_rows':len(predictions),'per_fold_metric_rows':len(foldscores),
  'seed_diagnostic_rows':len(seed_detail),'models':PAIR_NAMES,'seeds':SEEDS,
  'heldout_entire_formula_from_train':True,'cooc_only_train_9_formulas_each_fold':True,
  'chemistry_fixed_V3_derived_30_assertions':True,
  'all_formula_labels_from_same_10_formula_official_compendium':True,
  'independent_external_dataset':False,'independent_expert_gold_labels':False,
  'non_cooccurrence_is_not_biological_dissimilarity':True,
  'candidate_19_chemical_classes_not_recovered_from_original_paper1':True,
  'label_leakage_oracle_diagnostic':True,'observed_mean_oracle_AP':float(np.mean([z['invalid_leaked_pair_support_AP'] for z in leakage_checks])),
  'mean_proper_pair_AP':float(np.mean([z['proper_pair_support_AP'] for z in leakage_checks])),
  'test_input_sha256':sha(source),'formula_snapshot_sha256':sha(DATA/'formula_reviewed_snapshot.json'),
  'expert_form_scores_intentionally_blank':True,
  'selection_bias':'the ten formulas and herbs were selected in the original research; LOFO results do not generalize beyond those formulas',
  'model_warning':'Word2Vec embedding methods were NOT re-tuned on heldout labels; coarse 10-formula exploratory data',
  'citation':'Briere et al. 2026, Bioinformatics, doi:10.1093/bioinformatics/btag608',
  'interpretation':'Performance measures recovering co-occurrence in one withheld formula, not pharmacological, therapeutic, clinical or expert-rated similarity.'}
 (OUT/'benchmark_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
 return summary,manifest

if __name__=='__main__':
 summary,manifest=run()
 print(json.dumps({'summary':summary,'manifest':manifest},ensure_ascii=False,indent=2))