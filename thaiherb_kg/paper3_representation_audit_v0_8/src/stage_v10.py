"""Reproducible claim-context and RDF capability audit.

Research engineering metrics, not expert adjudicated scientific performance.
Preserves all frozen inputs and all previous source-review dispositions.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import csv
import hashlib
import json

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, PROV

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
DATA = ROOT / "data"
TH = Namespace("urn:thaiherb:v04:")
SOURCE_URL = "https://journals.sagepub.com/doi/full/10.1177/1934578X20933067"
DOI = "10.1177/1934578X20933067"
V3_SHA = "59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, items: list[dict[str, object]], fields: list[str] | None = None) -> None:
    assert items or fields
    names = fields or list(items[0])
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        out = csv.DictWriter(stream, fieldnames=names, extrasaction="raise")
        out.writeheader()
        for item in items:
            out.writerow(item)


def primary_corroborations(claims: list[dict[str,str]]) -> list[dict[str,str]]:
    """Five *additional* source claims, not upgrades of original source papers."""
    evidence = {
        "CA066": ("linalool", "Table 3", "71.9 (62.2-76.7)", "percent of essential-oil constituents; overall sample average and range", "GC-MS compositional profiling"),
        "CA067": ("geraniol", "Table 3", "1.4 (0.1-4.1)", "percent of essential-oil constituents; overall sample average and range", "GC-MS compositional profiling"),
        "CA068": ("terpinen-4-ol", "Table 4", "(+):(-) = 80:20 (sample 191118B)", "enantiomer percentage ratio, NOT essential-oil mass fraction", "chiral GC-MS"),
        "CA069": ("limonene", "Table 3", "2.1 (0.2-2.9)", "percent of essential-oil constituents; overall sample average and range", "GC-MS compositional profiling"),
        "CA070": ("camphor", "Table 3", "4.0 (0.0-5.5)", "percent of essential-oil constituents; overall sample average and range", "GC-MS compositional profiling"),
    }
    by_id = {r["assertion_id"]:r for r in claims}
    assertions = []
    for assertion_id, (compound, locator, value, units, method) in evidence.items():
        row = by_id[assertion_id]
        assert row["compound_label"] == compound, (assertion_id, row["compound_label"], compound)
        assert row["herb_scientific_name"].startswith("Coriandrum sativum")
        assertions.append({
            "corroboration_id":f"CORR_SATYAL2020_{assertion_id}",
            "assertion_id":assertion_id,
            "herb_scientific_name":row["herb_scientific_name"],
            "compound":compound,
            "original_source_id":row["source_id"],
            "original_disposition_unchanged":row["disposition"],
            "independent_publication": "Satyal, P., & Setzer, W. N. (2020)",
            "publication_type":"PRIMARY_ANALYTICAL_STUDY",
            "doi":DOI,
            "source_url":SOURCE_URL,
            "exact_source_locator": locator,
            "plant_material":"commercial coriander fruit essential oil, NOT fresh herb or standard dosage form",
            "method":method,
            "reported_value":value,
            "units_and_denominator":units,
            "chemical_presence": "SUPPORTED_WITH_SPECIFIC_MATERIAL_AND_METHOD",
            "author_review":"AI_ASSISTED_SINGLE_REVIEWER_NOT_HUMAN_ADJUDICATED",
            "source_test_eligibility":"NO_POSTHOC_DISCOVERY_AND_DIFFERENT_MATERIAL",
            "biological_or_clinical_validation":"NOT_INFERRED",
            "material_warning":"Commercial oil samples may include adulterated/atypical examples; not generalizable to every fruit/material",
        })
    return assertions


def plumbago_context_warnings(claims: list[dict[str,str]]) -> list[dict[str,str]]:
    name_to_context = {
        "CA086": "Earlier-literature occurrence described in introduction; subsequent Results discussion also cites earlier plumbagin reports. Table 1 compound identity not independently adjudicated here.",
        "CA087": "Elliptinone appears in prior-literature introduction; original LC-MS/MS Table 1 detection not independently confirmed.",
        "CA088": "3,3'-biplumbagin not found in the accessible introduction excerpt; absence from that excerpt does not establish absence from original study or species.",
        "CA089": "Droserone appears in prior-literature introduction; original LC-MS/MS Table 1 detection not independently confirmed.",
        "CA090": "Zeylanone appears in prior-literature introduction; original LC-MS/MS Table 1 detection not independently confirmed.",
    }
    by_id = {r["assertion_id"]:r for r in claims}
    result = []
    for id_, context in name_to_context.items():
        r = by_id[id_]
        result.append({
            "assertion_id":id_,"original_source_id":r["source_id"],"compound":r["compound_label"],
            "source_url": "https://www.nature.com/articles/s41598-022-13718-9",
            "evidence_region":"INTRODUCTION_PAST_LITERATURE; RESULTS_TABLE_1_NOT_ADJUDICATED",
            "source_material":"70% ethanol extract from aerial parts for original LC-MS/MS experiment",
            "decision":"DO_NOT_PROMOTE_OR_REJECT_UNTIL_TABLE_1_MANUALLY_VERIFIED",
            "source_claim_warning":context,"curation_type":"AI_ASSISTED_SAFETY_SCREEN_NOT_EXPERT_ADJUDICATION"
        })
    return result


def rdf_retention(frozen: list[dict[str,str]]) -> tuple[list[dict[str,object]], list[dict[str,object]],dict[str,object]]:
    graphs = {x:Graph().parse(RES/f"P3_{x}.ttl",format="turtle") for x in ("M1","M2","M3")}
    assert {x:len(g) for x,g in graphs.items()} == {"M1":207,"M2":1501,"M3":2733}
    g2, g3 = graphs["M2"], graphs["M3"]
    all_a = []
    so_po = {}
    for r in frozen:
        aid = URIRef("urn:thaiherb:v04:assertion:"+r["assertion_id"])
        subj, pred, obj = (next(g2.objects(aid,p),None) for p in (TH.subject, TH.predicate, TH.object))
        assert subj is not None and pred is not None and obj is not None
        so_po[r["assertion_id"]] = (subj,pred,obj)
    collisions = Counter(so_po.values())
    output = []
    for r in frozen:
        id_,aid = r["assertion_id"], URIRef("urn:thaiherb:v04:assertion:"+r["assertion_id"])
        spoof = so_po[id_]
        assert spoof in graphs["M1"]
        source = URIRef("urn:thaiherb:v04:source:"+r["source_id"])
        for model,g in graphs.items():
            named = model != "M1"
            assert (aid,PROV.wasDerivedFrom,source) in g if named else True
            assert (aid,DCTERMS.identifier,Literal(id_)) in g if named else True
            if model == "M3":
                assert (aid,TH.evidenceMode,Literal(r["evidence_mode"])) in g
                assert (aid,TH.directness,Literal(r["directness_or_direction"])) in g
                assert (aid,TH.contextText,Literal(r["source_locator_or_context"])) in g
                if not r["object_id"]:
                    assert any(g.objects(aid,TH.uncanonicalizedObject))
            output.append({
                "assertion_id":id_,"channel":r["channel"],"model":model,
                "underlying_source_assertion":1,"predicate_object_triple_present":1 if spoof in graphs["M1"] else 0,
                "individual_assertion_id_recoverable":int(named),
                "source_id_traceable":int(named),
                "evidence_mode_recoverable":int(model=="M3"),
                "directness_recoverable":int(model=="M3"),
                "source_context_text_recoverable":int(model=="M3"),
                "limitation_text_recoverable":int(model=="M3" and bool(r["limitation_or_finding"])),
                "clinical_missing_canonical_id_flag":int(model=="M3" and not r["object_id"]),
                "naive_spo_collision_size":collisions[spoof],
                "is_scientifically_validated":0,
            })
    groupings = defaultdict(list)
    for aid, triple in so_po.items():
        groupings[triple].append(aid)
    rows_collision = [
        {"collapse_group":"|".join(ids),"assertion_ids":";".join(ids),"count_assertions":len(ids),
         "distinct_spo_triples":1,"issue":"M1 cannot preserve source-specific distinctions for this SPO"}
        for t,ids in groupings.items() if len(ids)>1
    ]
    summary = []
    cols = ["predicate_object_triple_present","individual_assertion_id_recoverable","source_id_traceable",
            "evidence_mode_recoverable","directness_recoverable","source_context_text_recoverable",
            "limitation_text_recoverable","clinical_missing_canonical_id_flag"]
    for model in ("M1","M2","M3"):
        subset = [x for x in output if x["model"]==model]
        summary.append({"model":model,"source_assertion_denominator":len(subset),"rdf_triples":len(graphs[model]),
                        "distinct_SPO_count":len(groupings), "naive_SPO_collision_groups":len(rows_collision),
                        **{col:sum(int(r[col]) for r in subset) for col in cols},
                        "endpoint_scope":"DETERMINISTIC_REPRESENTATION_FIDELITY_NOT_ANSWER_ACCURACY"})
    diagnostic = {"models":{n:len(g) for n,g in graphs.items()},"assertions":len(frozen),
                  "unique_spo":len(groupings),"spo_collision_groups":len(rows_collision),
                  "clinical_missing_original_object_id":sum(not r["object_id"] for r in frozen),
                  "benchmark_gold":0,"validating_software":"rdflib","SHACL_Core":"NOT_RUN_PYSHACL_NOT_INSTALLED",
                  "scientific_validation":"NOT_ASSESSED"}
    return output, summary, {"diagnostic":diagnostic,"collisions":rows_collision}


def main() -> dict[str,object]:
    source = DATA/"P3_V3_208_LOCKED.csv"
    assert hashlib.sha256(source.read_bytes()).hexdigest()==V3_SHA
    claims = rows(RES/"P2_CHEM_EVIDENCE_100_v09.csv")
    assert len(claims)==100 and len(set(c["assertion_id"] for c in claims))==100
    frozen = rows(source)
    assert len(frozen)==208
    new_corrob = primary_corroborations(claims)
    write_csv(RES/"P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv",new_corrob)
    warnings = plumbago_context_warnings(claims)
    write_csv(RES/"P2_SOURCE_CONTEXT_WARNINGS_PLUMBAGO_5_v10.csv",warnings)
    rows_all = rows(RES/"P2_INDEPENDENT_CORROBORATION_v09.csv")
    union_ids = {r["assertion_id"] for r in new_corrob} | {r["assertion_id"] for r in rows_all}
    assert len(union_ids)==9
    claim_status = Counter(r["v08_claim_evidence_level"] for r in claims)
    ledger = [{"assertion_id":r["assertion_id"],"herb":r["herb_scientific_name"],"compound":r["compound_label"],
               "original_citation":r["source_citation_from_archive"],"original_source_id":r["source_id"],
               "original_source_disposition":r["disposition"],"prior_additional_corrob":int(r["assertion_id"] in {a["assertion_id"] for a in rows_all}),
               "new_additional_corrob":int(r["assertion_id"] in {a["assertion_id"] for a in new_corrob}),
               "source_independent_confirmatory_test_eligible":"NO_POSTHOC_SOURCE_DISCOVERY",
               "human_gold":"NOT_AVAILABLE","context_qualified": "YES" if r["assertion_id"] in {c["assertion_id"] for c in new_corrob} else "UNKNOWN"}
              for r in claims]
    write_csv(RES/"P2_ALL_CLAIMS_AUDIT_LEDGER_100_v10.csv",ledger)
    retain, summary, notes = rdf_retention(frozen)
    write_csv(RES/"P3_RDF_ASSERTION_RETENTION_624_v08.csv",retain)
    write_csv(RES/"P3_RDF_CAPABILITY_SUMMARY_v08.csv",summary)
    write_csv(RES/"P3_SPO_COLLISION_GROUPS_v08.csv",notes["collisions"])
    benchmark = rows(RES/"P3_V07_BENCHMARK_ELIGIBILITY.csv")
    assert len(benchmark)==32 and not any(b["adjudicated_gold"] for b in benchmark)
    controls = []
    for b in benchmark:
        controls.append({**b,"review_round": "NOT_STARTED","freeze_dataset_sha256":V3_SHA,
                         "model_predictions_locked":"NO","confirmation_scoring_permitted":"NO",
                         "conflict_of_interest_checked":"NO","reviewer_ratings_source":"NONE"})
    write_csv(RES/"P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv",controls)
    status = {"release":"P2_v1.0_P3_v0.8", "date":"2026-11-07",
              "original_p2_herb_compound_claims":100,"original_primary_fulltext_matches":5,
              "additional_source_corrob_before":len(rows_all),"additional_source_corrob_new":len(new_corrob),
              "distinct_claims_with_additional_corrob":len(union_ids),
              "source_review_warning_queue":len(warnings),"status_counts_v08":dict(claim_status),
              "P3":notes["diagnostic"],"unscored_reviewer_cases":len(benchmark),
              "scientific_overclaims_permitted":False,
              "original_v3_snapshot_sha256":V3_SHA,
              "SHACL_Core":"NOT_RUN_PYSHACL_NOT_INSTALLED"}
    (RES/"P2_P3_V10_V08_STATUS.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
    return status


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
