"""Checks for leakage, scientific boundaries, and reproducible v0.7 outputs."""
import csv,hashlib,json,sys
from pathlib import Path
import numpy as np
from sklearn.metrics import average_precision_score
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from validate_heldout_formulas import fast_average_precision,mscore
from evaluate_expert_labels import evaluate

def read(name):
 with (ROOT/'results'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def test_holdout_leakage_absence():
 rows=read('fold_eligibility_10.csv')
 assert len(rows)==10
 assert all(x['heldout_formula_id'] not in x['train_formula_ids'].split(';') for x in rows)
 assert all(x['test_formula_id_absent_from_training']=='1' for x in rows)
 assert all(int(x['training_formulas'])==9 for x in rows)
def test_f02_cold_start_gate():
 rows=read('fold_eligibility_10.csv')
 blocked=[x for x in rows if x['full_45_pair_comparison_eligible']=='0']
 assert len(blocked)==1 and blocked[0]['heldout_formula_id']=='F02_DTAM2566'
 assert blocked[0]['unseen_herbs_in_train']=='H07'
def test_predictions_complete_and_pair_outcomes():
 rows=read('heldout_pair_predictions.csv')
 assert len(rows)==9*45*9
 assert all(r['not_biological_ground_truth']=='1' for r in rows)
 assert len({(r['heldout_formula_id'],r['method']) for r in rows})==9*9
def test_metric_rows():
 r=read('per_fold_metrics.csv')
 assert len(r)==81
 assert all(0<=float(x['auroc'])<=1 and 0<=float(x['average_precision'])<=1 for x in r)
def test_permutation_and_leakage_oracle():
 data=json.loads((ROOT/'results/null_permutation_summary.json').read_text())
 assert data['within_fold_label_shuffle'] and data['repetitions']==2000
 leaked=read('label_leakage_demonstration.csv')
 assert len(leaked)==9
 assert np.mean([float(x['invalid_leaked_pair_support_AP']) for x in leaked])>np.mean([float(x['proper_pair_support_AP']) for x in leaked])
def test_approx_fast_ap_matches_sklearn():
 y=np.array([0,1,0,1,0,0,1]);s=np.array([1,0,1,3,1,1,3])
 assert abs(fast_average_precision(y,s)-average_precision_score(y,s))<1e-10
def test_expert_not_fabricated():
 for rater in ('R1','R2'):
  rows=read(f'BLINDED_EXPERT_{rater}_45.csv');assert len(rows)==45
  assert all(not r['chemistry_similarity_grade_0_1_2_or_NA'] for r in rows)
  assert not {'model','score','npmi','rank','heldout_y'}&set(rows[0])
 assert evaluate()['status']=='BLOCKED_GOLD_LABELS_INCOMPLETE'
def test_expert_raters_different_shuffle():
 a=[r['case_id'] for r in read('BLINDED_EXPERT_R1_45.csv')]
 b=[r['case_id'] for r in read('BLINDED_EXPERT_R2_45.csv')]
 assert set(a)==set(b) and a!=b
def test_original_formula_f05_retained():
 d=json.loads((ROOT/'data/formula_reviewed_snapshot.json').read_text())
 f=next(x for x in d['formulas'] if x['id']=='F05_DTAM2566')
 assert {'H01','H02','H03','H05','H10'}<=set(f['herbs'])
def test_no_misleading_validation_claims():
 data=json.loads((ROOT/'results/benchmark_manifest.json').read_text())
 assert data['independent_external_dataset'] is False
 assert data['independent_expert_gold_labels'] is False
 assert data['non_cooccurrence_is_not_biological_dissimilarity'] is True
 assert data['candidate_19_chemical_classes_not_recovered_from_original_paper1'] is True
 assert data['expert_form_scores_intentionally_blank'] is True
def test_dashboard_static_and_standalone():
 s=(ROOT/'dashboard/Paper1_Validation_v0.7.html').read_text()
 assert 'window.RESEARCH_DATA=' in s and '<!doctype html>' in s
 assert 'https://cdn' not in s and 'Unrated' in s and 'Invalid oracle' not in s