"""Scientific safety / dataset continuity checks for Paper 1 v0.6."""
import csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'audit_v06'))
from evidence_qualification import audit, SOURCES, CORROBORATIONS

def read(name):
 with (ROOT/'results/v06'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def test_qualification_is_non_independent():
 m=audit();assert m['locked_proxy_assertions']==30
 assert m['original_source_ids']==12
 assert m['original_herbs_with_single_source']==8
 assert m['independent_expert_evaluation'] is False
 assert m['primary_fulltext_quote_audit_complete'] is False
 assert m['compound_class_matches_original_paper1'] is False

def test_citations_do_not_invent_gold():
 rows=read('assertion_evidence_qualification_30.csv')
 assert len(rows)==30 and len({x['assertion_id'] for x in rows})==30
 assert all(x['independent_expert_validated']=='0' and x['original_paper1_compound_class_recovered']=='0' for x in rows)
 assert all(url.startswith('https://') for r in rows for url in r['additional_source_urls'].split(';') if url)

def test_context_warnings_present():
 d={x['assertion_id']:x for x in read('assertion_evidence_qualification_30.csv')}
 assert 'distilled' in d['CA018']['context_limitation']
 assert 'red-cultivar' in d['CA031']['context_limitation']
 assert 'red-cultivar' in d['CA032']['context_limitation']
 assert 'G. glabra' in d['CA037']['context_limitation']
 assert 'stereo' in d['CA047']['context_limitation']

def test_original_source_coverage_stress():
 r=read('source_holdout_embedding_eligibility_12.csv')
 assert len(r)==12
 assert sum(x['eligible_for_all_45_pairs']=='0' for x in r)==8
 assert sum(x['eligible_for_all_45_pairs']=='1' for x in r)==4

def test_all_paired_comparisons():
 rows=read('source_holdout_embedding_eligible_10seeds.csv')
 assert len(rows)==80
 assert {x['model'] for x in rows}=={'Chem-Proxy','Core-Proxy'}
 assert len({x['seed'] for x in rows})==10
 assert all(-1<=float(x['rank_rho_baseline_vs_holdout'])<=1 for x in rows)
 assert all(0<=int(x['top5_overlap'])<=5 for x in rows)

def test_metadata_restricts_source_types():
 assert len(SOURCES)==12
 assert 'CA018' in CORROBORATIONS
 assert SOURCES[CORROBORATIONS['CA018'][0]][1]=='primary_analytical'

def test_previous_gold_stays_blank():
 with (ROOT/'results/INDEPENDENT_DYAD_EXPERT_BLIND_45.csv').open(encoding='utf-8-sig') as f:
  r=list(csv.DictReader(f))
 assert len(r)==45
 assert all(not x['adjudicated_label'] and not x['expert1_label'] and not x['expert2_label'] for x in r)

def test_dashboard_contains_no_remote_scripts():
 s=(ROOT/'dashboard/Paper1_Source_Independence_v0.6.html').read_text()
 assert 'https://cdn.' not in s
 assert 'window.RESEARCH_DATA=' in s
 assert 'Paper 1' in s