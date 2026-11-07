"""Regression/integrity tests; they do not stand in for expert evaluation."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
import pytest
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'input'/'v04'
RESULTS=ROOT/'results'

@pytest.fixture(scope='module')
def data():return json.loads((OLD/'data'/'paper2_source_reviewed_species_v04.json').read_text(encoding='utf-8'))

def test_archive_36_entries_sha256():
    manifest=json.loads((OLD/'SHA256_MANIFEST.json').read_text())
    assert len(manifest['files'])==36
    for record in manifest['files']:
        assert hashlib.sha256((OLD/record['path']).read_bytes()).hexdigest()==record['sha256']

def test_frozen_herbs_formulas(data):
    assert len(data['herbs'])==20 and len(data['formulas'])==10

def test_74_species_memberships(data):
    assert sum(len(f['herbs']) for f in data['formulas'])==74

def test_100_chemistry_claims(data):
    assert sum(r['assertion_type']=='ChemistryOccurrenceAssertion' for r in data['assertions'])==100

def test_83_compound_identifiers(data):
    assert len(data['compounds'])==83

def test_9_archived_models_20seeds():
    f=pd.read_csv(OLD/'results'/'ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv')
    assert f.model.nunique()==9 and f.seed.nunique()==20 and len(f)==34200

def test_archived_replay_numerically_identical():
    r=json.loads((RESULTS/'P2_RUN_MANIFEST.json').read_text())
    assert r['archived']['replay_max_absolute_error']<1e-6

def test_new_perturb_nine_variants_20seeds():
    r=pd.read_csv(RESULTS/'P2_PERTURBATION_20SEED_PAIRED.csv')
    assert len(r)==9*20 and r.variant.nunique()==9
    assert r.groupby('variant').seed.nunique().eq(20).all()

def test_no_nonfinite_perturbation_scores():
    r=pd.read_csv(RESULTS/'P2_PERTURBATION_ALL_PAIR_SCORES.csv')
    assert len(r)==9*20*190 and np.isfinite(r.cosine).all()

def test_lofo_10_folds_650_metrics():
    r=pd.read_csv(RESULTS/'P2_LOFO_MODEL_METRICS_ALL_10_FOLDS.csv')
    assert r.fold.nunique()==10 and len(r)==650
    assert ((r.AP>=0)&(r.AP<=1)).all() and ((r.AUROC>=0)&(r.AUROC<=1)).all()

def test_five_baselines_three_embedding_methods():
    r=pd.read_csv(RESULTS/'P2_LOFO_MODEL_METRICS_ALL_10_FOLDS.csv')
    assert r.model.nunique()==8

def test_train_only_fold_excludes_heldout_formula():
    r=pd.read_csv(RESULTS/'P2_LOFO_COVERAGE.csv')
    assert len(r)==10 and r.train_formulas.eq(9).all()

def test_6_complete_4_partial():
    r=pd.read_csv(RESULTS/'P2_LOFO_COVERAGE.csv')
    assert sum(r.fold_type=='FULL_190')==6
    assert sum(r.fold_type=='PARTIAL_171_COLD_START')==4

def test_cold_pairs_never_predicted():
    r=pd.read_csv(RESULTS/'P2_LOFO_PREDICTIONS_ALL.csv')
    co=pd.read_csv(RESULTS/'P2_LOFO_COVERAGE.csv')
    for _,item in co.iterrows():
        cold=item.cold_herbs
        if isinstance(cold,str) and cold:
            fold=r[r.fold==item.heldout_formula]
            assert not (fold.herb_a.eq(cold)|fold.herb_b.eq(cold)).any()

def test_source_holdout_20_and_90percent_coverage():
    r=pd.read_csv(RESULTS/'P2_SOURCE_HOLDOUT_COVERAGE.csv')
    assert len(r)==20 and r.source_holdout.nunique()==20
    assert r.evaluable_pairs.eq(171).all() and r.blocked_pairs.eq(19).all()

def test_source_holdout_5_seeds():
    r=pd.read_csv(RESULTS/'P2_SOURCE_HOLDOUT_20_SOURCES_5SEEDS.csv')
    assert len(r)==100 and r.groupby('source_holdout').seed.nunique().eq(5).all()

def test_cluster_bootstrap_2000_and_paired_4000():
    b=pd.read_csv(RESULTS/'P2_LOFO_BOOTSTRAP_2000.csv')
    assert b.groupby(['model','coverage_type','endpoint']).replicate.nunique().eq(2000).all()
    p=pd.read_csv(RESULTS/'P2_PAIRED_CLUSTER_BOOTSTRAP_VS_PAIRSUPPORT.csv')
    assert p.bootstrap_draws.eq(4000).all()

def test_external_candidate_not_confirmatory():
    r=pd.read_csv(RESULTS/'P2_EXTERNAL_DOI_DEDUP_AND_ELIGIBILITY.csv')
    assert len(r)==11 and r.doi.nunique()==3 and not r.allowed_confirmatory_external_test.any()
    assert not r.doi_in_20_archived_original_source_records.any()

def test_original_35_classes_not_claimed():
    r=json.loads((RESULTS/'P2_TAXONOMY_HISTORICAL_VS_NEW.json').read_text())
    assert r['original_35class_compound_mapping_recovered'] is False
    assert r['new_provisional_name_based_families']==31

def test_exploratory_31_family_and_material():
    r=pd.read_csv(RESULTS/'P2_PROVISIONAL_CLASS_MATERIAL_SENSITIVITY_20SEEDS.csv')
    assert len(r)==60 and r.scenario.nunique()==3
    assert r.groupby('scenario').seed.nunique().eq(20).all()

def test_190_expert_review_cases_unfilled():
    for role in ['R1','R2']:
        x=pd.read_csv(RESULTS/f'P2_BLINDED_EXPERT_{role}_190_UNFILLED.csv')
        assert len(x)==190 and x.gold_score_0_to_3.isna().all()

def test_documentary_not_biological_truth():
    r=json.loads((RESULTS/'P2_RUN_MANIFEST.json').read_text())
    assert r['inference_scope']=='DOCUMENTARY_FORMULA_CO_MEMBERSHIP_NOT_BIOLOGICAL_TRUTH'

def test_standalone_dashboard_no_external_scripts():
    s=(ROOT/'dashboard'/'ThaiHerb_Paper2_Robustness_v13.html').read_text(encoding='utf-8')
    assert 'https://cdn' not in s and 'const DATA=' in s and '<script>' in s
