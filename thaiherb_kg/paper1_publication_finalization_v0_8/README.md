# ThaiHerb Paper 1 — Computational Feasibility Publication Finalization v0.8

**2026-11-07. Scientific status: internally reproducible V3-derived reconstruction, NOT an exact reproduction of the archived original Paper 1 study.**

This project consolidates manuscript, supplementary analyses, environmental manifest and a fully runnable computational feasibility reanalysis for the ten-herb ThaiHerb pilot. It deliberately does not label proxy reconstructions as the original experimental 19 compound classes.

## Key outputs

- `manuscript/Paper1_Feasibility_Reanalysis_v08.docx` and `.md`: integrated author-review manuscript with a new coherent analysis.
- `supplement/Paper1_Supplementary_Methods_Results_v08.docx` and `.md`: supplementary data tables and original-results reconciliation.
- `docs/PUBLICATION_FINALIZATION_REPORT_TH.md`: editorial decision record explaining the no-go publication signoff items.
- `results/all_reanalysis_scores_13models_10seeds.csv`: all 5,850 pairwise cosine values from 13 model variants × 10 seeds × 45 unordered pairs.
- `results/seed_repeatability_13models.csv`, `results/perturbation_sensitivity_10comparisons.csv`, and `results/ORIGINAL_MANUSCRIPT_VS_V08_REANALYSIS.csv`: main statistics and transparency checks.
- `results/FIG01_seed_rank_stability.png`, `results/FIG02_perturbation_sensitivity.png`: manuscript figures.
- `results/reanalysis_manifest.json`: source SHA-256, environment versions and guardrails.
- `supplement/BLINDED_EXPERT_R1_45.csv`, `BLINDED_EXPERT_R2_45.csv`, `ADJUDICATION_TEMPLATE_45.csv`: blank genuine-human-expert review forms; not machine-filled.

## Reproduce

```bash
python -m venv .venv
# Activate the environment using your operating system's standard command.
python -m pip install -r requirements.txt
python run_v08.py
```

For a bytewise-comparable source analysis use the frozen software versions and SHA-256 manifest provided. Floating-point outputs on a different hardware/software stack may differ slightly. Model-trained vectors are regenerated; no unseen original vectors are claimed.

## Critical scientific distinction

1. The *original* reviewer-revised manuscript describes a selected ten-herb feasibility experiment and its original reported results. The original class map/walk corpora/model archive are missing from the accessible project.
2. This *v0.8 reanalysis* uses later V3-derived herb/formula/chemical proxy inputs and candidate 19-class curation. Original and reconstructed numerical results **must not be combined** as a single experimental run.
3. The formula graph is source-reviewed by a single AI-assisted curator; chemical occurrence review is heterogeneous and not independent expert adjudication.
4. Version v0.7 leave-one-formula-out predicts within-compendium formula co-occurrence, not therapeutic or molecular similarity.
5. These data cannot establish clinical interchangeability, efficacy or safety.

## Folder map

```text
src/             versioned generator and analysis code
data/            locked inputs, NOT copied into public GitHub
results/         output CSVs, figures, environment/source hashes
manuscript/      integrated manuscript DOCX + Markdown
supplement/      supplementary document, evidence registry and empty reviewer templates
docs/            data dictionary, research decision record and release checklist
tests/           data-structure, scientific boundary and reproducibility checks
```

The full package is intended for authorized project use via the project's Google Drive. The public GitHub branch contains source code and controlled-access instructions only. Before journal submission the authors must provide their names, declarations, final reference checks and approve the study's use of the candidate chemical taxonomy.
