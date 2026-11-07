"""Matched-seed Cooc Word2Vec sensitivity to primary-source correction.

Exploratory experiment only: not byte-identical to archived Paper 1 embedding.
Do not use for Chem/Core or as a biological validity claim.
"""
import argparse,csv,hashlib,itertools,json,random,sys
from pathlib import Path
import numpy as np
from gensim.models import Word2Vec
from scipy.stats import spearmanr
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_paper1 import CHECKED_FORMULA_MEMBERS,SEEDS,METHODS,npmi,weights,csv_write

def walks(w,ids,seed):
    rng=random.Random(seed)
    adj={h:[] for h in ids}
    for (a,b),wt in w.items():
        if wt>0:
            adj[a].append((b,wt));adj[b].append((a,wt))
    result=[]
    for h in ids:
        for _ in range(60):
            sequence=[h]
            for _ in range(19):
                current=sequence[-1]
                neighbors=adj[current]
                if not neighbors:break
                sequence.append(rng.choices([n for n,_ in neighbors],weights=[v for _,v in neighbors],k=1)[0])
            result.append(sequence)
    rng.shuffle(result)
    return result

def stable_hash(s):
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],"big")

def embed(w,ids,seed):
    seq=walks(w,ids,seed)
    model=Word2Vec(sentences=seq,vector_size=32,window=5,min_count=1,sg=1,
        negative=5,epochs=15,workers=1,seed=seed,hashfxn=stable_hash,sample=1e-3)
    pairs=list(itertools.combinations(ids,2))
    return np.asarray([float(model.wv.similarity(a,b)) if a in model.wv and b in model.wv else np.nan for a,b in pairs])

def corr(a,b):
    val=float(spearmanr(a,b).statistic)
    return val if np.isfinite(val) else None

def test(path,out):
    data=json.loads(Path(path).read_text(encoding='utf8'))
    ids=[h['id'] for h in data['herbs']]
    before=data['formulas']
    from copy import deepcopy
    after=deepcopy(before)
    for f in after:
        f['herbs']=[h for h in f['herbs'] if CHECKED_FORMULA_MEMBERS.get((f['id'],h),(True,))[0] is not False]
    output=Path(out);output.mkdir(exist_ok=True,parents=True)
    detailed=[];summaries=[]
    for method in METHODS:
        original=weights(npmi(before,ids),method)
        partial=weights(npmi(after,ids),method)
        x=[embed(original,ids,seed) for seed in SEEDS]
        y=[embed(partial,ids,seed) for seed in SEEDS]
        paired=[]
        for seed,va,vb in zip(SEEDS,x,y):
            rho=corr(va,vb)
            a=set(np.argsort(-va)[:5]);b=set(np.argsort(-vb)[:5]);overlap=len(a&b)
            detailed.append({'weighting_method':method,'seed':seed,
                             'rank_spearman_original_vs_partial':round(rho,7),
                             'top5_overlap':overlap,
                             'mean_absolute_cosine_change':round(float(np.abs(va-vb).mean()),7)})
            paired.append(rho)
        pairx=[corr(u,v) for u,v in itertools.combinations(x,2)]
        pairy=[corr(u,v) for u,v in itertools.combinations(y,2)]
        summaries.append({'weighting_method':method,
                          'paired_seed_rank_rho_mean':round(float(np.mean(paired)),7),
                          'paired_seed_rank_rho_min':round(float(min(paired)),7),
                          'within_original_seed_rank_rho':round(float(np.mean(pairx)),7),
                          'within_partial_seed_rank_rho':round(float(np.mean(pairy)),7),
                          'paired_top5_overlap_mean':round(float(np.mean([v['top5_overlap'] for v in detailed if v['weighting_method']==method])),7),
                          'seed_count':len(SEEDS)})
        print('completed',method,flush=True)
    csv_write(output/'embedding_pair_seed_sensitivity.csv',detailed)
    csv_write(output/'embedding_sensitivity_summary.csv',summaries)
    (output/'embedding_environment.json').write_text(json.dumps({
       'analysis':'exploratory source-correction sensitivity; COOC ONLY',
       'input_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
       'seeds':SEEDS,'word2vec':{'vector_size':32,'window':5,'negative':5,'epochs':15,'sg':1,'workers':1,'sample':0.001},
       'walks':{'per_herb':60,'max_nodes':20},
       'original_archived_walks_and_vectors':'UNAVAILABLE',
       'validation_status':'UNVERIFIED - only 14 of 46 original positive formula membership rows source-reviewed',
       'runtime_versions':{'numpy':np.__version__, 'gensim':__import__('gensim').__version__,'scipy':__import__('scipy').__version__}
    },ensure_ascii=False,indent=2),encoding='utf8')
    return summaries

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',default='data/paper1_bootstrap_v3_proxy.json');p.add_argument('--out',default='results');a=p.parse_args()
    print(json.dumps(test(a.data,a.out),ensure_ascii=False,indent=2))