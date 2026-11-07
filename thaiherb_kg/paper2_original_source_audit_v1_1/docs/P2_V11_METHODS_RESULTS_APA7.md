# Paper 2 v1.1 — Source-specific evidence integrity and material-context audit

**Research release:** 7 November 2026. **Status:** AI-assisted source audit; not an independently adjudicated scientific validation.

## Objective

Determine whether each of 100 prespecified herb–compound assertions is traceable to its **original cited document**, at a **specified level of evidentiary directness**, without changing frozen manuscript assertions or conflating an external corroborating article with the original citation. A separate taxon-name crosswalk is maintained only when an authoritative botanical name source explicitly supports it.

## Dataset and methods

The study retained the locked `data/P2_CHEM_EVIDENCE_100_v05_LOCKED.csv` (100 rows; 20 sources). Records were grouped by `source_id` and the cited DOI/URL was screened. Publication type was assigned to one of: primary analytical study, primary study with literature-review background, species-focused review, or genus-focused review. A compound-specific grade was applied only if an identifiable primary abstract, source table or full-text section linked the **same taxon and analyte**. Each assigned grade includes source URL, locator, process context and limitations. Otherwise the record stays `UNRESOLVED_CLAIM_LOCATOR`—never `ABSENT`.

Screen categories were mutually exclusive:

- `PRIMARY_FULLTEXT_EXPERIMENT`: original article contains the specific directly assessed compound in the checked analytical result table. This category retains the previously reviewed five *Piper retrofractum* assertions from Luca et al. (2021).
- `PRIMARY_ABSTRACT_EXPERIMENT`: specific original study analytes reported in an abstract or authoritative bibliographic abstract; the analytical source full text is **not** reverified in this release.
- `PRIMARY_ABSTRACT_PROCESS_DEPENDENT`: compounds isolated or produced **after a specified preparation step**; native/untreated-plant presence is **not** implied.
- `SECONDARY_FULLTEXT_REVIEW`: cited review records the compound; the review authors did **not** conduct the referenced experiment.
- `UNRESOLVED_CLAIM_LOCATOR`: source-specific evidence not checked sufficiently to classify. This does not imply a negative finding.

All evidence screening was performed with AI assistance. Blank human reviewer columns remain unfilled. Earlier original dispositions remain immutable, and independently discovered articles remain separate post-hoc corroboration records.

## Results

| Original-source screening grade | Assertions | Interpretation |
|---|---:|---|
| Primary analytical full-text section/table checked | 5 | Original-source compound-specific support from a checked table |
| Primary original study, compound-specific abstract | 10 | Original-source abstract only; no full-text table audit |
| Primary original study, hydrolysis-dependent abstract | 5 | Process-dependent products; cannot infer native plant content |
| Review text with identifiable compound-specific section/table | 19 | Secondary support, **not** original primary analysis |
| Claim locator insufficiently checked | 61 | Still open; not biological absence |
| **Total** | **100** | Mutually exclusive screening strata |

Source-level document classification: **12 species-specific reviews, 3 genus-level reviews, 4 primary analytical papers, and 1 primary experimental study with secondary background statements**. Source-level classification does not mean every analyte in that source was verified. Detailed rows are in `results/P2_SOURCE_TYPE_AUDIT_20_v11.csv` and `results/P2_ORIGINAL_SOURCE_TRACE_100_v11.csv`.

### Context-sensitive examples

