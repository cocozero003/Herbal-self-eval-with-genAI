"""ThaiHerb20 Paper 2 robust baseline and source-integrity foundation.

Scientific boundary: V3-derived proxy; 35-class original archive is unavailable.
No claims of independent external validation or original manuscript replication.
"""
from __future__ import annotations
import csv, hashlib, itertools, json, math, platform, random, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import scipy
import sklearn
import gensim
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score
from gensim.models import Word2Vec

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; OUT=ROOT/'results'
SEEDS=[11,23,37,41,53,67,79,83,97,101,109,127,137,149,163,173,181,191,199,211,223]
METHODS=['PairSupport','DegreeProduct','PositiveNPMI','ExactCompoundJaccard','ExactCompoundIDFJaccard']


def save_csv(name,rows):
    if not rows:raise ValueError('Rows cannot be empty: '+name)
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def load():
    d=json.loads((DATA/'paper2_bootstrap_v3_proxy.json').read_text(encoding='utf-8'))
    p1=json.loads((DATA/'paper1_formula_reviewed_snapshot.json').read_text(encoding='utf-8'))
    return d,p1


def hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.iterdir()) if p.is_file()}


def form_pairs(forms,ids):
    n=len(forms);byh={h:{f['id'] for f in forms if h in f['herbs']} for h in ids}
    ans=[]
    for a,b in itertools.combinations(ids,2):
        na=len(byh[a]);nb=len(byh[b]);k=len(byh[a]&byh[b]);v=0.0
        if 0<k<n and na and nb:
            v=math.log((k/n)/((na/n)*(nb/n)))/(-math.log(k/n))
        ans.append({'herb_a':a,'herb_b':b,'support':k,'formula_count_a':na,'formula_count_b':nb,'npmi':v,'positive_npmi':max(v,0)})
    return ans


def chem_pairs(chem,ids):
    byh=defaultdict(set);byc=defaultdict(set)
    for row in chem:
        byh[row['subject_id']].add(row['object_id'])
        byc[row['object_id']].add(row['subject_id'])
    idf={c: math.log((len(ids)+1)/(len(h)+1))+1 for c,h in byc.items()}
    output=[]
    for a,b in itertools.combinations(ids,2):
        aa=byh[a];bb=byh[b];shared=aa&bb;allc=aa|bb
        j=len(shared)/len(allc) if allc else 0.
        jidf=sum(idf[x] for x in shared)/sum(idf[x] for x in allc) if allc else 0.
        output.append({'herb_a':a,'herb_b':b,'shared_compounds':len(shared),'compound_jaccard':j,'compound_idf_jaccard':jidf,'shared_compound_ids':';'.join(sorted(shared))})
    return output


def rank_corr(veca,vecb):
    if len(set(round(float(v),10) for v in veca))<=1 or len(set(round(float(v),10) for v in vecb))<=1:
        return None
    return float(spearmanr(veca,vecb).statistic)


def accuracy(y,s):
    y=np.asarray(y,int);s=np.asarray(s,float)
    assert set(np.unique(y))=={0,1}
    top=np.argsort(-s,kind='stable')[:10]
    return {'average_precision':float(average_precision_score(y,s)),
            'auroc':float(roc_auc_score(y,s)),
            'precision_at_10':float(y[top].mean())}


