import csv
import json
from collections import Counter
from pathlib import Path
from rdflib import Graph, RDF, Namespace, URIRef
from rdflib.namespace import PROV
from src.build import TH, test_custom_structure as structural_check, CHECKED_PIPER

BASE=Path(__file__).resolve().parents[1]
R=BASE/'results'
D=BASE/'data'

def records(path):
    with path.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def test_input_v3_immutable_208():
    rows=records(D/'P3_V3_208_LOCKED.csv')
    assert len(rows)==208
    assert Counter(x['channel'] for x in rows)=={'formula':71,'chemistry':100,'pharmacology_target':30,'clinical':7}

def test_input_v05_immutable_100():
    assert len(records(D/'P2_CHEM_EVIDENCE_100_v05_LOCKED.csv'))==100

def test_chemical_5_exactly():
    rows=records(R/'P2_CHEM_EVIDENCE_100_v06.csv')
    assert len(rows)==100
    assert {r['assertion_id'] for r in rows if r['disposition']=='PRIMARY_FULLTEXT_MATCH'}==set(CHECKED_PIPER)

def test_chemical_quantities_are_not_absolute_concentrations():
    for r in records(R/'P2_PRIMARY_ANALYTICAL_MATCHES_5.csv'):
        assert r['quantity_unit']=='mg PE/g extract (piperine equivalents, not analyte mass)'
        assert r['plant_part']=='dried fruit (peppercorn)'
        assert 'Table 3' in r['source_exact_locator_verified']

def test_unchecked_stay_unverified():
    rows=records(R/'P2_CHEM_UNRESOLVED_95.csv')
    assert len(rows)==95 and all(x['disposition']=='NOT_VERIFIED' for x in rows)

def test_curcuma_context_is_not_claimed_verified():
    rows=records(R/'P2_SPECIES_CONTEXT_REVIEW_QUEUE.csv')
    assert len(rows)==5
    assert all(r['status']=='OPEN_ISSUE_NOT_DISPROVED' for r in rows)

def test_source_metadata_review_separated_from_claim_review():
    r=records(R/'P2_SOURCE_REGISTRY_V06.csv')
    assert len(r)==21
    assert sum(x['literature_review_20261107']=='SOURCE_ARTICLE_AND_5_COMPOUNDS_TABLE_3_CHECKED' for x in r)==1

def test_m1_projection_207_unique_spo():
    g=Graph().parse(R/'P3_M1.ttl',format='turtle');assert len(g)==207

def test_m2_assertion_cardinality_and_source():
    g=Graph().parse(R/'P3_M2.ttl',format='turtle')
    assert len(set(g.subjects(RDF.type, TH.EvidenceAssertion)))==208
    assert structural_check(g)==[]

def test_m3_assertion_cardinality_and_source():
    g=Graph().parse(R/'P3_M3.ttl',format='turtle')
    assert len(set(g.subjects(RDF.type, TH.EvidenceAssertion)))==208
    assert structural_check(g)==[]

def test_collapsed_spo_is_two_opposite_ginger_platelet_contexts():
    d=records(D/'P3_V3_208_LOCKED.csv')
    a=[r for r in d if r['assertion_id'] in ('CLIN005','CLIN006')]
    assert len(a)==2
    assert {(r['subject_id'],r['predicate_or_topic'],r['object_label']) for r in a}.__len__()==1
    assert len({r['source_id'] for r in a})==2 and len({r['directness_or_direction'] for r in a})==2

def test_624_renderings_no_gold():
    rows=records(R/'P3_ALL_ASSERTIONS_MODEL_RENDERED_624.csv')
    assert len(rows)==624
    assert Counter(x['model'] for x in rows)=={'M1':208,'M2':208,'M3':208}
    assert all(x['validated_answer']=='NO' for x in rows)

def test_m3_qualifies_all_7_missing_ids():
    rows=records(R/'P3_ALL_ASSERTIONS_MODEL_RENDERED_624.csv')
    assert sum(x['model']=='M3' and x['status']=='OBJECT_ID_UNRESOLVED' for x in rows)==7

def test_models_not_fed_expert_gold():
    rows=records(R/'P3_CQ_BLINDED_BENCHMARK_TEMPLATE.csv')
    assert len(rows)==8
    assert all(not x['reviewer_1'] and not x['reviewer_2'] and not x['expected_answer'] for x in rows)

def test_negative_controls_pass():
    rows=records(R/'P3_CUSTOM_NEGATIVE_CONTROLS.csv')
    assert len(rows)==4 and all(x['pass']=='True' for x in rows)
    assert all(x['engine']=='CUSTOM_STRUCTURAL_CHECK_NOT_PYSHACL' for x in rows)

def test_real_shacl_status_not_misreported():
    status=json.loads((R/'P3_SHACL_RUNTIME_STATUS.json').read_text())
    assert status['status'] in ('PASS','FAIL','NOT_RUN_DEPENDENCY_UNAVAILABLE')
    if status['status']=='NOT_RUN_DEPENDENCY_UNAVAILABLE':
        assert status['claim_of_conformance'] is False

def test_projection_no_material_false_mapping():
    rows=records(R/'P3_PROJECTION_PARITY_208.csv')
    assert all(r['M3_material_id']=='NOT_NORMALIZED' for r in rows)

def test_readable_dashboards_exist():
    for fn in ('Paper2_ClaimAudit_v0.6.html','Paper3_M1M2M3_v0.4.html'):
        s=(BASE/'dashboard'/fn).read_text(encoding='utf-8')
        assert 'function render()' in s and 'Research' in s or 'research' in s


def test_shacl_runtime_negative_controls_if_run():
    status=json.loads((R/'P3_SHACL_RUNTIME_STATUS.json').read_text())
    if status.get('status')=='PASS':
        assert status['negative_controls_detected']==4
        assert len(records(R/'P3_SHACL_NEGATIVE_CONTROLS.csv'))==4
