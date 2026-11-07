"""Run actual SHACL Core including seeded negative controls.

This script refuses to claim conformance when pyshacl is unavailable. It does not
assess botanical, chemical, or clinical truth: SHACL is structural validation.
"""
from pathlib import Path
import csv
import json
import sys
from rdflib import Graph, RDF, Literal, Namespace
from rdflib.namespace import PROV

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
TH=Namespace('urn:thaiherb:v04:')
try:
    import pyshacl
    from pyshacl import validate
except ImportError:
    status={'status':'NOT_RUN_DEPENDENCY_UNAVAILABLE','reason':'pyshacl not installed','claim_of_conformance':False}
    (OUT/'P3_SHACL_RUNTIME_STATUS.json').write_text(json.dumps(status,indent=2))
    print(json.dumps(status))
    sys.exit(2)

shapes=Graph().parse(OUT/'P3_SHACL_CORE_SHAPES_V04.ttl',format='turtle')
graph=Graph().parse(OUT/'P3_M3.ttl',format='turtle')

def validate_graph(data):
    return validate(data_graph=data,shacl_graph=shapes,inference='none',advanced=False,
                    meta_shacl=False,abort_on_first=False)

conforms,report,report_text=validate_graph(graph)
report.serialize(destination=str(OUT/'P3_SHACL_CORE_REPORT.ttl'),format='turtle')
a=next(graph.subjects(RDF.type,TH.EvidenceAssertion))
src=next(graph.objects(a,PROV.wasDerivedFrom))
fixtures=[]

missing=Graph();missing+=graph;missing.remove((a,PROV.wasDerivedFrom,src))
fixtures.append(('missing_provenance_edge',missing))
double=Graph();double+=graph;double.add((a,TH.object,Literal('INJECTED_OTHER_OBJECT')))
fixtures.append(('double_object_cardinality',double))
wrong=Graph();wrong+=graph;wrong.remove((src,RDF.type,TH.SourceDocument))
fixtures.append(('untyped_source_document',wrong))
no_subject=Graph();no_subject+=graph
subject=next(no_subject.objects(a,TH.subject));no_subject.remove((a,TH.subject,subject))
fixtures.append(('missing_subject',no_subject))

out=[]
for name,data in fixtures:
    valid,report_graph,detail=validate_graph(data)
    out.append({'fixture':name,'expected_conforms':False,'observed_conforms':bool(valid),
                'negative_control_detected':not valid,'engine':'pyshacl','pyshacl_version':getattr(pyshacl,'__version__','UNREPORTED')})
with (OUT/'P3_SHACL_NEGATIVE_CONTROLS.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,list(out[0]));w.writeheader();w.writerows(out)
status={'status':'PASS' if conforms and all(x['negative_control_detected'] for x in out) else 'FAIL',
        'conforms':bool(conforms),'negative_controls_detected':sum(x['negative_control_detected'] for x in out),
        'negative_controls_total':len(out),'pyshacl_version':getattr(pyshacl,'__version__','UNREPORTED'),
        'report_file':'P3_SHACL_CORE_REPORT.ttl','negative_control_file':'P3_SHACL_NEGATIVE_CONTROLS.csv',
        'report_text':str(report_text), 'claim_of_scientific_validity':False}
(OUT/'P3_SHACL_RUNTIME_STATUS.json').write_text(json.dumps(status,indent=2))
print(json.dumps(status,indent=2));sys.exit(0 if status['status']=='PASS' else 1)
