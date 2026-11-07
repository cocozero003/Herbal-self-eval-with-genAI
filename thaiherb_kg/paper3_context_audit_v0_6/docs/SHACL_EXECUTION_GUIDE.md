# SHACL Core: reproducible validation gate

1. Install Python 3.11–3.13, `rdflib>=7.3,<8`, and `pyshacl>=0.31,<0.41` in an internet-enabled Python environment.
2. Unzip the controlled full research package with all `data/` and `results/` files.
3. Run `python src/validate_shacl.py`. This loads the actual `results/P3_M3.ttl` and `results/P3_SHACL_CORE_SHAPES_V04.ttl` using pySHACL with `inference='none'` and `advanced=False`.
4. Require a conformant baseline **and** four deliberately invalid negative fixtures to fail validation. Inspect `P3_SHACL_RUNTIME_STATUS.json`, `P3_SHACL_CORE_REPORT.ttl`, and `P3_SHACL_NEGATIVE_CONTROLS.csv`.
5. Record versions, environment, input SHA-256, exit code, and failure details. Do not treat shape conformance as chemical or clinical scientific truth.

At release build time pySHACL could not be installed in the container. This project's test suite and optional CI only exercise ordinary Python unit tests unless a networked environment installs pySHACL and executes `validate_shacl.py`. A GitHub Actions synthetic-graph check is **not** an authentic 208-record validation.
