"""Optional standards-complete SHACL run; never replace it with a hand-written pass."""
from pathlib import Path
import argparse, sys
from rdflib import Graph

ROOT=Path(__file__).resolve().parents[1]

def run(data_file: str, shapes_file: str):
    try:
        from pyshacl import validate
    except ImportError as exc:
        raise RuntimeError('SHACL_NOT_RUN: pyshacl unavailable. Install pyshacl to validate.') from exc
    data=Graph().parse(data_file)
    shapes=Graph().parse(shapes_file)
    conforms,report_graph,report_text=validate(data,shacl_graph=shapes,inference='rdfs',advanced=False,abort_on_first=False)
    return bool(conforms),str(report_text)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--data',default=str(ROOT/'paper3/v3_201assertions_provenance.ttl'))
    p.add_argument('--shapes',default=str(ROOT/'paper3/evidence_projection_shapes.ttl'))
    a=p.parse_args()
    try:
        conforms,report=run(a.data,a.shapes)
    except RuntimeError as err:
        print(err,file=sys.stderr);sys.exit(2)
    print(report);sys.exit(0 if conforms else 1)
