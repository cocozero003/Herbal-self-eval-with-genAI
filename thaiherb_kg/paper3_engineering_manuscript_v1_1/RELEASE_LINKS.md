# ThaiHerb Paper 3 v1.1 — Complete Engineering/Methods Manuscript

**Release date:** 2026-11-07.  
**Study:** Evidence-Centric RDF Knowledge Graph for Thai Herbal Medicine: Representation Fidelity, Provenance, and SHACL Conformance.

## Verifiable release artifacts
- [Google Drive versioned folder](https://drive.google.com/drive/folders/1bp-UKpXrDDMCpBiNt8370MC-KnGBNBAm)
- [Full reproducible ZIP](https://drive.google.com/file/d/123i4IuxLSuk1G5Vtej0orZHZOpPLHbKg/view) — SHA-256 `f9022b2bdf96e2a404e00a925a7fbc32917d2a130fc7af696ec81c5825b4fd22`
- [Manuscript review ZIP](https://drive.google.com/file/d/12JsHwUeb4ZZ9THLRqkg1kmF_D1t2VWoE/view) — SHA-256 `b6c23fdcc96e06bb22b2a2d05096e842f53cb00d3f2b250f3c437c5b2688e51b`
- [Full Word manuscript](https://drive.google.com/file/d/18Wlx3lA5EsK-UE6mwLQjPHH7cJzssOaK/view)
- [Standalone interactive evidence explorer](https://drive.google.com/file/d/1Q-KX7kaCWcsQV_cOrQLP-VXDtl1SAeVb/view)
- [Actual GitHub Actions pySHACL Core PASS run](https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018)

## Reproducible outcomes
- 208 immutable V3 assertions (71 formula, 100 chemistry, 30 pharmacology-target, 7 clinical); source SHA-256 `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`
- M1/M2/M3 RDF: 207 / 1,501 / 2,733 triples.
- 624 paired source-assertion–model audit records.
- Assertion ID and source recoverability 0/208/208; evidence context 0/0/208.
- One source identity collision in naive SPO (CLIN005/006), and three unadjudicated clinical context variation groups.
- Official pySHACL 0.40.2 validation run: 0 violations, 10/10 seeded negative controls detected.
- Eight **development-only** competency questions, 24 archived query outputs. Not an independent accuracy experiment.
- 45 expert review candidates **unfilled**, 0 independent adjudicated gold.
- 14/14 regression checks; 40/40 file hashes in versioned ZIP manifest, clean rerun result byte-identical; browser UI 5 tabs, 624 entries, filtering and no JS errors.
- Full manuscript ~4,700 words, 12 rendered Word pages, two tables and four figures. Author review ready.

## Scientific guardrails
RDF field retention is a deterministic representation property and **not** evidence of M3's superior semantic QA accuracy. SHACL confirms only the project's declared structural profile. The clinical evidence source material has not been independently adjudicated and clinical object IDs remain textual. The prospective source-disjoint expert-gold benchmark is not complete. Do not cite this release as a confirmed biological/clinical validation result. Actual author approval, original source checks, ethics, funding and journal format statements remain required.

This branch is separate from `main`; the full frozen research data remain in the authorized Google Drive package, while this GitHub branch provides manuscript text, analytic code, tests and reproducibility methods.
