"""ThaiHerb Paper 2 v0.4: primary-compendium species audit and class-free embeddings.

No chemical class ontology is reconstructed or claimed. No human expert gold labels.
The 20 focal herbs and 10 formulas are selected and not nationally representative.
"""
from __future__ import annotations
import csv, json, math, itertools, hashlib, random, platform
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import scipy, gensim
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score
from gensim.models import Word2Vec

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
DATA=ROOT/'data'
SEEDS=[11,23,37,41,53,67,79,83,97,101,109,127,137,149,163,173,181,191,199,211]
PDF_URL='https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf'
# This table was manually checked in the official full ingredient tables, including continuations.
# Presence is at the botanical-species level, NOT medicinal-part equivalence.
REVIEW={
 'F01_DTAM2566':(['H11','H12','H13','H14','H15','H16'],[1,2]),
 'F02_DTAM2566':([],[27,28]),
 'F03_DTAM2566':(['H18'],[122,123]),
 'F04_DTAM2566':(['H15','H17'],[143,144]),
 'F05_DTAM2566':(['H15','H16','H17','H20'],[161,162]),
 'F06_DTAM2566':(['H17'],[164,165]),
 'F07_DTAM2566':(['H12','H13','H19'],[240,241]),
 'F08_DTAM2566':(['H11','H12','H13','H14','H15'],[49,50,51]),
 'F09_DTAM2566':(['H11','H12','H13','H14','H15','H17'],[71,72]),
 'F10_DTAM2566':([],[386,387]),
}
SPECIAL={
 ('F01_DTAM2566','H11'):'Both Somo Thai pericarp and Ko Thung Pla insect gall, same botanical species; distinct materials.',
 ('F08_DTAM2566','H11'):'Only Ko Thung Pla gall is present: NOT Somo Thai fruit/pericarp material, although same botanical species.',
 ('F09_DTAM2566','H11'):'Somo Thai and Somo Thet (imported material) both recorded as Terminalia chebula pericarp.',
 ('F01_DTAM2566','H13'):'Aril and seed of Myristica fragrans are distinct medicinal materials; species-level collapse.',
 ('F07_DTAM2566','H13'):'Aril and seed of Myristica fragrans both listed; do not treat as same plant part.',
 ('F08_DTAM2566','H13'):'Aril and seed of Myristica fragrans both listed; do not treat as same plant part.',
 ('F09_DTAM2566','H13'):'Aril and seed of Myristica fragrans both listed; do not treat as same plant part.',
}

def csvsave(name,rows):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def readcsv(p):
    with Path(p).open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def seedhash(s):return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],'big')

def load():
    d=json.loads((DATA/'paper2_bootstrap_v3_proxy.json').read_text(encoding='utf-8'))
    paper1=json.loads((DATA/'paper1_formula_reviewed_snapshot.json').read_text(encoding='utf-8'))
    return d,paper1

