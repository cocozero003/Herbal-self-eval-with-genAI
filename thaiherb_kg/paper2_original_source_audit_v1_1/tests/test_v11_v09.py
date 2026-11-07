"""Release v1.1/v0.9 tests; simulated review data are never scientific outputs."""
import csv
from copy import deepcopy
from pathlib import Path
from rdflib import Graph, RDF, URIRef, Literal
from src.original_source_screen_v11 import run as screening, records, SOURCE_INFO, MATCH, TAXONOMY, RESULTS, DATA
from src.shacl_profile_check_v09 import run as shapes_run, check, mutated, inspect_shapes, SH
from src.blind_benchmark_v09 import (run as benchmark_run, read_csv, MODELS, BINARY_FIELDS,
                                      check_scoring_permissions, evaluate, exact_mcnemar,
                                      paired_bootstrap, create_templates)


def test_source_count():
    x=screening()
    assert x['total_claims']==100
    assert x['source_types_screened']==20


def test_immutable_origin_dispositions():
    original={r['assertion_id']:r['disposition'] for r in records(DATA/'P2_CHEM_EVIDENCE_100_v05_LOCKED.csv')}
    screened=records(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    assert all(r['original_disposition_immutable']==original[r['assertion_id']] for r in screened)


def test_distinct_chemical_claim_statuses():
    x=screening()['claim_screen_grades']
    assert x['PRIMARY_FULLTEXT_EXPERIMENT']==5
    assert x['PRIMARY_ABSTRACT_EXPERIMENT'] + x['PRIMARY_ABSTRACT_PROCESS_DEPENDENT']==15
    assert x['SECONDARY_FULLTEXT_REVIEW']==19
    assert x['UNRESOLVED_CLAIM_LOCATOR']==61


def test_no_clinical_claims_or_human_gold():
    a=records(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    assert all(r['adjudicated_gold']=='' for r in a)
    assert all(r['external_validation_eligible'].startswith('NO_') for r in a)


def test_taxon_synonym_authorities():
    assert len(TAXONOMY)==2
    assert {r['herb_id'] for r in TAXONOMY}=={'H12','H19'}
    assert all('powo.science.kew.org' in r['url'] for r in TAXONOMY)


def test_h19_hydrolysis_context_preserved():
    a=records(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    assert all('alkaline hydrolysis' in r['material_process_context'] for r in a if r['herb_id']=='H19')


def test_black_pepper_review_not_primary():
    a=records(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    assert all(r['original_source_claim_screen_grade']=='SECONDARY_FULLTEXT_REVIEW' for r in a if r['herb_id']=='H03')


def test_only_39_claims_have_specific_locators():
    assert len(MATCH)==39
    a=records(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    assert sum(bool(r['locator']) for r in a)==39


def test_source_type_distinguishes_genus_review():
    assert SOURCE_INFO['SRC_CURCUMA'][0]=='REVIEW_GENUS'
    assert SOURCE_INFO['SRC_GALANGAL'][0]=='REVIEW_GENUS'


def test_shacl_profile_baseline_passes():
    a=shapes_run()
    assert a['original_dataset_subshape_violations']==0
    assert a['engine']!='pyshacl'
    assert a['pyshacl_core_status']!='PASS'


def test_negative_controls_all_detected():
    a=shapes_run()
    assert a['negative_controls_detected']==a['negative_controls_total']==7


def test_malformed_subject_is_detected():
    g=Graph().parse(RESULTS/'P3_M3.ttl')
    shapes=Graph().parse(RESULTS/'P3_SHACL_CORE_SHAPES_V04.ttl')
    issues=check(mutated(g,'wrong_subject_nodekind'),shapes)
    assert any(x['constraint']==SH.NodeKindConstraintComponent for x in issues)


def test_shacl_profile_rule_coverage():
    shapes=Graph().parse(RESULTS/'P3_SHACL_CORE_SHAPES_V04.ttl')
    rules=inspect_shapes(shapes)
    assert len(rules)==6
    assert any(r['class'] for r in rules)
    assert any(r['nodekind']==SH.IRI for r in rules)


def test_missing_source_class_detected():
    g=Graph().parse(RESULTS/'P3_M3.ttl')
    shapes=Graph().parse(RESULTS/'P3_SHACL_CORE_SHAPES_V04.ttl')
    issues=check(mutated(g,'wrong_source_class'),shapes)
    assert any(x['constraint']==SH.ClassConstraintComponent for x in issues)


def test_benchmark_matrix_is_blinded():
    template=create_templates()
    assert len(template)==96
    assert {(r['case_id'],r['model']) for r in template}=={
        (r['case_id'],m) for r in read_csv(RESULTS/'P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv') for m in MODELS}
    assert all(r['answer_correct']=='' for r in template)


def test_gate_hard_blocks_current_data():
    x=benchmark_run()
    assert x['confirmatory_accuracy_reported'] is False
    assert x['num_gold_cases']==0


def test_exact_mcnemar_reference_cases():
    assert exact_mcnemar([1,1,1,1],[0,0,0,0])['exact_two_sided_p']==0.125
    assert exact_mcnemar([1,0],[1,0])['exact_two_sided_p']==1.


def test_paired_bootstrap_zero_delta():
    a=paired_bootstrap([1,0,1,0],[1,0,1,0],reps=100)
    assert a['delta_b_minus_a']==0
    assert a['ci95_percentile_low']==0
    assert a['ci95_percentile_high']==0


def test_synthetic_only_valid_gate_demonstration():
    # Unit-test-only synthetic adjudications, not saved to research dataset.
    gold=read_csv(RESULTS/'P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv')
    for r in gold:
        r.update({'eligible_for_blind_scoring':'YES', 'independent_gold_available':'YES',
                  'reviewer_1':'SIMULATED_A','reviewer_2':'SIMULATED_B',
                  'adjudicated_gold':'SIMULATED_REFERENCE',
                  'conflict_of_interest_checked':'YES','model_predictions_locked':'YES',
                  'confirmation_scoring_permitted':'YES'})
    prediction=create_templates()
    for r in prediction:
        r.update({'prediction_frozen':'YES','blinded_assessor_id':'SIMULATED_REVIEWER'})
        r.update({field:'1' for field in BINARY_FIELDS})
    result=evaluate(gold,prediction)
    assert result['status']=='ELIGIBLE_FOR_CONFIRMATORY_SCORING'
    assert result['num_gold_cases']==32
    assert result['endpoints']['answer_correct']['rates']['M3']==1
