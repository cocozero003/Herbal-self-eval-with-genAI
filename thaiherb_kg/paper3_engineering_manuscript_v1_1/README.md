# ThaiHerb Paper 3 v1.1 — Full Author-Review Research Manuscript

**Release date:** 2026-11-07  
**Scope:** Evidence-centric Thai herbal Knowledge Graph; reproducible source-assertion fidelity, provenance, qualifier-ablation and authentic SHACL Core profile conformance.

## Research question

Can a provenance-aware, evidence-qualified RDF design preserve source-specific interpretation fields lost in naive SPO projection on a frozen collection of 208 source assertions?

The answer is a **deterministic structural representation result**, not an independently measured semantic answer accuracy advantage or a biological validation claim.

## Primary deliverable

- `manuscript/Paper3_EvidenceCentric_KG_Full_Manuscript.docx` — complete ~4,700-word English research manuscript, two tables, four embedded figures, APA 7 references, ethics/AI and availability disclosures.
- `manuscript/Paper3_EvidenceCentric_KG_Full_Manuscript.md` — source manuscript.
- `dashboard/ThaiHerb_Paper3_EvidenceKG_Research_Explorer.html` — standalone interactive dashboard for auditable original assertion IDs and model fields.
- `figures/` — figures for scientific review in PNG format.
- `results/` — all new empirical tables and frozen GitHub Actions pySHACL report.
- `data/` — original V3 208-assertion frozen CSV, 3 RDF projections, 34-triple shapes graph, development-only CQ result snapshot and unfilled real-expert review template.
- `src/evaluate_p3.py`, `src/make_figures.py`, `src/build_manuscript.py`, `src/build_dashboard.py`, `src/test_dashboard_browser.py` — reproducible code.
- `tests/` — invariant and provenance-fidelity regression tests.

## Verified results

- `208` original evidence assertions: `71` formula, `100` chemistry, `30` target and `7` clinical, with `45` linked source IDs.
- `207 / 1501 / 2733` distinct RDF triples for M1/M2/M3.
- Recoverable source-assertion identities: `0 / 208 / 208` out of 208.
- Recoverable provenance source links: `0 / 208 / 208` out of 208.
- Recoverable evidence mode and context: `0 / 0 / 208` out of 208.
- One naive SPO collapse (CLIN005 and CLIN006) spanning two source-specific clinical assertions.
- Three clinically context-varying review candidate groups, **none independently adjudicated as biological contradiction**.
- Authentic pySHACL 0.40.2 Core validation **PASS**: 0 structural violations; 10/10 seeded negative controls detected. See https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018 .
- Adjudicated independent expert-gold responses: `0/45`. Source-disjoint biological accuracy and external generalizability **NOT MEASURED**.

## Reproduce locally

From the extracted project root:

```bash
python -m pip install -r requirements.txt
python src/evaluate_p3.py
python src/make_figures.py
python src/build_dashboard.py
python src/build_manuscript.py
python -m pytest -q tests
```

Optional interactive browser smoke (Chromium and Playwright required):

```bash
python -m pip install playwright
python src/test_dashboard_browser.py
```

Official pySHACL was already run and authenticated on GitHub Actions; `results/P3_PYSHACL_CORE_RUNTIME.json` is the historical machine report from that completed CI run. Do not claim another CI or local pySHACL test occurred unless executed and logged.

## Critical limitations

1. Measured field recovery is the direct effect of model construction, not a blinded answer-quality test. No inferential significance test is appropriate for those deterministic design differences.
2. The original source corpus contains some review-based or not fully primary-full-text-adjudicated claims; the preservation of a source ID is not verification of its scientific content.
3. Normalized preparation, plant part, dose, comparator, population and clinical outcome ontologies are not fully implemented in this V3 projection; seven clinical object IDs remain uncoded rather than invented.
4. No blinded expert adjudication exists. The 45-case review template includes developmental and post hoc examples, not a locked prospective independent benchmark.
5. Original published historical graph statistics (such as 5,148 triples reported in earlier drafts) are not assigned to this frozen 2,733-triple projection.
6. The P3 V3 formula set (71) is not silently updated with the newer Paper 2 formula set (74).

**Publication readiness:** Complete author-review engineering/methods manuscript. Submission to a journal remains subject to authors' approval, journal fit, original-source verification, ethics/data statements, and decisions on whether peer reviewers require externally adjudicated evaluation.
