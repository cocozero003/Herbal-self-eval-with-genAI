import sys
from pathlib import Path
import csv,json
import pytest
from rdflib import Graph
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evaluate_p3 import main
@pytest.fixture(scope='module')
def audit():return main()
def csvrows(p):
 with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def test_freeze(audit): assert audit['assertions']==208 and audit['source_sha256'].startswith('59f914')
def test_model_sizes(audit):assert audit['projection_triples']=={'M1':207,'M2':1501,'M3':2733}
def test_channels(audit):assert audit['channels']=={'formula':71,'chemistry':100,'pharmacology_target':30,'clinical':7}
def test_624(audit):assert len(csvrows(ROOT/'results/P3_ASSERTION_AUDIT_624.csv'))==624
def test_sensitivity(audit):
 s=csvrows(ROOT/'results/P3_MODEL_CAPABILITY_SUMMARY.csv');m={x['model']:x for x in s}
 assert [(int(m[k]['provenance']),int(m[k]['context'])) for k in ('M1','M2','M3')]==[(0,0),(208,0),(208,208)]
def test_208_edges(audit):assert all(int(d['edge_recoverable'])==208 for d in csvrows(ROOT/'results/P3_MODEL_CAPABILITY_SUMMARY.csv'))
def test_collisions(audit):
 c=csvrows(ROOT/'results/P3_SPO_COLLISION_AUDIT.csv');assert len(c)==1 and set(c[0]['assertion_ids'].split(';'))=={'CLIN005','CLIN006'}
def test_3_context_groups(audit):assert len(csvrows(ROOT/'results/P3_CLINICAL_CONTEXT_VARIATION.csv'))==3
def test_ablation_no_fake_accuracy(audit):
 d=csvrows(ROOT/'results/P3_CONTEXT_ABLATION.csv');assert len(d)==6
 assert int(d[-1]['source_recoverable'])==0 and int(d[0]['source_recoverable'])==208
 assert all('not answer accuracy' in x['interpretation'] for x in d)
def test_no_gold(audit):assert audit['expert_adjudicated_gold']==0 and audit['comparative_semantic_accuracy_status'].startswith('NOT_MEASURED')
def test_legacy_development(audit):assert len(csvrows(ROOT/'results/P3_DEVELOPMENT_CQ_24_SUMMARY.csv'))==24
def test_shacl_authentic(audit):assert audit['actual_pyshacl']['status']=='PASS' and audit['actual_pyshacl']['negative_controls_detected']==10
def test_clinical_uncanonicalized(audit):assert audit['missing_clinical_canonical_object_ids']==7
def test_45_source_ids(audit):assert audit['source_ids']==45
