"""Independent reproducibility assertions; not clinical-scientific validity tests."""
from collections import Counter
from pathlib import Path
import csv
import json
import sys
import pytest
from rdflib import Graph

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src import stage_v08


def test_p2_100_audited():
    rows=stage_v08.read_csv(ROOT/'results/P2_CHEM_EVIDENCE_100_v08.csv')
    assert len(rows)==100
    assert len(set(x['assertion_id'] for x in rows))==100
    assert len(set(x['compound_id_internal'] for x in rows))==83


def test_publication_types_distinct_from_claim_status():
    rows=stage_v08.read_csv(ROOT/'results/P2_SOURCE_TYPE_AUDIT_20.csv')
    cnt=Counter(x['publication_type_source_screen'] for x in rows)
    assert len(rows)==20
    assert cnt['REVIEW_SPECIES']==12 and cnt['REVIEW_GENUS']==3
    assert sum(x.startswith('PRIMARY') for x in cnt for _ in range(cnt[x]))==5
    assert all(x['individual_compound_fulltext_all_five_verified']=='NO' for x in rows)


def test_prior_primary_fulltext_not_upgraded_falsely():
    rows=stage_v08.read_csv(ROOT/'results/P2_CHEM_EVIDENCE_100_v08.csv')
    assert {x['assertion_id'] for x in rows if x['v08_claim_evidence_level']=='PRIMARY_FULLTEXT_MATCH'} == {f'CA{i:03d}' for i in range(6,11)}
    assert all(x['v08_expert_gold']=='NOT_ADJUDICATED' for x in rows)


def test_h19_processing_not_conflated_with_native_occurrence():
    rows=stage_v08.read_csv(ROOT/'results/P2_CHEM_EVIDENCE_100_v08.csv')
    h19=[x for x in rows if x['herb_id']=='H19']
    assert len(h19)==5
    assert all(x['v08_claim_evidence_level']=='PRIMARY_ABSTRACT_AFTER_HYDROLYSIS' for x in h19)
    assert all('HYDROLYSIS' in x['v08_material_scope_warning'] for x in h19)


def test_genus_reviews_not_promoted():
    rows=stage_v08.read_csv(ROOT/'results/P2_CHEM_EVIDENCE_100_v08.csv')
    assert all(x['v08_claim_evidence_level']=='NOT_VERIFIED' for x in rows if x['source_id'] in ['SRC_GALANGAL','SRC_ACORUS','SRC_CURCUMA'])


def test_p3_original_v3_immutable():
    import hashlib
    p=ROOT/'data/P3_V3_208_LOCKED.csv'
    assert hashlib.sha256(p.read_bytes()).hexdigest()=='59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774'


def test_p3_source_gap_explicit():
    x=json.loads((ROOT/'results/P3_V06_AUDIT_SUMMARY.json').read_text())
    assert x['unique_source_ids_visible']==45
    assert x['historical_source_registry_claim']==67
    assert not x['historical_source_registry_rebuilt']
    assert x['independent_blinded_gold']==0


def test_p3_clinical_ids_unresolved_and_preserved():
    rows=stage_v08.read_csv(ROOT/'results/P3_CLINICAL_OBJECT_7_REMAINING.csv')
    assert len(rows)==7
    assert all(not x['object_id_original'] and x['object_label_original'] for x in rows)
    assert all(x['external_canonical_id']=='NOT_RESOLVED' for x in rows)


def test_p3_no_invented_gold():
    rows=stage_v08.read_csv(ROOT/'results/P3_CQ_CANDIDATE_QUEUE.csv')
    assert len(rows)>=8
    assert all(not row['independent_gold'] and not row['reviewer_1'] and not row['reviewer_2'] for row in rows)
    assert all(x['split']!='INDEPENDENT_TEST' for x in rows)


def test_p3_collision_exact_source():
    rows=stage_v08.read_csv(ROOT/'results/P3_SPO_COLLISIONS.csv')
    assert len(rows)==1
    assert set(rows[0]['assertion_ids'].split(';'))=={'CLIN005','CLIN006'}


@pytest.mark.parametrize('model,triples',[('M1',207),('M2',1501),('M3',2733)])
def test_p3_frozen_rdf_parity(model,triples):
    g=Graph().parse(ROOT/f'results/P3_{model}.ttl',format='turtle')
    assert len(g)==triples


def test_p3_repeated_deterministic_diagnostics():
    rows=stage_v08.read_csv(ROOT/'results/P3_V06_RDF_QUERY_DIAGNOSTICS_24.csv')
    assert len(rows)==24
    assert len({(r['case_id'],r['model']) for r in rows})==24
    assert all(r['scientific_accuracy']=='NOT_EVALUATED' for r in rows)


def test_run_v08_deterministic(tmp_path):
    assert stage_v08.build_p2()['total_claims']==100
    assert stage_v08.build_p3()['frozen_v3_rows']==208


def test_semantic_guards_not_certification():
    status=json.loads((ROOT/'results/P3_SHACL_RUNTIME_STATUS.json').read_text())
    assert status.get('claim_of_conformance') is False if status.get('status','').startswith('NOT_RUN') else True