"""Release checks. Structural integrity only; not scientific adjudication."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import pytest
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import PROV
from src.stage_v10 import main, rdf_retention, primary_corroborations, plumbago_context_warnings, rows, V3_SHA, TH

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results'
D=ROOT/'data'


def test_original_frozen_v3_unchanged():
    assert hashlib.sha256((D/'P3_V3_208_LOCKED.csv').read_bytes()).hexdigest()==V3_SHA


def test_orig_100_claims_identical():
    old=rows(R/'P2_CHEM_EVIDENCE_100_v09.csv')
    new=rows(R/'P2_ALL_CLAIMS_AUDIT_LEDGER_100_v10.csv')
    assert len(new)==len(old)==100
    assert {x['assertion_id'] for x in old}=={x['assertion_id'] for x in new}
    old_dict={x['assertion_id']:x for x in old}
    assert all(r['original_source_disposition']==old_dict[r['assertion_id']]['disposition'] for r in new)


def test_primary_additional_source_is_one_real_2020_article():
    c=rows(R/'P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv')
    assert len(c)==5
    assert {x['assertion_id'] for x in c}=={'CA066','CA067','CA068','CA069','CA070'}
    assert all(x['doi']=='10.1177/1934578X20933067' for x in c)
    assert all(x['source_test_eligibility'].startswith('NO_POSTHOC') for x in c)
    assert all(x['original_source_id']!='CORR_2020_SATYAL' for x in c)


def test_terpinen_enantiomer_ratio_not_compound_concentration():
    c={x['assertion_id']:x for x in rows(R/'P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv')}
    assert 'NOT essential-oil mass fraction' in c['CA068']['units_and_denominator']
    assert c['CA068']['exact_source_locator']=='Table 4'


def test_plumbago_introduction_caution():
    c=rows(R/'P2_SOURCE_CONTEXT_WARNINGS_PLUMBAGO_5_v10.csv')
    assert len(c)==5
    assert all(x['decision'].startswith('DO_NOT_PROMOTE_OR_REJECT') for x in c)


def test_aggregate_distinct_corrob_id():
    x=rows(R/'P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv')
    y=rows(R/'P2_INDEPENDENT_CORROBORATION_v09.csv')
    assert len(set(r['assertion_id'] for r in x+y))==9


def test_projection_denominator_and_triples():
    summary=rows(R/'P3_RDF_CAPABILITY_SUMMARY_v08.csv')
    counts={'M1':207,'M2':1501,'M3':2733}
    assert {x['model']:int(x['rdf_triples']) for x in summary}==counts
    assert all(int(x['source_assertion_denominator'])==208 for x in summary)
    for name,total in counts.items():
        assert len(Graph().parse(R/f'P3_{name}.ttl'))==total


@pytest.mark.parametrize('model,source,evidence,directness,context',[
    ('M1',0,0,0,0),('M2',208,0,0,0),('M3',208,208,208,208)
])
def test_traceability_is_actual_model_capability(model,source,evidence,directness,context):
    s={x['model']:x for x in rows(R/'P3_RDF_CAPABILITY_SUMMARY_v08.csv')}[model]
    assert int(s['source_id_traceable'])==source
    assert int(s['evidence_mode_recoverable'])==evidence
    assert int(s['directness_recoverable'])==directness
    assert int(s['source_context_text_recoverable'])==context
    assert s['endpoint_scope']=='DETERMINISTIC_REPRESENTATION_FIDELITY_NOT_ANSWER_ACCURACY'


def test_all_624_rows_are_actual_assertions():
    a=rows(R/'P3_RDF_ASSERTION_RETENTION_624_v08.csv')
    assert len(a)==624
    assert Counter(x['model'] for x in a)=={'M1':208,'M2':208,'M3':208}


def test_identical_spo_collapse_not_biological_contradiction():
    c=rows(R/'P3_SPO_COLLISION_GROUPS_v08.csv')
    assert len(c)==1
    assert set(c[0]['assertion_ids'].split(';'))=={'CLIN005','CLIN006'}


def test_seven_missing_clinical_iri_are_flagged_not_guessed():
    a=rows(R/'P3_RDF_ASSERTION_RETENTION_624_v08.csv')
    assert sum(int(x['clinical_missing_canonical_id_flag']) for x in a if x['model']=='M3')==7


def test_no_gold_no_confirmatory_accuracy():
    cases=rows(R/'P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv')
    assert len(cases)==32
    assert all(x['adjudicated_gold']=='' and x['review_round']=='NOT_STARTED' for x in cases)
    assert all(x['confirmation_scoring_permitted']=='NO' for x in cases)


def test_source_counts_no_formulav3_mutation():
    frozen=rows(D/'P3_V3_208_LOCKED.csv')
    assert Counter(x['channel'] for x in frozen)=={'formula':71,'chemistry':100,'pharmacology_target':30,'clinical':7}


def test_claim_status_not_clinical_safety():
    status=json.loads((R/'P2_P3_V10_V08_STATUS.json').read_text())
    assert not status['scientific_overclaims_permitted']
    assert status['SHACL_Core'].startswith('NOT_RUN')
    assert status['P3']['benchmark_gold']==0


def test_pyshacl_status_cannot_falsely_conform_when_unavailable():
    from src.validate_shacl_v08 import run
    status = run()
    assert status['engine'] == 'pyshacl'
    if not status['dependency_available']:
        assert status['status'] == 'NOT_RUN'
        assert status['authentic_conformance'] is None
        assert status['claim_of_scientific_validity'] is False


def test_corrob_9_are_not_prespecified_external_gold():
    c=rows(R/'P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv')
    assert all('NO_POSTHOC' in x['source_test_eligibility'] for x in c)
    original=rows(R/'P2_CHEM_EVIDENCE_100_v09.csv')
    assert len([x for x in original if x['disposition']=='PRIMARY_FULLTEXT_MATCH'])==5
