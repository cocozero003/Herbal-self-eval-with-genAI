"""Paper 2 v1.3: actual internal robustness experiments on frozen v0.4 data.

Gold labels are documentary *formula co-membership* only. They are NOT
biological truth or external validation. The historical 35 classes are absent.
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, itertools, json, math, platform, random, sys, time
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'input' / 'v04'
RESULTS = ROOT / 'results'
RESULTS.mkdir(parents=True, exist_ok=True)
SOURCE_V12 = ROOT / 'input' / 'evidence_v12'
OLD_SRC = OLD / 'src' / 'reanalyse.py'
spec = importlib.util.spec_from_file_location('thaiherb_v04_reanalyse_locked', OLD_SRC)
v04 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v04)
SEEDS = list(v04.SEEDS)
assert len(SEEDS) == 20


def save_csv(name, rows):
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / name, index=False, encoding='utf-8-sig')
    return df


def write_json(name, obj):
    (RESULTS / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding='utf-8')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rho(x, y):
    r = spearmanr(x, y).statistic
    return float(r) if np.isfinite(r) else None


def make_perturbed_cooc_walks(formulas, ids, seed, threshold=0., omit_formula=None):
    forms = [f for f in formulas if f['id'] != omit_formula]
    if threshold <= 0:
        return v04.cooc_walks(forms, ids, seed)
    edges = v04.cooc_pairs(forms, ids)
    adj = defaultdict(list)
    for edge in edges:
        if edge['positive_npmi'] >= threshold:
            a,b,w = edge['herb_a'],edge['herb_b'],edge['positive_npmi']
            adj[a].append((b,w)); adj[b].append((a,w))
    rng = random.Random(seed); walks=[]
    for h in ids:
        for _ in range(60):
            path=[h]
            for _ in range(19):
                neighbors=adj[path[-1]]
                if not neighbors:break
                path.append(rng.choices([a for a,w in neighbors],weights=[w for a,w in neighbors])[0])
            walks.append(path)
    rng.shuffle(walks)
    return walks


def prune_for_seed(chemistry, ids, keep, seed):
    rng = random.Random(2_026_110_700 + seed + keep * 10000)
    byh = defaultdict(list)
    for c in chemistry: byh[c['subject_id']].append(c)
    selected=[]
    for h in ids:
        claims = sorted(byh[h], key=lambda a:a['assertion_id'])
        assert len(claims)==5
        selected.extend(rng.sample(claims,keep))
    assert len(selected)==len(ids)*keep
    return selected


def report_old_integrity():
    manifest=json.loads((OLD/'SHA256_MANIFEST.json').read_text(encoding='utf-8'))
    print('Original manifest type',type(manifest).__name__)
    return manifest


def loading():
    d=json.loads((OLD/'data'/'paper2_source_reviewed_species_v04.json').read_text(encoding='utf-8'))
    ids=[h['id'] for h in d['herbs']]
    forms=d['formulas']
    chemistry=[r for r in d['assertions'] if r['assertion_type']=='ChemistryOccurrenceAssertion']
    assert (len(ids),len(forms),len(chemistry),sum(len(f['herbs']) for f in forms),len(d['compounds'])) == (20,10,100,74,83)
    pairs=list(itertools.combinations(ids,2))
    return d,ids,forms,chemistry,pairs


def mean_95(values):
    v=np.asarray(values,dtype=float)
    return {'mean':round(float(np.mean(v)),6),'sd':round(float(np.std(v,ddof=1)),6) if len(v)>1 else 0.,
            'low':round(float(np.quantile(v,.025)),6),'high':round(float(np.quantile(v,.975)),6)}


def run_replay(ids,forms,pairs):
    baseline=pd.read_csv(OLD/'results'/'ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv')
    assert len(baseline)==34200 and set(baseline.seed)==set(SEEDS)
    lookup=baseline.set_index(['model','seed','herb_a','herb_b'])['cosine']
    score=v04.vectors(v04.cooc_walks(forms,ids,11),ids,11)
    original=np.array([lookup.loc[('Cooc-NPMI',11,a,b)] for a,b in pairs])
    mad=float(np.max(np.abs(score-original)))
    assert mad<1e-6, mad
    archived=pd.read_csv(OLD/'results'/'SEED_REPEATABILITY_20SEEDS.csv')
    assert len(archived)==9 and archived.seeds.eq(20).all()
    save_csv('P2_ARCHIVED_SEED_REPEATABILITY_20SEEDS.csv',archived)
    return lookup,{'n_models':9,'n_seeds':20,'fits_archived':180,'scores_archived':len(baseline),
                   'replay_model':'Cooc-NPMI','replay_seed':11,'replay_max_absolute_error':mad,
                   'archive_is_previous_actual_run':True}


def perturbations(ids,forms,chemistry,pairs,lookup):
    index={p:i for i,p in enumerate(pairs)}
    output=[];scores=[]
    configs=[('Cooc-NPMI-Threshold0.15','Cooc-NPMI'),('Cooc-NPMI-Threshold0.30','Cooc-NPMI'),
             ('Cooc-Remove-F08','Cooc-NPMI'),('Chem-Prune3','Chem-Exact'),('Chem-Prune2','Chem-Exact'),
             ('Core-Exact25','Core-Exact50'),('Core-Exact75','Core-Exact50'),('Cooc-Support2','Cooc-NPMI'),
             ('Chem-ExactPrune4','Chem-Exact')]
    for seed in SEEDS:
        for variant,base in configs:
            original=np.array([lookup.loc[(base,seed,a,b)] for a,b in pairs],dtype=float)
            if variant=='Cooc-NPMI-Threshold0.15':
                vec=v04.vectors(make_perturbed_cooc_walks(forms,ids,seed,.15),ids,seed)
            elif variant=='Cooc-NPMI-Threshold0.30':
                vec=v04.vectors(make_perturbed_cooc_walks(forms,ids,seed,.30),ids,seed)
            elif variant=='Cooc-Remove-F08':
                vec=v04.vectors(make_perturbed_cooc_walks(forms,ids,seed,0,'F08_DTAM2566'),ids,seed)
            elif variant=='Chem-Prune3':
                claims=prune_for_seed(chemistry,ids,3,seed)
                vec=v04.vectors(v04.chem_walks(claims,ids,seed),ids,seed)
            elif variant=='Chem-Prune2':
                claims=prune_for_seed(chemistry,ids,2,seed)
                vec=v04.vectors(v04.chem_walks(claims,ids,seed),ids,seed)
            else:
                vec=np.array([lookup.loc[(variant,seed,a,b)] for a,b in pairs])
            assert len(vec)==190 and np.isfinite(vec).all()
            corr=rho(original,vec)
            k=10; topA=set(np.argsort(-original)[:k]);topB=set(np.argsort(-vec)[:k])
            output.append({'variant':variant,'baseline':base,'seed':seed,'rank_spearman':corr,
                            'top10_overlap_count':len(topA & topB),'herb_pair_count':190,
                            'outcome':'INTERNAL_RANK_PERTURBATION_NOT_BIOLOGICAL_VALIDATION'})
            for (a,b),sim in zip(pairs,vec):
                scores.append({'variant':variant,'seed':seed,'herb_a':a,'herb_b':b,'cosine':round(float(sim),8)})
    df=save_csv('P2_PERTURBATION_20SEED_PAIRED.csv',output)
    save_csv('P2_PERTURBATION_ALL_PAIR_SCORES.csv',scores)
    sm=[]
    for name,g in df.groupby('variant',sort=True):
        st=mean_95(g['rank_spearman'])
        sm.append({'variant':name,'baseline':g.baseline.iloc[0],'seeds':20,'pairs':190,
                   'mean_rank_spearman':st['mean'],'sd_over_seeds':st['sd'],
                   'top10_overlap_mean':round(float(g.top10_overlap_count.mean()),3),
                   'uncertainty_type':'seed_variation_not_source_generalization'})
    save_csv('P2_PERTURBATION_SUMMARY.csv',sm)
    return df


def deterministic_baselines(ids,chemistry,pairs):
    byh={h:set(r['object_id'] for r in chemistry if r['subject_id']==h) for h in ids}
    dfreq=Counter(c for cs in byh.values() for c in cs)
    def weighted(a,b):
        inter=byh[a]&byh[b];union=byh[a]|byh[b]
        w=lambda c: math.log((len(ids)+1)/(dfreq[c]+1))+1
        return sum(w(c) for c in inter)/sum(w(c) for c in union) if union else 0.
    jaccard={(a,b):len(byh[a]&byh[b])/len(byh[a]|byh[b]) for a,b in pairs}
    idf={(a,b):weighted(a,b) for a,b in pairs}
    return jaccard,idf


def leave_one_formula_out(ids,forms,chemistry,pairs,lookup):
    jaccard,idf=deterministic_baselines(ids,chemistry,pairs)
    predictions=[];metrics=[];coverage=[];rankrows=[]
    for form in forms:
        fold=form['id']; train=[f for f in forms if f['id']!=fold]
        occ=Counter(h for f in train for h in f['herbs'])
        cold={h for h in ids if occ[h]==0}
        eligible=[(a,b) for a,b in pairs if a not in cold and b not in cold]
        coverage.append({'heldout_formula':fold,'train_formulas':9,'cold_herbs':';'.join(sorted(cold)),
                         'eligible_pairs':len(eligible),'total_pairs':190,'blocked_pairs':190-len(eligible),
                         'fold_type':'FULL_190' if not cold else 'PARTIAL_171_COLD_START',
                         'positive_pairs_eligible':sum(a in form['herbs'] and b in form['herbs'] for a,b in eligible)})
        y=np.array([int(a in form['herbs'] and b in form['herbs']) for a,b in eligible],dtype=int)
        if y.sum()==0 or y.sum()==len(y):
            continue
        co=v04.cooc_pairs(train,ids)
        co_lookup={(r['herb_a'],r['herb_b']):r for r in co}
        baseline={
            'PairSupport': np.array([co_lookup[p]['support'] for p in eligible],float),
            'DegreeProduct': np.array([co_lookup[p]['formula_count_a']*co_lookup[p]['formula_count_b'] for p in eligible],float),
            'PositiveNPMI': np.array([co_lookup[p]['positive_npmi'] for p in eligible],float),
            'ChemJaccard':np.array([jaccard[p] for p in eligible],float),
            'ChemIDFJaccard':np.array([idf[p] for p in eligible],float)
        }
        for name,raw in baseline.items():
            metrics.append({'fold':fold,'coverage_type':'FULL_190' if not cold else 'PARTIAL_171_COLD_START',
                            'model':name,'seed':'DETERMINISTIC','AP':float(average_precision_score(y,raw)),
                            'AUROC':float(roc_auc_score(y,raw)),'pairs':len(y),'positive_pairs':int(y.sum())})
            for (a,b),true,sim in zip(eligible,y,raw):
                predictions.append({'fold':fold,'model':name,'seed':'DETERMINISTIC','herb_a':a,'herb_b':b,
                                    'documentary_label':int(true),'score':float(sim),'coverage_type': 'FULL_190' if not cold else 'PARTIAL_171_COLD_START'})
        for seed in SEEDS:
            co_walks=v04.cooc_walks(train,ids,seed)
            chem_walks=v04.chem_walks(chemistry,ids,seed)
            sequences={
                'Cooc-NPMI-TrainOnly':co_walks,
                'Core-Exact50-TrainOnly':v04.mixed(co_walks,chem_walks,seed,.5)[0]
            }
            for name,seq in sequences.items():
                scores=v04.vectors(seq,ids,seed)
                scores_by_pair=dict(zip(pairs,scores))
                raw=np.array([scores_by_pair[p] for p in eligible],dtype=float)
                assert np.isfinite(raw).all()
                metrics.append({'fold':fold,'coverage_type':'FULL_190' if not cold else 'PARTIAL_171_COLD_START',
                                'model':name,'seed':seed,'AP':float(average_precision_score(y,raw)),
                                'AUROC':float(roc_auc_score(y,raw)),'pairs':len(y),'positive_pairs':int(y.sum())})
                for (a,b),true,sim in zip(eligible,y,raw):
                    predictions.append({'fold':fold,'model':name,'seed':seed,'herb_a':a,'herb_b':b,
                                        'documentary_label':int(true),'score':float(sim),'coverage_type':'FULL_190' if not cold else 'PARTIAL_171_COLD_START'})
            chem_arch=np.array([lookup.loc[('Chem-Exact',seed,a,b)] for a,b in eligible],dtype=float)
            metrics.append({'fold':fold,'coverage_type':'FULL_190' if not cold else 'PARTIAL_171_COLD_START',
                            'model':'Chem-Exact-FormulaIndependent','seed':seed,
                            'AP':float(average_precision_score(y,chem_arch)),
                            'AUROC':float(roc_auc_score(y,chem_arch)),'pairs':len(y),'positive_pairs':int(y.sum())})
            for (a,b),true,sim in zip(eligible,y,chem_arch):
                predictions.append({'fold':fold,'model':'Chem-Exact-FormulaIndependent','seed':seed,
                                    'herb_a':a,'herb_b':b,'documentary_label':int(true),
                                    'score':float(sim),'coverage_type':'FULL_190' if not cold else 'PARTIAL_171_COLD_START'})
        print('LOFO',fold,'cold',len(cold),'finished',flush=True)
    metric_df=save_csv('P2_LOFO_MODEL_METRICS_ALL_10_FOLDS.csv',metrics)
    save_csv('P2_LOFO_PREDICTIONS_ALL.csv',predictions)
    save_csv('P2_LOFO_COVERAGE.csv',coverage)
    # The independent resampling unit is the held-out *formula*, not a herb pair or random seed.
    models=sorted(metric_df.model.unique())
    summaries=[]
    fold_agg=metric_df.groupby(['coverage_type','model','fold'])[['AP','AUROC']].mean().reset_index()
    rng=np.random.default_rng(20261107)
    bootstrap=[]
    for cover in ['FULL_190','PARTIAL_171_COLD_START']:
        f=fold_agg[fold_agg.coverage_type==cover]
        n=f.fold.nunique()
        for model in models:
            t=f[f.model==model].set_index('fold').sort_index()
            if len(t)!=n:raise ValueError((cover,model,len(t),n))
            summary={'model':model,'coverage_type':cover,'heldout_formulas':n,'seed_fits_per_fold':20 if 'Exact' in model or 'TrainOnly' in model else 1,
                     'mean_AP_across_formulas':round(float(t.AP.mean()),6),
                     'mean_AUROC_across_formulas':round(float(t.AUROC.mean()),6),
                     'not_biological_accuracy':1}
            for endpoint in ['AP','AUROC']:
                values=t[endpoint].to_numpy()
                picks=rng.integers(0,n,size=(2000,n))
                reps=values[picks].mean(axis=1)
                summary[endpoint+'_CI_lower']=round(float(np.quantile(reps,.025)),6)
                summary[endpoint+'_CI_upper']=round(float(np.quantile(reps,.975)),6)
                for j,z in enumerate(reps):bootstrap.append({'coverage_type':cover,'model':model,'endpoint':endpoint,'replicate':j,'bootstrap_value':float(z)})
            summaries.append(summary)
    save_csv('P2_LOFO_SUMMARY_CLUSTER_BOOTSTRAP.csv',summaries)
    save_csv('P2_LOFO_BOOTSTRAP_2000.csv',bootstrap)
    save_csv('P2_LOFO_FORMULA_LEVEL_MEANS.csv',fold_agg)
    return metric_df,fold_agg,pd.DataFrame(summaries)


def source_holdout(ids,forms,chem,pairs,lookup):
    source_ids=sorted(set(c['source_id'] for c in chem));assert len(source_ids)==20
    records=[];scores=[]
    for source in source_ids:
        remaining=[c for c in chem if c['source_id']!=source]
        lost=sorted(set(ids)-set(c['subject_id'] for c in remaining));assert len(lost)==1
        eligible=[p for p in pairs if p[0] not in lost and p[1] not in lost]
        assert len(eligible)==171
        correlations=[]
        for seed in SEEDS[:5]:
            walks=v04.chem_walks(remaining,ids,seed)
            v=v04.vectors(walks,ids,seed)
            new=dict(zip(pairs,v))
            base=[lookup.loc[('Chem-Exact',seed,*p)] for p in eligible]
            cand=[new[p] for p in eligible]
            corr=rho(base,cand)
            correlations.append(corr)
            scores.append({'source_holdout':source,'lost_herb':lost[0],'seed':seed,'remaining_pairs':171,
                           'blocked_pairs':19,'rank_spearman_remaining_pairs':corr})
        records.append({'source_holdout':source,'lost_herb':lost[0],'source_claims_removed':5,
                        'remaining_chem_claims':95,'covered_herbs':19,'cold_start_herbs':1,
                        'evaluable_pairs':171,'blocked_pairs':19,'coverage_fraction':171/190,
                        'mean_rank_spearman_known_pairs':float(np.mean(correlations)),
                        'independent_source_level_gold':'NONE','status':'INTERNAL_SOURCE_HOLDOUT_NOT_EXTERNAL_VALIDITY'})
    save_csv('P2_SOURCE_HOLDOUT_20_SOURCES_5SEEDS.csv',scores)
    save_csv('P2_SOURCE_HOLDOUT_COVERAGE.csv',records)
    return pd.DataFrame(records)


def external_gate():
    p=SOURCE_V12/'P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv'
    ext=pd.read_csv(p)
    assert len(ext)==11
    records=[]
    for _,row in ext.iterrows():
        records.append({'case_id':row['case_id'],'assertion_id':row['assertion_id'],
                        'doi':row['doi'],'herb_id':row['herb_id'],'plant_part':row['plant_part'],
                        'observed_compound':row['compound'],'source_doi_distinct':row['source_disjoint_from_archived_citation'],
                        'selected_after_development':'YES','binary_negative_controls':0,
                        'independent_gold': 'NO', 'external_test_eligible':'NO_POSTHOC_POSITIVE_ONLY',
                        'preparation_match_still_requires_review':row['eligibility']=='CONTEXT_REVIEW_REQUIRED'})
    save_csv('P2_EXTERNAL_11_POSITIVE_PILOT_GATE.csv',records)
    return {'rows':11,'unique_doi':int(ext.doi.nunique()),'source_overlap':'doi disjoint per prior audit; not independently held-out',
            'no_confirmatory_AUROC_AP':True,'why':'post-hoc selected positives only, no blinded negative controls, material contexts differ'}


def class_gate():
    p=SOURCE_V12/'P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv'
    d=pd.read_csv(p,dtype=str)
    assert len(d)==83 and d.original_35class_id.isna().all()
    names=d.proposed_family.nunique()
    result={'original_35class_count_historical':35,'original_35class_compound_mapping_recovered':False,
            'new_provisional_name_based_families':int(names),'compound_rows':83,
            'confirmed_historical_class_replication':False,'candidate_mapping_all_83_not_adjudicated':True}
    write_json('P2_TAXONOMY_HISTORICAL_VS_NEW.json',result)
    return result


def data_freeze():
    paths=[OLD/'data'/'paper2_source_reviewed_species_v04.json',OLD/'results'/'ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv',
           SOURCE_V12/'P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv',SOURCE_V12/'P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv']
    return [{'file':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths]


def main():
    start=time.monotonic()
    d,ids,forms,chem,pairs=loading()
    archived,checks=run_replay(ids,forms,pairs)
    print('v0.4 replay passes max delta',checks['replay_max_absolute_error'],flush=True)
    pert=perturbations(ids,forms,chem,pairs,archived)
    print('perturbations',len(pert),'seed comparisons',flush=True)
    metric,fold,summ=leave_one_formula_out(ids,forms,chem,pairs,archived)
    sources=source_holdout(ids,forms,chem,pairs,archived)
    external=external_gate();taxonomy=class_gate()
    spec={'title':'Paper2 v1.3 actual internal robustness on frozen 20-herb species graph',
          'original_herbs':20,'original_formulas':10,'species_formula_memberships':74,'chemical_claims':100,
          'exact_compound_ids':83,'pair_universe':190,'seeds':SEEDS,
          'archived':checks,'new_perturbation_rows':len(pert),'LOFO_model_metric_rows':len(metric),
          'LOFO_complete_case_folds':int(fold[fold.coverage_type=='FULL_190'].fold.nunique()),
          'LOFO_partial_case_folds':int(fold[fold.coverage_type=='PARTIAL_171_COLD_START'].fold.nunique()),
          'source_holdout_count':len(sources),'source_holdout_seeds':5,'class_gate':taxonomy,
          'external_gate':external,'source_fingerprint':data_freeze(),
          'libraries':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
                       'gensim':v04.gensim.__version__},'elapsed_seconds':round(time.monotonic()-start,1),
          'inference_scope':'DOCUMENTARY_FORMULA_CO_MEMBERSHIP_NOT_BIOLOGICAL_TRUTH',
          'other_limitations':['NO_ORIGINAL_35_CLASSES','NO_EXPERT_GOLD','EXTERNAL_POSITIVE_ONLY_POSTHOC',
                               'ONLY_10_SELECTED_FORMULAS','CHEMICAL_FIXED_5_PER_HERB_INCOMPLETE']}
    write_json('P2_RUN_MANIFEST.json',spec)
    print('DONE',json.dumps({'time':spec['elapsed_seconds'],'rows':len(metric),'pert':len(pert)}),flush=True)

if __name__=='__main__':main()
