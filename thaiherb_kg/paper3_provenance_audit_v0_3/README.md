# ThaiHerb Paper 3 v0.3 — provenance and structural RDF audit

Frozen historical V3 CSV: 208 assertions = 71 formula + 100 chemistry + 30 pharmacology-target + 7 clinical. 45 source IDs observed; original reported 67 full registry records not independently recovered.

This version's newly authored source-attributed RDF has **2,834 triples and 208 assertion nodes**, retaining seven clinical object descriptions as RDF literals with missing-canonical-ID flags, not invented IDs. This is **not** reconstruction of historical 5,148-triple RDF; older v0.2 exported 201 assertions / 1,497 triples.

Shapes prepared, actual pySHACL Core execution **NOT_RUN** because dependency unavailable. Custom mechanical/semantic tests run and passed, but they are not SHACL conformance. Actual M1/M2/M3 held-out benchmark and human gold are not complete.

Contents of the full local release ZIP: original V3 locked 208-row CSV, P2-v0.4 crosswalk, 100 chemistry locator queue, seven clinical canonical issue rows, RDF graph/ontology/shapes, provenance audit, executable validation entrypoint, offline HTML, SHA256 manifest and tests.

This GitHub branch exposes verification code and methods. Full datasets are in the user-delivered reproducibility ZIP, not published here. Drive folder creation succeeded but release ZIP upload was not verified.

Run `python src/verify_rdf.py /path/to/extracted/Paper3_Provenance_StructuralAudit_v0.3_2026-11-07` with RDFLib installed.
