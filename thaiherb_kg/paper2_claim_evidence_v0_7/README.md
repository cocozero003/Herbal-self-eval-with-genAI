# Current controlled release — 2026-11-07

Paper 2 **v0.7**, Paper 3 **v0.5**, **research development only**.

P2: 100 assertions = 5 primary full-text + 5 primary abstract-only + 10 secondary-only + 80 not verified.
P3: frozen 208 assertions, 8 competency development cases, 24 deterministic RDF query outputs from 3 projections; no accuracy claims.

`pySHACL` Core **NOT_RUN** due to package installation/network DNS failure. No human-review gold, external biological validation or scientific clinical inference.

Run `python -m pip install -r requirements.txt`, `python src/stage_next.py`, `python -m src.build_dashboard`, `python -m pytest -q tests`, and when installed `python src/validate_shacl.py`.

Output manifest: `SHA256_MANIFEST.json`. `main` and historical datasets unchanged.
