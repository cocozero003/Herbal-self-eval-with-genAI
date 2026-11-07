"""Auditable local evaluation of the SHACL Core *subset* used in this project.

Supported constraints: targetClass, property/path (IRI), minCount, maxCount,
nodeKind=IRI/Literal, class (direct rdf:type). Does NOT implement SHACL Core
as a whole. The W3C SHACL standard engine gate remains NOT_RUN without
pySHACL. This module is a limited implementation for offline QA only.
"""
from __future__ import annotations
import csv
import importlib.util
import json
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal, BNode, RDF
from rdflib.namespace import DCTERMS, PROV, XSD

SH = Namespace('http://www.w3.org/ns/shacl#')
TH = Namespace('urn:thaiherb:v04:')
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'
SUPPORTED = {SH.minCount, SH.maxCount, SH.nodeKind, SH['class'], SH.path}


def inspect_shapes(shapes:Graph):
    constraints=[]
    for shape in shapes.subjects(RDF.type,SH.NodeShape):
        for target in shapes.objects(shape,SH.targetClass):
            for pshape in shapes.objects(shape,SH.property):
                paths=list(shapes.objects(pshape,SH.path))
                if len(paths)!=1 or not isinstance(paths[0],URIRef):
                    raise ValueError('Only simple IRI property paths are supported')
                unknown={pred for pred,_ in shapes.predicate_objects(pshape)}-SUPPORTED
                if unknown:raise ValueError('Unsupported SHACL constraints: '+str(unknown))
                constraints.append({
                    'targetClass':target,'sourceShape':pshape,'path':paths[0],
                    'min':next((int(x) for x in shapes.objects(pshape,SH.minCount)),None),
                    'max':next((int(x) for x in shapes.objects(pshape,SH.maxCount)),None),
                    'nodekind':next(shapes.objects(pshape,SH.nodeKind),None),
                    'class':next(shapes.objects(pshape,SH['class']),None),
                })
    if not constraints:raise ValueError('No supported shape constraints found')
    return constraints


def check(data:Graph, shapes:Graph):
    rules=inspect_shapes(shapes)
    errors=[]
    for rule in rules:
        for focus in data.subjects(RDF.type,rule['targetClass']):
            values=list(data.objects(focus,rule['path']))
            def push(component,value=None,detail=''):
                errors.append({'focus':focus,'path':rule['path'],'constraint':component,
                               'value':value,'source_shape':rule['sourceShape'],'message':detail})
            n=len(values)
            if rule['min'] is not None and n<rule['min']:
                push(SH.MinCountConstraintComponent,detail=f'Found {n}, minimum {rule["min"]}')
            if rule['max'] is not None and n>rule['max']:
                push(SH.MaxCountConstraintComponent,detail=f'Found {n}, maximum {rule["max"]}')
            for value in values:
                kind=rule['nodekind']
                if kind==SH.IRI and not isinstance(value,URIRef):
                    push(SH.NodeKindConstraintComponent,value,'Expected IRI')
                elif kind==SH.Literal and not isinstance(value,Literal):
                    push(SH.NodeKindConstraintComponent,value,'Expected literal')
                klass=rule['class']
                if klass is not None and (value,RDF.type,klass) not in data:
                    push(SH.ClassConstraintComponent,value,'Value lacks direct rdf:type '+str(klass))
    return errors


def validation_report(errors):
    # Distinctly labeled as a partial implementation; SHACL Core conformance
    # must not be attributed to this report.
    graph=Graph()
    report=BNode()
    graph.add((report,RDF.type,SH.ValidationReport))
    graph.add((report,SH.conforms,Literal(len(errors)==0,datatype=XSD.boolean)))
    graph.add((report,DCTERMS.description,Literal('Local subset checker only; not full pySHACL Core execution.')))
    for v in errors:
        result=BNode()
        for p,o in [(RDF.type,SH.ValidationResult),
                    (SH.focusNode,v['focus']),(SH.resultPath,v['path']),
                    (SH.sourceConstraintComponent,v['constraint']),
                    (SH.sourceShape,v['source_shape']),
                    (SH.resultSeverity,SH.Violation),(SH.resultMessage,Literal(v['message']))]:
            graph.add((result,p,o))
        if v['value'] is not None: graph.add((result,SH.value,v['value']))
        graph.add((report,SH.result,result))
    return graph


