"""Recheck the released herb-compound evidence and frozen RDF projections.

Requires the full research ZIP from the versioned Google Drive folder.
This script does not create expert gold labels or scientific validation.
"""
from pathlib import Path
import csv
import json
import hashlib
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]

def load_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))

def validate_release():
    results = ROOT / "results"
    claims = load_csv(results / "P2_CHEM_EVIDENCE_100_v09.csv")
    corroborations = load_csv(results / "P2_INDEPENDENT_CORROBORATION_v09.csv")
    benchmark = load_csv(results / "P3_V07_BENCHMARK_ELIGIBILITY.csv")
    assert len(claims) == 100
    assert len(set(x["assertion_id"] for x in claims)) == 100
    assert len(corroborations) == 4
    assert all(x["external_test_eligible"].startswith("NO_") for x in corroborations)
    assert all(x["adjudicated_gold"] == "" for x in benchmark)
    expected = {"M1":207, "M2":1501, "M3":2733}
    for name, count in expected.items():
        actual = len(Graph().parse(results / ("P3_" + name + ".ttl"), format="turtle"))
        assert actual == count, (name, actual, count)
    source_hash = hashlib.sha256((ROOT / "data/P3_V3_208_LOCKED.csv").read_bytes()).hexdigest()
    assert source_hash == "59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774"
    return {"status":"STRUCTURAL_CHECKS_PASS", "claims":100,
            "new_corroborations":4, "benchmark_gold":0,
            "shacl_core":"NOT_RUN_DEPENDENCY_UNAVAILABLE",
            "rdf_triples":expected, "v3_frozen_sha256":source_hash}

if __name__ == "__main__":
    print(json.dumps(validate_release(), indent=2))
