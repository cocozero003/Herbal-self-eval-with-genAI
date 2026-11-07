"""Run the real pySHACL engine on frozen 208-assertion M3 graph.

Fails closed if pySHACL unavailable. Emits actual RDF validation report and
negative controls. A shape-conformant graph does not imply scientific truth.
"""
from __future__ import annotations
import copy
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DCTERMS

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUTPUT=ROOT/'results'
OUTPUT.mkdir(parents=True, exist_ok=True)
SHACL=Namespace('http://www.w3.org/ns/shacl#')
TH=Namespace('urn:thaiherb:v04:')
PROV=Namespace('http://www.w3.org/ns/prov#')


def _write_json(name,data):
    (OUTPUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')

def run():
    try:
        from pyshacl import validate
        ver=importlib.metadata.version('pyshacl')
    except (ImportError,importlib.metadata.PackageNotFoundError) as err:
        _write_json('P3_PYSHACL_CORE_RUNTIME.json',{'status':'NOT_RUN_MISSING_PYSHACL','error':str(err),'environment':platform.platform()})
        raise SystemExit('Cannot declare SHACL Core conformance: pySHACL not installed')
    dataset=DATA/'P3_M3.ttl'
    shapes=DATA/'P3_SHACL_CORE_SHAPES_V04.ttl'
    graph=Graph().parse(dataset,format='turtle')
    shape_graph=Graph().parse(shapes,format='turtle')
    assert len(graph)==2733,(len(graph),'Unexpected frozen model')
    assert len(list(graph.subjects(RDF.type,TH.EvidenceAssertion)))==208
    kwargs={'shacl_graph':shape_graph,'inference':'none','advanced':False,
            'meta_shacl':False,'abort_on_first':False,
            'allow_warnings':False,'allow_infos':False,'debug':False}
    conforms,report,text=validate(graph,**kwargs)
    if hasattr(report,'serialize'):
        report.serialize(OUTPUT/'P3_PYSHACL_REAL_REPORT.ttl',format='turtle')
    (OUTPUT/'P3_PYSHACL_REAL_REPORT.txt').write_text(text,encoding='utf-8')
    assertions=sorted(set(graph.subjects(RDF.type,TH.EvidenceAssertion)),key=str)
    target=assertions[0]
    valid_predicates=[DCTERMS.identifier,TH.subject,TH.predicate,TH.object,TH.channel,PROV.wasDerivedFrom]
    assert all(any(graph.objects(target,p)) for p in valid_predicates)
    firstsource=next(graph.objects(target,PROV.wasDerivedFrom))
    assert (firstsource,RDF.type,TH.SourceDocument) in graph
    tests=[]
    def mutate_and_check(case,func):
        mutated=Graph()
        for statement in graph:mutated.add(statement)
        func(mutated)
        res,_,detail=validate(mutated,**kwargs)
        tests.append({'case_id':case,'expected_conforms':False,'actual_conforms':bool(res),
                      'detected':not bool(res),'report_preview':detail[:160]})
        if bool(res):raise AssertionError('SHACL did not detect: '+case)
    def remove_prop(g,p):
        for obj in list(g.objects(target,p)): g.remove((target,p,obj))
    mutate_and_check('MISSING_IDENTIFIER',lambda g:remove_prop(g,DCTERMS.identifier))
    mutate_and_check('MISSING_SUBJECT',lambda g:remove_prop(g,TH.subject))
    mutate_and_check('MISSING_PREDICATE',lambda g:remove_prop(g,TH.predicate))
    mutate_and_check('MISSING_OBJECT',lambda g:remove_prop(g,TH.object))
    mutate_and_check('MISSING_CHANNEL',lambda g:remove_prop(g,TH.channel))
    mutate_and_check('MISSING_PROVENANCE',lambda g:remove_prop(g,PROV.wasDerivedFrom))
    def wrong_subject(g):
        remove_prop(g,TH.subject);g.add((target,TH.subject,Literal('not an IRI')))
    mutate_and_check('WRONG_SUBJECT_NODE_KIND',wrong_subject)
    def wrong_source(g):
        remove_prop(g,PROV.wasDerivedFrom);g.add((target,PROV.wasDerivedFrom,Literal('bad source')))
    mutate_and_check('WRONG_PROVENANCE_NODE_KIND',wrong_source)
    def source_untyped(g):
        g.remove((firstsource,RDF.type,TH.SourceDocument))
    mutate_and_check('SOURCE_CLASS_MISSING',source_untyped)
    def excess_id(g):
        g.add((target,DCTERMS.identifier,Literal('another identifier')))
    mutate_and_check('DUPLICATE_IDENTIFIER',excess_id)
    result={
        'status':'PASS' if conforms and all(x['detected'] for x in tests) else 'FAIL',
        'engine':'pyshacl','engine_version':ver,'rdflib_version':importlib.metadata.version('rdflib'),
        'python_version':platform.python_version(),'runner':os.getenv('GITHUB_ACTIONS','local'),
        'baseline_conforms':bool(conforms),'actual_violations':len(list(report.subjects(RDF.type,SHACL.ValidationResult))) if hasattr(report,'subjects') else None,
        'original_v3_assertions':208,'m3_triples':len(graph),'shapes_count':len(shape_graph),
        'data_sha256':hashlib.sha256(dataset.read_bytes()).hexdigest(),
        'shapes_sha256':hashlib.sha256(shapes.read_bytes()).hexdigest(),
        'negative_controls_total':len(tests),'negative_controls_detected':sum(x['detected'] for x in tests),
        'semantics':'Structural SHACL Core for project profile only, not chemical, clinical, or external validity.'}
    _write_json('P3_PYSHACL_CORE_RUNTIME.json',result)
    with (OUTPUT/'P3_PYSHACL_REAL_NEGATIVE_CONTROLS.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(tests[0]));writer.writeheader();writer.writerows(tests)
    print(json.dumps(result,indent=2))
    if result['status']!='PASS':raise SystemExit(1)
    return result

if __name__=='__main__':run()
