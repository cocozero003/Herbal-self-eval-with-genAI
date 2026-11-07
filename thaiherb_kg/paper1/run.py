"""Paper 1: source-locked Cooc weighting audit, not a rerun of historical embeddings."""
from pathlib import Path
import json,statistics
from shared import load_json,weights,ranks,correlation,write_csv,sha256
ROOT=Path(__file__).resolve().parents[1]

def run():
    doc=load_json(ROOT/'data/paper1_bootstrap.json')
    herbs=[r['id'] for r in doc['herbs']]; forms=doc['formulas']
    assert len(herbs)==10 and len(forms)==10
    edges=weights(forms,herbs)
    assert len(edges)==45 and sum(x['npmi']>0 for x in edges.values())==23
    original={(x['a'],x['b']):x['npmi'] for x in doc['pairs']}
    assert all(abs(edges[k]['npmi']-v)<1e-7 for k,v in original.items() if v is not None and v>0)
    items=[{'a':a,'b':b,**row} for (a,b),row in edges.items()]
    write_csv(ROOT/'paper1/edge_weight_comparison.csv',items)
    methods=['npmi','support_weight','degree_weight','combined_weight']
    lofo=[]
    for f in forms:
        new=weights([x for x in forms if x['id']!=f['id']],herbs)
        for method in methods:
            x=[edges[p][method] for p in edges]; y=[new[p][method] for p in edges]
            lofo.append({'heldout_formula':f['id'],'weighting':method,
                         'spearman_with_full_edges':correlation(x,y),
                         'top5_overlap_fraction':len(set(ranks(edges,method)[:5])&set(ranks(new,method)[:5]))/5})
    write_csv(ROOT/'paper1/lofo_edge_analysis.csv',lofo)
    baseline=ranks(edges,'npmi');
    summary={'source':'V3 shared-base reconstruction; NOT independently confirmed identical to original Paper 1 rows',
             'n_herbs':len(herbs),'n_formulas':len(forms),'n_pairs':len(edges),'positive_npmi':23,
             'methods':{m:{'top5_overlap_vs_baseline':len(set(baseline[:5])&set(ranks(edges,m)[:5]))/5,
                           'mean_lofo_edge_spearman':statistics.mean(x['spearman_with_full_edges'] for x in lofo if x['weighting']==m and x['spearman_with_full_edges'] is not None)} for m in methods},
             'caveat':'Graph-edge robustness is not embedding robustness or biological validity.'}
    (ROOT/'paper1/results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary
if __name__=='__main__':print(json.dumps(run(),indent=2))
