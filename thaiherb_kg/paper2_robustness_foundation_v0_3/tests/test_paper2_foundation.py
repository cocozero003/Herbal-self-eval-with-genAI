"""Paper 2 research-integrity tests: no hallucinated gold or class ontology."""
from pathlib import Path
import csv,json,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1]

def read(name):
    with (ROOT/'results'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def meta():return json.loads((ROOT/'results/foundation_manifest.json').read_text())

def test_data_and_claim_scope():
    m=meta()
    assert m['n_herbs']==20 and m['n_formulas']==10
    assert m['n_formula_memberships']==71 and m['n_chemistry_assertions']==100
    assert m['n_distinct_compounds']==83 and m['positive_npmi_edges']==82
    assert m['original_35_classes_available'] is False
    assert m['independent_expert_biological_gold_available'] is False

def test_input_hash_lock():
    for name,h in meta()['data_sha256'].items():
        assert hashlib.sha256((ROOT/'data'/name).read_bytes()).hexdigest()==h

def test_matrix_source_review_boundary():
    r=read('formula_herb_200_matrix.csv')
    assert len(r)==200 and sum(int(x['herb_present_proxy']) for x in r)==71
    legacy=[x for x in r if x['review_class']=='PAPER1_SINGLE_CURATOR_CROSSWALK']
    added=[x for x in r if x['review_class']=='NEW_HERB_NOT_YET_PRIMARY_VERIFIED']
    assert len(legacy)==len(added)==100
    assert all(x['independent_adjudication']=='0' for x in r)
    cross=read('formula_id_crosswalk_10.csv')
    assert len(cross)==10 and all(x['legacy_10herb_match']=='1' for x in cross)
    assert all(x['new_10herb_source_reviewed']=='0' for x in cross)

def test_source_holdout_coverage_is_blocked():
    r=read('leave_one_source_out_20.csv');assert len(r)==20
    assert all(x['unrepresented_herb_count']=='1' for x in r)
    assert all(x['eligible_for_complete_190pair_chemistry_comparison']=='0' for x in r)

def test_formula_holdout_and_cold_start_eligibility():
    r=read('formula_heldout_eligibility_10.csv');assert len(r)==10
    blocked={x['heldout_formula'] for x in r if x['full_190_pair_eligible']=='0'}
    assert blocked=={'F02_DTAM2566','F03_DTAM2566','F05_DTAM2566','F07_DTAM2566'}
    assert all(x['test_formula_not_in_training']=='1' and x['train_formulas']=='9' for x in r)

def test_output_metrics_finite_and_no_labels_from_heldout_formula():
    x=read('lofo_baseline_metrics.csv');assert len(x)==30
    assert len(read('lofo_baseline_predictions.csv'))==6*5*190
    assert {x['method'] for x in x}=={'PairSupport','DegreeProduct','PositiveNPMI','ExactCompoundJaccard','ExactCompoundIDFJaccard'}
    assert all(0<=float(z['average_precision'])<=1 and 0<=float(z['auroc'])<=1 for z in x)
    d=json.loads((ROOT/'data/paper2_bootstrap_v3_proxy.json').read_text())
    forms={f['id']:set(f['herbs']) for f in d['formulas']}
    for r in read('lofo_baseline_predictions.csv'):
        target=int(r['herb_a'] in forms[r['heldout_formula']] and r['herb_b'] in forms[r['heldout_formula']])
        assert int(r['heldout_formula_cooccurrence_label'])==target

def test_sparse_edges_all_pairs():
    g=read('cooc_pair_weights_190.csv');assert len(g)==190
    assert sum(float(x['positive_npmi'])>0 for x in g)==82
    assert all(float(x['positive_npmi'])>=0 for x in g)
    c=read('exact_compound_pairs_190.csv');assert len(c)==190
    assert all(0<=float(x['compound_jaccard'])<=1 for x in c)

def test_panel_pruning_no_fabricated_class():
    p=read('exact_chemistry_panel_pruning_8.csv');assert len(p)==8
    assert all(x['total_edges']=='80' for x in p)
    assert all(x['scope']=='exact_compound_only_not_original_35_classes' for x in p)

def test_expert_forms_blank_and_blinded():
    a=read('BLINDED_EXPERT_R1_190.csv');b=read('BLINDED_EXPERT_R2_190.csv')
    assert len(a)==len(b)==190
    assert {x['case_id'] for x in a}=={x['case_id'] for x in b}
    assert [x['case_id'] for x in a]!=[x['case_id'] for x in b]
    assert all(not r['chemical_similarity_grade_0_1_2_or_NA'] for r in a+b)
    assert all('model' not in k and 'score' not in k for k in a[0])
    assert all(not r['adjudicated_chemistry'] for r in read('EXPERT_ADJUDICATION_BLANK_190.csv'))

def test_dashboard_no_remote_resources():
    content=(ROOT/'dashboard/Paper2_Robustness_v0.3.html').read_text()
    assert '<!doctype html>' in content and 'window.RESEARCH_DATA=' in content
    assert 'https://cdn' not in content and '<script src=' not in content
    assert '35-class' in content and '20/20' in content