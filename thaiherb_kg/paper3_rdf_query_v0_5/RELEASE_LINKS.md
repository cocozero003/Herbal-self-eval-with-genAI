# ThaiHerb controlled research release (7 November 2026)

Two papers are version-separated, and historical archives/main remain unchanged.

## Authoritative runnable packages

- Paper 2 v0.7, fully reproducible: https://drive.google.com/file/d/1xRwKUdfbvhKDhM1cjszvnB9HS-Ud8ac1/view
- Paper 3 v0.5, fully reproducible: https://drive.google.com/file/d/1uEEttdspXvhbF6NMog-i2WqGuGFaCMai/view
- Combined complete research package: https://drive.google.com/file/d/14gs6QCa81n5DnwrOKoKlD4Fix0kYw_PD/view
- Offline searchable explorer: https://drive.google.com/file/d/1Xyj9VLtiLDLwyxlCacumMRcbL61xoa6Y/view

## Integrity and scientific boundaries

- Paper 2 source review: 5 primary full-text, 5 primary abstract-only, 10 secondary review-only, 80 NOT_VERIFIED. These are not gold labels or 20 laboratory-confirmed chemicals.
- Paper 3: unchanged V3 208 source assertions; 8 development questions and 24 deterministic RDF query results. No expert-adjudicated answer accuracy, no M3 superiority claim.
- 34 pytest checks passed in the ChatGPT authoring runtime, using archived inputs.
- Actual pySHACL Core validation NOT RUN: package unavailable to the authoring environment. Four custom controls do not replace pySHACL.

The code here is a public-readable companion; the full frozen datasets and all generated outputs are in Drive ZIPs above. Run from extracted FULL package with `python -m pip install -r requirements.txt`, `python src/stage_next.py`, `python -m src.build_dashboard`, `python -m pytest -q tests`, and, after installing pySHACL, `python src/validate_shacl.py`.
