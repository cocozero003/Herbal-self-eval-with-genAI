"""Explicitly exploratory class-family and material-context sensitivity tests.

The chemical classes are *new, provisional 31-family hypotheses*, NOT original
35-class labels. Removing F08 H11 is a material-specific counterfactual, not
correction to the archival species-level formula membership.
"""
import itertools, importlib.util, json, random
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'input'/'v04'
OUT=ROOT/'results'
PREV=ROOT/'input'/'evidence_v12'
spec=importlib.util.spec_from_file_location('v04',OLD/'src'/'reanalyse.py');v04=importlib.util.module_from_spec(spec);spec.loader.exec_module(v04)

def main():
    d=json.loads((OLD/'data'/'paper2_source_reviewed_species_v04.json').read_text(encoding='utf-8'))
    ids=[h['id'] for h in d['herbs']];forms=d['formulas'];claims=[c for c in d['assertions'] if c['assertion_type']=='ChemistryOccurrenceAssertion']
    pairs=list(itertools.combinations(ids,2))
    archive=pd.read_csv(OLD/'results'/'ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv').set_index(['model','seed','herb_a','herb_b'])['cosine']
    family=pd.read_csv(PREV/'P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv',dtype=str)
    assert len(family)==83 and family.reconstructed_family_id.nunique()==31 and family.original_35class_id.isna().all()
    mapping=dict(zip(family.compound_id_internal,family.reconstructed_family_id))
    assert all(c['object_id'] in mapping for c in claims)
    family_claims=[{**c,'object_id':mapping[c['object_id']]} for c in claims]
    material_forms=[{**f,'herbs':[h for h in f['herbs'] if not (f['id']=='F08_DTAM2566' and h=='H11')]} for f in forms]
    assert sum(len(f['herbs']) for f in material_forms)==73
    rows=[];scores=[]
    for seed in v04.SEEDS:
        ch=v04.chem_walks(family_claims,ids,seed)
        co=v04.cooc_walks(forms,ids,seed)
        scenarios={
            'Chem-ExploratoryFamily31':v04.vectors(ch,ids,seed),
            'Core-ExploratoryFamily31-50':v04.vectors(v04.mixed(co,ch,seed,.5)[0],ids,seed),
            'Cooc-MaterialCounterfactualF08H11':v04.vectors(v04.cooc_walks(material_forms,ids,seed),ids,seed)
        }
        for name,v in scenarios.items():
            ref=('Chem-Exact' if name.startswith('Chem-') else 'Core-Exact50' if name.startswith('Core-') else 'Cooc-NPMI')
            origin=np.array([archive.loc[(ref,seed,a,b)] for a,b in pairs])
            rank=float(spearmanr(v,origin).statistic)
            top10=len(set(np.argsort(-v)[:10]) & set(np.argsort(-origin)[:10]))
            rows.append({'scenario':name,'reference':ref,'seed':seed,'rank_spearman':rank,
                         'top10_overlap':top10,'scientific_status':'PROVISIONAL_SENSITIVITY_NO_ORIGINAL_35CLASS_REPLICATION'})
            for (a,b),sim in zip(pairs,v):
                scores.append({'scenario':name,'seed':seed,'herb_a':a,'herb_b':b,'cosine':float(sim)})
    pd.DataFrame(rows).to_csv(OUT/'P2_PROVISIONAL_CLASS_MATERIAL_SENSITIVITY_20SEEDS.csv',index=False)
    pd.DataFrame(scores).to_csv(OUT/'P2_PROVISIONAL_CLASS_MATERIAL_PAIR_SCORES.csv',index=False)
    print(pd.DataFrame(rows).groupby('scenario')[['rank_spearman','top10_overlap']].agg(['mean','std']).to_string())

if __name__=='__main__':main()
