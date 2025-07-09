def ingest_all(schema):
    # TODO: load PDFs/CSVs and return raw data dict
    return {
        "monograph": open(schema["files"]["monograph"], "rb").read(),
        "stability": schema["files"]["stability"],
        "traditional_use": schema["files"]["traditional_use"]
    }
