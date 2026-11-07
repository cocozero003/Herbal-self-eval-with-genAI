"""Blind, paired, model-parity benchmark harness with a hard no-gold gate.

Never synthesize an independent gold answer. A publication score requires
all predeclared cases to be adjudicated and every model judgment locked.
Development fixtures in unit tests are explicitly synthetic.
"""
from __future__ import annotations
import csv
import json
import math
import random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'
MODELS=('M1','M2','M3')
BINARY_FIELDS=('answer_correct','citation_correct','evidence_complete','abstention_appropriate')

def read_csv(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))

def write_csv(path,rows):
    if not rows:raise ValueError('empty CSV')
    with Path(path).open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def create_templates():
    gold=read_csv(RESULTS/'P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv')
    expected = {r['case_id'] for r in gold}
    assert len(expected)==32 and len(gold)==32
    template=[]
    for r in gold:
        for model in MODELS:
            template.append({'case_id':r['case_id'],'model':model,
              'predicted_answer':'','predicted_citation_ids':'','runtime_ms':'',
              'prediction_frozen':'NO', 'blinded_assessor_id':'',
              'answer_correct':'','citation_correct':'','evidence_complete':'',
              'abstention_appropriate':'', 'assessor_notes':''})
    write_csv(RESULTS/'P3_V09_BLINDED_SCORING_TEMPLATE_96.csv',template)
    return template

def check_scoring_permissions(gold,predictions):
    errors=[]
    ids=[r.get('case_id') for r in gold]
    if len(ids)!=32 or len(set(ids))!=32:errors.append('Expected 32 unique predeclared cases')
    for r in gold:
        if r.get('eligible_for_blind_scoring')!='YES':errors.append(r['case_id']+': not eligible')
        if r.get('independent_gold_available')!='YES':errors.append(r['case_id']+': independent gold absent')
        if not all(r.get(k,'').strip() for k in ['reviewer_1','reviewer_2','adjudicated_gold']):
            errors.append(r['case_id']+': reviewer adjudication missing')
        if r.get('conflict_of_interest_checked')!='YES':errors.append(r['case_id']+': reviewer conflicts not cleared')
        if r.get('model_predictions_locked')!='YES':errors.append(r['case_id']+': predictions not locked')
        if r.get('confirmation_scoring_permitted')!='YES':errors.append(r['case_id']+': scoring not authorized')
    expected={(id_,m) for id_ in ids for m in MODELS}
    actual=[(r['case_id'],r['model']) for r in predictions]
    if len(actual)!=len(expected) or set(actual)!=expected:
        errors.append('Prediction matrix must be exactly 32 cases x 3 models')
    for r in predictions:
        key=r['case_id']+' '+r['model']
        if r.get('prediction_frozen')!='YES':errors.append(key+': prediction not frozen')
        for f in BINARY_FIELDS:
            if r.get(f) not in ('0','1'):
                errors.append(key+': '+f+' lacks independent binary adjudication')
        if not r.get('blinded_assessor_id','').strip():errors.append(key+': assessor missing')
    return errors

def exact_mcnemar(a,b):
    assert len(a)==len(b)
    b01=sum(x==1 and y==0 for x,y in zip(a,b))
    b10=sum(x==0 and y==1 for x,y in zip(a,b))
    d=b01+b10
    if d==0:return {'discordant_a_only':0,'discordant_b_only':0,'exact_two_sided_p':1.0}
    smaller=min(b01,b10)
    p=min(1.0,2*sum(math.comb(d,k) for k in range(smaller+1))/2**d)
    return {'discordant_a_only':b01,'discordant_b_only':b10,'exact_two_sided_p':p}

def paired_bootstrap(a,b,reps=1000,seed=42):
    assert len(a)==len(b) and len(a)>0
    rnd=random.Random(seed)
    n=len(a)
    diffs=[]
    for _ in range(reps):
        ids=[rnd.randrange(n) for _ in range(n)]
        diffs.append(sum(b[i]-a[i] for i in ids)/n)
    diffs.sort()
    return {'delta_b_minus_a':sum(y-x for x,y in zip(a,b))/n,
            'ci95_percentile_low':diffs[int(0.025*(reps-1))],
            'ci95_percentile_high':diffs[int(0.975*(reps-1))]}

def evaluate(gold,predictions):
    blockers=check_scoring_permissions(gold,predictions)
    if blockers:
        return {'status':'BLOCKED_NO_INDEPENDENT_GOLD_OR_LOCKED_PREDICTIONS',
                'confirmatory_accuracy_reported':False,'num_gold_cases':0,
                'blockers_count':len(blockers),'sample_blockers':blockers[:8],
                'comment':'Not a scientific validation. Populate using independent blinded reviewers before scoring.'}
    keys=[r['case_id'] for r in gold]
    by={(r['case_id'],r['model']):r for r in predictions}
    scores={}
    for metric in BINARY_FIELDS:
        series={model:[int(by[id_,model][metric]) for id_ in keys] for model in MODELS}
        comparison=[]
        for m1,m2 in [('M1','M2'),('M1','M3'),('M2','M3')]:
            exact=exact_mcnemar(series[m1],series[m2])
            exact.update(paired_bootstrap(series[m1],series[m2]))
            exact.update({'model_a':m1,'model_b':m2,
                          'bonferroni_3_pairs_p':min(1.,3*exact['exact_two_sided_p'])})
            comparison.append(exact)
        scores[metric]={'rates':{m:sum(series[m])/len(keys) for m in MODELS},
                        'paired_comparisons':comparison}
    return {'status':'ELIGIBLE_FOR_CONFIRMATORY_SCORING','num_gold_cases':len(keys),
            'endpoints':scores,'scope':'Blinded adjudicated assessment; still requires review of eligibility and protocol.'}

def run():
    template=create_templates()
    gold=read_csv(RESULTS/'P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv')
    output=evaluate(gold,template)
    (RESULTS/'P3_V09_BENCHMARK_GATE_REPORT.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    assert output['status'].startswith('BLOCKED_')
    return output

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