def basic_audit(d,p1):
    ids=[h['id'] for h in d['herbs']];assert len(ids)==len(set(ids))==20
    forms=d['formulas'];assert len(forms)==10
    claims=d['assertions'];fchem=[a for a in claims if a['assertion_type']=='ChemistryOccurrenceAssertion']
    fformula=[a for a in claims if a['assertion_type']=='FormulaMembershipAssertion']
    assert len(fchem)==100 and len(fformula)==71 and len(claims)==171
    assert all(len([a for a in fchem if a['subject_id']==h])==5 for h in ids)
    assert len({a['object_id'] for a in fchem})==83
    assert len(set(a['source_id'] for a in fchem))==20
    original={f['id']:f for f in p1['formulas']}
    legacy=[];matrix=[];form_audit=[]
    h10=set(ids[:10]);h20=set(ids[10:]);assert len(h10)==10 and len(h20)==10
    for f in forms:
        f0=original[f['id']]
        a=set(f['herbs'])&h10;b=set(f0['herbs']);assert a==b,(f['id'],a,b)
        legacy.append({'formula_id':f['id'],'paper1_title_th':f0['title'],'legacy_10herb_match':1,
                       'source_url':f0['source_url'],'paper1_printed_pages':';'.join(map(str,f0['printed_pages'])),
                       'paper2_imported_source_locator':f['locator'],
                       'new_10herb_source_reviewed':0,'review_status':'LEGACY_CROSSWALK_MATCH_NOT_INDEPENDENT_20_HERB_AUDIT'})
        form_audit.append({'formula_id':f['id'],'thai_title_from_paper1_crosswalk':f0['title'],
                           'n_total_focal_herbs':len(f['herbs']),'n_old_herbs':len(a),
                           'n_new_herbs':len(set(f['herbs'])&h20),'source_status':'NEW_HERBS_UNREVIEWED_V3_PROXY'})
        for h in ids:
            matrix.append({'formula_id':f['id'],'herb_id':h,'herb_present_proxy':int(h in f['herbs']),
                           'review_class':'PAPER1_SINGLE_CURATOR_CROSSWALK' if h in h10 else 'NEW_HERB_NOT_YET_PRIMARY_VERIFIED',
                           'independent_adjudication':0,'source_url':f0['source_url']})
    save_csv('formula_id_crosswalk_10.csv',legacy)
    save_csv('formula_herb_200_matrix.csv',matrix)
    save_csv('formula_context_10.csv',form_audit)
    source_by_herb=defaultdict(set)
    for c in fchem:source_by_herb[c['subject_id']].add(c['source_id'])
    frag=[]
    for source in sorted({x['source_id'] for x in fchem}):
        remain=[x for x in fchem if x['source_id']!=source]
        bad=sorted(set(ids)-{x['subject_id'] for x in remain})
        frag.append({'removed_chemistry_source':source,'removed_assertions':len(fchem)-len(remain),
                    'unrepresented_herb_count':len(bad),'unrepresented_herb_ids':';'.join(bad),
                    'eligible_for_complete_190pair_chemistry_comparison':int(not bad),
                    'source_dependence_note':'one source per herb in this 100-row panel'})
    save_csv('leave_one_source_out_20.csv',frag)
    return ids,forms,fchem,frag,legacy


def do_robustness(forms,ids,chem):
    full=form_pairs(forms,ids);pos=sum(r['positive_npmi']>0 for r in full)
    assert len(full)==190 and pos==82
    save_csv('cooc_pair_weights_190.csv',full)
    chemical=chem_pairs(chem,ids)
    save_csv('exact_compound_pairs_190.csv',chemical)
    chemidx={(r['herb_a'],r['herb_b']):r for r in chemical}
    pairorder=[(r['herb_a'],r['herb_b']) for r in full]
    lofo=[];baselines=[];allpred=[];blocked=[]
    for heldout in forms:
        train=[f for f in forms if f['id']!=heldout['id']]
        assert len(train)==9 and heldout['id'] not in {f['id'] for f in train}
        count=Counter(h for f in train for h in f['herbs'])
        unseen=sorted(h for h in ids if count[h]==0)
        eligible=not unseen
        other=form_pairs(train,ids)
        y=np.array([int(a in heldout['herbs'] and b in heldout['herbs']) for a,b in pairorder])
        assert 0<y.sum()<190
        for key in ('positive_npmi','support'):
            before=np.array([float(z[key]) for z in full])
            after=np.array([float(z[key]) for z in other])
            top0=set(np.argsort(-before,kind='stable')[:10]);top1=set(np.argsort(-after,kind='stable')[:10])
            lofo.append({'heldout_formula':heldout['id'],'comparison_measure':key,
                         'spearman_all_190_pairs':rank_corr(before,after),
                         'top10_overlap':len(top0&top1),'positives_in_heldout_formula':int(y.sum()),
                         'unseen_herbs_in_training':';'.join(unseen),'complete_190pair_evaluation_eligible':int(eligible),
                         'not_external_validation':1})
        blocked.append({'heldout_formula':heldout['id'],'train_formulas':9,'test_formula_not_in_training':1,
                        'heldout_positive_pairs':int(y.sum()),'heldout_pair_prevalence':float(y.mean()),
                        'cold_start_herbs':';'.join(unseen),'full_190_pair_eligible':int(eligible)})
        if not eligible:continue
        predictions={
            'PairSupport':np.array([float(r['support']) for r in other]),
            'DegreeProduct':np.array([float(r['formula_count_a']*r['formula_count_b']) for r in other]),
            'PositiveNPMI':np.array([float(r['positive_npmi']) for r in other]),
            'ExactCompoundJaccard':np.array([float(chemidx[p]['compound_jaccard']) for p in pairorder]),
            'ExactCompoundIDFJaccard':np.array([float(chemidx[p]['compound_idf_jaccard']) for p in pairorder])
        }
        for method,score in predictions.items():
            result=accuracy(y,score)
            baselines.append({'heldout_formula':heldout['id'],'method':method,
                              'pair_count':190,'positive_pairs':int(y.sum()),**result,'label_is_formula_membership_not_biology':1})
            for (a,b),yv,sv in zip(pairorder,y,score):
                allpred.append({'heldout_formula':heldout['id'],'method':method,'herb_a':a,'herb_b':b,
                                'heldout_formula_cooccurrence_label':int(yv),'prediction_without_heldout_formula':round(float(sv),9)})
    save_csv('formula_heldout_eligibility_10.csv',blocked)
    save_csv('lofo_graph_sensitivity_20rows.csv',lofo)
    save_csv('lofo_baseline_metrics.csv',baselines)
    save_csv('lofo_baseline_predictions.csv',allpred)
    return full,chemical,blocked,lofo,baselines


