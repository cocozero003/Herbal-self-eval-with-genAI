# ThaiHerb KG: Evidence source-disjoint pilot and authentic SHACL Core release

**Date:** 2026-11-07  
**Paper 2 research version:** v1.2  
**Paper 3 research version:** v1.0  
**Manuscript scientific readiness:** NOT READY (requires independent human adjudication and historical archive/class recovery).

## Four user-requested gates

1. **100 primary full-text checks of original sources:** 100 original assertions retained and typed; only 5 original-source primary experimental full-text matches remain. The original bibliography includes reviews, so 100 original *primary* studies cannot be claimed without replacing source IDs. `results/P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv` preserves the original source status; new research never upgrades an old reference.
2. **Official pySHACL:** `src/validate_pyshacl.py` validates the authentic 208-assertion/2,733-triple M3 graph against the actual frozen SHACL shapes, followed by 10 seeded invalid mutations. It fails when pySHACL cannot be imported. `.github/workflows` runs the official release on an internet-enabled GitHub Actions runner. Use only the completed workflow log and result artifact for official claims.
3. **Independent expert gold:** 45 review candidates; all reviewer names, signatures and gold cells left blank. `src/score_gate.py` refuses scientific accuracy metrics until genuinely independent human records are provided. ChatGPT cannot sign or impersonate two human experts.
4. **Original 35 classes and external benchmark:** original 35→83 chemical map has not been recovered, so a separately versioned **31-family preliminary reconstruction** is supplied with explicit non-equivalence. An **11-record source-DOI-disjoint, positive-only, post-hoc analytic pilot** from three actual experimental studies is bundled. This is not a confirmatory external held-out benchmark; one previously used coriander study is explicitly excluded.

## Reproduce

```bash
python -m pip install -r requirements.txt
python src/build_release.py
python -m pytest -q tests
python src/score_gate.py
python src/validate_pyshacl.py
```

The last command requires real `pyshacl`, otherwise fails closed. SHA256 manifest records frozen input and authored outputs. No labels or numeric accuracy results are fabricated.

## Key data files

- `results/P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv` — all original claims with source status preserved
- `results/P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv` — 11 sample-specific GC–MS observations and exact table locators
- `results/P2_EXTERNAL_SOURCE_REGISTRY_V12.csv` — DOI/source audit and explicit prior-use exclusions
- `results/P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv` — 31 candidate families, **not original 35**
- `results/P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv` — expert review casebook with blank human gold
- `results/P3_PYSHACL_CORE_RUNTIME.json` — authentic environment status, not a simulated pass

## Contextual analytical sources (not clinical efficacy sources)

- Long, D. M., Quoc, L. P. T., Nhung, T. T. P., Thy, V. B., & Nhu, N. L. Q. (2023). Chemical profiles and biological activities of essential oil of *Citrus hystrix* DC. peels. *Korean Journal of Food Preservation, 30*(3), 395–404. https://doi.org/10.11002/kjfp.2023.30.3.395
- Sytykiewicz, H., Łukasik, I., & Goławska, S. (2026). GC-MS profiling, antioxidant and enzyme inhibitory activities of basil (*Ocimum basilicum* L.) and clove (*Syzygium aromaticum* L.) essential oils and their binary mixtures. *Molecules, 31*(18), 3292. https://doi.org/10.3390/molecules31183292
- Albaqami, J. J., et al. (2022). Chemical composition and biological activities of the leaf essential oils of *Curcuma longa*, *Curcuma aromatica* and *Curcuma angustifolia*. *Antibiotics, 11*(11), 1547. https://doi.org/10.3390/antibiotics11111547. Full author list should be verified before APA7 manuscript submission.
- Satyal, P., & Setzer, W. N. (2020). Chemical compositions of commercial essential oils from *Coriandrum sativum* fruits and aerial parts. *Natural Product Communications*. https://doi.org/10.1177/1934578X20933067 — excluded from external pilot because previous development already used it.
