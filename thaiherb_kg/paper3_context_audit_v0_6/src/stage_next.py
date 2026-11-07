"""Paper 2 v0.7 and Paper 3 v0.5 next-stage evidence and query preparation.

Only source-anchored, claim-level statuses are added; 208 V3 assertions frozen.
"""
from __future__ import annotations
import csv, json, hashlib, collections
from pathlib import Path
from rdflib import Graph, Literal, URIRef, RDF
from rdflib.namespace import DCTERMS, PROV

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results'; RES.mkdir(exist_ok=True)
DATA=ROOT/'data'; TH='urn:thaiherb:v04:'

def readcsv(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows,fields=None):
    rows=list(rows);fields=fields or list(rows[0])
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
def jwrite(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# Bibliographically checked publication and a bounded, claim-specific locator.
# The *review* papers do not constitute primary compound quantification.
SOURCE_AUDITS={
 'SRC_GINGER': dict(evidence_url='https://www.mdpi.com/2304-8158/8/6/185',doi='10.3390/foods8060185',
   locator='Mao et al. (2019), section 2.1 (composition), section 2.10 (6-paradol and 6-shogaol in bioactivity experiments)',
   level='SECONDARY_ONLY',context='Ginger rhizome/derived components; extraction and quantitative levels vary or are not stated for these five claims.'),
 'SRC_GARLIC': dict(evidence_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC6678835/',doi='10.3390/foods8070246',
   locator='Shang et al. (2019), abstract and section 2/organosulfur composition',
   level='SECONDARY_ONLY',context='Garlic organosulfur compounds; review aggregates processing conditions, tissues and studies.'),
 'SRC_PLAI': dict(evidence_url='https://pubmed.ncbi.nlm.nih.gov/28585369/',doi='10.1002/jsfa.8474',
   locator='Verma et al. (2018), publisher/PubMed abstract, Results (five major constituents)',
   level='PRIMARY_ABSTRACT_ONLY',context='Hydrodistilled essential oil of Zingiber montanum rhizomes from India; GC-FID / GC-MS. Full table inaccessible in this review session.'),
}
# Abstract percent is an inter-sample range, not values of individual subject samples.
PLAI_RANGES={'CA021':'13.5–38.0','CA022':'20.6–35.3','CA023':'9.0–31.3','CA024':'1.1–4.8','CA025':'1.0–4.4'}

def build_evidence():
    rows=readcsv(RES/'P2_CHEM_EVIDENCE_100_v06.csv')
    assert len(rows)==100 and len({x['assertion_id'] for x in rows})==100
    seen=[]
    for row in rows:
        row.update({'v07_review_level':'', 'v07_source_locator':'', 'v07_source_url':'','v07_source_context':'',
                    'v07_source_doi':'','v07_quantity_source':'','v07_quantity_unit':'','v07_review_status':'',
                    'v07_chemical_structure_identity':'NOT_ADJUDICATED','v07_authority':'AI_ASSISTED_SOURCE_READING',
                    'v07_full_text_checked':'NO','v07_primary_original_study':'UNKNOWN'})
        if row['disposition']=='PRIMARY_FULLTEXT_MATCH':
            row['v07_review_level']='PRIMARY_FULLTEXT_MATCH'
            row['v07_source_locator']=row['fulltext_claim_locator']
            row['v07_source_url']=row['source_access_url']
            row['v07_source_context']=row['verification_scope']
            row['v07_source_doi']='10.3390/antiox10101642'
            row['v07_quantity_source']=row['reported_quantity']
            row['v07_quantity_unit']=row['quantity_unit']
            row['v07_full_text_checked']='YES'
            row['v07_primary_original_study']='YES'
        elif row['source_id'] in SOURCE_AUDITS:
            source=SOURCE_AUDITS[row['source_id']]
            row['v07_review_level']=source['level'];row['v07_source_locator']=source['locator']
            row['v07_source_url']=source['evidence_url'];row['v07_source_context']=source['context']
            row['v07_source_doi']=source['doi']
            row['v07_primary_original_study']='YES' if source['level']=='PRIMARY_ABSTRACT_ONLY' else 'NO'
            if row['assertion_id'] in PLAI_RANGES:
                row['v07_quantity_source']=PLAI_RANGES[row['assertion_id']]
                row['v07_quantity_unit']='percent of essential oil; range across samples in abstract'
            # Preserve v0.6 raw dispositions; expose v0.7 separately to avoid meaning drift.
        else:row['v07_review_level']='NOT_VERIFIED'
        row['v07_review_status']='SOURCE_LEVEL_SECONDARY_OR_ABSTRACT_ONLY' if row['v07_review_level'] in ('SECONDARY_ONLY','PRIMARY_ABSTRACT_ONLY') else row['v07_review_level']
        seen.append(row)
    ctr=collections.Counter(x['v07_review_level'] for x in seen)
    assert ctr=={'NOT_VERIFIED':80,'SECONDARY_ONLY':10,'PRIMARY_FULLTEXT_MATCH':5,'PRIMARY_ABSTRACT_ONLY':5},ctr
    writecsv(RES/'P2_CHEM_EVIDENCE_100_v07.csv',seen)
    writecsv(RES/'P2_NEWLY_REVIEWED_15.csv',[x for x in seen if x['source_id'] in SOURCE_AUDITS])
    writecsv(RES/'P2_STILL_UNVERIFIED_80.csv',[x for x in seen if x['v07_review_level']=='NOT_VERIFIED'])
    summary={'status':'SOURCE_REVIEW_ONLY_NOT_GOLD','input_sha256':sha(RES/'P2_CHEM_EVIDENCE_100_v06.csv'),
          'counts':dict(ctr),'total':100,'full_text_primary':5,'primary_abstract_only':5,'secondary_review_only':10,
          'not_verified':80,'expert_adjudicated':False,'external_biological_validation':False}
    jwrite(RES/'P2_V07_AUDIT_SUMMARY.json',summary)
    src=[]
    for source, meta in SOURCE_AUDITS.items():
        src.append({'source_id':source,**meta,'verdict':'SOURCE_IDENTIFIED_NOT_CANONICAL_STRUCTURE_VALIDATED',
           'independent_heldout_dataset':'NOT_ESTABLISHED','source_disjointness':'NOT_VERIFIED',
           'date_checked':'2026-11-07'})
    src.append({'source_id':'SRC_RETRO','evidence_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC8533580/',
       'doi':'10.3390/antiox10101642','locator':'Luca et al. (2021), Section 3.1 Table 3, final species column',
       'level':'PRIMARY_FULLTEXT_MATCH','context':'Methanolic dried fruit extract; PE mg per g extract, not pure analyte mass.',
       'verdict':'MATCH_FOR_5_CLAIMS','independent_heldout_dataset':'NOT_ESTABLISHED',
       'source_disjointness':'NOT_VERIFIED','date_checked':'2026-11-07'})
    writecsv(RES/'P2_V07_EVIDENCE_SOURCE_REGISTRY.csv',src)
    return summary

# Fixed, knowledge-graph competency-question development set (not benchmark gold).
CASE_SPECS=[
('CQD01','taxonomy','Is the botanical material identified beyond a species ID?', 'H11','ingredient_member_of','', 'material_required'),
('CQD02','material_preparation','Can the exact plant part be confirmed for H11?', 'H11','ingredient_member_of','', 'material_required'),
('CQD03','formula_version','Which formula IDs include H01 in original V3?', 'H01','ingredient_member_of','','edge'),
('CQD04','chemistry','Which compounds are reported for H02?', 'H02','reported_contains','','edge'),
('CQD05','directness','Does 6-shogaol have a direct TRPA1 channel assertion?', '6-shogaol','agonist','T_TRPA1','directness_required'),
('CQD06','clinical_context','What clinical contexts are reported for ginger and platelet aggregation?', 'H01','platelet aggregation','','context_required'),
('CQD07','discordance','Do distinct ginger platelet studies have differing effects/contexts?', 'H01','platelet aggregation','','discordance_review'),
('CQD08','safety_regulatory','Is product authorization or clinical safety established for ginger?', 'H01','regulatory_approval','','regulatory_unavailable'),
]

def entity(text):return URIRef(TH+'entity:'+__import__('urllib.parse',fromlist=['quote']).quote(text,safe=''))
def rel(text):return URIRef(TH+'relation:'+__import__('urllib.parse',fromlist=['quote']).quote(text,safe=''))

def answer_case(g,model,case):
    case_id,cat,question,sub,pred,obj,rule=case
    # Full graph query, no gold labels, no lookup in the original CSV when answering.
    subject=entity(sub);predicate=rel(pred)
    basic=[(o,) for o in g.objects(subject,predicate)] if model=='M1' else []
    rec=[]
    if model=='M1':
        for (o,) in basic:rec.append({'object':str(o).replace(TH+'entity:',''), 'id':'','source_id':'',
            'context':'','directness':'','limitation':''})
    else:
        for a in g.subjects(URIRef(TH+'subject'),subject):
            if (a,URIRef(TH+'predicate'),predicate) not in g:continue
            if (a,RDF.type,URIRef(TH+'EvidenceAssertion')) not in g:continue
            for o in g.objects(a,URIRef(TH+'object')):
                sid=next(g.objects(a,DCTERMS.identifier),Literal(''))
                source=next(g.objects(a,PROV.wasDerivedFrom),URIRef(''))
                rec.append({'object':str(o).replace(TH+'entity:',''), 'id':str(sid),
                    'source_id':str(source).replace(TH+'source:',''),
                    'context':str(next(g.objects(a,URIRef(TH+'contextText')),Literal(''))),
                    'directness':str(next(g.objects(a,URIRef(TH+'directness')),Literal(''))),
                    'limitation':str(next(g.objects(a,URIRef(TH+'limitationText')),Literal(''))),
                    'object_label':str(next(g.objects(a,URIRef(TH+'objectLabel')),Literal('')))})
    rec.sort(key=lambda r:(r['object'],r['id']))
    if obj:rec=[r for r in rec if r['object']==str(entity(obj)).replace(TH+'entity:','')]
    status='SUPPORTED_EDGES' if rec else 'ABSTAIN_NOT_IN_GRAPH'
    qualification=''
    if rule=='material_required':
        status='ABSTAIN_INSUFFICIENT_MATERIAL';qualification='No canonical material/plant part identifiers in frozen V3; do not infer gall=fruit or seed=aril.'
    elif rule=='regulatory_unavailable':
        status='ABSTAIN_NOT_REGULATORY_DATA';qualification='No authorization or product safety conclusion is supported by these assertions.'
    elif rule=='directness_required' and rec:
        if model!='M3':status='ABSTAIN_DIRECTNESS_UNAVAILABLE';qualification='Directness is not represented in this model projection.'
        elif any(r['directness']!='direct_compound_target' for r in rec):
            status='ABSTAIN_NOT_DIRECT_BINDING';qualification='Source assertion does not document direct compound-target mode.'
    elif rule in ('context_required','discordance_review') and rec:
        if model!='M3':status='ABSTAIN_CONTEXT_UNAVAILABLE';qualification='Study context and effect direction not represented in projection.'
        else:
            status='QUALIFIED_CONTEXT_RECORDS' if rule=='context_required' else 'POSSIBLE_CONTEXT_DISCORDANCE_NEEDS_EXPERT'
            qualification='Source contexts differ; do not infer genuine biological contradiction or clinical efficacy.'
    elif rule=='edge' and rec:
        qualification=('M1 cannot return per-assertion citations.' if model=='M1' else 'Source assertion presence, not independently established botanical/clinical truth.')
    return {'case_id':case_id,'category':cat,'question':question,'model':model,'query_rule':rule,
         'status':status,'edge_count':len(rec),'distinct_assertion_ids':len({r['id'] for r in rec if r['id']}),
         'citation_count':len({r['source_id'] for r in rec if r['source_id']}),
         'assertion_ids':';'.join(r['id'] for r in rec if r['id']),
         'source_ids':';'.join(sorted({r['source_id'] for r in rec if r['source_id']})),
         'answer_summary':('Study-level context records are distinct and require qualitative review.' if status=='POSSIBLE_CONTEXT_DISCORDANCE_NEEDS_EXPERT' else status),
         'qualification':qualification,'returned_records_json':json.dumps(rec,ensure_ascii=False),
         'benchmark_gold':'NOT_AVAILABLE','scientific_accuracy':'NOT_EVALUATED'}

def build_query():
    graphs={model:Graph().parse(RES/f'P3_{model}.ttl',format='turtle') for model in ('M1','M2','M3')}
    assert tuple(len(graphs[m]) for m in ('M1','M2','M3'))==(207,1501,2733)
    cases=[{'case_id':x[0],'category':x[1],'question':x[2],'subject_id':x[3],
            'predicate':x[4],'object_id':x[5],'rule':x[6],'reviewer1':'','reviewer2':'',
            'adjudicated_answer':'','gold_reference':'','case_status':'DEVELOPMENT_ONLY'} for x in CASE_SPECS]
    writecsv(RES/'P3_V05_CQ_DEVELOPMENT_8.csv',cases)
    out=[answer_case(graphs[model],model,c) for c in CASE_SPECS for model in ('M1','M2','M3')]
    writecsv(RES/'P3_V05_ENGINE_OUTPUTS_24.csv',out)
    # Cardinality verified independently from graph, not just original table strings.
    m1_c=next(r for r in out if r['model']=='M1' and r['case_id']=='CQD06')
    m2_c=next(r for r in out if r['model']=='M2' and r['case_id']=='CQD06')
    m3_c=next(r for r in out if r['model']=='M3' and r['case_id']=='CQD06')
    assert m1_c['edge_count']<m2_c['edge_count'] and m2_c['edge_count']==m3_c['edge_count']
    # Structural coverage is not answer accuracy. No adjudicated gold.
    summary={'source_snapshot':'P3_V3_208_LOCKED.csv','source_sha256':sha(DATA/'P3_V3_208_LOCKED.csv'),
      'cases':len(cases),'model_case_runs':len(out),'rdf_triple_counts':{m:len(g) for m,g in graphs.items()},
      'm1_platelet_spo_count':m1_c['edge_count'],'m2_platelet_assertion_count':m2_c['edge_count'],
      'm3_platelet_assertion_count':m3_c['edge_count'],
      'comparison_endpoint':'REPRESENTATION_DIAGNOSTIC_ONLY','expert_gold':'NOT_DONE',
      'shacl_status':'NOT_RUN_DEPENDENCY_UNAVAILABLE','accuracy':'NOT_EVALUATED'}
    jwrite(RES/'P3_V05_QUERY_SUMMARY.json',summary)
    return summary

def main():
    p2=build_evidence();p3=build_query()
    jwrite(RES/'NEXT_STAGE_BUILD_REPORT.json',{'paper2':p2,'paper3':p3})
    print(json.dumps({'p2':p2['counts'],'p3':{'cases':p3['cases'],'records':p3['model_case_runs'],
         'platelet':(p3['m1_platelet_spo_count'],p3['m2_platelet_assertion_count'],p3['m3_platelet_assertion_count'])}},indent=2))
if __name__=='__main__':main()