# Clean ZIP extraction and full rerun, Paper 2 v1.3

Date: 2026-11-07

Full archive: `ThaiHerb_Paper2_v13_Robustness_FULL_20261107.zip`.

The archive was extracted into an independent clean directory and the following commands completed: `python src/run_robustness.py`, `python src/run_sensitivity_extensions.py`, `python src/paired_formula_bootstrap.py`, and `python -m pytest -q tests`.

Result: **CLEAN_REPLAY_ALL_PASS**, **23/23 pytest tests passed**.

| Output | Original SHA256 | Clean rerun SHA256 | Exact byte match |
|---|---|---|---|
| P2_LOFO_SUMMARY_CLUSTER_BOOTSTRAP.csv | `fa90a0180a275da6` | `fa90a0180a275da6` | TRUE |
| P2_PERTURBATION_SUMMARY.csv | `faf9ab37be6342ed` | `faf9ab37be6342ed` | TRUE |
| P2_SOURCE_HOLDOUT_COVERAGE.csv | `2eccaa520421aa53` | `2eccaa520421aa53` | TRUE |
| P2_PAIRED_CLUSTER_BOOTSTRAP_VS_PAIRSUPPORT.csv | `2d1cad6d59fefa2e` | `2d1cad6d59fefa2e` | TRUE |
| P2_PROVISIONAL_CLASS_MATERIAL_SENSITIVITY_20SEEDS.csv | `e26c7a7b72bce3e7` | `e26c7a7b72bce3e7` | TRUE |

The tests concern reproducibility and documentary internal robustness, not expert-gold biological accuracy or independent external validity.

Full ZIP SHA256: `15c94317001f9b10d3788a51fa75daea1d7350e8e81ad9d7a3371ab8c76a61ef`.
