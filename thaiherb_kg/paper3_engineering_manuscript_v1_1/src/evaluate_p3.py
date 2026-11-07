"""Frozen ThaiHerb V3 RDF projection integrity audit.

This evaluates deterministic representation features, not expert-grounded answer
accuracy. Run with `python src/evaluate_p3.py` from the project root.
"""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from rdflib import Graph, URIRef, Literal, RDF, Namespace
from rdflib.namespace import DCTERMS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
TH = Namespace("urn:thaiherb:v04:")
PROV = Namespace("http://www.w3.org/ns/prov#")
EXPECTED_SHA = "59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def graph_value(g, subj, pred):
    return next(iter(g.objects(subj, pred)), None)


def main():
    source = DATA / "P3_V3_208_LOCKED.csv"
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    assert sha == EXPECTED_SHA, "Frozen input changed"
    records = read_csv(source)
    assert len(records) == 208 and len({x["assertion_id"] for x in records}) == 208
    graphs = {model: Graph().parse(DATA / f"P3_{model}.ttl", format="turtle") for model in ("M1", "M2", "M3")}
    assert {m: len(g) for m, g in graphs.items()} == {"M1": 207, "M2": 1501, "M3": 2733}
    # Reified M3 is the reference for the exact terms used in a projection,
    # while the 208-row original CSV is the source-assertion denominator.
    m3 = graphs["M3"]
    rows = []
    required = ["id", "provenance", "evidence_mode", "directness", "context", "status", "limitation", "uncanonicalized"]
    for rec in records:
        aid = rec["assertion_id"]
        node = URIRef(f"urn:thaiherb:v04:assertion:{aid}")
        subj = graph_value(m3, node, TH.subject)
        pred = graph_value(m3, node, TH.predicate)
        obj = graph_value(m3, node, TH.object)
        assert subj is not None and pred is not None and obj is not None, aid
        for model, graph in graphs.items():
            if model == "M1":
                base = ((subj, pred, obj) in graph)
                result = dict(id=0, provenance=0, evidence_mode=0, directness=0,
                              context=0, status=0, limitation=0, uncanonicalized=0)
            else:
                base = (graph_value(graph, node, TH.subject) == subj and
                        graph_value(graph, node, TH.predicate) == pred and
                        graph_value(graph, node, TH.object) == obj)
                result = dict(
                    id=int(str(graph_value(graph, node, DCTERMS.identifier) or "") == aid),
                    provenance=int(graph_value(graph, node, PROV.wasDerivedFrom) is not None),
                    evidence_mode=int(graph_value(graph, node, TH.evidenceMode) is not None),
                    directness=int(graph_value(graph, node, TH.directness) is not None),
                    context=int(graph_value(graph, node, TH.contextText) is not None),
                    status=int(graph_value(graph, node, TH.originalStatus) is not None),
                    limitation=int(graph_value(graph, node, TH.limitationText) is not None),
                    uncanonicalized=int(graph_value(graph, node, TH.uncanonicalizedObject) is not None),
                )
            rows.append({"assertion_id": aid, "channel": rec["channel"], "model": model,
                         "edge_recoverable": int(base), **result})
    assert len(rows) == 624
    for m in graphs:
        assert sum(r["edge_recoverable"] for r in rows if r["model"] == m) == 208
    row_columns = ["assertion_id", "channel", "model", "edge_recoverable"] + required
    write_csv(OUT / "P3_ASSERTION_AUDIT_624.csv", rows, row_columns)
    summary = []
    for m, g in graphs.items():
        subset = [r for r in rows if r["model"] == m]
        stats = {col: sum(int(r[col]) for r in subset) for col in ["edge_recoverable"] + required}
        summary.append({"model": m, "assertions": 208, "rdf_triples": len(g),
                        "rdf_triples_per_assertion": round(len(g)/208, 3), **stats})
    write_csv(OUT / "P3_MODEL_CAPABILITY_SUMMARY.csv", summary, list(summary[0].keys()))
    by_channel = []
    for ch in ["formula", "chemistry", "pharmacology_target", "clinical"]:
        for m in graphs:
            sub = [r for r in rows if r["model"] == m and r["channel"] == ch]
            by_channel.append({"channel": ch, "model": m, "n_assertions": len(sub),
                               **{col: sum(int(r[col]) for r in sub) for col in ["edge_recoverable"] + required}})
    write_csv(OUT / "P3_CHANNEL_CAPABILITY_SUMMARY.csv", by_channel, list(by_channel[0].keys()))
    groups = defaultdict(list)
    for rec in records:
        node = URIRef(f"urn:thaiherb:v04:assertion:{rec['assertion_id']}")
        groups[(graph_value(m3, node, TH.subject), graph_value(m3, node, TH.predicate), graph_value(m3, node, TH.object))].append(rec["assertion_id"])
    collisions = [{"assertion_ids": ";".join(ids), "collision_size": len(ids),
                   "effect": "distinct source assertions collapse to one SPO"}
                  for ids in groups.values() if len(ids) > 1]
    assert len(groups) == 207 and len(collisions) == 1 and set(collisions[0]["assertion_ids"].split(";")) == {"CLIN005", "CLIN006"}
    write_csv(OUT / "P3_SPO_COLLISION_AUDIT.csv", collisions, list(collisions[0].keys()))

    clinical = defaultdict(list)
    for r in records:
        if r["channel"] == "clinical": clinical[(r["subject_id"],r["predicate_or_topic"])].append(r)
    discordance = []
    for (plant, topic), lst in clinical.items():
        directions = set(x["directness_or_direction"] for x in lst)
        if len(lst) > 1 and len(directions) > 1:
            discordance.append({"subject_id": plant, "topic": topic,
                                "n_assertions": len(lst), "assertion_ids": ";".join(x["assertion_id"] for x in lst),
                                "directions": ";".join(sorted(directions)),
                                "n_distinct_sources": len(set(x["source_id"] for x in lst)),
                                "review_status": "CONTEXT_VARIATION_NOT_BIOLOGICAL_CONTRADICTION",
                                "independent_adjudication": "PENDING"})
    assert len(discordance) == 3 and sum(x["n_assertions"] for x in discordance) == 7
    write_csv(OUT / "P3_CLINICAL_CONTEXT_VARIATION.csv", discordance, list(discordance[0].keys()))

    # Ablation below is a purely structural intervention; not evidence of actual
    # question-answer correctness. A removed property is deleted on all its nodes.
    ablations = []
    for label, predicates in [
        ("intact_M3", []),
        ("remove_provenance", [PROV.wasDerivedFrom]),
        ("remove_evidence_mode", [TH.evidenceMode]),
        ("remove_directness", [TH.directness]),
        ("remove_context", [TH.contextText]),
        ("remove_all_qualifiers", [PROV.wasDerivedFrom, TH.evidenceMode, TH.directness, TH.contextText]),
    ]:
        removed = set(predicates)
        retain = {"source": 0, "evidence_mode": 0, "directness": 0, "context": 0}
        for rec in records:
            node = URIRef(f"urn:thaiherb:v04:assertion:{rec['assertion_id']}")
            for key, pred in [("source", PROV.wasDerivedFrom), ("evidence_mode", TH.evidenceMode),
                              ("directness", TH.directness), ("context", TH.contextText)]:
                if pred not in removed and graph_value(m3, node, pred) is not None:
                    retain[key] += 1
        ablations.append({"ablation": label, "assertions": 208,
                          **{f"{k}_recoverable": v for k, v in retain.items()},
                          "interpretation": "deterministic field-deletion sensitivity; not answer accuracy"})
    write_csv(OUT / "P3_CONTEXT_ABLATION.csv", ablations, list(ablations[0].keys()))
    legacy = read_csv(DATA / "P3_V05_ENGINE_OUTPUTS_24.csv")
    assert len(legacy) == 24 and len({x["case_id"] for x in legacy}) == 8
    development = []
    for d in legacy:
        development.append({"case_id": d["case_id"], "category": d["category"], "model": d["model"],
                            "query_status": d["status"], "edge_count": d["edge_count"],
                            "citations_from_rdf": d["citation_count"],
                            "evaluation_type": "ARCHIVED_DEVELOPMENT_QUERY_OUTPUTS_NOT_BLIND_GOLD"})
    write_csv(OUT / "P3_DEVELOPMENT_CQ_24_SUMMARY.csv", development, list(development[0].keys()))

    expert = read_csv(DATA / "P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv")
    assert len(expert) == 45 and all(not d.get("adjudicated_gold", "").strip() for d in expert)
    authentic = json.loads((OUT / "P3_PYSHACL_CORE_RUNTIME.json").read_text(encoding="utf-8"))
    assert authentic["status"] == "PASS" and authentic["negative_controls_detected"] == 10
    q = {"source_sha256": sha, "projection_triples": {m: len(g) for m, g in graphs.items()},
         "assertions": 208, "channels": dict(Counter(x["channel"] for x in records)),
         "source_ids": len({r["source_id"] for r in records}),
         "distinct_spo": len(groups), "spo_collision_groups": len(collisions),
         "clinically_discordant_context_candidate_groups": len(discordance),
         "clinical_evidence_not_adjudicated": 7,
         "missing_clinical_canonical_object_ids": sum(1 for r in records if r["channel"]=="clinical" and not r["object_id"]),
         "actual_pyshacl": {k:authentic[k] for k in ("engine", "engine_version", "status", "baseline_conforms", "actual_violations", "negative_controls_total", "negative_controls_detected")},
         "development_queries": 8, "development_query_model_outputs": 24,
         "expert_candidate_cases": len(expert), "expert_adjudicated_gold": 0,
         "comparative_semantic_accuracy_status": "NOT_MEASURED_NO_HUMAN_GOLD",
         "material_preparation_normalized_field_status": "NOT_COMPLETE_IN_V3_PROJECTION",
         "biological_truth_or_clinical_efficacy": "NOT_ASSESSED",
         "reconstruction_note": "Exact data-model field recovery, not independent scientific performance."}
    (OUT / "P3_V11_EXPERIMENT_SUMMARY.json").write_text(json.dumps(q, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(q, indent=2))
    return q

if __name__ == "__main__": main()
