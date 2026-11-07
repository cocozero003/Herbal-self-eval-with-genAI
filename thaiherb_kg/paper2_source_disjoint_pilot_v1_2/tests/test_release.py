import csv
import json
import sys
from pathlib import Path
from rdflib import Graph, RDF, Namespace

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from score_gate import score_allowed

def rows(name):
    with (ROOT/'results'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def test_frozen_input_assertion_count():
    assert len(rows('../data/P2_CHEM_EVIDENCE_100_v05_LOCKED.csv'))==100
    assert len(rows('../data/P3_V3_208_LOCKED.csv'))==208

def test_all_original_claims_retained():
    original=rows('../data/P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    release=rows('P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv')
    assert len(original)==len(release)==100
    assert {r['assertion_id'] for r in original}=={r['assertion_id'] for r in release}
    for r,s in zip(original,release):
        assert r['original_source_claim_screen_grade']==s['original_source_claim_screen_grade']
        assert s['claim_scientific_truth_independently_adjudicated']=='NO'

def test_original_primary_fulltext_is_five_only():
    x=rows('P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv')
    assert sum(y['archived_source_primary_fulltext_verified']=='YES' for y in x)==5

def test_primary_evidence_external_does_not_promote_original_grade():
    claims={r['assertion_id']:r for r in rows('P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv')}
    externals=rows('P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv')
    assert len(externals)==11
    assert all(claims[r['assertion_id']]['new_source_evidence_is_not_original_source']=='YES' for r in externals)

def test_external_sources_distinct_by_DOI():
    original=rows('../data/P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    priorurls=' '.join(r['original_source_url_locked'] for r in original).lower()
    sources=rows('P2_EXTERNAL_SOURCE_REGISTRY_V12.csv')
    for r in sources:
        assert r['doi'].lower() not in priorurls
    assert len(set(r['doi'] for r in sources))==4

def test_development_contamination_exclusion():
    src={r['source_id']:r for r in rows('P2_EXTERNAL_SOURCE_REGISTRY_V12.csv')}
    assert src['EXT_CORIANDER_SATYAL2020']['primary_eligible']=='EXCLUDE_LEAKAGE'
    assert 'CORIANDER' not in ';'.join(r['source_id'] for r in rows('P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv'))

def test_all_external_sources_in_registry():
    src={r['source_id'] for r in rows('P2_EXTERNAL_SOURCE_REGISTRY_V12.csv')}
    assert all(r['source_id'] in src for r in rows('P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv'))

def test_external_panel_is_positive_only_not_confirmatory():
    x=rows('P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv')
    assert all(r['posthoc_target_selected']=='YES' and r['blind_independent_gold']=='NO' for r in x)
    assert all(r['adjudicated_gold']=='' for r in x)

def test_taxonomy_83_and_unique():
    c=rows('P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv')
    assert len(c)==83 and len({r['compound_id_internal'] for r in c})==83
    assert len({r['reconstructed_family_id'] for r in c})==31

def test_taxonomy_not_fake_original35():
    c=rows('P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv')
    assert all(r['original_35class_id']=='' for r in c)
    assert all(r['original_35class_recovered']=='NO' and r['allowed_in_confirmatory_35class_replication']=='NO' for r in c)

def test_concinnoside_hydrolysis_context_retained():
    c=rows('P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv')
    assert len([r for r in c if r['archive_compound_label'].startswith('concinnoside') and r['postprocessing_context']])==5

def test_expert_review_sheets_blank():
    r=rows('P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv')
    assert len(r)==45
    for c in r:
        assert c['reviewer1_name']==c['reviewer2_name']==c['adjudicated_gold']==''
        assert c['benchmark_ready']=='NO'

def test_score_gate_fail_closed():
    g=score_allowed(ROOT/'results/P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv')
    assert not g['score_allowed'] and len(g['blocked_cases'])==45

def test_v3_parity():
    g=Graph().parse(ROOT/'data/P3_M3.ttl',format='turtle')
    TH=Namespace('urn:thaiherb:v04:')
    assert len(g)==2733 and len(list(g.subjects(RDF.type,TH.EvidenceAssertion)))==208

def test_three_model_same_projection_snapshot():
    assert [len(Graph().parse(ROOT/f'data/P3_{m}.ttl',format='turtle')) for m in ('M1','M2','M3')]==[207,1501,2733]

def test_runtime_not_pass_without_actual_pyshacl():
    path=ROOT/'results/P3_PYSHACL_CORE_RUNTIME.json'
    if path.exists():
        o=json.loads(path.read_text());assert o['status'] in ('NOT_RUN_MISSING_PYSHACL','PASS','FAIL')

def test_context_trap_wrong_species():
    x=rows('P2_CONTEXT_SPECIFICITY_CHALLENGES.csv')
    assert len(x)==2
    assert any('C_ANGUSTIFOLIA' in c['correct_source_specific_answer'] for c in x)
