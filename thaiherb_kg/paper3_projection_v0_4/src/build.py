"""ThaiHerb P2 v0.6 / P3 v0.4 controlled evidence and projection rebuild.

All checked labels are narrow, source-anchored literature checks. No expert gold.
"""
from __future__ import annotations
import csv
import hashlib
import html
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, URIRef, Literal, Namespace, RDF
from rdflib.namespace import DCTERMS, PROV, XSD

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
TH = Namespace("urn:thaiherb:v04:")
SH = Namespace("http://www.w3.org/ns/shacl#")


def read_csv(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else [])
    with (OUT/name).open("w", encoding="utf-8-sig", newline="") as f:
        w=csv.DictWriter(f, fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def write_json(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


# Evidence directly inspected at original (open-access) article, Table 3 (last species column).
# IMPORTANT: units are piperine equivalents per g methanolic extract, not pure analyte mass.
CHECKED_PIPER = {
    "CA006": ("piperine", "93.86 ± 0.13"),
    "CA007": ("pellitorine", "206.95 ± 0.22"),
    "CA008": ("piperlongumine", "14.19 ± 0.14"),
    "CA009": ("piperolein B", "2.70 ± 0.01"),
    "CA010": ("guineensine", "29.73 ± 0.05"),
}
DOI = "https://doi.org/10.3390/antiox10101642"
PMC = "https://pmc.ncbi.nlm.nih.gov/articles/PMC8533580/"
CHECK_DATE="2026-11-07"


def build_p2():
    base=read_csv("P2_CHEM_EVIDENCE_100_v05_LOCKED.csv")
    assert len(base)==100 and len({x['assertion_id'] for x in base})==100
    checked=[]; audit=[]
    for r in base:
        d=dict(r)
        d.update({
            "evidence_review_date": CHECK_DATE if d['assertion_id'] in CHECKED_PIPER else "",
            "source_exact_locator_verified": "",
            "reported_quantity_exact_source": "",
            "quantity_unit": "",
            "source_material_verified": "",
            "extraction_verified": "",
            "verification_scope": "NOT_VERIFIED",
            "source_access_url": "",
            "review_procedure": "AI_ASSISTED_SOURCE_TEXT_INSPECTION" if d['assertion_id'] in CHECKED_PIPER else "NOT_REVIEWED_CLAIM_SPECIFIC",
            "claim_review_note": ""
        })
        if d['assertion_id'] in CHECKED_PIPER:
            label, amount=CHECKED_PIPER[d['assertion_id']]
            assert d['source_id']=="SRC_RETRO" and d['compound_label'].casefold()==label.casefold()
            d['disposition']="PRIMARY_FULLTEXT_MATCH"
            d['source_publication_status']="OPEN_ACCESS_PRIMARY_ANALYTICAL_ARTICLE_REVIEWED"
            d['source_type']="primary analytical study of Piper species"
            d['primary_vs_secondary']="PRIMARY_ANALYTICAL_MEASUREMENT"
            d['fulltext_claim_locator']="Section 3.1, Table 3, final column (Piper retrofractum)"
            d['plant_part']="dried fruit (peppercorn)"
            d['preparation']="methanolic fruit extract"
            d['extraction_method']="methanol; LC-HRMS/MS and LC-DAD profile"
            d['assay']="LC-DAD piperamide quantification (piperine equivalents)"
            d['reported_quantity']=amount
            d['DOI_or_PMID_claim_verified']="DOI_AND_TABLE_3_TEXT_CHECKED"
            d['reason']="Table 3 explicitly reports named analyte under P. retrofractum; compound structure/CID not independently reconciled. Single-curator AI-assisted source read."
            d['source_exact_locator_verified']="Luca et al. (2021), Antioxidants 10(10),1642, Section 3.1/Table 3, P. retrofractum column"
            d['reported_quantity_exact_source']=amount
            d['quantity_unit']="mg PE/g extract (piperine equivalents, not analyte mass)"
            d['source_material_verified']="Piper retrofractum Vahl, dried fruits"
            d['extraction_verified']="methanolic fruit extract"
            d['verification_scope']="NAMED_COMPOUND_IN_EXTRACT_TABLE; NOT_CANONICAL_STRUCTURE_OR_BIOLOGICAL_VALIDITY"
            d['source_access_url']=PMC
            d['claim_review_note']="PE denotes piperine equivalents; not a whole-fruit concentration. Do not infer that all preparations contain the same amount."
            checked.append(d)
        elif d['source_id']=="SRC_CURCUMA":
            d['claim_review_note']="Species/context sensitive: genus-level Curcuma essential-oil review does not by itself verify this exact species/compound pairing."
        audit.append(d)
    assert len(checked)==5
    fields=list(audit[0]);write_csv('P2_CHEM_EVIDENCE_100_v06.csv',audit,fields)
    write_csv('P2_PRIMARY_ANALYTICAL_MATCHES_5.csv', checked,fields)
    write_csv('P2_CHEM_UNRESOLVED_95.csv',[r for r in audit if r['disposition']!='PRIMARY_FULLTEXT_MATCH'],fields)
    r=read_csv('P2_SOURCE_REGISTRY_v05_LOCKED.csv')
    for s in r:
        s['literature_review_20261107']='NOT_REVIEWED_IN_THIS_STAGE'
        s['literature_review_scope']=''
        if s['source_id']=='SRC_RETRO':
            s['literature_review_20261107']='SOURCE_ARTICLE_AND_5_COMPOUNDS_TABLE_3_CHECKED'
            s['literature_review_scope']='primary measurement in methanolic dried fruit extract only; not biological validity'
        elif s['source_id']=='SRC_GINGER':
            s['literature_review_20261107']='BIBLIOGRAPHIC_METADATA_CHECKED'
            s['literature_review_scope']='Mao et al., Foods 2019, 8(6),185; review, not yet 5 individual claims'
        elif s['source_id']=='SRC_CHEBULA':
            s['literature_review_20261107']='BIBLIOGRAPHIC_METADATA_CHECKED'
            s['literature_review_scope']='Wang et al., Molecules 2024,29(23),5547; fruit-focused review, not 5 individual claims'
        elif s['source_id']=='SRC_CURCUMA':
            s['literature_review_20261107']='BIBLIOGRAPHIC_METADATA_CHECKED_CONTEXT_ALERT'
            s['literature_review_scope']='Dosoky & Setzer 2018 Curcuma species essential oil review; exact species/analyte context unresolved'
    write_csv('P2_SOURCE_REGISTRY_V06.csv',r)
    write_csv('P2_SPECIES_CONTEXT_REVIEW_QUEUE.csv',[{
        'assertion_id':x['assertion_id'],'herb_scientific_name':x['herb_scientific_name'],
        'compound':x['compound_label'],'source_id':x['source_id'],
        'issue':'Genus-level Curcuma oil review; target-species occurrence must be confirmed with exact table/line',
        'status':'OPEN_ISSUE_NOT_DISPROVED','doi':x['source_url_from_archive']
    } for x in audit if x['source_id']=='SRC_CURCUMA'])
    write_json('P2_CHEM_REVIEW_SUMMARY.json',{'frozen_rows':100,'primary_analytical_claims_source_reviewed':5,'claim_unverified_remaining':95,
        'source_checked':DOI,'fulltext_locator':'Table 3 / P. retrofractum column','reviewer_type':'AI-assisted single-curator','independent_adjudication':'NOT_DONE',
        'structural_canonicalization':'NOT_VERIFIED', 'external_corpus':'NOT_VALIDATED'})


def urn_id(value):
    # Protect original text (including spaces) as a URI path component. NEVER call this an external canonical ID.
    return URIRef(str(TH)+"entity:"+quote(value,safe=''))

def source_uri(value):return URIRef(str(TH)+"source:"+quote(value,safe=''))
def assert_uri(value):return URIRef(str(TH)+"assertion:"+quote(value,safe=''))


def build_models(rows):
    graphs={m:Graph() for m in ['M1','M2','M3']}
    for name,g in graphs.items():
        g.bind('th',TH);g.bind('prov',PROV);g.bind('dct',DCTERMS)
    proj=[]
    for r in rows:
        rid=r['assertion_id']; assert rid and r['subject_id']
        s=urn_id(r['subject_id']); o=(urn_id(r['object_id']) if r['object_id'] else Literal(r['object_label']))
        p=URIRef(str(TH)+'relation:'+quote(r['predicate_or_topic'],safe=''))
        if not r['object_id'] and not r['object_label']: raise ValueError('No object content for '+rid)
        # M1: naive SPO; evidence assertion ID is carried in an audit sidecar because RDF triples may collapse duplicates.
        graphs['M1'].add((s,p,o))
        for m in ['M2','M3']:
            g=graphs[m];a=assert_uri(rid)
            g.add((a,RDF.type,TH.EvidenceAssertion))
            g.add((a,DCTERMS.identifier,Literal(rid)))
            g.add((a,TH.subject,s))
            g.add((a,TH.predicate,p))
            g.add((a,TH.object,o))
            g.add((a,TH.channel,Literal(r['channel'])))
            g.add((a,PROV.wasDerivedFrom,source_uri(r['source_id'])))
            g.add((source_uri(r['source_id']),RDF.type,TH.SourceDocument))
        gm=graphs['M3']; a=assert_uri(rid)
        gm.add((a,TH.evidenceMode,Literal(r['evidence_mode'])))
        gm.add((a,TH.directness,Literal(r['directness_or_direction'])))
        gm.add((a,TH.originalStatus,Literal(r['assertion_status'])))
        gm.add((a,TH.objectLabel,Literal(r['object_label'])))
        if r['source_locator_or_context']:
            gm.add((a,TH.contextText,Literal(r['source_locator_or_context'])))
        if r['limitation_or_finding']:
            gm.add((a,TH.limitationText,Literal(r['limitation_or_finding'])))
        if not r['object_id']:
            gm.add((a,TH.uncanonicalizedObject,Literal(True,datatype=XSD.boolean)))
        proj.append({'assertion_id':rid,'channel':r['channel'],'source_id':r['source_id'],
            'M1_relation':str(p),'M1_subject':str(s),'M1_object':str(o),'M2_assertion':str(a),
            'M3_context_structured':'NO','M3_context_text_available':'YES' if r['source_locator_or_context'] else 'NO',
            'M3_material_id':'NOT_NORMALIZED',
            'M3_qualification_type':'SOURCE_TEXT_ONLY; NO_CLAIM_OF_NORMALIZED_ASSAY'})
    for m,g in graphs.items():
        g.serialize(OUT/f'P3_{m}.ttl',format='turtle')
    write_csv('P3_PROJECTION_PARITY_208.csv',proj)
    return graphs


def answer_row(r, model):
    # Controlled lookup by assertion ID, no natural-language matching and no gold label visibility.
    item={'model':model,'assertion_id':r['assertion_id'],'channel':r['channel'],'subject':r['subject_id'],
          'relation':r['predicate_or_topic'],'object':r['object_label'] or r['object_id'],
          'source_id':'','evidence_qualifiers':'','status':'ASSERTION_RENDERED','reason':'', 'validated_answer':'NO'}
    if model in ['M2','M3']:
        item['source_id']=r['source_id']
    if model=='M3':
        item['evidence_qualifiers']=r['directness_or_direction']+' | '+r['evidence_mode']
        if not r['object_id']:
            item['status']='OBJECT_ID_UNRESOLVED'
            item['reason']='Unresolved canonical object; source text preserved, not clinical adjudication'
        elif r['channel']=='chemistry':
            item['status']='ASSERTION_UNVERIFIED_IN_PROJECTION'
            item['reason']='Historical label not automatically promoted by Paper 2 pilot audit'
        elif r['channel']=='pharmacology_target' and r['directness_or_direction']!='direct_compound_target':
            item['status']='FUNCTIONAL_OR_PREPARATION_QUALIFIED'
            item['reason']='Not interpreted as direct compound-protein binding'
    return item


def build_p3():
    rows=read_csv('P3_V3_208_LOCKED.csv')
    counts=dict(Counter(r['channel'] for r in rows))
    assert len(rows)==208 and len({r['assertion_id'] for r in rows})==208
    assert counts=={'formula':71,'chemistry':100,'pharmacology_target':30,'clinical':7}
    graphs=build_models(rows)
    all_output=[answer_row(r,model) for model in ['M1','M2','M3'] for r in rows]
    write_csv('P3_ALL_ASSERTIONS_MODEL_RENDERED_624.csv', all_output)
    write_csv('P3_ASSERTION_PROJECTION_IDS.csv',[{'assertion_id':r['assertion_id'],
        'M1_original_source_id_audit_sidecar':r['source_id'],
        'M1_has_source_in_RDF':'NO', 'M2_has_source_in_RDF':'YES', 'M3_has_source_in_RDF':'YES',
        'input_version':'P3-V3-legacy-208'} for r in rows])
    summary={'baseline':'P3-V3-legacy-208','rows':len(rows),'by_channel':counts,
             'rdf_triples':{x:len(g) for x,g in graphs.items()},
             'identical_input_assertions':True,'qualifications':'M3 source text/directness only; material/preparation not normalized',
             'gold_expert_adjudicated':'NOT_DONE','benchmark_comparison':'NOT_RUN'}
    write_json('P3_PROJECTION_SUMMARY.json',summary)
    # One held-out-template item for each prespecified CQ category; reviewers fill all gold fields independently.
    categories=['taxonomy','plant_material_preparation','formula_version','compound_occurrence',
                'pharmacology_directness','clinical_population_regimen','context_discordance',
                'unknown_safety_regulatory_uncertainty']
    cqs=[{'case_id':f'CQ_TEMPLATE_{i+1:02d}','category':cat,'question':'',
          'eligible_assertion_ids':'','source_disjoint_group':'','allowed_sources':'',
          'expected_answer':'','justified_abstention_category':'',
          'reviewer_1':'','reviewer_2':'','adjudicator':'',
          'status':'AWAITING_INDEPENDENT_HUMAN_CASE_AUTHORING'} for i,cat in enumerate(categories)]
    write_csv('P3_CQ_BLINDED_BENCHMARK_TEMPLATE.csv',cqs)
    write_csv('P3_EXPERIMENTAL_QUERY_DEVELOPMENT_ONLY.csv',[{'assertion_id':r['assertion_id'],
       'query':'Look up assertion ID '+r['assertion_id'],'input_version':'P3-V3-legacy-208',
       'usage':'DEVELOPMENT_SMOKE_ONLY_NO_GOLD', 'answer_m1':(r['subject_id']+' '+r['predicate_or_topic']+' '+(r['object_label'] or r['object_id'])),
       'answer_m2_source':r['source_id'],'answer_m3_qualifier':r['directness_or_direction']}
       for r in rows[:8]])
    return summary


def test_custom_structure(g):
    """Not pySHACL: narrow source-edge/IRI checks for regression and seeded defects only."""
    ids=set(g.subjects(RDF.type,TH.EvidenceAssertion))
    issues=[]
    for a in ids:
        for predicate,label in [(TH.subject,'subject'),(TH.predicate,'predicate'),(TH.object,'object'),(PROV.wasDerivedFrom,'source')]:
            values=list(g.objects(a,predicate))
            if len(values)!=1:issues.append((str(a),label,len(values)))
            if values and label in ('source','subject') and not isinstance(values[0],URIRef):issues.append((str(a),label,'not_iri'))
        for src in g.objects(a,PROV.wasDerivedFrom):
            if (src,RDF.type,TH.SourceDocument) not in g:issues.append((str(a),'source_class_missing',str(src)))
    return issues


def build_semantic_controls(g):
    """Add explicit semantic safeguards; these are not SHACL Core validations."""
    original=list(g.subjects(RDF.type,TH.EvidenceAssertion))
    assert len(original)==208
    a=original[0]
    missing=Graph();missing+=g
    src=next(missing.objects(a,PROV.wasDerivedFrom));missing.remove((a,PROV.wasDerivedFrom,src))
    duplicate=Graph();duplicate+=g
    duplicate.add((a,TH.object,Literal('INJECTED_BAD_OBJECT')))
    wrong=Graph();wrong+=g
    wrong.remove((src,RDF.type,TH.SourceDocument))
    checks=[('authentic',0,len(test_custom_structure(g))),
            ('missing_provenance',1,len(test_custom_structure(missing))),
            ('double_object',1,len(test_custom_structure(duplicate))),
            ('wrong_source_type',1,len(test_custom_structure(wrong)))]
    results=[{'fixture':label,'expected_finding_min':n,'observed_findings':count,
              'pass':count>=n if n else count==0,'engine':'CUSTOM_STRUCTURAL_CHECK_NOT_PYSHACL'} for label,n,count in checks]
    write_csv('P3_CUSTOM_NEGATIVE_CONTROLS.csv',results)
    # These negative controls are semantic policy checks, NOT proven violations in authentic corpus.
    write_csv('P3_SEMANTIC_NEGATIVE_CONTROLS.csv',[
        {'control':'functional_claim_must_not_become_direct_binding','input':'functional_target_association','expected':'KEEP_FUNCTIONAL','status':'RULE_DECLARED_NOT_EXPERT_VALIDATION'},
        {'control':'gall_must_not_be_equivalent_to_fruit','input':'Terminalia chebula gall/fruit','expected':'DISTINCT_MATERIAL_IDENTITIES','status':'RULE_DECLARED_NOT_PROVEN_FOR_ALL_INGREDIENTS'},
        {'control':'essential_oil_review_must_not_be_mapped_to_all_species','input':'Curcuma essential oils article','expected':'VERIFY_SPECIES_SPECIFIC_TABLE_ROW','status':'RULE_DECLARED'},
        {'control':'clinical_text_object_must_not_be_assigned_fake_iri','input':'7 V3 clinical assertions','expected':'PRESERVE_ORIGINAL_TEXT_AND_FLAG_UNMAPPED','status':'RULE_DECLARED'}])
    return results


def make_shacl_shapes():
    text='''@prefix th: <urn:thaiherb:v04:> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dct: <http://purl.org/dc/terms/> .

th:EvidenceAssertionShape a sh:NodeShape ;
  sh:targetClass th:EvidenceAssertion ;
  sh:property [ sh:path dct:identifier ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:Literal ] ;
  sh:property [ sh:path th:subject ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI ] ;
  sh:property [ sh:path th:predicate ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI ] ;
  sh:property [ sh:path th:object ; sh:minCount 1 ; sh:maxCount 1 ] ;
  sh:property [ sh:path th:channel ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:Literal ] ;
  sh:property [ sh:path prov:wasDerivedFrom ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI ; sh:class th:SourceDocument ] .
'''
    (OUT/'P3_SHACL_CORE_SHAPES_V04.ttl').write_text(text,encoding='utf8')
    Graph().parse(data=text,format='turtle')


def run_shacl_if_available():
    import importlib.util, sys
    shapes=OUT/'P3_SHACL_CORE_SHAPES_V04.ttl';graph=OUT/'P3_M3.ttl'
    if not importlib.util.find_spec('pyshacl'):
        value={'status':'NOT_RUN_DEPENDENCY_UNAVAILABLE','dependency':'pyshacl','python':sys.version.split()[0],
               'graph':graph.name,'shape_file':shapes.name,'claim_of_conformance':False,
               'install_instruction':'pip install pyshacl>=0.31,<0.41 then python src/validate_shacl.py'}
    else:
        from pyshacl import validate
        conform,report,verbose=validate(data_graph=str(graph),shacl_graph=str(shapes),inference='none',advanced=False,meta_shacl=False)
        report.serialize(destination=str(OUT/'P3_SHACL_CORE_REPORT.ttl'),format='turtle')
        value={'status':'PASS' if conform else 'FAIL','conforms':bool(conform),'dependency':'pyshacl','report':'P3_SHACL_CORE_REPORT.ttl','summary':str(verbose)}
    write_json('P3_SHACL_RUNTIME_STATUS.json',value)
    return value


def make_dashboard(title, data_file, out_file, intro):
    rows=json.loads((OUT/data_file).read_text(encoding='utf8')) if data_file.endswith('.json') else None
    if rows is None:
        with (OUT/data_file).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    payload=json.dumps(rows,ensure_ascii=False).replace('</','<\\/')
    columns=list(rows[0]) if rows else []
    # Functional offline filter, table rendering, and pagination; no external dependencies.
    doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+'''</title><style>
body{margin:0;background:#f8f9fc;color:#172538;font-family:system-ui,Segoe UI,sans-serif}header{background:#102b4e;color:white;padding:28px max(18px,5vw)}header p{color:#d5e4ee;max-width:950px;line-height:1.6}main{margin:25px auto;max-width:1400px;padding:0 16px}.panel{padding:18px;background:white;border:1px solid #dae3ee;border-radius:12px;margin:12px 0}.panel input{width:100%;max-width:560px;padding:12px;font-size:1rem;border-radius:8px;border:1px solid #a7b7c9}table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:9px 10px;vertical-align:top;text-align:left;border-bottom:1px solid #e6ebf1;max-width:300px;overflow-wrap:anywhere}th{background:#e9f0f9;position:sticky;top:0}#wrap{overflow:auto;max-height:74vh}small{color:#536b82}button{background:#102b4e;color:white;padding:8px 12px;border:0;border-radius:7px;cursor:pointer;margin-right:8px}button:disabled{opacity:.4}#count{margin:12px 0}span.notice{font-weight:600;color:#a14c10}</style></head><body><header><h1>'''+html.escape(title)+'''</h1><p>'''+html.escape(intro)+'''</p></header><main><div class="panel"><label for="filter">Search evidence, assertion IDs, and source metadata</label><p><input id="filter" placeholder="Type to filter all columns" autocomplete="off"></p><p class="notice">Research audit only; not clinical or regulatory advice. Search results are not gold-standard validation.</p><div id="count"></div><button id="prev">Previous</button><button id="next">Next</button> <small id="page"></small></div><div class="panel" id="wrap"><table><thead id="head"></thead><tbody id="body"></tbody></table></div></main>
<script>const rows='''+payload+''';const cols='''+json.dumps(columns)+''';const el=id=>document.getElementById(id);let filtered=rows,step=25,page=0;const safe=s=>String(s??'');function render(){el('head').replaceChildren();el('body').replaceChildren();const h=document.createElement('tr');cols.forEach(k=>{const c=document.createElement('th');c.textContent=k;h.appendChild(c)});el('head').appendChild(h);filtered.slice(page*step,(page+1)*step).forEach(r=>{const t=document.createElement('tr');cols.forEach(k=>{const c=document.createElement('td');c.textContent=safe(r[k]);t.appendChild(c)});el('body').appendChild(t)});el('count').textContent=filtered.length+' of '+rows.length+' records';el('page').textContent='Page '+(page+1)+' of '+Math.max(1,Math.ceil(filtered.length/step));el('prev').disabled=page===0;el('next').disabled=(page+1)*step>=filtered.length;}el('filter').addEventListener('input',()=>{let q=el('filter').value.toLowerCase().trim();filtered=rows.filter(r=>!q||cols.some(k=>safe(r[k]).toLowerCase().includes(q)));page=0;render()});el('prev').onclick=()=>{page=Math.max(0,page-1);render()};el('next').onclick=()=>{page++;render()};render();</script></body></html>'''
    (ROOT/'dashboard'/out_file).write_text(doc,encoding='utf-8')


def main():
    build_p2()
    p3=build_p3()
    make_shacl_shapes()
    model=Graph().parse(OUT/'P3_M3.ttl',format='turtle')
    negative=build_semantic_controls(model)
    shacl=run_shacl_if_available()
    make_dashboard('Paper 2 v0.6 | Compound-Level Source Review','P2_CHEM_EVIDENCE_100_v06.csv','Paper2_ClaimAudit_v0.6.html',
       '100 original research assertions; five analytically source-matched from Piper retrofractum; 95 remain unverified. No expert gold labels.')
    make_dashboard('Paper 3 v0.4 | M1, M2, M3 Source-Parity Explorer','P3_ALL_ASSERTIONS_MODEL_RENDERED_624.csv','Paper3_M1M2M3_v0.4.html',
       'Same frozen 208 V3 assertions for each of three representation projections. Output is a rendering smoke test, not question-answer benchmark accuracy.')
    write_json('BUILD_REPORT.json',{'date':'2026-11-07','p2_verified':5,'p2_pending':95,'p3':p3,
       'custom_controls':negative,'shacl':shacl})
    print(json.dumps({'p2':{'checked':5,'unverified':95},'p3':p3,'shacl':shacl['status']},indent=2))

if __name__=='__main__':main()

