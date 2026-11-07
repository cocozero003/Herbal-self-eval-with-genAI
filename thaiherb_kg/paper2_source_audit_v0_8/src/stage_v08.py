"""P2 v0.8 / P3 v0.6 research-data integrity and candidate benchmark utilities.

This script never infers clinical, biological, regulatory or expert-ground-truth
validity from an archived assertion or a citation existing on the internet.
"""
from __future__ import annotations
import csv
import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from rdflib import Graph, URIRef, Literal, RDF
from rdflib.namespace import DCTERMS, PROV
from .stage_next import answer_case, CASE_SPECS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RESULTS = ROOT / 'results'
DOCS = ROOT / 'docs'


def read_csv(path):
    with Path(path).open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, columns=None):
    rows = list(rows)
    columns = list(columns or (rows[0].keys() if rows else []))
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# These are SOURCE-LEVEL publication classifications checked against the cited
# publication page/abstract; not claim-level biological validations.
# Values are provenance/protocol observations, not expert-review ratings.
SOURCE_CLASS = {
    'SRC_GINGER': ('REVIEW_SPECIES', 'SPECIES', 'Rhizome review; multiple processing types', 'https://www.mdpi.com/2304-8158/8/6/185'),
    'SRC_RETRO': ('PRIMARY_ANALYTICAL', 'SPECIES', 'Methanolic dried fruit extract; compound table in original study', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8533580/'),
    'SRC_BLACK': ('REVIEW_SPECIES', 'SPECIES', 'Black pepper berry, piperine and essential oil; primary measurements not from review authors', 'https://link.springer.com/article/10.1186/s40816-021-00292-2'),
    'SRC_GARLIC': ('REVIEW_SPECIES', 'SPECIES', 'Organosulfur review; fresh/processed forms must not be equated', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6678835/'),
    'SRC_PLAI': ('PRIMARY_ANALYTICAL', 'SPECIES', 'Hydrodistilled rhizome essential oil; GC-FID and GC-MS; abstract matched', 'https://scijournals.onlinelibrary.wiley.com/doi/10.1002/jsfa.8474'),
    'SRC_GALANGAL': ('REVIEW_GENUS', 'GENUS', 'Alpinia species-wide review, not exact Alpinia galanga material study', 'https://pubs.rsc.org/en/content/articlehtml/2017/ra/c6ra27830b'),
    'SRC_BASIL': ('REVIEW_SPECIES', 'SPECIES', 'Ocimum tenuiflorum phytochemical review', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11521583/'),
    'SRC_LICORICE': ('REVIEW_SPECIES', 'SPECIES', 'Licorice composition/biological review', 'https://pubmed.ncbi.nlm.nih.gov/34961221/'),
    'SRC_CLOVE': ('REVIEW_SPECIES', 'SPECIES', 'Clove nutrition and phytochemistry review', 'https://pubmed.ncbi.nlm.nih.gov/36313111/'),
    'SRC_KAFFIR': ('REVIEW_SPECIES', 'SPECIES', 'Citrus hystrix review; plant part dependent', 'https://arabjchem.org/citrus-hystrix-a-review-of-phytochemistry-pharmacology-and-industrial-applications-research-progress/'),
    'SRC_CHEBULA': ('REVIEW_SPECIES', 'FRUIT', 'Terminalia chebula fruit review; fruit not insect gall material', 'https://pubmed.ncbi.nlm.nih.gov/39683707/'),
    'SRC_CARDAMOM': ('PRIMARY_ANALYTICAL_ABSTRACT_METADATA', 'FRUIT', 'Amomum testaceum fruit essential-oil compositional report; original tables not inspected', 'https://www.tandfonline.com/doi/abs/10.1080/10412905.2001.9699621'),
    'SRC_NUTMEG': ('REVIEW_SPECIES', 'SPECIES', 'Nutmeg phytochemical review; seed and aril contexts differ', 'https://pubmed.ncbi.nlm.nih.gov/28082856/'),
    'SRC_CORIANDER': ('REVIEW_SPECIES', 'SPECIES', 'Coriander essential-oil review; fruit/leaf context differs', 'https://pubmed.ncbi.nlm.nih.gov/36677754/'),
    'SRC_NIGELLA': ('REVIEW_SPECIES', 'SPECIES', 'Nigella sativa comprehensive review', 'https://pubmed.ncbi.nlm.nih.gov/39769174/'),
    'SRC_KAEMPFERIA': ('REVIEW_SPECIES', 'SPECIES', 'Kaempferia galanga rhizome phytochemistry review', 'https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2021.675350/full'),
    'SRC_ACORUS': ('REVIEW_GENUS', 'GENUS', 'Acorus genus review; calamus subspecies and beta-asarone contexts require verification', 'https://pubmed.ncbi.nlm.nih.gov/37894595/'),
    'SRC_PLUMBAGO': ('PRIMARY_ANALYTICAL', 'SPECIES', 'Tentative LC-MS/MS of 70% ethanol aerial-part extract; introductory compound mentions not all measured in study', 'https://www.nature.com/articles/s41598-022-13718-9'),
    'SRC_SOMPOI': ('PRIMARY_ISOLATION_AFTER_HYDROLYSIS', 'SPECIES', 'Concinnosides A-E isolated from alkaline hydrolysate of pod saponins, not intact crude pods', 'https://pubmed.ncbi.nlm.nih.gov/9145500/'),
    'SRC_CURCUMA': ('REVIEW_GENUS', 'GENUS', 'Curcuma spp. essential-oil review; exact C. aromatica species row required', 'https://pubmed.ncbi.nlm.nih.gov/30200410/'),
}

# New promoted statuses require a specific named compound actually appearing
# in the accessible primary abstract or source paper abstract.
UPGRADES = {
    **{f'CA{i:03d}': ('SECONDARY_ABSTRACT_NAME_MATCH', 'Ashokkumar et al. (2021), abstract Results: piperine and volatile oils listed for Piper nigrum',
                       'https://link.springer.com/article/10.1186/s40816-021-00292-2') for i in range(11, 16)},
    **{f'CA{i:03d}': ('SECONDARY_ABSTRACT_NAME_MATCH', 'Bhattarai et al. (2024), abstract: rosmarinic, oleanolic, luteolin and ursolic acid; excludes eugenol from this promotion',
                       'https://pmc.ncbi.nlm.nih.gov/articles/PMC11521583/') for i in range(31, 35)},
    **{f'CA{i:03d}': ('PRIMARY_ABSTRACT_AFTER_HYDROLYSIS', 'Gafur et al. (1997), abstract: named concinnosides A-E from alkaline hydrolysate of Acacia concinna pod saponins; NOT intact pod occurrence',
                       'https://pubmed.ncbi.nlm.nih.gov/9145500/') for i in range(91, 96)},
}


def build_p2():
    records = read_csv(RESULTS/'P2_CHEM_EVIDENCE_100_v07.csv')
    assert len(records) == 100 and len(set(r['assertion_id'] for r in records)) == 100
    assert len(SOURCE_CLASS) == 20
    srcmap = {}
    for r in records:
        srcmap[r['source_id']] = r
    assert set(srcmap) == set(SOURCE_CLASS)
    source_rows = []
    for key, (ptype, scope, risk, evidence_url) in SOURCE_CLASS.items():
        row = srcmap[key]
        source_rows.append({
            'source_id': key, 'herb_id': row['herb_id'], 'scientific_name': row['herb_scientific_name'],
            'doi_url_in_frozen_registry': row['source_url_from_archive'],
            'publication_type_source_screen': ptype, 'scope': scope,
            'source_verified_url': evidence_url,
            'source_scope_and_material_warning': risk,
            'individual_compound_fulltext_all_five_verified': 'NO',
            'external_heldout_eligible': 'NO_USED_AS_INPUT_SOURCE',
            'review_scope': 'PUBLICATION_TYPE_AND_ACCESSIBLE_ABSTRACT_ONLY',
            'researcher_adjudicated': 'NO'
        })
    write_csv(RESULTS/'P2_SOURCE_TYPE_AUDIT_20.csv', source_rows)
    bysource = {r['source_id']: r for r in source_rows}
    rows = []
    for original in records:
        r = dict(original)
        source = bysource[r['source_id']]
        r.update({'v08_source_type': source['publication_type_source_screen'],
                  'v08_source_scope': source['scope'],
                  'v08_material_scope_warning': source['source_scope_and_material_warning'],
                  'v08_source_access_url': source['source_verified_url'],
                  'v08_claim_evidence_level': r['v07_review_level'],
                  'v08_claim_exact_locator': r['v07_source_locator'],
                  'v08_claim_review_reason': 'PRESERVED_FROM_V07',
                  'v08_expert_gold': 'NOT_ADJUDICATED',
                  'v08_external_biological_validation': 'NOT_DONE',
                  'v08_chemical_canonicalization': 'NOT_ADJUDICATED'})
        if r['assertion_id'] in UPGRADES:
            level, locator, url = UPGRADES[r['assertion_id']]
            r['v08_claim_evidence_level'] = level
            r['v08_claim_exact_locator'] = locator
            r['v08_source_access_url'] = url
            r['v08_claim_review_reason'] = 'NAMED_IN_SOURCE_ABSTRACT; NOT_EXPERT_GOLD'
        if r['source_id'] == 'SRC_SOMPOI':
            r['v08_material_scope_warning'] = 'Prosapogenols obtained AFTER ALKALINE HYDROLYSIS of pod saponins; do not imply free concinnosides A-E occur unchanged in native pods or formulation.'
        if r['source_id'] in ('SRC_GALANGAL','SRC_ACORUS','SRC_CURCUMA'):
            r['v08_claim_review_reason'] = 'GENUS_LEVEL_REVIEW; NOT_SPECIES_COMPOUND_VERIFIED'
        if r['source_id'] == 'SRC_PLUMBAGO':
            r['v08_claim_review_reason'] = 'SOURCE_PRIMARY_STUDY; REQUIRES_CHECK_AGAINST_ACTUAL_LCMS_COMPOUND_TABLE_NOT_INTRODUCTORY_PRIOR_REPORTS'
        rows.append(r)
    counts = dict(sorted(Counter(r['v08_claim_evidence_level'] for r in rows).items()))
    write_csv(RESULTS/'P2_CHEM_EVIDENCE_100_v08.csv', rows)
    write_csv(RESULTS/'P2_OPEN_CLAIM_QUEUE_v08.csv', [r for r in rows if r['v08_claim_evidence_level']=='NOT_VERIFIED'])
    levels = ('PRIMARY_FULLTEXT_MATCH','PRIMARY_ABSTRACT_ONLY','PRIMARY_ABSTRACT_AFTER_HYDROLYSIS',
              'SECONDARY_ONLY','SECONDARY_ABSTRACT_NAME_MATCH','NOT_VERIFIED')
    assert set(counts).issubset(set(levels)), counts
    # Original chemical ID set counts must not drift between papers.
    assert len(set(r['compound_id_internal'] for r in rows)) == 83
    byclass = dict(sorted(Counter(x['publication_type_source_screen'] for x in source_rows).items()))
    summary = {'version': 'P2v08', 'total_claims': 100, 'distinct_compound_ids': 83,
               'claim_evidence_counts': counts, 'source_publication_types': byclass,
               'n_source_documents_reviewed_for_type': 20,
               'claims_validated_by_independent_experts': 0,
               'external_source_disjoint_test_set': 'NOT_AVAILABLE',
               'original_35_class_taxonomy': 'NOT_RECOVERED',
               'primary_analytical_fulltext_confirmations': counts.get('PRIMARY_FULLTEXT_MATCH',0),
               'warning': 'Publication-type review is NOT compound-specific confirmation or biological validation'}
    save_json(RESULTS/'P2_V08_REVIEW_SUMMARY.json', summary)
    # Original 35-class map not present in previously inspected source archives.
    archive_report = {
      'status': 'NOT_RECOVERED', 'source_examined': 'ThaiHerb20_Paper2_WebApp_v1.zip; Paper2 v0.4/v0.5 releases',
      'finding': 'Original 35-class counts appear in manuscript/bootstrap metadata; no 83-to-35 mapping table or original class-aware model state recovered',
      'reference': 'Prior audit P2_ORIGINAL_CLASS_RECOVERY_AUDIT.md',
      'new_candidate_taxonomy_equivalent_to_original': False}
    save_json(RESULTS/'P2_ORIGINAL_35_CLASS_RECOVERY_STATUS.json', archive_report)
    return summary


def build_p3():
    # Frozen V3 data are immutable; M1/M2/M3 projection files remain identical to v0.5.
    rows = read_csv(DATA/'P3_V3_208_LOCKED.csv')
    assert len(rows)==208 and len({r['assertion_id'] for r in rows})==208
    assert Counter(r['channel'] for r in rows)=={'formula':71,'chemistry':100,'pharmacology_target':30,'clinical':7}
    graphs={m:Graph().parse(RESULTS/f'P3_{m}.ttl',format='turtle') for m in ('M1','M2','M3')}
    assert {m:len(g) for m,g in graphs.items()}=={'M1':207,'M2':1501,'M3':2733}
    collision = defaultdict(list)
    for r in rows:
        key=(r['subject_id'],r['predicate_or_topic'],r['object_id'] or r['object_label'])
        collision[key].append(r)
    collisions=[]
    for key,group in collision.items():
        if len(group)>1:
            collisions.append({'subject_id':key[0],'predicate':key[1],'object':key[2],
              'input_assertion_count':len(group),'m1_distinct_spo_count':1,
              'assertion_ids':';'.join(r['assertion_id'] for r in group),
              'sources':';'.join(r['source_id'] for r in group),
              'scientific_interpretation':'SPO duplicates collapse; not sufficient to label an actual clinical contradiction'})
    write_csv(RESULTS/'P3_SPO_COLLISIONS.csv',collisions,
              ['subject_id','predicate','object','input_assertion_count','m1_distinct_spo_count','assertion_ids','sources','scientific_interpretation'])
    assert len(collisions)==1 and 'CLIN005' in collisions[0]['assertion_ids'] and 'CLIN006' in collisions[0]['assertion_ids']
    clinical=[r for r in rows if r['channel']=='clinical']
    missing=[]
    for r in clinical:
        missing.append({'assertion_id':r['assertion_id'],'object_label_original':r['object_label'],
          'object_id_original':r['object_id'],'source_id':r['source_id'],
          'context_original':r['source_locator_or_context'],
          'export_in_M1_M2_M3':'YES_AS_LITERAL', 'external_canonical_id':'NOT_RESOLVED',
          'method':'PRESERVE_VERBATIM_SOURCE_TEXT', 'expert_gold':'NOT_AVAILABLE'})
    assert all(not r['object_id'] for r in clinical)
    write_csv(RESULTS/'P3_CLINICAL_OBJECT_7_REMAINING.csv',missing)
    chem=[r for r in rows if r['channel']=='chemistry']
    write_csv(RESULTS/'P3_CHEMISTRY_LOCATOR_100_QUEUE.csv',[{
        'assertion_id':r['assertion_id'],'compound_label':r['object_label'],
        'source_id':r['source_id'],'v3_locator':r['source_locator_or_context'],
        'source_specific_compound_locator':'NOT_RECONCILED_FROM_FROZEN_V3',
        'status':'NEEDS_SOURCE_SPECIFIC_REVIEW'} for r in chem])
    unique_sources=sorted(set(r['source_id'] for r in rows))
    write_csv(RESULTS/'P3_SOURCE_45_REGISTRY_SCOPE.csv', [{
       'source_id':sid,'channels':';'.join(sorted(set(x['channel'] for x in rows if x['source_id']==sid))),
       'assertion_count':sum(x['source_id']==sid for x in rows),
       'status':'PRESENT_IN_V3_208', 'full_67_registry_reconciled':'NO'} for sid in unique_sources])
    assert len(unique_sources)==45
    # 8 development cases are preserved and DO NOT become independent test/gold.
    candidate=[]
    cases=[]
    for case in CASE_SPECS:
        cid,cat,question,subject,pred,obj,rule=case
        candidate.append({'case_id':cid,'question':question,'category':cat,'source':'EXISTING_DEVELOPMENT_V05',
             'subject_id':subject,'predicate':pred,'object_id':obj,'rule':rule,
             'independent_gold':'','reviewer_1':'','reviewer_2':'',
             'split':'DEVELOPMENT_ONLY', 'note':'No blinded expert validity labels'})
        cases.append(case)
    # Additional source-grounded candidates are sampled deterministically across
    # channels, NOT turned into evaluated cases or benchmark gold.
    for i,r in enumerate(rows):
        if i%9!=0:continue
        category={'formula':'formula_version','chemistry':'chemistry',
             'clinical':'clinical_context','pharmacology_target':'pharmacology_directness'}[r['channel']]
        candidate.append({'case_id':f'CQA_{r["assertion_id"]}',
           'question':f'What archived relation and source context are recorded for assertion {r["assertion_id"]}?',
           'category':category,'source':'FROZEN_SOURCE_ASSERTION_CANDIDATE',
           'subject_id':r['subject_id'],'predicate':r['predicate_or_topic'],
           'object_id':r['object_id'],'rule':'development_assertion_lookup',
           'independent_gold':'','reviewer_1':'','reviewer_2':'',
           'split':'NOT_ELIGIBLE_FOR_LOCKED_TEST',
           'note':'Generated for reviewer prompt evaluation only; NOT independent competency-question gold'})
    write_csv(RESULTS/'P3_CQ_CANDIDATE_QUEUE.csv',candidate)
    # True comparative outcomes from existing 8 dev cases, not clinical/semantic accuracy.
    answers=[]
    for case in cases:
        for model in ('M1','M2','M3'):
            answers.append(answer_case(graphs[model],model,case))
    write_csv(RESULTS/'P3_V06_RDF_QUERY_DIAGNOSTICS_24.csv',answers)
    assert len(answers)==24
    summary={'version':'P3v06','frozen_v3_rows':len(rows),
          'v3_input_sha256':sha256(DATA/'P3_V3_208_LOCKED.csv'),
          'channel_counts':dict(Counter(r['channel'] for r in rows)),
          'unique_source_ids_visible':45,'historical_source_registry_claim':67,
          'historical_source_registry_rebuilt':False,
          'clinical_uncanonicalized_ids':len(missing),
          'chemistry_locator_queue':len(chem),
          'm1_spo_collapse_groups':len(collisions),
          'triple_counts':{m:len(g) for m,g in graphs.items()},
          'development_questions':len(cases),'query_outputs':len(answers),
          'candidate_questions':len(candidate),'independent_blinded_gold':0,
          'scientific_comparative_accuracy':'NOT_EVALUATED',
          'semantic_negative_controls':'IMPLEMENTATION_TESTS_ONLY',
          'shacl_core':'NOT_RUN' }
    save_json(RESULTS/'P3_V06_AUDIT_SUMMARY.json', summary)
    return summary


def main():
    p2=build_p2(); p3=build_p3()
    save_json(RESULTS/'V08_V06_BUILD_STATUS.json',{'paper2':p2,'paper3':p3})
    print(json.dumps({'paper2':p2['claim_evidence_counts'],
                      'paper3':{'rows':p3['frozen_v3_rows'],'sources':p3['unique_source_ids_visible'],
                                'query_outputs':p3['query_outputs']}},ensure_ascii=False,indent=2))

if __name__=='__main__':main()