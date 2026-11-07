"""Paper 2: paired weighting sensitivity and chemistry hub audit with fixed original data."""
from pathlib import Path
from collections import defaultdict,Counter
import json, math,statistics
from shared import load_json,weights,ranks,correlation,write_csv
ROOT=Path(__file__).resolve().parents[1]

def chem_similarity(records,herbs):
    byherb={h:set() for h in herbs}
    for row in records:
        if row.get('channel')=='chemistry' and row['subject_id'] in byherb:
            byherb[row['subject_id']].add(row['object_id'])
    df=Counter(c for compounds in byherb.values() for c in compounds)
    # Smoothed inverse frequency: IDF is a computational ranking metric, not evidence grade.
    idf={c:math.log((len(herbs)+1)/(n+1))+1 for c,n in df.items()}
    out=[]
    for i,a in enumerate(herbs):
        for b in herbs[i+1:]:
            sa,sb=byherb[a],byherb[b];inter=sa&sb;union=sa|sb
            out.append({'a':a,'b':b,'shared_compounds':len(inter),
               'jaccard':len(inter)/len(union) if union else 0,
               'idf_jaccard':sum(idf[c] for c in inter)/sum(idf[c] for c in union) if union else 0,
               'shared_compound_ids':';'.join(sorted(inter))})
    return out,df

def run():
    doc=load_json(ROOT/'data/paper2_bootstrap.json')
    herbs=[x['id'] for x in doc['herbs']];forms=doc['formulas']
    w=weights(forms,herbs);assert len(herbs)==20 and len(forms)==10
    assert len(w)==190 and sum(v['npmi']>0 for v in w.values())==82
    write_csv(ROOT/'paper2/cooc_weight_comparison.csv',[{'a':a,'b':b,**row} for (a,b),row in w.items()])
    methods=['npmi','support_weight','degree_weight','combined_weight']; lofo=[]
    for form in forms:
        alt=weights([x for x in forms if x['id']!=form['id']],herbs)
        for m in methods:
            rho=correlation([x[m] for x in w.values()],[alt[p][m] for p in w])
            lofo.append({'heldout_formula':form['id'],'method':m,'edge_rank_spearman':rho,
               'top10_overlap':len(set(ranks(w,m)[:10])&set(ranks(alt,m)[:10]))/10})
    write_csv(ROOT/'paper2/lofo_edge_analysis.csv',lofo)
    chemistry,degree=chem_similarity(doc['assertions'],herbs)
    write_csv(ROOT/'paper2/chemical_similarity_190pairs.csv',chemistry)
    summary={'data_status':'V3 shared-base projection; Paper 2 original row equivalence unverified',
       'n_herbs':len(herbs),'n_formulas':len(forms),'n_formula_edges':82,
       'n_chemistry_assertions':sum(x.get('channel')=='chemistry' for x in doc['assertions']),
       'compound_degree_frequency':{str(k):v for k,v in sorted(Counter(degree.values()).items())},
       'n_chemically_overlapping_pairs':sum(x['shared_compounds']>0 for x in chemistry),
       'methods':{m:{'mean_lofo_edge_rank_spearman':statistics.mean(x['edge_rank_spearman'] for x in lofo if x['method']==m and x['edge_rank_spearman'] is not None),
                    'mean_lofo_top10_overlap':statistics.mean(x['top10_overlap'] for x in lofo if x['method']==m)} for m in methods},
       'warning':'Not a 20-seed embedding rerun; no blinded expert benchmark, no verified chemical structures or Tanimoto computations.'}
    (ROOT/'paper2/results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary
if __name__=='__main__':print(json.dumps(run(),indent=2))