def audit(d,p1):
    herbs={h['id']:h for h in d['herbs']}
    orig={f['id']:f for f in d['formulas']}
    legacy={f['id']:f for f in p1['formulas']}
    assert len(herbs)==20 and len(orig)==len(legacy)==len(REVIEW)==10
    rows=[];diff=[];mat=[];correction=[]
    for fid,(new,pages) in REVIEW.items():
        new=set(new);old=set(orig[fid]['herbs']);past=set(legacy[fid]['herbs'])
        assert set(old)&set(list(herbs)[:10])==past, fid
        checked=past|new
        for h in herbs:
            was=int(h in old);now=int(h in checked)
            note=SPECIAL.get((fid,h),'')
            rec={'formula_id':fid,'herb_id':h,'thai_name':herbs[h]['thai'],'prior_v03_present':was,'source_reviewed_species_present':now,
              'audit_layer':'PAPER1_INHERITED_SINGLE_CURATOR' if h in list(herbs)[:10] else 'NEW_HERB_MANUAL_PRIMARY_COMPENDIUM',
              'official_printed_pages':';'.join(map(str,pages)),'pdf_pages_zero_index':';'.join(str(x+8) for x in pages),
              'source_url':PDF_URL,'scientific_name':herbs[h]['scientific'],
              'interpretation':'SPECIES_PROJECTION_NOT_MEDICINAL_MATERIAL_EQUIVALENCE',
              'special_material_note':note,'independent_human_adjudication':0}
            rows.append(rec)
            if h in list(herbs)[10:]:mat.append(rec)
            if was!=now:diff.append({**rec,'change':'ADD_MISSING_SPECIES_MEMBERSHIP' if now else 'REMOVE_UNSUPPORTED_SPECIES_MEMBERSHIP'})
        correction.append({'formula_id':fid,'official_printed_pages':';'.join(map(str,pages)),
          'v03_herbs':len(old),'v04_species_herbs':len(checked),'added':len(checked-old),'removed':len(old-checked),'all_ten_new_herb_cells_reviewed':1})
        orig[fid]['herbs']=sorted(checked)
        orig[fid]['title_th']=legacy[fid]['title']
        orig[fid]['name_status']='source_reviewed_from_official_compendium_single_curator'
        orig[fid]['official_printed_pages']=pages
    assert len(rows)==200 and len(mat)==100
    assert len(diff)==3 and {(r['formula_id'],r['herb_id']) for r in diff}=={('F09_DTAM2566',x) for x in ('H11','H15','H17')}
    assert sum(len(f['herbs']) for f in orig.values())==74
    # Freeze a semantically consistent snapshot: formula metadata, herb counts and assertions must change together.
    newherbs=[]
    for h in d['herbs']:
        hh=dict(h);hh['v3_formula_count']=hh.get('formula_count');hh['v3_reported_formula_count']=hh.get('reported_formula_count')
        hh['formula_count']=sum(hh['id'] in f['herbs'] for f in orig.values())
        hh['reported_formula_count']=hh['formula_count'];newherbs.append(hh)
    chemistry=[a for a in d['assertions'] if a['assertion_type']=='ChemistryOccurrenceAssertion']
    membership=[]
    for fid,form in orig.items():
        for h in form['herbs']:
            membership.append({'assertion_id':'FAV04_'+fid.split('_')[0]+'_'+h,
              'assertion_type':'FormulaMembershipAssertion','subject_id':h,'predicate_or_topic':'ingredient_species_member_of',
              'object_id':fid,'object_label':form['title_th'],'evidence_mode':'official_compendium',
              'directness_or_direction':'documentary_species_projection','source_id':'SRC_FORMULA',
              'source_locator_or_context':'Printed pages '+','.join(map(str,form['official_printed_pages'])),
              'assertion_status':'AI_ASSISTED_SINGLE_CURATOR_SOURCE_REVIEW',
              'limitation_or_finding':'Species-level only; does not imply medicinal material or plant part identity.',
              'channel':'formula'})
    assert len(membership)==74 and len(chemistry)==100
    csvsave('SOURCE_REVIEW_FORMULA_ASSERTIONS_74.csv',membership)
    dataset={'source_dataset':'V3-derived formula projection + official compendium review of H11-H20','formula_projection':'species_level','original_35_class_table_recovered':False,
      'herbs':newherbs,'formulas':list(orig.values()),'assertions':membership+chemistry,'compounds':d['compounds'],'source_pdf':PDF_URL,
      'original_v3_assertions_count':len(d['assertions'])}
    (DATA/'paper2_source_reviewed_species_v04.json').write_text(json.dumps(dataset,ensure_ascii=False,indent=2),encoding='utf-8')
    csvsave('SOURCE_REVIEW_MATRIX_200.csv',rows);csvsave('NEW_HERBS_SOURCE_REVIEW_100.csv',mat);csvsave('FORMULA_MEMBERSHIP_CORRECTIONS.csv',diff);csvsave('FORMULA_SPECIES_AUDIT_10.csv',correction)
    return dataset,diff,mat

