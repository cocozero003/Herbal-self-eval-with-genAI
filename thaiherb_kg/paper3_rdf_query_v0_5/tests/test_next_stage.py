import csv, json, hashlib
from pathlib import Path
from rdflib import Graph
from src.stage_next import build_evidence, build_query, answer_case, CASE_SPECS, RES, DATA, readcsv

def test_p2_audit_tiers():
    s=build_evidence(); assert s['total']==100 and sum(s['counts'].values())==100
    assert s['full_text_primary']==5 and s['primary_abstract_only']==5 and s['secondary_review_only']==10 and s['not_verified']==80

def test_ginger_and_garlic_remain_secondary():
    items=readcsv(RES/'P2_CHEM_EVIDENCE_100_v07.csv')
    for r in items:
        if r['source_id'] in ('SRC_GARLIC','SRC_GINGER'):
            assert r['v07_review_level']=='SECONDARY_ONLY' and r['v07_primary_original_study']=='NO'

def test_plai_is_abstract_only():
    rows=readcsv(RES/'P2_CHEM_EVIDENCE_100_v07.csv')
    for r in rows:
        if r['source_id']=='SRC_PLAI':
            assert r['v07_review_level']=='PRIMARY_ABSTRACT_ONLY'
            assert r['v07_full_text_checked']=='NO' and r['v07_quantity_unit'].startswith('percent')

def test_p3_frozen_unchanged():
    rows=readcsv(DATA/'P3_V3_208_LOCKED.csv');assert len(rows)==208
    assert len({x['assertion_id'] for x in rows})==208

def test_same_corpus_three_projections():
    s=build_query();assert s['model_case_runs']==24 and s['cases']==8
    assert s['rdf_triple_counts']=={'M1':207,'M2':1501,'M3':2733}

def test_platelet_sources_not_folded_in_m2_m3():
    rows=readcsv(RES/'P3_V05_ENGINE_OUTPUTS_24.csv')
    m={x['model']:x for x in rows if x['case_id']=='CQD06'}
    assert int(m['M1']['edge_count'])==2
    assert int(m['M2']['edge_count'])==3 and int(m['M3']['edge_count'])==3
    assert 'CLIN005' in m['M3']['assertion_ids'] and 'CLIN006' in m['M3']['assertion_ids']

def test_no_risk_overclaim():
    rows=readcsv(RES/'P3_V05_ENGINE_OUTPUTS_24.csv')
    assert all(r['scientific_accuracy']=='NOT_EVALUATED' and r['benchmark_gold']=='NOT_AVAILABLE' for r in rows)
    assert all(r['status'].startswith('ABSTAIN') for r in rows if r['category']=='safety_regulatory')

def test_material_unknown_is_abstention():
    rows=readcsv(RES/'P3_V05_ENGINE_OUTPUTS_24.csv')
    assert all(r['status']=='ABSTAIN_INSUFFICIENT_MATERIAL' for r in rows if r['category'] in ('material_preparation','taxonomy'))

def test_directness_only_in_m3():
    rows=readcsv(RES/'P3_V05_ENGINE_OUTPUTS_24.csv')
    by={r['model']:r for r in rows if r['case_id']=='CQD05'}
    assert by['M1']['status'].startswith('ABSTAIN') and by['M2']['status'].startswith('ABSTAIN')
    assert by['M3']['status']=='SUPPORTED_EDGES'

def test_dashboard_offline():
    from src.build_dashboard import build_dashboard
    build_dashboard()
    page=(RES.parent/'dashboard'/'ThaiHerb_P2v07_P3v05_EvidenceExplorer.html').read_text()
    assert 'DATA_PLACEHOLDER' not in page and 'PRIMARY_ABSTRACT_ONLY' in page and 'CQD07' in page
