# Draft methods/results addendum (author-review only)

## Paper 2. Source-type-aware claim review

A fixed, source-reviewed, 20-herb collection of 100 archived herb–compound assertions (83 distinct internal compound identifiers) was carried forward without silent addition or deletion. Each of the 20 associated publications was classified by documentary study design and taxonomic scope. These source-level labels were kept separate from claim-level evidence. Claim promotion required a named analyte in a source-specific analytical table or an accessible study/review abstract. Bibliographic identification, a correct DOI and a PubChem entity were not treated as proof of a botanical occurrence in a specified material.

Five *Piper retrofractum* analytes previously checked in Luca et al. (2021), Table 3, remained primary table matches. Five major *Zingiber montanum* essential-oil constituents remained primary abstract matches (Verma et al., 2018). A further five concinnoside names were located in the abstract of Gafur et al. (1997), but were isolated from alkaline hydrolysates of pod saponins; these were encoded as a separate transformation-dependent category, not evidence of native unprocessed phytochemical occurrence. Five *Piper nigrum* names (Ashokkumar et al., 2021) and four *Ocimum tenuiflorum* names (Bhattarai et al., 2024) were matched in review abstracts, so were assigned to secondary, abstract-level evidence. These are methodological/source-audit results, not independently confirmed chemical identities.

The final claim-status distribution in this release was: 5 primary full-text, 5 primary abstract, 5 primary abstract after hydrolysis, 9 secondary abstract, 10 pre-existing secondary review, and 66 not claim-verified. The study design breakdown of the 20 literature sources was 12 species reviews, 3 genus reviews and 5 primary or original analytical reports. The source audits were AI-assisted and not independently adjudicated. The original 35-class taxonomy and authoritative class path definitions were not recovered. External source-disjoint biological validation therefore remains unavailable.

## Paper 3. Representation parity without accuracy claims

The original V3 corpus was held at 208 unique assertion IDs (71 formula memberships, 100 chemistry occurrences, 30 pharmacology targets and 7 clinical assertions). Three projection views were generated from the same exact source records. M1 retained naive SPO edges (207 unique RDF triples); M2 retained reified assertion/source metadata (1,501 triples); M3 added archived context/directness text to assertion nodes (2,733 triples). The M1 duplicate corresponds to clinical records CLIN005 and CLIN006 sharing a subject–predicate–object while representing distinct source studies. This example demonstrates structural loss of individual evidence provenance but cannot establish semantic contradiction or clinical superiority.

Eight development competency questions were executed identically against all three RDF graphs, producing 24 deterministic output records. All expert-gold, inter-rater and accuracy fields remained blank/NOT_EVALUATED. Seven original clinical assertions retain non-canonical source-text objects, and 45 IDs occur in the dataset, against 67 historical source-registry records reported by an earlier manuscript. The mismatch cannot be reconciled without the original full reference registry.

SHACL Core validation remains **NOT_RUN** in the present local environment because pySHACL could not be installed. A standalone standards-compliant validation entrypoint and negative fixtures exist; custom graph-integrity tests should not be described as SHACL Core validation or experimental scientific truth.

## Publication scope

These results demonstrate a reproducible evidence audit and controlled graph representations. Neither external biological generalizability (Paper 2) nor comparative QA accuracy/clinical truth (Paper 3) may be claimed until independent sources and expert-adjudicated held-out questions are obtained and analyzed with a prespecified scoring protocol.

## References

Ashokkumar, K., Murugan, M., Dhanya, M. K., Pandian, A., & Warkentin, T. D. (2021). Phytochemistry and therapeutic potential of black pepper [*Piper nigrum* (L.)] essential oil and piperine: A review. *Clinical Phytoscience, 7*, 52. https://doi.org/10.1186/s40816-021-00292-2

Bhattarai, K., Bhattarai, R., Pandey, R. D., Paudel, B., & Bhattarai, H. D. (2024). A comprehensive review of the phytochemical constituents and bioactivities of *Ocimum tenuiflorum*. *The Scientific World Journal, 2024*, 8895039. https://doi.org/10.1155/2024/8895039

Gafur, M. A., Obata, T., Kiuchi, F., & Tsuda, Y. (1997). Acacia concinna saponins. I. Structures of prosapogenols, concinnosides A–F, isolated from the alkaline hydrolysate of the highly polar saponin fraction. *Chemical & Pharmaceutical Bulletin, 45*(4), 620–625. https://doi.org/10.1248/cpb.45.620

Luca, S. V., Gaweł-Bęben, K., Strzępek-Gomółka, M., Czech, K., Trifan, A., Zengin, G., Korona-Glowniak, I., Minceva, M., Gertsch, J., & Skalicka-Woźniak, K. (2021). Insights into the phytochemical and multifunctional biological profile of spices from the genus *Piper*. *Antioxidants, 10*(10), 1642. https://doi.org/10.3390/antiox10101642

Verma, R. S., et al. (2018). Chemical composition and antibacterial, antifungal, allelopathic and acetylcholinesterase inhibitory activities of cassumunar-ginger. *Journal of the Science of Food and Agriculture, 98*(1), 321–327. https://doi.org/10.1002/jsfa.8474

World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/

World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/
