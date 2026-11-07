"""Paper 1 computational feasibility reanalysis from version-frozen reconstructed inputs.

Honesty boundary: V3-derived 30 asserted compounds and AI-candidate 19 classes
are not authenticated copies of the original 10-herb Paper 1 training archive.
"""
from __future__ import annotations
import csv, hashlib, itertools, json, math, os, platform, random, sys
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
import scipy
import gensim
from scipy.stats import spearmanr
from gensim.models import Word2Vec
ROOT = Path(__file__).resolve().parents[1]
SEEDS = [11,23,37,41,53,67,79,83,97,101]

def readcsv(f):
 with open(f,'r',encoding='utf-8-sig',newline='') as inp:return list(csv.DictReader(inp))
def dumpcsv(f,rows):
 assert rows
 with open(f,'w',encoding='utf-8-sig',newline='') as out:
  w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def seedhash(s):return int.from_bytes(hashlib.sha256(s.encode('utf8')).digest()[:8],'big')
def statistic(v):
 v=np.asarray(v,float)
 return {'mean':round(float(np.mean(v)),6),'sd_population':round(float(np.std(v)),6),'min':round(float(np.min(v)),6),'max':round(float(np.max(v)),6)}
def pair_npmi(formulas,herbs):
 sets={h:set(f['id'] for f in formulas if h in f['herbs']) for h in herbs}
 n=len(formulas);out=[]
 for a,b in itertools.combinations(herbs,2):
  k=len(sets[a]&sets[b]);pa=len(sets[a])/n;pb=len(sets[b])/n
  val=math.log((k/n)/(pa*pb))/-math.log(k/n) if 0<k<n else 0.
  out.append({'herb_a':a,'herb_b':b,'support':k,'npmi':val,'positive_npmi':max(val,0.)})
 return out

def cooc_walks(formulas,herbs,seed,threshold=0,mode='npmi'):
 pairs=pair_npmi(formulas,herbs)
 degree=Counter()
 for row in pairs:
  if row['positive_npmi']>0:
   degree.update([row['herb_a'],row['herb_b']])
 adjacency=defaultdict(list)
 for r in pairs:
  a,b=r['herb_a'],r['herb_b'];v=r['positive_npmi'];n=r['support']
  if v<=threshold or v<=0:continue
  if mode in ('support','combined'):v *= n/(n+2.)
  if mode in ('degree','combined'):v /= max(1,degree[a]*degree[b])**.25
  adjacency[a].append((b,v));adjacency[b].append((a,v))
 rnd=random.Random(seed);walks=[]
 for h in herbs:
  for i in range(60):
   walk=[h]
   for k in range(19):
    adj=adjacency[walk[-1]]
    if not adj:break
    walk.append(rnd.choices([a for a,w in adj],weights=[w for a,w in adj],k=1)[0])
   walks.append(walk)
 rnd.shuffle(walks)
 return walks

def chem_walks(chem,herbs,classes,seed):
 byh=defaultdict(list);byc=defaultdict(list);byk=defaultdict(set)
 for r in chem:
  h=r['subject_id'];c=r['object_label'];k=classes[c]
  byh[h].append(c);byc[c].append(h);byk[k].add(c)
 byk={k:sorted(v) for k,v in byk.items()}
 rnd=random.Random(seed);paths=[]
 for h in herbs:
  for i in range(60):
   path=[h];here=h
   for j in range(5):
    if not byh[here]:break
    c=rnd.choice(byh[here]);k=classes[c]
    if rnd.random()<.5:
     neigh=rnd.choice(byc[c]);path.extend(['C:'+c,neigh]);here=neigh
    else:
     c2=rnd.choice(byk[k]);neigh=rnd.choice(byc[c2]);path.extend(['C:'+c,'K:'+k,'C:'+c2,neigh]);here=neigh
   paths.append(path)
 rnd.shuffle(paths)
 return paths

def merge_walks(co,chem,seed,ratio=.5):
 assert 0<=ratio<=1
 n=len(co);assert n==len(chem)==600
 nco=int(round(n*ratio));nch=n-nco
 combined=co[:nco]+chem[:nch]
 random.Random(seed).shuffle(combined)
 return combined,{'cooc_walks':nco,'chem_walks':nch,'cooc_tokens':sum(map(len,co[:nco])),'chem_tokens':sum(map(len,chem[:nch]))}

def train_one(corpus,ids,seed):
 m=Word2Vec(sentences=corpus,vector_size=32,window=5,min_count=1,sg=1,negative=5,epochs=15,workers=1,seed=seed,hashfxn=seedhash,sample=.001)
 return np.array([float(m.wv.similarity(a,b)) if a in m.wv and b in m.wv else np.nan for a,b in itertools.combinations(ids,2)])

