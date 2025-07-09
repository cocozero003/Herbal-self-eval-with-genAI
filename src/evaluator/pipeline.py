from .ingestion import ingest_all
from .parser_monograph import parse_monograph
from .parser_stability import parse_stability
from .parser_traditional import parse_traditional
from src.llm.summarizer import Summarizer
from src.llm.consistency_checker import ConsistencyChecker

def run_pipeline(input_schema, output_path):
    # 1. Ingest raw files
    raw = ingest_all(input_schema)
    # 2. Parse modules
    monograph = parse_monograph(raw["monograph"])
    stability = parse_stability(raw["stability"])
    traditional = parse_traditional(raw["traditional_use"])
    # 3. Summarize each module
    summarizer = Summarizer()
    sum_mon = summarizer.summarize(monograph, "quality")
    sum_stab = summarizer.summarize(stability, "safety")
    sum_trad = summarizer.summarize(traditional, "efficacy")
    # 4. Consistency checks
    checker = ConsistencyChecker()
    issues = checker.check_all([sum_mon, sum_stab, sum_trad])
    # 5. TODO: assemble and write output package
    print("Pipeline complete. Issues found:", issues)
