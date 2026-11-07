# FINAL controlled release — ThaiHerb KG 2026-11-07

Paper 2 **v0.7** and Paper 3 **v0.5**. Both versions are development-grade, not submitted or independently adjudicated. Previous README and ZIP snapshots remain archived; use only the `FINAL_REPRODUCIBLE` packages below for clean reproduction.

## Verified Google Drive packages

- [Paper 2 v0.7 FINAL](https://drive.google.com/file/d/1ui8vxNz3zAh4ZE1LsdOsqwSbW67mj53C/view)
- [Paper 3 v0.5 FINAL](https://drive.google.com/file/d/1oKGWe-DhtTS_PdAlBusoNs6V8Dg0x70h/view)
- [Combined FINAL](https://drive.google.com/file/d/1ynu2k9bj8v1qLf6K0B20u_vjlua-lbAi/view)
- [Paper 2 evidence registry + offline interactive dashboard](https://drive.google.com/drive/folders/1Yo6Mfn26lkuSEgQ5sWmPkbJf2iTGGr_y)
- [Paper 3 RDF and query engine files](https://drive.google.com/drive/folders/1Xxag-QbzndliWIvJJXchtYteegHvaSeV)

## Validated software status

- 65 archive entries, 65 SHA-256 checks including manifest excluded from own manifest; 65-file manifest contents are fully checked. (Manifest lists 65 content files; there are 66 entries including manifest.)
- Clean extraction: **34/34 pytest passed**. This verifies code/structure, not biological accuracy.
- P2: 100 claims stratified: 5 full-text primary, 5 abstract-only primary, 10 secondary reviews, 80 not verified.
- P3: 208 historical source assertions frozen; 8 CQ development cases, 24 RDF query outputs, no expert gold, no accuracy results.
- Real pySHACL Core: **NOT RUN** due to no package access in ChatGPT container.

## Reproduce

```bash
python -m pip install -r requirements.txt
python src/stage_next.py
python -m src.build_dashboard
python -m pytest -q tests
python -m pip install "pyshacl>=0.31,<0.41"
python src/validate_shacl.py
```

Full source data are intentionally delivered in Drive packages rather than GitHub; do not infer the absence of files in this branch means the repository alone can run all data-dependent tests.
