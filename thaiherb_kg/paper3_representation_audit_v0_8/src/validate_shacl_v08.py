"""Standards-complete SHACL Core validation when the real pySHACL is installed.

The code never reports a conformance pass when the dependency is missing.
Negative controls are mutated copies of the authentic frozen M3 graph.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import importlib.util
import json
from rdflib import Graph, RDF, URIRef, Literal, Namespace
from rdflib.namespace import DCTERMS, PROV

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
TH=Namespace('urn:thaiherb:v04:')


def write_status(result):
    file=OUT/'P3_V08_SHACL_RUN_STATUS.json'
    file.write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


def run():
    if importlib.util.find_spec('pyshacl') is None:
        return write_status({
            'status':'NOT_RUN', 'engine':'pyshacl',
            'dependency_available':False, 'authentic_conformance':None,
            'test_cases_passed':None,
            'reason':'The pyshacl distribution is not installed; this is not a SHACL Core pass.',
            'claim_of_scientific_validity':False,
            'install_command':'python -m pip install "pyshacl>=0.31,<0.41"'})
    import pyshacl
    from pyshacl import validate
    g=Graph().parse(OUT/'P3_M3.ttl',format='turtle')
    shapes=Graph().parse(OUT/'P3_SHACL_CORE_SHAPES_V04.ttl',format='turtle')
    def v(x):
        return validate(data_graph=x,shacl_graph=shapes,advanced=False,
                        inference='none',abort_on_first=False,meta_shacl=False)
    conforms,report,detail=v(g)
    report.serialize(destination=str(OUT/'P3_V08_SHACL_REPORT.ttl'),format='turtle')
    first=next(g.subjects(RDF.type,TH.EvidenceAssertion))
    source=next(g.objects(first,PROV.wasDerivedFrom))
    entity=next(g.objects(first,TH.subject))
    ident=next(g.objects(first,DCTERMS.identifier))
    controls=[]
    for name,remove,add in [
        ('missing_provenance',(first,PROV.wasDerivedFrom,source),None),
        ('missing_subject',(first,TH.subject,entity),None),
        ('missing_identifier',(first,DCTERMS.identifier,ident),None),
        ('wrong_source_class',(source,RDF.type,TH.SourceDocument),None),
        ('double_object',None,(first,TH.object,Literal('DELIBERATELY_WRONG_SECOND_VALUE'))),
    ]:
        copy=Graph()
        copy+=g
        if remove:copy.remove(remove)
        if add:copy.add(add)
        observed,negative_report,_=v(copy)
        controls.append({'fixture':name,'negative_control_detected':not observed,
                         'expected_conforms':False,'observed_conforms':bool(observed),
                         'validation_results':len(list(negative_report.subjects(RDF.type,URIRef('http://www.w3.org/ns/shacl#ValidationResult'))))})
    with (OUT/'P3_V08_SHACL_NEGATIVE_CONTROLS.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(controls[0]));w.writeheader();w.writerows(controls)
    status='PASS' if conforms and all(x['negative_control_detected'] for x in controls) else 'FAIL'
    return write_status({'status':status,'engine':'pyshacl',
                         'version':getattr(pyshacl,'__version__','UNREPORTED'),
                         'authentic_conformance':bool(conforms),
                         'negative_controls_passed':sum(x['negative_control_detected'] for x in controls),
                         'negative_controls_total':len(controls),
                         'data_graph_triples':len(g),'shapes_graph_triples':len(shapes),
                         'report_path':'results/P3_V08_SHACL_REPORT.ttl',
                         'claim_of_scientific_validity':False})


if __name__=='__main__':
    result=run();print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='PASS' else 2)
