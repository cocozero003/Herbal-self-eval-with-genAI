# ThaiHerb Paper 1: Source-Integrity Restoration and Exploratory Model Reanalysis (v0.4)

**Date:** 7 November 2026  
**Research subject:** Evidence-channel-specific graph embeddings for Thai herbal medicine: a provenance-aware ten-herb pilot  
**Scientific status:** Formula projection source-reviewed, chemistry/Core exploratory; **not yet publication-ready**.

## Executive summary

The official Department of Thai Traditional and Alternative Medicine (DTAM)/Thai FDA 2023 reference-formula compendium was reviewed across **all ingredient-table pages** for the **ten specified formula variants**. The ten-focal-herb projection comprises **46 present and 54 absent** pairings in a 10×10 formula–herb matrix. These 46 memberships correspond to the previously archived V3-derived projection and yield **23 positive NPMI herb-pair edges** from 45 possible pairs. This is a single-curator, model-assisted source review; an independent second reviewer has not yet adjudicated it.

The previous v0.3 deletion of ginger, Java long pepper, and black pepper from `F05_DTAM2566` was erroneous because the formula's ingredient list continues from **printed page 161 to 162**. All three are explicitly listed on page 162 (ingredient rows 10, 12 and 13). **All v0.3 performance changes based on that deletion must be treated as invalidated diagnostic outputs and excluded from scientific conclusions.** This is a source-reading issue, not a biological inference. See official source URL below.

The chemistry panel extracted from the V3-linked bootstrap has 30 herb–compound assertions, three per herb, and 25 distinct compound strings, matching manuscript *counts*. However, the original manuscript's manually curated **19-class mapping** and the original model vectors/walk corpora were not recovered. We therefore performed a **new, explicitly exploratory reconstruction** of Chem/Core using a candidate 18-class mapping and did not label the resulting embeddings as reproductions of the manuscript.

## Primary source and data scope

Department of Thai Traditional and Alternative Medicine & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง: ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

| ID | Official formula and dosage form | Source printed pages | Focal-herb count |
|---|---|---|---:|
| F01 | ยาธาตุบรรจบ ชนิดผง | 1–2 | 3 |
| F02 | ยาประสะกะเพรา ชนิดผง | 27–28 | 7 |
| F03 | ยาไฟประลัยกัลป์ ชนิดผง | 122–123 | 7 |
| F04 | ยาประสะไพล ชนิดผง | 143–144 | 6 |
| F05 | ยาประสะว่านนางคำ ชนิดผง | 161–162 | 5 |
| F06 | ยาปลูกไฟธาตุ ชนิดแคปซูล | 164–165 | 4 |
| F07 | ยาแก้ไอ ขับเสมหะ สูตร 2 ชนิดผง | 240–241 | 5 |
| F08 | ยามหาจักรใหญ่ ชนิดผง | 49–51 | 3 |
| F09 | ยาวิสัมพยาใหญ่ ชนิดผง | 71–72 | 3 |
| F10 | ยาทาพระเส้น ชนิดผง | 386–387 | 3 |

**Important:** Only the ten designated focal herbs are represented. The above counts are not total ingredients of each formula. Source PDF page indices are printed page + 8 (0-based). Clinical usage directions in the compendium were not added as training labels.

## Methodology

1. Build the 100-cell binary matrix by reviewing every ingredient table for the ten designated source versions, including continuations.
2. Compute NPMI over the ten **formula records**, not the number of individual herb occurrences. Set nonpositive NPMI to zero for the positive-edge random-walk projection. This yields 23 positive links.
3. Compare original positive NPMI with support-weighted, degree-adjusted, and combined positive-NPMI Cooc projections (10 matched random seeds, 32-dimensional skip-gram, 60 walks per focal herb, maximum walk length 20).
4. For Chem/Core, use the **V3-derived 30-compound proxy** and newly assigned chemical-class labels to rebuild a typed motif walk model (`H-C-H` and `H-C-K-C-H`). The rebuilt class mapping contains 18 classes, not the 19 classes reported in the manuscript. Treat all model results as exploratory reconstructions.
5. No therapeutic activity, biological similarity truth, source-specific chemical assay claims, or clinical validity are inferred from cosine similarity.

