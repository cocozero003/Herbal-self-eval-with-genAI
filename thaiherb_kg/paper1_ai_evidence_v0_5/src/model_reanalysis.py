"""Reproducible 10-herb exploratory sibling-model reanalysis.

Chem class labels are NEW candidate annotations, NOT recovered 19 original
compound classes. Results never reproduce claimed archived Paper 1 vectors.
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import csv,random,hashlib,json
import numpy as np
from scipy.stats import spearmanr
from gensim.models import Word2Vec
from formula_audit import write_csv,npmi

# Candidate taxonomy for exploratory reconstruction ONLY; not the original study class table.
CLASS = {
'6-gingerol':'ginger phenolic ketone','6-shogaol':'ginger phenolic ketone','zingerone':'ginger phenolic ketone',
'piperine':'piperidine alkaloid','pellitorine':'alkamide','piperlongumine':'piperidine alkaloid',
'beta-caryophyllene':'sesquiterpene hydrocarbon','limonene':'monoterpene hydrocarbon',
'allicin':'organosulfur thiosulfinate','alliin':'organosulfur amino acid','diallyl sulfide':'organosulfur sulfide',
'sabinene':'monoterpene hydrocarbon','DMPBD':'phenylbutanoid','terpinen-4-ol':'monoterpene alcohol',
"1'-acetoxychavicol acetate":'phenylpropanoid ester',"1'-acetoxyeugenol acetate":'phenylpropanoid ester','galangin':'flavonol',
'rosmarinic acid':'phenolic acid','oleanolic acid':'triterpenoid', 'eugenol':'phenylpropanoid phenol',
'glycyrrhizin':'triterpene saponin','liquiritin':'flavonoid glycoside','liquiritigenin':'flavanone',
'eugenyl acetate':'phenylpropanoid ester','beta-pinene':'monoterpene hydrocarbon'
}
SEEDS=[11,23,37,41,53,67,79,83,97,101]

def st_hash(s):return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],'big')

def cos_vectors(sentences,herb_ids,seed):
    model=Word2Vec(sentences=sentences,vector_size=32,window=5,min_count=1,sg=1,negative=5,epochs=15,workers=1,seed=seed,hashfxn=st_hash,sample=0.001)
    return np.array([float(model.wv.similarity(a,b)) if a in model.wv and b in model.wv else np.nan for a,b in combinations(herb_ids,2)])

def generate_cooc(formulas,ids,seed,mode='npmi'):
    rows=npmi(formulas,ids);degs={h:sum(r['positive_npmi']>0 and h in (r['herb_a'],r['herb_b']) for r in rows) for h in ids}
    adj=defaultdict(list)
    for r in rows:
        a,b=r['herb_a'],r['herb_b'];v=r['positive_npmi'];n=r['support']
        if v<=0:continue
        if mode in ('support','combined'):v*=n/(n+2.)
        if mode in ('degree','combined'):v/=max(1,degs[a]*degs[b])**.25
        adj[a].append((b,v));adj[b].append((a,v))
    rnd=random.Random(seed)
    seq=[]
    for h in ids:
        for _ in range(60):
            w=[h]
            for _ in range(19):
                choices=adj[w[-1]]
                if not choices:break
                w.append(rnd.choices([x for x,_ in choices],weights=[z for _,z in choices],k=1)[0])
            seq.append(w)
    rnd.shuffle(seq)
    return seq

def chem_lookup(chem):
    byh=defaultdict(list);byc=defaultdict(list);byk=defaultdict(list)
    for r in chem:
        h=r['subject_id'];c=r['object_label'];k=CLASS[c]
        byh[h].append(c);byc[c].append(h);byk[k].append(c)
    for k in byk:byk[k]=sorted(set(byk[k]))
    return byh,byc,byk

def generate_chem(chem,ids,seed):
    """H-C-H and H-C-K-C-H motifs (typed tokens retained in walk corpus)."""
    byh,byc,byk=chem_lookup(chem)
    rnd=random.Random(seed);paths=[]
    for h in ids:
        for _ in range(60):
            path=[h];here=h
            for _ in range(5):
                if not byh[here]:break
                c=rnd.choice(byh[here]); klass=CLASS[c]
                if rnd.random()<0.5:
                    neigh=rnd.choice(byc[c]);path.extend(['C:'+c,neigh]);here=neigh
                else:
                    c2=rnd.choice(byk[klass]);neigh=rnd.choice(byc[c2]);path.extend(['C:'+c,'K:'+klass,'C:'+c2,neigh]);here=neigh
            paths.append(path)
    rnd.shuffle(paths);return paths

def train(snapshot,chem,output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    ids=[h['id'] for h in snapshot['herbs']]
    assert len(chem)==30 and len({r['object_label'] for r in chem})==25
    assert set(r['object_label'] for r in chem)==set(CLASS)
    chemistry_rows=[{'herb':r['subject_id'],'compound':r['object_label'],'candidate_class':CLASS[r['object_label']],'source_id':r['source_id'],'source_locator':r.get('source_locator_or_context',''),'research_status':'V3_PROXY_ORIGINAL_19_CLASS_TABLE_UNAVAILABLE'} for r in chem]
    write_csv(out/'chemistry_panel_30_exploratory.csv',chemistry_rows)
    pairs=list(combinations(ids,2));results=[];by_model=defaultdict(list)
    for model in ['Cooc-NPMI','Cooc-Support','Cooc-Degree','Cooc-Combined','Chem-Proxy','Core-Proxy']:
        for seed in SEEDS:
            if model=='Cooc-NPMI':seq=generate_cooc(snapshot['formulas'],ids,seed)
            elif model.startswith('Cooc-'):seq=generate_cooc(snapshot['formulas'],ids,seed,model.split('-')[-1].lower())
            elif model=='Chem-Proxy':seq=generate_chem(chem,ids,seed)
            else:
                c1=generate_cooc(snapshot['formulas'],ids,seed);c2=generate_chem(chem,ids,seed)
                seq=c1[:len(c1)//2]+c2[:len(c2)//2];random.Random(seed).shuffle(seq)
            v=cos_vectors(seq,ids,seed)
            by_model[model].append(v)
            results.extend({'model':model,'seed':seed,'herb_a':a,'herb_b':b,'cosine':round(float(x),9)} for (a,b),x in zip(pairs,v))
    write_csv(out/'embedding_cosine_45pairs_10seeds.csv',results)
    summary=[];pairsum=[]
    for model,vals in by_model.items():
        rho=[float(spearmanr(a,b).statistic) for a,b in combinations(vals,2)]
        topmean=np.mean(np.stack(vals),axis=0)
        summary.append({'model':model,'seeds':len(vals),'seed_pair_rank_spearman_mean':round(float(np.mean(rho)),6),'seed_pair_rank_spearman_sd':round(float(np.std(rho)),6),'seed_pair_rank_spearman_min':round(float(min(rho)),6),'class_status':'original' if model.startswith('Cooc') else 'new_candidate_proxy','not_original_manuscript_vectors':1})
        pairsum.extend({'model':model,'herb_a':a,'herb_b':b,'mean_cosine':round(float(x),6),'sd_cosine':round(float(np.std([v[i] for v in vals])),6)} for i,((a,b),x) in enumerate(zip(pairs,topmean)))
    write_csv(out/'embedding_10seed_summary.csv',summary)
    write_csv(out/'embedding_pair_summary.csv',pairsum)
    (out/'computational_manifest.json').write_text(json.dumps({'n_herbs':len(ids),'n_chem':len(chem),'n_unique_compounds':25,'candidate_class_count':len(set(CLASS.values())),'reported_original_class_count':19,'candidate_class_ontology':'new exploratory taxonomy, not recovered original','environment':{'numpy':np.__version__,'gensim':__import__('gensim').__version__,'scipy':__import__('scipy').__version__},'seeds':SEEDS,'walks_per_herb':60,'walk_max_nodes_cooc':20,'embedding_dim':32,'sg':1,'epochs':15,'worker':1,'validation':'unverified chemistry original panel equivalence; no biological independent validation'},ensure_ascii=False,indent=2),encoding='utf8')
    return summary

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--data',default='data/paper1_bootstrap_v3_proxy.json');ap.add_argument('--snapshot',default='results/formula_reviewed_snapshot.json');ap.add_argument('--out',default='results')
    args=ap.parse_args();data=json.loads(Path(args.data).read_text());snapshot=json.loads(Path(args.snapshot).read_text());chem=[a for a in data['assertions'] if a['assertion_type']=='ChemistryOccurrenceAssertion']
    print(json.dumps(train(snapshot,chem,args.out),indent=2))