1. *Piper nigrum* CA011–CA015: the archived Ashokkumar et al. (2021) reference is a **review**. Its Sections on piperine and essential oils and Tables 2–3 summarize different origins and plant parts. Review percentages must not be presented as original experiments or universal composition.
2. *Allium sativum* CA016–CA020: Shang et al. (2019), Section 2 explicitly discusses allicin, alliin, diallyl sulfide, diallyl disulfide, and ajoene. These are **secondary** review mentions, and processing may change component profiles.
3. *Zingiber montanum* CA021–CA025: Verma et al. (2018) describes rhizome hydrodistillation, GC-FID/GC-MS and five detected volatile constituents in its abstract. Study ranges are sample-dependent; full article tables remain unchecked.
4. *Wurfbainia testacea* CA056–CA060: Sirat et al. (2001) used the name *Amomum testaceum* and detected five oil constituents in hydrodistilled fruit. Royal Botanic Gardens, Kew identifies the older binomial as a **homotypic synonym**, supporting a formal taxon crosswalk; it does not generalize oil concentrations across geographic origins.
5. *Senegalia rugata* CA091–CA095: Gafur et al. (1997) used *Acacia concinna* and described concinnosides A–E in products of **alkaline hydrolysis of highly polar saponin fractions from pods**. Kew identifies the older name as a **heterotypic synonym**. These are preparation-dependent prosapogenols; do not create unqualified native plant-to-compound edges.
6. *Kaempferia galanga* CA076–CA080: Wang et al. (2021) Tables 3–4 synthesize chemistry and essential oil analyses from different locations. `eucalyptol` denotes `1,8-cineole` in that table, but these are still secondary evidence rows.
7. *Curcuma aromatica* CA096–CA100: the cited Dosoky and Setzer (2018) article reviews **multiple Curcuma species**. A genus-wide hit cannot be assumed to validate the C. aromatica assertion. These remain unresolved pending species-specific full-text tracing.

## Interpretation and publication constraints

These categories are **documentary traceability endpoints**, not validated chemical prevalence or therapeutic endpoints. The current release does not establish a complete original-source 100/100 analytical audit, expert agreement, the historical 35-class chemistry taxonomy, independent source-disjoint performance, or claim-level safety/efficacy. If a review is used to support a chemical occurrence, the manuscript must explicitly state that evidentiary tier and carry through the relevant preparation/part/origin context.

## Reproducibility and verification

Run `python -m src.original_source_screen_v11`; frozen data are not rewritten. Unit tests verify row counts, immutable original dispositions, taxon crosswalk source links, processing context and missing expert gold fields.

## References (APA 7th edition)

Ashokkumar, K., Murugan, M., Dhanya, M. K., Pandian, A., & Warkentin, T. D. (2021). Phytochemistry and therapeutic potential of black pepper [*Piper nigrum* (L.)] essential oil and piperine: A review. *Clinical Phytoscience, 7*, Article 52. https://doi.org/10.1186/s40816-021-00292-2

Gafur, M. A., Obata, T., Kiuchi, F., & Tsuda, Y. (1997). Acacia concinna saponins. I. Structures of prosapogenols, concinnosides A–F, isolated from the alkaline hydrolysate of the highly polar saponin fraction. *Chemical and Pharmaceutical Bulletin, 45*(4), 620–625. https://doi.org/10.1248/cpb.45.620

Royal Botanic Gardens, Kew. (n.d.). *Senegalia rugata (Lam.) Britton & Rose*. Plants of the World Online. https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:518300-1

Royal Botanic Gardens, Kew. (n.d.). *Wurfbainia testacea (Ridl.) Škorničk. & A.D.Poulsen*. Plants of the World Online. https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:77178292-1

Shang, A., Cao, S.-Y., Xu, X.-Y., Gan, R.-Y., Tang, G.-Y., Corke, H., Mavumengwana, V., & Li, H.-B. (2019). Bioactive compounds and biological functions of garlic (*Allium sativum* L.). *Foods, 8*(7), Article 246. https://doi.org/10.3390/foods8070246

Sirat, H. M., Hong, L. F., & Khaw, S. H. (2001). Chemical compositions of the essential oil of the fruits of *Amomum testaceum* Ridl. *Journal of Essential Oil Research, 13*(2), 86–87. https://doi.org/10.1080/10412905.2001.9699621

Verma, R. S., Joshi, N., Padalia, R. C., Singh, V. R., Goswami, P., Verma, S. K., Iqbal, H., Chanda, D., Verma, R. K., Darokar, M. P., Chauhan, A., & Kandwal, M. K. (2018). Chemical composition and antibacterial, antifungal, allelopathic and acetylcholinesterase inhibitory activities of cassumunar-ginger. *Journal of the Science of Food and Agriculture, 98*(1), 321–327. https://doi.org/10.1002/jsfa.8474

Wang, S.-Y., Zhao, H., Xu, H.-T., Han, X.-D., Wu, Y.-S., Xu, F.-F., Yang, X.-B., Göransson, U., & Liu, B. (2021). *Kaempferia galanga* L.: Progresses in phytochemistry, pharmacology, toxicology and ethnomedicinal uses. *Frontiers in Pharmacology, 12*, Article 675350. https://doi.org/10.3389/fphar.2021.675350