def cooc_pairs(formulas,ids):
    n=len(formulas);occ={h:{f['id'] for f in formulas if h in f['herbs']} for h in ids}; out=[]
    for a,b in itertools.combinations(ids,2):
        k=len(occ[a]&occ[b]);na=len(occ[a]);nb=len(occ[b]);v=math.log((k/n)/((na/n)*(nb/n)))/-math.log(k/n) if 0<k<n and na and nb else 0.
        out.append({'herb_a':a,'herb_b':b,'support':k,'npmi':v,'positive_npmi':max(0,v),'formula_count_a':na,'formula_count_b':nb})
    return out

def cooc_walks(formulas,ids,seed,mode='npmi'):
    pairs=cooc_pairs(formulas,ids);deg=Counter()
    for r in pairs:
        if r['positive_npmi']>0:deg.update([r['herb_a'],r['herb_b']])
    adj=defaultdict(list)
    for r in pairs:
        w=r['positive_npmi'];s=r['support']
        if w<=0 or (mode=='support2' and s<2):continue
        if mode in ('support','combined'):w*=s/(s+2)
        if mode=='combined':w/=max(1,deg[r['herb_a']]*deg[r['herb_b']])**.25
        a,b=r['herb_a'],r['herb_b'];adj[a].append((b,w));adj[b].append((a,w))
    rnd=random.Random(seed);walks=[]
    for h in ids:
        for _ in range(60):
            path=[h]
            for _ in range(19):
                choices=adj[path[-1]]
                if not choices:break
                path.append(rnd.choices([x[0] for x in choices],weights=[x[1] for x in choices])[0])
            walks.append(path)
    rnd.shuffle(walks);return walks

def chem_walks(claims,ids,seed):
    byh=defaultdict(list);byc=defaultdict(list)
    for c in claims:
        byh[c['subject_id']].append(c['object_id']);byc[c['object_id']].append(c['subject_id'])
    rnd=random.Random(seed);walks=[]
    for h in ids:
        for _ in range(60):
            here=h;path=[h]
            for _ in range(5):
                if not byh[here]:break
                c=rnd.choice(byh[here]);here=rnd.choice(byc[c]);path.extend(['C:'+c,here])
            walks.append(path)
    rnd.shuffle(walks);return walks

def mixed(co,ch,seed,ratio):
    k=int(round(1200*ratio));seq=co[:k]+ch[:1200-k];random.Random(seed).shuffle(seq)
    return seq,{'cooc_walks':k,'chem_walks':1200-k,'cooc_tokens':sum(map(len,co[:k])),'chem_tokens':sum(map(len,ch[:1200-k]))}

def vectors(walks,ids,seed):
    m=Word2Vec(sentences=walks,vector_size=32,window=5,negative=5,epochs=15,min_count=1,workers=1,sg=1,seed=seed,hashfxn=seedhash,sample=.001)
    return np.array([float(m.wv.similarity(a,b)) for a,b in itertools.combinations(ids,2)],float)

def summary_stats(x):return {'mean':round(float(np.mean(x)),6),'sd':round(float(np.std(x)),6),'min':round(float(np.min(x)),6),'max':round(float(np.max(x)),6)}

