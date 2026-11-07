"""Paired formula-cluster bootstrap; not a confirmatory superiority test.

DO NOT treat correlated herb-pair predictions or random seeds as independent.
"""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
RNG=np.random.default_rng(20261107)
summary=pd.read_csv(OUT/'P2_LOFO_FORMULA_LEVEL_MEANS.csv')
models=sorted(summary.model.unique())
rows=[]
for cover in ['FULL_190','PARTIAL_171_COLD_START']:
    piece=summary[summary.coverage_type==cover]
    ref=piece[piece.model=='PairSupport'].sort_values('fold').set_index('fold')
    folds=list(ref.index)
    n=len(folds)
    indices=RNG.integers(0,n,size=(4000,n))
    for model in models:
        candidate=piece[piece.model==model].set_index('fold').loc[folds]
        for endpoint in ['AP','AUROC']:
            diff=candidate[endpoint].to_numpy()-ref[endpoint].to_numpy()
            boot=diff[indices].mean(axis=1)
            rows.append({'coverage_type':cover,'model':model,'reference':'PairSupport',
                         'endpoint':endpoint,'fold_clusters':n,
                         'mean_paired_difference':round(float(diff.mean()),6),
                         'cluster_boot_95_low':round(float(np.quantile(boot,.025)),6),
                         'cluster_boot_95_high':round(float(np.quantile(boot,.975)),6),
                         'bootstrap_draws':4000,'confirmatory_p_value':'NOT_COMPUTED_EXPLORATORY',
                         'interpretation':'DOC_FORMULA_MEMBERSHIP_NOT_BIOLOGICAL_GENERALIZATION'})
pd.DataFrame(rows).to_csv(OUT/'P2_PAIRED_CLUSTER_BOOTSTRAP_VS_PAIRSUPPORT.csv',encoding='utf-8-sig',index=False)
print(pd.DataFrame(rows).query("coverage_type=='FULL_190' and endpoint=='AP'")[['model','mean_paired_difference','cluster_boot_95_low','cluster_boot_95_high']].to_string(index=False))