## Results: newly rerun model stability (NOT manuscript-reproduction metrics)

| Model/projection | Mean Spearman rho of all 45 pairs of seed runs | SD | Interpretation |
|---|---:|---:|---|
| Cooc–Original positive NPMI | 0.932159 | 0.026501 | Reimplementation from the source-reviewed formula projection |
| Cooc–Support adjusted | 0.955722 | 0.017159 | Sensitivity: n/(n+2) shrinkage |
| Cooc–Degree corrected | 0.956583 | 0.015627 | Sensitivity: positive-edge hub correction |
| Cooc–Combined | 0.962278 | 0.012503 | Sensitivity: support and hub correction |
| Chem–Proxy | 0.914317 | 0.025000 | Newly reconstructed candidate compound taxonomy |
| Core–Proxy | 0.755977 | 0.052626 | Newly reconstructed combined walk sampler |

All numbers above come from `results/embedding_cosine_45pairs_10seeds.csv` and `results/embedding_10seed_summary.csv`; no held-out gold-standard metric has been calculated. Avoid comparing numerical differences to original manuscript stability as evidence of superiority because walk implementations, source panels and class taxonomy differ.

### Original manuscript's reported reference values, preserved without rewriting history

The existing paper reported seed-rank Spearman rho Cooc **0.946**, Chem **0.977**, Core **0.945**. These were *not recalculated from original archived vectors* here. Do not silently replace original values with new reconstruction values in the existing manuscript.

## Source verification and reproducibility gates

| Criterion | State | Proof / remaining task |
|---|---|---|
| Formula identities and dosage forms | Source-reviewed | Ten official printed formula sections and forms |
| 100 candidate herb–formula decisions | Single-curator reviewed | `results/formula_herb_100_matrix.csv`; needs independent adjudication |
| 46 focal-herb positive formula memberships | Source-reviewed | Source locators and raw names in crosswalk; v0.3 deletion retracted |
| 23 positive Cooc NPMI edges | Recomputed | `results/npmi_45pairs.csv` |
| Chemistry 30 rows / 25 compound strings | Recovered as V3 proxy | `results/chemistry_panel_30_exploratory.csv`; no original row equivalence claim |
| Original 19 compound classes | **MISSING** | Must recover paper archive or independently recurate and declare new methods |
| Original skip-gram vectors and walk corpora | **MISSING** | Reproduction of reported seed outcomes not established |
| Item-level compound source/plant-part evidence | **PENDING** | Requires primary article/assay locator for each row |
| Independent herb-pair biological validation | **NOT PERFORMED** | Template provided; expert adjudication needed |
| Publishing rights and authoritative PDF snapshot/hash | **NOT LOCKED** | Source URL provided; original 433-page PDF not redistributed |

## Retraction of an earlier internal finding (v0.3)

The v0.3 partial-correction experiment described three F05 co-occurrence edges as absent and reported a drop from 46 to 43 memberships. This was a **false-negative source verification** caused by incomplete pagination. The F05 section begins on printed page 161 but its ingredients continue on page 162. The prior v0.3 case is preserved as an audit history artifact and should **not** be cited as a genuine data-cleaning improvement. The correct v0.4 source-reviewed projection retains 46 memberships.

## Recommended paper positioning

Keep Paper 1 as a ten-herb feasibility study and disclose data-selection limitations. Use the v0.4 source-integrity audit to strengthen documentary traceability and to develop a supplemental sensitivity table. Do not claim a newly demonstrated biologically superior weighting scheme or higher clinical validity without an independent reference standard. The original chemistry classes should be found before finalizing a fully reproducible manuscript or used only after creating a clearly distinct, prospectively versioned protocol.

## APA 7 references (selected)

Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง: ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. In *Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 135–144). https://doi.org/10.1145/3097983.3098036

Grover, A., & Leskovec, J. (2016). node2vec: Scalable feature learning for networks. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 855–864). https://doi.org/10.1145/2939672.2939754

World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/
