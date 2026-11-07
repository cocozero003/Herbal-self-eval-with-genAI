# Paper 1 — Manuscript Editorial Addendum (7 November 2026)

## Scope and status
This document is a **separate editorial addendum**, not a revised journal submission or a replacement of the existing manuscript. The originally submitted/reviewed manuscript is preserved unaltered. The v0.4 audit is based on a **single-curator, model-assisted** review of ten official DTAM/Thai FDA formula tables and original study claims.

## Source-integrity correction superseding v0.3
An earlier interim audit wrongly excluded ginger, Java long pepper, and black pepper from *ยาประสะว่านนางคำ* (F05). These ingredients appear on printed page 162, the continuation of the ingredient table beginning on page 161. The purported 46→43 correction and all downstream numerical findings premised on that deletion are **invalidated and must not be cited**.

## Formula data reanalysis
The source-reviewed selected-formula matrix comprises ten herbs × ten formula variants: 46 present memberships and 54 absences. It reproduces 23 positive-NPMI co-occurrence edges among 45 herb pairs. Formula pages: F01 1–2; F02 27–28; F03 122–123; F04 143–144; F05 161–162; F06 164–165; F07 240–241; F08 49–51; F09 71–72; F10 386–387. Source: https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

## Newly computed exploratory analysis (NOT original-paper reproduction)
Ten matched-seed reanalysis gives mean pairwise seed-rank Spearman rho: Cooc NPMI 0.932159, Cooc Support 0.955722, Cooc Degree 0.956583, Cooc Combined 0.962278, Chem V3 proxy 0.914317 and Core V3 proxy 0.755977. Algorithm implementation, walk corpora and chemistry classes differ from original archived manuscript settings and data. These metrics cannot be used to claim that v0.4 improves biological validity or replaces original manuscript results.

## Remaining requirements before a publication-grade revision
1. Independently re-check the complete 100-cell formula matrix, including absence checks, and adjudicate disagreements.
2. Locate/restore the original Paper 1 chemistry table with its 19 chemical classes and primary references, or prospectively recurate a new panel and transparently label a methodological revision.
3. Recover original model walks/vectors or explicitly treat new implementation as a separate computational reproducibility study.
4. Validate item-level herbal part/preparation/compound provenance with source-specific locators.
5. Obtain independent blinded pair-level domain expert labels and calculate task validity plus confidence intervals.

## Editorial recommendation
Retain Paper 1 as a feasibility study. Add a source-integrity methods paragraph and a carefully labeled supplemental Cooc weighting sensitivity table only after the remaining data source and independent-review gates are satisfied. Do not present Chem/Core reconstruction as direct replication of the manuscript's 19-class chemical channel.

## Literature and primary documentation
Department of Thai Traditional and Alternative Medicine & Thai FDA. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง: ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf
