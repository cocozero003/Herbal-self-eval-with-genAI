"""Guarded expert scoring: no results until two genuine independent and complete ratings exist.

A reviewer can enter NA when evidence is insufficient. NA is not a negative label.
"""
import csv,json,itertools,math
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score,ndcg_score
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'

def read(name):
 with open(OUT/name,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def evaluate():
 r1=read('BLINDED_EXPERT_R1_45.csv');r2=read('BLINDED_EXPERT_R2_45.csv')
 cases=read('CASE_KEY_INTERNAL_45.csv');adj=read('ADJUDICATION_TEMPLATE_45.csv')
 assert len(r1)==len(r2)==len(cases)==len(adj)==45
 a={r['case_id']:r for r in r1};b={r['case_id']:r for r in r2};j={r['case_id']:r for r in adj}
 assert set(a)==set(b)==set(j)=={r['case_id'] for r in cases}
 dimensions=['chemistry','formula_context']
 grades={'0','1','2','NA'}
 for dim in dimensions:
  field=f'{dim}_similarity_grade_0_1_2_or_NA'
  items=[(a[k][field],b[k][field],j[k][f'adjudicated_{dim}_0_1_2_or_NA']) for k in a]
  if any(not x or not y or not z for x,y,z in items):
   return {'status':'BLOCKED_GOLD_LABELS_INCOMPLETE','dimension':dim,'n_cases':45,
           'n_completed_two_rater_adjudication':sum(bool(x and y and z) for x,y,z in items),
           'expert_validation_is_complete':False,'metrics':None}
  if any(x not in grades or y not in grades or z not in grades for x,y,z in items):
   raise ValueError('Unrecognized label')
  for key in a:
   if a[key][field] != b[key][field] and not j[key]['adjudicator_comment']:
    return {'status':'BLOCKED_DISCORDANCE_UNDOCUMENTED','dimension':dim,'case_id':key,'expert_validation_is_complete':False,'metrics':None}
  for key in a:
   if j[key]['source_independence_accepted_Y_N_U'] != 'Y' or not j[key]['evidence_url'] or not j[key]['evidence_locator']:
    return {'status':'BLOCKED_INDEPENDENT_SOURCE_REVIEW','dimension':dim,'case_id':key,'expert_validation_is_complete':False,'metrics':None}
 # Descriptive ranking evaluation on user-entered labels, not a verified independent study.
 predictions=read('heldout_pair_predictions.csv')
 pairmap={(r['case_id']):(r['herb_a_id'],r['herb_b_id']) for r in cases}
 lookup={}
 for r in predictions:
  key=(r['herb_a'],r['herb_b'],r['method'])
  lookup.setdefault(key,[]).append(float(r['prediction_score_without_heldout_formula']))
 outputs=[];summary={}
 for dim in dimensions:
  col=f'{dim}_similarity_grade_0_1_2_or_NA';g=f'adjudicated_{dim}_0_1_2_or_NA'
  keys=list(a)
  p1=[a[k][col] for k in keys];p2=[b[k][col] for k in keys]
  kk=[i for i,(x,y) in enumerate(zip(p1,p2)) if x!='NA' and y!='NA']
  kappa=float(cohen_kappa_score([int(p1[i]) for i in kk],[int(p2[i]) for i in kk],weights='quadratic')) if len(kk)>=2 else None
  valid=[k for k in keys if j[k][g]!='NA']
  summary[dim]={'rater_quadratic_kappa':kappa,'comparable_rater_cases':len(kk),'adjudicated_evaluable_cases':len(valid)}
  if len(valid)<15:
   return {'status':'BLOCKED_FEWER_THAN_15_EVALUABLE_GOLD','dimension':dim,'cases':len(valid),'expert_validation_is_complete':False,'metrics':None}
  y=np.array([int(j[k][g]) for k in valid],float)
  methods=['Chem-Proxy','Core-Proxy','ClassJaccard'] if dim=='chemistry' else ['Cooc-NPMI','Cooc-Support','Cooc-Degree','Cooc-Combined','Core-Proxy','DegreeProduct','PairSupport']
  for m in methods:
   x=np.array([np.mean(lookup[(pairmap[k][0],pairmap[k][1],m)]) for k in valid],float)
   rho=float(spearmanr(x,y).statistic) if np.std(x)>1e-12 and np.std(y)>1e-12 else None
   ndcg=float(ndcg_score([y],[x],k=min(10,len(valid)))) if np.max(y)>0 else None
   outputs.append({'dimension':dim,'method':m,'n_adjudicated_pairs':len(valid),
                   'spearman':rho,'ndcg_at_10':ndcg,'rater_kappa':kappa,
                   'review_status':'USER_ENTERED_LABELS_NOT_INDEPENDENTLY_AUDITED'})
 with (OUT/'expert_scoring_if_supplied.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(outputs[0]));w.writeheader();w.writerows(outputs)
 return {'status':'USER_ENTERED_EXPERT_LABELS_SCORED_WITHOUT_INDEPENDENCE_CERTIFICATION',
         'dimensions':summary,'result_rows':len(outputs),'expert_validation_is_complete':False,
         'metrics':'See expert_scoring_if_supplied.csv; certify reviewer independence outside this script'}

if __name__=='__main__':
 result=evaluate();(OUT/'expert_evaluation_gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))