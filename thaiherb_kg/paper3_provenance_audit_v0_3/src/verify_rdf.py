from __future__ import annotations
import csv
import hashlib
import json
import sys
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, PROV

TH = Namespace("urn:thaiherb:v03:")

def count_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def verify(root: Path):
    m = json.loads((root / "SHA256_MANIFEST.json").read_text(encoding="utf-8"))
    assert all((root / x["path"]).is_file() and
        hashlib.sha256((root / x["path"]).read_bytes()).hexdigest() == x["sha256"]
        for x in m["files"]), "Manifest mismatch"
    assertions = count_csv(root / "data/P3_V3_ORIGINAL_208_LOCKED.csv")
    assert len(assertions) == 208
    graph = Graph().parse(root / "P3_DATA_GRAPH.ttl", format="turtle")
    nodes = set(graph.subjects(RDF.type, TH.EvidenceAssertion))
    assert len(nodes) == 208
    assert all(len(list(graph.objects(node, PROV.wasDerivedFrom))) == 1 for node in nodes)
    assert sum(bool(list(graph.objects(node, TH.objectText))) for node in nodes) == 7
    assert all(len(list(graph.objects(node, TH.objectIRI))) +
               len(list(graph.objects(node, TH.objectText))) == 1 for node in nodes)
    Graph().parse(root / "P3_SHAPES.ttl", format="turtle")
    shacl = json.loads((root / "P3_SHACL_SUMMARY.json").read_text(encoding="utf-8"))
    assert shacl["status"] == "NOT_RUN", "Unexpected SHACL claim; inspect current report"
    print(f"PASS {len(nodes)} RDF assertions; {len(graph)} triples; SHACL NOT_RUN")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python verify_rdf.py EXTRACTED_P3_RELEASE_DIRECTORY")
    verify(Path(sys.argv[1]))
