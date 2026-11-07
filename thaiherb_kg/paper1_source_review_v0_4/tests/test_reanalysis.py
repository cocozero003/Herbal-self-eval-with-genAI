import json,sys,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from formula_audit import verify,FORMULAS,npmi
from model_reanalysis import CLASS,generate_cooc,generate_chem,train

def test_all_formula_source_names_and_counts():
    assert len(FORMULAS)==10
    assert sum(len(x[4]) for x in FORMULAS)==46
    assert sum(x[5] for x in FORMULAS)>46
    assert all(x[3][0] <= x[3][1] for x in FORMULAS)

def test_f05_long_table_not_false_omission():
    f=next(x for x in FORMULAS if x[0]=='F05_DTAM2566')
    assert f[3]==(161,162)
    assert {'H01','H02','H03','H05','H10'}==set(f[4])

def test_all_100_matrix_source_reviewed(tmp_path):
    _,pairs,m=verify(ROOT/'data/paper1_bootstrap_v3_proxy.json',tmp_path)
    assert m['herb_formula_matrix_cells']==100
    assert m['present_memberships']==46 and m['absent_memberships']==54
    assert m['positive_npmi_edges']==23
    data=list(csv.DictReader(open(tmp_path/'formula_herb_100_matrix.csv',encoding='utf-8-sig')))
    assert len(data)==100 and all(x['agreement']=='1' for x in data)

def test_chemistry_proxy_counts():
    d=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text())
    rows=[x for x in d['assertions'] if x['assertion_type']=='ChemistryOccurrenceAssertion']
    assert len(rows)==30 and len(set(x['object_label'] for x in rows))==25
    assert set(x['object_label'] for x in rows)==set(CLASS)

def test_walks_have_herb_ids():
    d=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text())
    ids=[x['id'] for x in d['herbs']]
    assert len(generate_cooc(d['formulas'],ids,42))==600
    chem=[x for x in d['assertions'] if x['assertion_type']=='ChemistryOccurrenceAssertion']
    assert len(generate_chem(chem,ids,42))==600

def test_full_results_no_model_claims():
    s=json.loads((ROOT/'results/computational_manifest.json').read_text())
    assert s['reported_original_class_count']==19
    assert s['candidate_class_ontology'].startswith('new exploratory')
    assert len(list(csv.DictReader(open(ROOT/'results/embedding_pair_summary.csv',encoding='utf-8-sig'))))==270

def test_no_expert_claim_or_data_frozen():
    r=json.loads((ROOT/'results/audit_manifest.json').read_text())
    assert r['original_paper1_training_archive_matched'] is False
    assert r['withdraw_v0_3_three_edge_deletion'] is True
    assert 'NOT independent' in r['source_verification']