def panel_pruning(chem,ids,n=8):
    original=chem_pairs(chem,ids)
    baseline=np.array([r['compound_jaccard'] for r in original])
    byherb=defaultdict(list)
    for r in chem:byherb[r['subject_id']].append(r)
    scores=[]
    for rep in range(n):
        rnd=random.Random(20261107+rep)
        reduced=[]
        for h in ids:
            panel=byherb[h];assert len(panel)==5
            remove=rnd.randrange(5)
            reduced.extend(x for j,x in enumerate(panel) if j!=remove)
        vec=np.array([r['compound_jaccard'] for r in chem_pairs(reduced,ids)])
        corr=rank_corr(baseline,vec)
        scores.append({'replicate':rep+1,'retained_per_herb':4,'total_edges':len(reduced),
                      'rank_spearman_vs_all5':corr,'top10_overlap':len(set(np.argsort(-baseline)[:10])&set(np.argsort(-vec)[:10])),
                      'scope':'exact_compound_only_not_original_35_classes'})
    save_csv('exact_chemistry_panel_pruning_8.csv',scores)
    return scores


def do_report(d,ids,forms,chem,frag,full,chemical,blocked,baselines,pruning):
    groups=defaultdict(list)
    for row in baselines:groups[row['method']].append(row)
    stats=[]
    for name in METHODS:
        subset=groups[name]
        vals=np.array([r['average_precision'] for r in subset])
        rng=np.random.default_rng(4200)
        draws=rng.integers(0,len(vals),(3000,len(vals)))
        ci=np.quantile(vals[draws].mean(axis=1),[.025,.975])
        stats.append({'model':name,'eligible_folds':len(subset),'mean_average_precision':round(float(np.mean(vals)),6),
                      'fold_bootstrap_low':round(float(ci[0]),6),'fold_bootstrap_high':round(float(ci[1]),6),
                      'mean_auroc':round(float(np.mean([r['auroc'] for r in subset])),6),
                      'mean_p10':round(float(np.mean([r['precision_at_10'] for r in subset])),6),
                      'not_external_biological_validity':1})
    save_csv('lofo_baseline_summary.csv',stats)
    sids=Counter(c['source_id'] for c in chem)
    manifest={'version':'v0.3','stage':'Paper2 source-integrity and baseline robustness foundation',
              'source_dataset':'V3-derived proxy; original Paper2 raw archive unavailable',
              'n_herbs':20,'n_formulas':10,'n_formula_memberships':sum(map(lambda x:len(x['herbs']),forms)),
              'n_chemistry_assertions':len(chem),'n_distinct_compounds':len({x['object_id'] for x in chem}),
              'original_35_classes_available':False,'original_190_pair_vectors_available':False,
              'positive_npmi_edges':sum(r['positive_npmi']>0 for r in full),
              'first10_herb_formula_memberships_match_paper1_curator_review':True,
              'added10_formula_memberships_primary_verified':False,
              'single_source_herbs':sum(1 for h in ids if len({c['source_id'] for c in chem if c['subject_id']==h})==1),
              'chemistry_source_holdout_invalid_190pair':sum(x['eligible_for_complete_190pair_chemistry_comparison']==0 for x in frag),
              'folds_with_full_190pair_coverage':sum(x['full_190_pair_eligible']==1 for x in blocked),
              'cold_start_folds':[x['heldout_formula'] for x in blocked if not x['full_190_pair_eligible']],
              'compound_panel_5_per_herb_is_selected_not_exhaustive':True,
              'formula_holdout_is_internal_document_test_not_external':True,
              'full_model_chance_cannot_be_concluded':True,
              'independent_expert_biological_gold_available':False,
              'data_sha256':hashes(),'environment':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__,'gensim':gensim.__version__,'platform':platform.platform()},
              'literature_context':'Briere et al 2026 Bioinformatics doi:10.1093/bioinformatics/btag608'}
    (OUT/'foundation_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest,stats


def run():
    OUT.mkdir(exist_ok=True)
    d,p1=load();ids,forms,chem,frag,legacy=basic_audit(d,p1)
    full,chemical,blocked,lofo,baselines=do_robustness(forms,ids,chem)
    pruning=panel_pruning(chem,ids)
    manifest,stats=do_report(d,ids,forms,chem,frag,full,chemical,blocked,baselines,pruning)
    print(json.dumps({'manifest':manifest,'benchmarks':stats,'chem_pruning':pruning},ensure_ascii=False,indent=2))
    return manifest,stats

if __name__=='__main__':run()