def run_models(dataset):
    ids=[h['id'] for h in dataset['herbs']];formulas=dataset['formulas'];chem=[x for x in dataset['assertions'] if x['assertion_type']=='ChemistryOccurrenceAssertion']
    assert len(chem)==100 and len(ids)==20 and len(formulas)==10
    pairs=list(itertools.combinations(ids,2));assert len(pairs)==190
    npmi=cooc_pairs(formulas,ids);csvsave('COOC_EDGES_SOURCE_REVIEWED_190.csv',npmi)
    pset=defaultdict(list)
    for c in chem:pset[c['subject_id']].append(c)
    rnd=random.Random(20261107);pruned=[]
    for h in ids:
        r=pset[h][:];assert len(r)==5;pruned.extend([x for j,x in enumerate(r) if j!=rnd.randrange(len(r))])
    modes=['Cooc-NPMI','Cooc-Support','Cooc-Combined','Cooc-Support2','Chem-Exact','Chem-ExactPrune4','Core-Exact50','Core-Exact25','Core-Exact75']
    allscores=[];token=[];storage=defaultdict(list)
    for seed in SEEDS:
        co=cooc_walks(formulas,ids,seed);cs=cooc_walks(formulas,ids,seed,'support');cc=cooc_walks(formulas,ids,seed,'combined');s2=cooc_walks(formulas,ids,seed,'support2')
        ch=chem_walks(chem,ids,seed);cp=chem_walks(pruned,ids,seed)
        corp={'Cooc-NPMI':co,'Cooc-Support':cs,'Cooc-Combined':cc,'Cooc-Support2':s2,'Chem-Exact':ch,'Chem-ExactPrune4':cp}
        for ratio in (.5,.25,.75):
            name=f'Core-Exact{int(ratio*100)}';seq,st=mixed(co,ch,seed,ratio);corp[name]=seq;token.append({'model':name,'seed':seed,**st,'cooc_token_share':st['cooc_tokens']/(st['cooc_tokens']+st['chem_tokens'])})
        for name in modes:
            v=vectors(corp[name],ids,seed)
            if not np.isfinite(v).all():raise RuntimeError('missing vector '+name)
            storage[name].append(v)
            allscores.extend({'model':name,'seed':seed,'herb_a':a,'herb_b':b,'cosine':round(float(x),8)} for (a,b),x in zip(pairs,v))
        print('finished seed',seed,flush=True)
    csvsave('ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv',allscores);csvsave('CORE_TOKEN_BUDGETS.csv',token)
    scores=[];perpair=[]
    for name in modes:
        vals=np.array(storage[name]);rhos=[float(spearmanr(a,b).statistic) for a,b in itertools.combinations(vals,2)]
        scores.append({'model':name,'seeds':20,'seed_pair_comparisons':190,'herb_pairs':190,**summary_stats(rhos),'biological_gold_available':0,'status':'SOURCE_REVIEWED_SPECIES_AND_EXACT_COMPOUND_RECONSTRUCTION'})
        for (a,b),mu,sd in zip(pairs,vals.mean(axis=0),vals.std(axis=0)):
            perpair.append({'model':name,'herb_a':a,'herb_b':b,'mean_cosine':round(float(mu),8),'sd_cosine':round(float(sd),8)})
    csvsave('SEED_REPEATABILITY_20SEEDS.csv',scores);csvsave('MEAN_PAIR_SIMILARITIES.csv',perpair)
    perturb=[]
    for variant,baseline in [('Cooc-Support','Cooc-NPMI'),('Cooc-Combined','Cooc-NPMI'),('Cooc-Support2','Cooc-NPMI'),('Chem-ExactPrune4','Chem-Exact'),('Core-Exact25','Core-Exact50'),('Core-Exact75','Core-Exact50')]:
        a=np.mean(storage[variant],axis=0);b=np.mean(storage[baseline],axis=0)
        perturb.append({'variant':variant,'baseline':baseline,'mean_ranking_spearman':round(float(spearmanr(a,b).statistic),6),'top10_overlap':len(set(np.argsort(-a)[:10])&set(np.argsort(-b)[:10])),'not_biological_validity':1})
    csvsave('PERTURBATION_COMPARISON_20SEEDS.csv',perturb)
    # Fixed-pair simple baselines used only for descriptive structural overlap.
    byh={h:set(c['object_id'] for c in chem if c['subject_id']==h) for h in ids}
    chemj=[{'herb_a':a,'herb_b':b,'shared_exact_compounds':len(byh[a]&byh[b]),'jaccard':len(byh[a]&byh[b])/max(1,len(byh[a]|byh[b]))} for a,b in pairs]
    csvsave('EXACT_COMPOUND_OVERLAP_190.csv',chemj)
    return scores,npmi,perturb,chemj

