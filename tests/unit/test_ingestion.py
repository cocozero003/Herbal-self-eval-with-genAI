from src.evaluator.ingestion import ingest_all

def test_ingest_all(tmp_path):
    assert isinstance(ingest_all({"files": {"monograph": __file__, "stability": __file__, "traditional_use": __file__}}), dict)
