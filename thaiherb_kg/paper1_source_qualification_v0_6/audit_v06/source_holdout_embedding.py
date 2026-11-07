"""Exploratory Chem/Core leave-one-source-out stress test, with strict coverage blocking.

Only holdouts preserving at least one chemical assertion for EVERY focal herb
are eligible for a 45-pair rank comparison. This prevents silently ranking
herbs whose chemistry evidence has disappeared entirely.
"""
import csv, itertools, json, sys, random
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import model_reanalysis as model
from evidence_qualification import read_csv, save_csv, OUT, R, ROOT as BASE

def run():
    old=read_csv(R/'19_class_candidate/embedding_cosine_45pairs_10seeds.csv')
    original_rows=read_csv(R/'CHEMICAL_ASSERTION_EVIDENCE_REVIEW_30.csv')
    taxa={r['name']:r['class_v05'] for r in read_csv(R/'CHEMICAL_IDENTITY_TAXONOMY_25.csv')}
    model.CLASS.clear();model.CLASS.update(taxa)
    data=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text(encoding='utf-8'))
    snapshot=json.loads((R/'formula_reviewed_snapshot.json').read_text(encoding='utf-8'))
    chem=[a for a in data['assertions'] if a['assertion_type']=='ChemistryOccurrenceAssertion']
    srcmap={r['assertion_id']:r['occurrence_source_id'] for r in original_rows}
    assert set(srcmap)=={a['assertion_id'] for a in chem}
    ids=[r['id'] for r in data['herbs']]
    pairs=list(itertools.combinations(ids,2))
    baselines={}
    for m in ('Chem-Proxy','Core-Proxy'):
        for seed in model.SEEDS:
            z={(r['herb_a'],r['herb_b']):float(r['cosine']) for r in old if r['model']==m and int(r['seed'])==seed}
            assert len(z)==45
            baselines[(m,seed)]=np.array([z[p] for p in pairs])
    status=[];results=[]
    for source in sorted(set(srcmap.values())):
        filtered=[a for a in chem if srcmap[a['assertion_id']]!=source]
        remaining={a['subject_id'] for a in filtered}
        absent=sorted(set(ids)-remaining)
        eligible=not absent
        status.append({'source_removed':source,'rows_removed':len(chem)-len(filtered),
                       'herbs_missing_chemistry':';'.join(absent),'eligible_for_all_45_pairs':int(eligible),
                       'reason':('PASS: each herb still represented' if eligible else 'BLOCK: at least one focal herb loses all chemical assertions')})
        if not eligible:continue
        for seed in model.SEEDS:
            cooc=model.generate_cooc(snapshot['formulas'],ids,seed)
            chemseq=model.generate_chem(filtered,ids,seed)
            for m in ('Chem-Proxy','Core-Proxy'):
                if m=='Chem-Proxy':seq=chemseq
                else:
                    seq=cooc[:len(cooc)//2]+chemseq[:len(chemseq)//2]
                    random.Random(seed).shuffle(seq)
                new=model.cos_vectors(seq,ids,seed)
                before=baselines[(m,seed)]
                rho=float(spearmanr(before,new).statistic)
                top1=set(np.argsort(-before)[:5]);top2=set(np.argsort(-new)[:5]);overlap=len(top1&top2)
                results.append({'held_out_source':source,'model':m,'seed':seed,'rank_rho_baseline_vs_holdout':round(rho,7),
                                'mean_absolute_cosine_change':round(float(np.mean(np.abs(before-new))),7),
                                'top5_overlap':overlap,'retained_assertions':len(filtered),'baseline_taxonomy':'new candidate 19-class; not archived original'})
    save_csv(OUT/'source_holdout_embedding_eligibility_12.csv',status)
    assert results
    save_csv(OUT/'source_holdout_embedding_eligible_10seeds.csv',results)
    groups=defaultdict(list)
    for r in results:groups[(r['held_out_source'],r['model'])].append(r)
    summary=[{'source_removed':s,'model':m,'seeds':len(g),
              'mean_rank_rho':round(float(np.mean([x['rank_rho_baseline_vs_holdout'] for x in g])),6),
              'mean_top5_overlap':round(float(np.mean([x['top5_overlap'] for x in g])),4)} for (s,m),g in groups.items()]
    save_csv(OUT/'source_holdout_model_summary.csv',summary)
    out={'holdouts_total':len(status),'holdouts_blocked_due_to_missing_herb_evidence':sum(not int(x['eligible_for_all_45_pairs']) for x in status),
         'holdouts_eligible':len(groups)//2,'paired_seed_model_comparisons':len(results),'exploratory_not_biological_accuracy':True}
    (OUT/'source_holdout_model_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    return out

if __name__=='__main__':print(json.dumps(run(),indent=2))