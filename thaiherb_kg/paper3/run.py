"""Paper 3: real-source assertion inventory, RDF projection and independent-review queue.

Structural CSV checks are NOT a substitute for SHACL Core nor scientific verification.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import quote
import json,csv,hashlib
from rdflib import Graph,Namespace,URIRef,Literal,RDF
from shared import load_json,write_csv
ROOT=Path(__file__).resolve().parents[1]
EX=Namespace('https://example.org/thaiherb/ontology/')
PROV=Namespace('http://www.w3.org/ns/prov#')

def run():
    d=load_json(ROOT/'data/paper3_ui_subset.json');records=d['assertions']; sources=d['sources']
    ids=[r['assertion_id'] for r in records]
    assert len(ids)==208 and len(ids)==len(set(ids))
    missing=[];typecounts=Counter();channelcounts=Counter();g=Graph();g.bind('ex',EX);g.bind('prov',PROV)
    for r in records:
        aid=r['assertion_id'];typ=r['assertion_type'];channel=r['channel']
        typecounts[typ]+=1;channelcounts[channel]+=1
        errors=[]
        for key in ['assertion_id','assertion_type','subject_id','source_id']:
            if not (r.get(key) or '').strip():errors.append('missing_'+key)
        if not r.get('object_id'):errors.append('missing_canonical_object_id')
        if r.get('source_id') not in sources:errors.append('unresolved_source')
        if 'compound-specific table/page locator not uniformly harmonized' in r.get('source_locator_or_context',''):
            errors.append('non_specific_source_locator')
        for err in errors: missing.append({'assertion_id':aid,'channel':channel,'issue':err,'source_id':r.get('source_id','')})
        # Do not synthesize object IDs: unresolvable assertions remain pending RDF export.
        if not r.get('object_id') or not r.get('subject_id') or r.get('source_id') not in sources:
            continue
        a=EX['assertion/'+aid]
        g.add((a,RDF.type,EX.EvidenceAssertion));g.add((a,EX.subject,EX['entity/'+quote(r['subject_id'],safe='')]))
        g.add((a,EX.predicate,EX['predicate/'+quote(r['predicate_or_topic'],safe='')]))
        g.add((a,EX.object,EX['entity/'+quote(r['object_id'],safe='')]))
        g.add((a,PROV.wasDerivedFrom,EX['source/'+r['source_id']]))
        if typ=='PharmacologyTargetAssertion':
            g.add((a,RDF.type,EX.PharmacologyTargetAssertion))
            g.add((a,EX.hasTarget,EX['entity/'+quote(r['object_id'],safe='')]))
            g.add((a,EX.directness,Literal(r.get('directness_or_direction',''))))
        if typ=='ChemistryOccurrenceAssertion':
            # We only know the herb identity, not an independently verified plant material.
            # Do not assert ex:plantMaterial without a material canonical ID.
            pass
        g.add((a,EX.assertionType,Literal(typ)))
        g.add((a,EX.sourceLocator,Literal(r.get('source_locator_or_context',''))))
    write_csv(ROOT/'paper3/curation_issues.csv',missing)
    g.serialize(destination=str(ROOT/'paper3/v3_201assertions_provenance.ttl'),format='turtle')
    queue=[]
    for item in d['discordance']:
        queue.append({'set_id':item['id'],'topic':item['title'],'assertion_ids':';'.join(item['assertionIds']),
         'reviewer_1':'','reviewer_2':'','review_decision':'','context_difference':'',
         'source_verification':'PENDING','adjudication_notes':''})
    write_csv(ROOT/'paper3/contradiction_review_queue.csv',queue)
    questions=[
        ('CQ01','botanical identity','Is the herb identified to an accepted taxon?'),
        ('CQ02','formula version','Which frozen formula version supports a membership?'),
        ('CQ03','chemistry source','What is the source and plant material for a compound occurrence?'),
        ('CQ04','pharmacology','Is a target effect direct, functional or inferred?'),
        ('CQ05','clinical context','Are outcomes and study populations comparable?'),
        ('CQ06','discordance','Is a disagreement a true contradiction or assay-context difference?'),
        ('CQ07','missing evidence','Does missing curated evidence imply biological absence?'),
        ('CQ08','provenance','Can a graph answer be traced to the original publication?')]
    write_csv(ROOT/'paper3/blinded_benchmark_template.csv',[
      {'cq_id':q,'category':c,'question_template':s,'case_id':'','expected_answer':'',
       'reference_source_id':'','expert_1':'','expert_2':'','adjudicated':'','split':'UNASSIGNED'} for q,c,s in questions])
    # No fabricated expert scores or compound target validation.
    summary={'assertions_total':len(records),'assertion_types':dict(typecounts),
       'channels':dict(channelcounts),'source_registry_ids':len(sources),
       'rdf_exported_assertions':len(set(str(s) for s in g.subjects(RDF.type,EX.EvidenceAssertion))),
       'rdf_triples':len(g),'curation_issues':dict(Counter(x['issue'] for x in missing)),
       'candidate_discordance_sets':len(queue),
       'SHACL':'NOT RUN in this Python environment unless pyshacl separately installed',
       'note':'RDF ontology namespace is a local MVP placeholder, not an externally ratified ontology. No independent expert evaluation.'}
    (ROOT/'paper3/results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary
if __name__=='__main__':print(json.dumps(run(),indent=2))
