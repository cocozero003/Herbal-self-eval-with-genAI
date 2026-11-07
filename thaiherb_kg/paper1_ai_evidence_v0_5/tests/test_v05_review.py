import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load_csv(name):
    with (ROOT/'results'/name).open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def test_scope():
    d=json.loads((ROOT/'results/CURATION_AND_ABLATION_SUMMARY.json').read_text())
    assert d['identity']['evidence_assertions']==30
    assert d['identity']['verified_named_pubchem_records']==23
    assert d['identity']['unique_compounds']==25
    assert d['identity']['original_19_class_recovered'] is False
    assert d['identity']['independent_expert_review_completed'] is False

def test_identity_and_taxonomy():
    rows=load_csv('CHEMICAL_IDENTITY_TAXONOMY_25.csv')
    assert len(rows)==25
    assert len({r['class_v04'] for r in rows})==18
    assert len({r['class_v05'] for r in rows})==19
    d={r['name']:r for r in rows}
    assert d['piperine']['class_v05']!='cinnamamide lactam'
    assert d['piperlongumine']['class_v05']=='cinnamamide lactam'
    assert not d['limonene']['pubchem_cid_candidate']
    assert not d['DMPBD']['pubchem_cid_candidate']

def test_assertion_provenance():
    rows=load_csv('CHEMICAL_ASSERTION_EVIDENCE_REVIEW_30.csv')
    assert len(rows)==30 and len({r['assertion_id'] for r in rows})==30
    assert all(r['occurrence_source_url'].startswith('https://') for r in rows)
    assert all(r['ready_for_original_replication']=='0' for r in rows)
    assert len({r['herb_id'] for r in rows})==10
    assert all(r['source_type'] for r in rows)

def test_45_dyads_and_no_fake_gold():
    rows=load_csv('HERB_PAIR_EXPLANATION_45.csv')
    assert len(rows)==45 and all(r['expert_gold_label']=='UNAVAILABLE' for r in rows)
    gold=load_csv('INDEPENDENT_DYAD_EXPERT_BLIND_45.csv')
    assert len(gold)==45 and all(not r['adjudicated_label'] and not r['expert1_label'] for r in gold)

def test_ablation_pairing():
    ab=load_csv('CLASS_TAXONOMY_ABLATION_10SEEDS.csv')
    assert len(ab)==20
    assert {r['model'] for r in ab}=={'Chem-Proxy','Core-Proxy'}
    assert all(0 <= float(r['rank_rho_v04_18_vs_v05_19']) <= 1 for r in ab)
    assert all(0 <= int(r['top5_overlap']) <= 5 for r in ab)

def test_original_study_isolated():
    rows=load_csv('ORIGINAL_MANUSCRIPT_TOP15_REFERENCE.csv')
    assert len(rows)==15
    assert all(r['comparison_status'].startswith('description only') for r in rows)
    summary=json.loads((ROOT/'results/CURATION_AND_ABLATION_SUMMARY.json').read_text())
    assert summary['identity']['original_19_class_recovered'] is False