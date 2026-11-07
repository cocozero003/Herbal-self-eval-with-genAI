# Paper 2 v1.0: Source-specific corroboration and context integrity (author-review methods/results)

**Dataset boundary.** The original 20-herb panel contains 100 fixed herb–compound assertions with a separately frozen 74-membership species-level formula revision. This v1.0 release does not alter the previously audited 100-claim table, original source assignment, the unavailable historical 35-class taxonomy, model scores, or expert gold. Its contribution is a provenance-preserving independent-source corroboration layer and the caution queue for one previously assigned experimental publication.

## Additional primary analytical evidence

Five compound-occurrence assertions concerning *Coriandrum sativum* (CA066–CA070) were cross-referenced to a separate primary study by Satyal and Setzer (2020). The authors analyzed commercial fruit essential oils (coriander) and herb essential oils (cilantro) as different materials. In Table 3, among the commercial **fruit essential-oil** compositions, linalool was reported at 71.9% overall (62.2–76.7%), geraniol 1.4% (0.1–4.1%), limonene 2.1% (0.2–2.9%), and camphor 4.0% (0.0–5.5%). These percentages are composition percentages in analyzed commercial oils, **not** concentration per gram of fresh plant, a therapeutic dose, or a fixed value for all specimens. Terpinen-4-ol was demonstrated by **chiral GC–MS** as reported in Table 4. For sample 191118B, the (+):(−) enantiomer distribution was 80:20; this ratio is **not** terpinen-4-ol concentration in the oil (Satyal & Setzer, 2020). The same work raised potential adulteration in certain commercial samples, strengthening the material-specific caveat.

These five records are explicitly named **additional, source-independent corroborations**. They neither retroactively verify each herb–compound assertion's originally cited publication nor provide a predeclared external test dataset. The four prior separate corroborations from v0.9 remain distinguishable. Across both releases, nine different original claim IDs have at least one added source-specific corroboration, while only five original-source claims retain `PRIMARY_FULLTEXT_MATCH` status. This does not imply that the other 95 are biologically false.

## Context-warning queue

The archived original source for five *Plumbago indica* assertions is Selim et al. (2022), which contains experimental LC–MS/MS analysis of **70% ethanol extracts from aerial parts**. Its introductory section also mentions prior phytochemical literature, including plumbagin, elliptinone, droserone, and zeylanone, which cannot automatically be counted as compounds directly detected in the paper's own Table 1. All five assertions (CA086–CA090) remain in a **manual original-table review queue**. No species-level negative conclusion was drawn, and no new source-specific full-text positive status was assigned without adjudication. Drug efficacy or antifibrotic findings from a rat model cannot validate the five particular chemistry occurrences or human clinical effects (Selim et al., 2022).

## Reproducibility and analysis rules

The script `src/stage_v10.py` reads the frozen v0.9 claim table and writes two independent-source/clarification CSVs, preserving all original `disposition` values unchanged. The 100-row ledger documents source lineage and flags post hoc source discovery. Every new record includes source DOI/URL, exact locator, analysis method, plant material, denominator and limitations. No missing quantity was inferred. There is no two-reviewer curation panel, source-disjoint held-out benchmark, nor demonstrated generalizability.

## References (APA 7)

Satyal, P., & Setzer, W. N. (2020). Chemical compositions of commercial essential oils from *Coriandrum sativum* fruits and aerial parts. *Natural Product Communications, 15*(7). https://doi.org/10.1177/1934578X20933067

Selim, N. M., Melk, M. M., Melek, F. R., Saleh, D. O., Sobeh, M., & El-Hawary, S. S. (2022). Phytochemical profiling and anti-fibrotic activities of *Plumbago indica* L. and *Plumbago auriculata* Lam. in thioacetamide-induced liver fibrosis in rats. *Scientific Reports, 12*, Article 9864. https://doi.org/10.1038/s41598-022-13718-9
