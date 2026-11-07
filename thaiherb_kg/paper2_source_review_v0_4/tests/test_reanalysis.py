"""Paper2 v0.4 reproducibility and claim-boundary tests."""
import json,csv,hashlib,itertools
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'
def rows(name):
 with (RESULTS/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def manifest():return json.loads((RESULTS/'RELEASE_MANIFEST.json').read_text())
def test_formula_audit_100():
 x=rows('NEW_HERBS_SOURCE_REVIEW_100.csv');assert len(x)==100
 assert all(x['audit_layer']=='NEW_HERB_MANUAL_PRIMARY_COMPENDIUM' and x['independent_human_adjudication']=='0' for x in x)
def test_three_real_corrections_are_locked():
 x=rows('FORMULA_MEMBERSHIP_CORRECTIONS.csv');assert len(x)==3
 assert {(z['formula_id'],z['herb_id']) for z in x}=={('F09_DTAM2566',h) for h in ('H11','H15','H17')}
 assert all(int(r['source_reviewed_species_present'])==1 for r in x)
def test_200_formula_matrix():
 x=rows('SOURCE_REVIEW_MATRIX_200.csv');assert len(x)==200
 assert sum(int(z['source_reviewed_species_present']) for z in x)==74
 assert sum(int(z['prior_v03_present']) for z in x)==71
def test_species_vs_material_is_explicit():
 x=rows('SOURCE_REVIEW_MATRIX_200.csv');d={(z['formula_id'],z['herb_id']):z for z in x}
 assert 'gall' in d[('F08_DTAM2566','H11')]['special_material_note']
 assert 'Aril and seed' in d[('F09_DTAM2566','H13')]['special_material_note']
def test_original_35_class_does_not_sneak_in():
 x=manifest();assert x['original_35_class_mapping_available'] is False
 assert x['chemical_classes_used'] is False and x['chemical_model']=='H-C-H exact compound only'
def test_all_190_pair_score_predictions():
 x=rows('ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv');assert len(x)==9*20*190
 assert len({(r['model'],r['seed'],r['herb_a'],r['herb_b']) for r in x})==len(x)
 assert all(-1.00001<=float(r['cosine'])<=1.00001 for r in x)
def test_20_seeds_190_pair_correlations():
 x=rows('SEED_REPEATABILITY_20SEEDS.csv');assert len(x)==9
 assert all(int(z['seeds'])==20 and int(z['seed_pair_comparisons'])==190 for z in x)
def test_summary_is_recomputed():
 x=rows('ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv');d=rows('SEED_REPEATABILITY_20SEEDS.csv')
 for z in d:
  name=z['model'];vectors=[]
  for seed in [11,23,37,41,53,67,79,83,97,101,109,127,137,149,163,173,181,191,199,211]:
   vectors.append(np.array([float(r['cosine']) for r in x if r['model']==name and int(r['seed'])==seed]))
  corr=[spearmanr(a,b).statistic for a,b in itertools.combinations(vectors,2)]
  assert abs(np.mean(corr)-float(z['mean']))<2e-6
def test_formula_holdouts_rebuilt_on_corrected_data():
 x=rows('LOFO_COVERAGE_10.csv');assert len(x)==10
 assert sum(int(z['all_190_pairs_evaluable']) for z in x)==6
 assert {z['heldout_formula'] for z in x if z['cold_start_herbs']}=={'F02_DTAM2566','F03_DTAM2566','F05_DTAM2566','F07_DTAM2566'}
def test_single_source_chemistry_and_no_external_claim():
 x=manifest();assert x['chemical_source_ids']==20 and x['chemical_assertions']==100
 assert x['independent_external_formula_corpus'] is False and x['genuine_independent_expert_labels'] is False
def test_input_sha256():
 for p,h in manifest()['inputs_sha256'].items():
  assert hashlib.sha256((ROOT/'data'/p).read_bytes()).hexdigest()==h
def test_perturbation_and_limited_claims():
 x=rows('PERTURBATION_COMPARISON_20SEEDS.csv');assert len(x)==6
 assert all(int(z['not_biological_validity'])==1 for z in x)
def test_sufficient_formula_source_locators():
 x=rows('NEW_HERBS_SOURCE_REVIEW_100.csv');assert all(z['official_printed_pages'] and z['source_url'].startswith('https://') for z in x)
def test_snapshot_assertions_counts_reconciled():
 d=json.loads((ROOT/'data/paper2_source_reviewed_species_v04.json').read_text())
 assert len(d['assertions'])==174
 assert sum(x['assertion_type']=='FormulaMembershipAssertion' for x in d['assertions'])==74
 assert sum(x['assertion_type']=='ChemistryOccurrenceAssertion' for x in d['assertions'])==100
 assert sum(h['formula_count'] for h in d['herbs'])==74
 for h in d['herbs']:
  assert h['formula_count']==sum(h['id'] in f['herbs'] for f in d['formulas'])
 assert d['original_v3_assertions_count']==171

def test_official_formula_titles_crosswalked():
 d=json.loads((ROOT/'data/paper2_source_reviewed_species_v04.json').read_text())
 assert len({f['title_th'] for f in d['formulas']})==10
 assert all(f['name_status']=='source_reviewed_from_official_compendium_single_curator' for f in d['formulas'])
def test_deterministic_seed11_replay():
 import sys
 sys.path.insert(0,str(ROOT/'src'))
 from reanalyse import cooc_walks,vectors
 d=json.loads((ROOT/'data/paper2_source_reviewed_species_v04.json').read_text())
 ids=[h['id'] for h in d['herbs']]
 current=vectors(cooc_walks(d['formulas'],ids,11),ids,11)
 archived=[float(x['cosine']) for x in rows('ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv') if x['model']=='Cooc-NPMI' and x['seed']=='11']
 assert len(archived)==190 and np.allclose(current,archived,atol=2e-7)