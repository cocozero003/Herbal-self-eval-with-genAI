# ThaiHerb Paper 1 — Formula Integrity and Sibling Embedding Reanalysis v0.4

**Release date:** 2026-11-07  
**Scope:** Ten herbs, ten official formula variants, 100 audit decisions, 46 focal-herb memberships, 23 positive-NPMI Cooc links, 30 V3-derived chemistry proxy assertions, 10-seed reanalysis.  
**Status:** Formula layer source-reviewed by one curator; **NOT** independent expert-validated. The original chemistry 19-class panel and model vectors are not recovered. New Chem/Core are exploratory reconstructions only.

## Read first

- `docs/RESEARCH_REPORT_TH.md`: methodology, results, primary source and limitations
- `docs/OPEN_RESEARCH_GATES_TH.md`: remaining publication-critical inputs
- `results/audit_manifest.json`: computed counts and source review scope
- `results/computational_manifest.json`: model settings and environmental versions

## Corrected important error

The v0.3 source audit removed ginger, Java long pepper and black pepper from F05. This is wrong: the official formula continues on **printed page 162**, where all three are listed. The prior finding and downstream numerical sensitivity results must be disregarded. The v0.4 formula table is aligned with the selected ten DTAM/FDA ingredient tables (printed pages 1–2, 27–28, 49–51, 71–72, 122–123, 143–144, 161–162, 164–165, 240–241, 386–387).

## Quick start

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest -q tests
```

The `run_all.py` command recreates formula audit outputs, NPMI, chemical proxy table, and Cooc/Chem/Core exploratory model outputs for ten random seeds. The primary PDF is not redistributed. The V3-derived bootstrap is a **research proxy**, not the original frozen training dataset.

## Web

Open `Paper1_SourceIntegrity_Dashboard.html` in a modern browser. This displays the audited formula matrix and model results without relying on a backend or network requests.

## Manuscript safety

The original reviewed manuscript is in `manuscript/Paper1_source_manuscript_reviewed_v3.docx` (reference only). The reanalysis does **not** replace the published/archived results or prove biological validity. Use the report as a methodological correction and a reviewer-ready audit trail, but do not submit as a final manuscript without completing outstanding gates.

## Versioning

- v0.3: historical erroneous 3-edge F05 deletion, explicitly deprecated
- v0.4: source-reviewed formula projection; corrected F05; new model reconstructions with provenance disclaimers

Public source: https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf
