"""Guard independent M1/M2/M3 benchmark claims from premature scoring."""
from pathlib import Path
import csv

def check_benchmark_eligibility(csv_path: str) -> dict:
    path = Path(csv_path)
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    eligible = [r for r in rows if r["eligible_for_blind_scoring"] == "YES"]
    adjudicated = [r for r in eligible if r["independent_gold_available"] == "YES"
                   and r["reviewer_1"] and r["reviewer_2"] and r["adjudicated_gold"]]
    return {"case_total": len(rows), "eligible_cases": len(eligible),
            "fully_adjudicated_cases": len(adjudicated),
            "confirmatory_metrics_authorized": len(adjudicated) > 0 and len(adjudicated) == len(eligible)}

if __name__ == "__main__":
    import json
    print(json.dumps(check_benchmark_eligibility("results/P3_V07_BENCHMARK_ELIGIBILITY.csv"), indent=2))