def run():
 root=ROOT;out=root/'results';out.mkdir(exist_ok=True)
 data=json.loads((root/'data/paper1_bootstrap_v3_proxy.json').read_text(encoding='utf8'))
 snap=json.loads((root/'data/formula_reviewed_snapshot.json').read_text(encoding='utf8'))
 tax=readcsv(root/'data/CHEMICAL_IDENTITY_TAXONOMY_25.csv')
 cl19={r['name']:r['class_v05'] for r in tax};cl18={r['name']:r['class_v04'] for r in tax}
 assert len(cl19)==25 and len(set(cl19.values()))==19 and len(set(cl18.values()))==18
 ids=[h['id'] for h in data['herbs']];assert len(ids)==10 and len(snap['formulas'])==10
 formulas=snap['formulas'];chem=[r for r in data['assertions'] if r['assertion_type']=='ChemistryOccurrenceAssertion']
 assert len(chem)==30 and set(r['object_label'] for r in chem)==set(cl19)
 pairs=list(itertools.combinations(ids,2));npmi=pair_npmi(formulas,ids)
 assert len(pairs)==45 and sum(r['positive_npmi']>0 for r in npmi)==23
 dumpcsv(out/'cooc_pair_weights_45.csv',[{k:round(v,8) if isinstance(v,float) else v for k,v in x.items()} for x in npmi])
 # Four thresholds, chemistry pruning and mixing ratio each rerun using paired seeds.
 variants=['Cooc-NPMI','Cooc-Support','Cooc-Degree','Cooc-Combined','Chem-Candidate19','Core-Candidate19',
  'Cooc-thr0p05','Cooc-thr0p15','Cooc-thr0p30','Chem-PruneFirst2','Core-Cooc25','Core-Cooc75','Chem-Candidate18']
 sim=defaultdict(dict);detail=[];tokenstats=[]
 chem_pruned=[];perherb=Counter()
 for r in chem:
  if perherb[r['subject_id']]<2:chem_pruned.append(r)
  perherb[r['subject_id']]+=1
 assert len(chem_pruned)==20
 for seed in SEEDS:
  co=cooc_walks(formulas,ids,seed);ch=chem_walks(chem,ids,cl19,seed);ch18=chem_walks(chem,ids,cl18,seed)
  chprune=chem_walks(chem_pruned,ids,cl19,seed)
  corpus={
   'Cooc-NPMI':co,'Cooc-Support':cooc_walks(formulas,ids,seed,mode='support'),
   'Cooc-Degree':cooc_walks(formulas,ids,seed,mode='degree'),
   'Cooc-Combined':cooc_walks(formulas,ids,seed,mode='combined'),
   'Chem-Candidate19':ch,'Chem-Candidate18':ch18,'Chem-PruneFirst2':chprune,
   'Cooc-thr0p05':cooc_walks(formulas,ids,seed,threshold=.05),
   'Cooc-thr0p15':cooc_walks(formulas,ids,seed,threshold=.15),
   'Cooc-thr0p30':cooc_walks(formulas,ids,seed,threshold=.30),
  }
  for name,ratio in [('Core-Candidate19',.5),('Core-Cooc25',.25),('Core-Cooc75',.75)]:
   seq,stat=merge_walks(co,ch,seed,ratio);corpus[name]=seq
   tokenstats.append({'model':name,'seed':seed,'walk_ratio_cooc':ratio,**stat,'effective_cooc_token_share':stat['cooc_tokens']/(stat['cooc_tokens']+stat['chem_tokens'])})
  for key in variants:
   val=train_one(corpus[key],ids,seed)
   assert np.isfinite(val).all(),key
   sim[key][seed]=val
   detail.extend({'model':key,'seed':seed,'herb_a':a,'herb_b':b,'cosine':round(float(v),8)} for (a,b),v in zip(pairs,val))
  print('completed seed',seed,flush=True)
 dumpcsv(out/'all_reanalysis_scores_13models_10seeds.csv',detail)
 dumpcsv(out/'core_channel_contributions_by_seed.csv',tokenstats)
 summaries=[];pairsum=[]
 for key in variants:
  vals=np.array([sim[key][s] for s in SEEDS]);rhos=[float(spearmanr(x,y).statistic) for x,y in itertools.combinations(vals,2)]
  summaries.append({'model':key,'seeds':len(SEEDS),'herb_pairs':45,'seed_pair_comparisons':45,**{f'rank_rho_{k}':v for k,v in statistic(rhos).items()},'result_status':'V3_DERIVED_REANALYSIS_NOT_ORIGINAL_STUDY'})
  for (a,b),mu,sd in zip(pairs,np.mean(vals,axis=0),np.std(vals,axis=0)):
   pairsum.append({'model':key,'herb_a':a,'herb_b':b,'mean_cosine':round(float(mu),8),'sd_cosine':round(float(sd),8)})
 dumpcsv(out/'seed_repeatability_13models.csv',summaries)
 dumpcsv(out/'mean_herb_pair_similarity_13models.csv',pairsum)
 compare={'Cooc-Support':'Cooc-NPMI','Cooc-Degree':'Cooc-NPMI','Cooc-Combined':'Cooc-NPMI',
  'Cooc-thr0p05':'Cooc-NPMI','Cooc-thr0p15':'Cooc-NPMI','Cooc-thr0p30':'Cooc-NPMI',
  'Chem-PruneFirst2':'Chem-Candidate19','Chem-Candidate18':'Chem-Candidate19',
  'Core-Cooc25':'Core-Candidate19','Core-Cooc75':'Core-Candidate19'}
 sensitivity=[]
 for pert,base in compare.items():
  x=np.mean(np.array([sim[pert][s] for s in SEEDS]),axis=0);y=np.mean(np.array([sim[base][s] for s in SEEDS]),axis=0)
  perseed=[float(spearmanr(sim[pert][s],sim[base][s]).statistic) for s in SEEDS]
  ov=len(set(np.argsort(-x)[:5])&set(np.argsort(-y)[:5]))
  sensitivity.append({'perturbation':pert,'baseline':base,'mean_rank_spearman':round(float(spearmanr(x,y).statistic),6),
    'paired_seed_rank_spearman_mean':round(float(np.mean(perseed)),6),'paired_seed_rank_spearman_sd':round(float(np.std(perseed)),6),
    'top5_overlap_mean_vectors':ov,'mean_absolute_cosine_shift':round(float(np.mean(np.abs(x-y))),6),
    'no_biological_gold_labels':1})
 dumpcsv(out/'perturbation_sensitivity_10comparisons.csv',sensitivity)
 # Untrained label diagnostic is descriptive and neither held-out validation nor therapeutic link.
 family={h['id']:h['family'] for h in data['herbs']}
 family_diag=[]
 for m in ('Cooc-NPMI','Chem-Candidate19','Core-Candidate19'):
  v=np.mean(np.array([sim[m][s] for s in SEEDS]),axis=0)
  same=[float(v[i]) for i,(a,b) in enumerate(pairs) if family[a]==family[b]]
  other=[float(v[i]) for i,(a,b) in enumerate(pairs) if family[a]!=family[b]]
  family_diag.append({'model':m,'same_family_pairs':len(same),'different_family_pairs':len(other),
    'same_family_mean':round(float(np.mean(same)),6),'different_family_mean':round(float(np.mean(other)),6),
    'descriptive_difference':round(float(np.mean(same)-np.mean(other)),6),'label_absent_from_training':1,'not_independent_validation':1})
 dumpcsv(out/'botanical_family_descriptive_3models.csv',family_diag)
 # Reproducibility and provenance guardrails.
 env={'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,'gensim':gensim.__version__,
  'platform':platform.platform(),'word2vec_parameters':{'dimensions':32,'window':5,'negative':5,'epochs':15,'min_count':1,'workers':1,'sg':1,'sample':.001},
  'seeds':SEEDS,'source_input_sha256':{str(p.relative_to(root)):sha(p) for p in sorted((root/'data').iterdir()) if p.is_file()},
  'reanalysis_model_count':len(variants),'model_fits':len(variants)*len(SEEDS),'source_status':'V3_PROJECTED_NOT_ORIGINAL_PAPER1_ARCHIVE',
  'candidate19_class_status':'CURATED_AI_ASSISTED_NOT_RECOVERED_ORIGINAL','clinical_or_biological_validation':False,
  'independent_expert_review_available':False,'formula_source_review':'single_curator_AI_assisted',
  'no_source_independent_test_set':True,
  'claim_controls':['Original manuscript results not independently reproduced','Internal formula LOFO not external truth','No clinical efficacy claims','No recovered original chemical class table']}
 (out/'reanalysis_manifest.json').write_text(json.dumps(env,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'seed_repeatability':summaries,'sensitivity':sensitivity,'family':family_diag},ensure_ascii=False,indent=2),flush=True)
 return env

if __name__=='__main__':run()