def lofo(dataset):
    forms=dataset['formulas'];ids=[h['id'] for h in dataset['herbs']];pairs=list(itertools.combinations(ids,2))
    folds=[];details=[]
    for hold in forms:
        train=[x for x in forms if x['id']!=hold['id']];occ=Counter(h for f in train for h in f['herbs']);cold=[h for h in ids if not occ[h]]
        y=np.array([int(a in hold['herbs'] and b in hold['herbs']) for a,b in pairs]);ep=cooc_pairs(train,ids)
        folds.append({'heldout_formula':hold['id'],'train_formulas':9,'cold_start_herbs':';'.join(cold),'all_190_pairs_evaluable':int(not cold),'label_prevalence':round(float(y.mean()),6),'positive_pairs':int(y.sum())})
        if cold:continue
        for name,x in [('PairSupport',np.array([z['support'] for z in ep],float)),('PositiveNPMI',np.array([z['positive_npmi'] for z in ep],float)),('DegreeProduct',np.array([z['formula_count_a']*z['formula_count_b'] for z in ep],float))]:
            details.append({'heldout_formula':hold['id'],'model':name,'average_precision':round(float(average_precision_score(y,x)),6),'auroc':round(float(roc_auc_score(y,x)),6),'not_external_biological_validation':1})
    csvsave('LOFO_COVERAGE_10.csv',folds);csvsave('LOFO_STRUCTURAL_BASELINES.csv',details)
    return folds,details

def main():
    orig,p1=load();dataset,diffs,mat=audit(orig,p1);seed,npmi,pert,chemj=run_models(dataset);folds,base=lofo(dataset)
    npos=sum(r['positive_npmi']>0 for r in npmi)
    chem= [x for x in dataset['assertions'] if x['assertion_type']=='ChemistryOccurrenceAssertion']
    source_counts=Counter(x['source_id'] for x in chem)
    status={'release':'Paper2 v0.4','release_date':'2026-11-07','study_type':'exploratory internal robustness on a source-reviewed species-projection',
      'official_source_pdf':PDF_URL,'formula_source_review':'AI-assisted single-curator, reviewed all added-H11-H20 cells using full ingredient tables; human independent adjudication not available',
      'original_memberships':71,'source_reviewed_species_memberships':74,'added_rows':len(diffs),'source_reviewed_added_herb_cells':len(mat),'unique_herbs':20,'formula_count':10,
      'positive_npmi_edges':npos,'rare_positive_npmi_edges_support_one':sum(r['positive_npmi']>0 and r['support']==1 for r in npmi),
      'chemical_assertions':len(chem),'exact_compounds':len({x['object_id'] for x in chem}),'chemical_source_ids':len(source_counts),
      'original_35_class_mapping_available':False,'chemical_classes_used':False,'chemical_model':'H-C-H exact compound only',
      'genuine_independent_expert_labels':False,'independent_external_formula_corpus':False,
      '20_seed_models':len(seed),'model_fits':20*len(seed),'pairs_per_model':190,
      'LOFO_full_pair_eligible_folds':sum(x['all_190_pairs_evaluable'] for x in folds),
      'inputs_sha256':{p.name:sha(p) for p in sorted(DATA.glob('*')) if p.is_file()},
      'software_versions':{'numpy':np.__version__,'scipy':scipy.__version__,'gensim':gensim.__version__,'python':platform.python_version()},
      'special_material_caution':'H11 Terminalia chebula herb may be gall vs fruit; H13 Myristica fragrans aril vs seed; botanical species is not medicinal-material identity.'}
    (OUT/'RELEASE_MANIFEST.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SUMMARY',json.dumps({'formula_memberships':74,'positive_npmi':npos,'models':seed,'lofo_eligible':status['LOFO_full_pair_eligible_folds']},ensure_ascii=False,indent=2),flush=True)
    return status
if __name__=='__main__': main()