def mutated(data:Graph, change:str):
    g=Graph();g+=data
    assertion=next(g.subjects(RDF.type,TH.EvidenceAssertion))
    by={
      'missing_provenance':(PROV.wasDerivedFrom,'REMOVE'),
      'missing_subject':(TH.subject,'REMOVE'),
      'missing_identifier':(DCTERMS.identifier,'REMOVE'),
      'duplicate_object':(TH.object,'DOUBLE'),
      'wrong_subject_nodekind':(TH.subject,'TO_LITERAL'),
      'duplicate_provenance':(PROV.wasDerivedFrom,'DOUBLE'),
    }
    if change=='wrong_source_class':
        source=next(g.objects(assertion,PROV.wasDerivedFrom))
        g.remove((source,RDF.type,TH.SourceDocument))
    else:
        path,op=by[change]
        current=next(g.objects(assertion,path))
        if op=='REMOVE':g.remove((assertion,path,current))
        if op=='DOUBLE':g.add((assertion,path,Literal('synthetic duplicate for negative control')))
        if op=='TO_LITERAL':
            g.remove((assertion,path,current));g.add((assertion,path,Literal('bad node kind')))
    return g


def run():
    data=Graph().parse(RESULTS/'P3_M3.ttl',format='turtle')
    shapes=Graph().parse(RESULTS/'P3_SHACL_CORE_SHAPES_V04.ttl',format='turtle')
    errors=check(data,shapes)
    report=validation_report(errors)
    report.serialize(destination=RESULTS/'P3_V09_SHACL_SUBSET_REPORT.ttl',format='turtle')
    checks=[]
    for name in ['missing_provenance','missing_subject','missing_identifier',
                 'wrong_source_class','duplicate_object','wrong_subject_nodekind','duplicate_provenance']:
        e=check(mutated(data,name),shapes)
        checks.append({'fixture':name,'expected':'FAIL','observed':'FAIL' if e else 'PASS',
                       'violations':len(e),'detected':str(bool(e)).upper(),
                       'not_true_shacl_core':'YES'})
    with (RESULTS/'P3_V09_NEGATIVE_CONTROLS_7.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(checks[0]));writer.writeheader();writer.writerows(checks)
    installed=importlib.util.find_spec('pyshacl') is not None
    summary={'release':'Paper3-v0.9','engine':'LOCAL_SUBSET_NOT_FULL_SHACL_CORE',
             'supported_constraint_operators':['targetClass','path_IRI','minCount','maxCount','nodeKind_IRI_Literal','class_direct_type'],
             'data_triples':len(data),'original_source_assertions':208,
             'original_dataset_subshape_violations':len(errors),'original_dataset_subshape_pass':not errors,
             'negative_controls_detected':sum(bool(x['violations']) for x in checks),
             'negative_controls_total':len(checks),'pyshacl_installed':installed,
             'pyshacl_core_status':'NOT_RUN' if not installed else 'NOT_RUN_USE_OFFICIAL_VALIDATOR',
             'output_report':'results/P3_V09_SHACL_SUBSET_REPORT.ttl',
             'limitations':'Limited shape-specific offline check; W3C Core pass NOT claimed. Independent expert validation NOT performed.'}
    (RESULTS/'P3_V09_SHACL_PROFILE_STATUS.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    assert not errors, f'Authentic source graph failed local subset: {errors[:2]}'
    assert sum(bool(x['violations']) for x in checks)==len(checks)
    return summary

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
