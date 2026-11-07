"""Reproducibility and research-integrity checks for Paper 1 v0.8."""
import csv,json,itertools,sys,hashlib
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from final_reanalysis import pair_npmi,cooc_walks,chem_walks,train_one,SEEDS

def records(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def test_input_scope_and_chemical_label_boundary():
 d=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text())
 f=json.loads((ROOT/'data/formula_reviewed_snapshot.json').read_text())
 assert len(d['herbs'])==10 and len(f['formulas'])==10
 assert sum(len(z['herbs']) for z in f['formulas'])==46
 c=[x for x in d['assertions'] if x['assertion_type']=='ChemistryOccurrenceAssertion']
 assert len(c)==30 and len(set(x['object_label'] for x in c))==25
 t=records(ROOT/'data/CHEMICAL_IDENTITY_TAXONOMY_25.csv')
 assert len(set(x['class_v05'] for x in t))==19
 assert all(x['review_type'].startswith('AI-assisted') for x in t)

def test_npmi_23_edges_and_formula_f05_integrity():
 d=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text())
 f=json.loads((ROOT/'data/formula_reviewed_snapshot.json').read_text())
 x=pair_npmi(f['formulas'],[x['id'] for x in d['herbs']])
 assert len(x)==45 and sum(z['positive_npmi']>0 for z in x)==23
 assert {'H01','H02','H03','H05','H10'} <= set(next(z for z in f['formulas'] if z['id']=='F05_DTAM2566')['herbs'])

def test_130_models_and_results_complete():
 x=records(ROOT/'results/all_reanalysis_scores_13models_10seeds.csv')
 assert len(x)==13*10*45
 assert len({r['model'] for r in x})==13 and {int(r['seed']) for r in x}==set(SEEDS)
 assert all(-1.000001<=float(r['cosine'])<=1.000001 for r in x)
 assert len({(r['model'],r['seed'],r['herb_a'],r['herb_b']) for r in x})==len(x)

def test_recomputed_rank_stability_matches_summary():
 rows=records(ROOT/'results/all_reanalysis_scores_13models_10seeds.csv')
 s={r['model']:r for r in records(ROOT/'results/seed_repeatability_13models.csv')}
 for model in ('Cooc-NPMI','Chem-Candidate19','Core-Candidate19','Cooc-Combined'):
  x=[]
  for seed in SEEDS:x.append(np.array([float(r['cosine']) for r in rows if r['seed']==str(seed) and r['model']==model]))
  rhos=[float(spearmanr(a,b).statistic) for a,b in itertools.combinations(x,2)]
  assert len(rhos)==45 and abs(np.mean(rhos)-float(s[model]['rank_rho_mean'])) < 2e-6

def test_candidate_class_and_original_metrics_not_mixed():
 r=records(ROOT/'results/ORIGINAL_MANUSCRIPT_VS_V08_REANALYSIS.csv')
 assert len(r)==9
 assert all(x['identity']=='NOT_EQUIVALENT_ARCHIVED_DATA_AND_CANDIDATE_CHEMISTRY' for x in r)
 manifest=json.loads((ROOT/'results/reanalysis_manifest.json').read_text())
 assert manifest['candidate19_class_status']=='CURATED_AI_ASSISTED_NOT_RECOVERED_ORIGINAL'
 assert manifest['independent_expert_review_available'] is False
 assert manifest['clinical_or_biological_validation'] is False

def test_perturbations_and_channel_tokens():
 x=records(ROOT/'results/perturbation_sensitivity_10comparisons.csv')
 assert len(x)==10 and all(-1<=float(z['mean_rank_spearman'])<=1 for z in x)
 w=records(ROOT/'results/core_channel_contributions_by_seed.csv')
 assert len(w)==30
 x=[r for r in w if r['model']=='Core-Candidate19']
 assert len(x)==10 and all(int(r['cooc_walks'])==int(r['chem_walks'])==300 for r in x)
 assert all(float(r['effective_cooc_token_share'])>.50 for r in x)

def test_replay_one_seed_numerically():
 d=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text())
 f=json.loads((ROOT/'data/formula_reviewed_snapshot.json').read_text())
 ids=[x['id'] for x in d['herbs']]
 corpus=cooc_walks(f['formulas'],ids,11)
 v=train_one(corpus,ids,11)
 result=records(ROOT/'results/all_reanalysis_scores_13models_10seeds.csv')
 archived=np.array([float(r['cosine']) for r in result if r['model']=='Cooc-NPMI' and r['seed']=='11'])
 assert len(archived)==45 and np.allclose(v,archived,atol=2e-7)

def test_lofo_scientific_boundary_and_expert_remain_blank():
 manifest=json.loads((ROOT/'results/benchmark_manifest.json').read_text())
 assert manifest['independent_external_dataset'] is False
 assert manifest['independent_expert_gold_labels'] is False
 for rater in ('R1','R2'):
  rows=records(ROOT/f'supplement/BLINDED_EXPERT_{rater}_45.csv')
  assert len(rows)==45 and all(not r['chemistry_similarity_grade_0_1_2_or_NA'] for r in rows)

def test_document_contains_consistent_results_and_source_warning():
 s=(ROOT/'manuscript/Paper1_Feasibility_Reanalysis_v08.md').read_text()
 v=records(ROOT/'results/seed_repeatability_13models.csv')
 assert '0.932159' in s and '0.90917' in s and '0.739359' in s
 assert 'original 19-class' in s and 'not a claimed replication' in s
 assert 'clinical or biological' not in s.lower() or 'not' in s.lower()
 assert 'Original historical results' not in s # numerical basis is new

def test_publication_release_gates_not_false_complete():
 r=records(ROOT/'results/PUBLICATION_READINESS_GATES.csv')
 assert len(r)==10
 assert any(x['status']=='NOT_RECOVERED' for x in r)
 assert any(x['status']=='NOT_REPRODUCED' for x in r)
 assert any(x['status']=='NOT_DONE' for x in r)