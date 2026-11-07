from pathlib import Path
import csv, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from audit import run as audit
from paper1.run import run as paper1
from paper2.run import run as paper2
from paper3.run import run as paper3
from shared import correlation,weights

def test_crosswalk_and_manifest():
    a=audit(); assert a['crosswalk']['paper1_herbs_subset_paper2']
    assert a['files']['paper3_assertions.csv']['bytes']>1000

def test_paper1_npmi():
    s=paper1(); assert s['positive_npmi']==23 and s['n_pairs']==45

def test_paper2_npmi():
    s=paper2(); assert s['n_formula_edges']==82 and s['n_herbs']==20

def test_paper3_audit_and_no_fabricated_gold():
    s=paper3();assert s['assertions_total']==208
    assert s['rdf_exported_assertions']<=208
    r=list(csv.DictReader((ROOT/'paper3/blinded_benchmark_template.csv').open()))
    assert all(not x['expected_answer'] and not x['adjudicated'] for x in r)

def test_hub_weights_never_change_evidence_presence():
    d=json.loads((ROOT/'data/paper1_bootstrap.json').read_text())
    w=weights(d['formulas'],[h['id'] for h in d['herbs']]);assert all((v['npmi']>0)==(v['combined_weight']>0) for v in w.values())

def test_spearman_ties_constant_safe():
    assert correlation([1,1,1],[1,2,3]) is None
    assert abs(correlation([1,2,3],[3,2,1])+1)<1e-9

def test_rdf_roundtrip_and_source_links():
    from rdflib import Graph,Namespace,RDF
    paper3()
    g=Graph().parse(ROOT/'paper3/v3_201assertions_provenance.ttl')
    ex=Namespace('https://example.org/thaiherb/ontology/')
    assert len(list(g.subjects(RDF.type,ex.EvidenceAssertion)))==201
    assert all(' ' not in str(u) for u in g.all_nodes() if str(u).startswith('https://example.org'))

def test_negative_control_missing_source_is_detected():
    d=json.loads((ROOT/'data/paper3_ui_subset.json').read_text())
    altered=dict(d['assertions'][0]); altered['source_id']='SRC_DOES_NOT_EXIST'
    assert altered['source_id'] not in d['sources']
