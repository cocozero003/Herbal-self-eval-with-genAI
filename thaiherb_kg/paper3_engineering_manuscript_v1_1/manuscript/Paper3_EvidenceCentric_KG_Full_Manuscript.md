# An Evidence-Centric RDF Knowledge Graph for Thai Herbal Medicine: Reproducible Evaluation of Representation Fidelity, Provenance, and SHACL Conformance

**Manuscript type:** Original research — biomedical knowledge representation / methods and resource evaluation  
**Status:** Full author-review manuscript; independent semantic validation not completed  
**Version:** Paper 3 v1.1, 7 November 2026  
**Authors:** [To be completed and approved by the research team]  
**Affiliations and corresponding author:** [To be completed by authors]

## Abstract

**Background:** Herbal knowledge graphs integrate evidence from historical formula documents, phytochemistry reports, pharmacological experiments, and clinical studies. However, a single unqualified subject–predicate–object (SPO) statement may obscure the provenance, assay context, and evidentiary directness required for cautious interpretation.

**Objective:** To evaluate the deterministic representation fidelity, source traceability, contextual qualification, and standards-based structural validation of three RDF representations of the same frozen Thai herbal evidence corpus. This engineering study did not seek to establish clinical efficacy or independently adjudicated question-answer accuracy.

**Methods:** A frozen collection of 208 evidence assertions (71 formula membership, 100 chemistry, 30 pharmacology-target, and seven clinical) linked to 45 source identifiers was projected into (M1) naive SPO triples, (M2) assertion-identified, provenance-aware RDF, and (M3) evidence- and context-qualified RDF. All graphs were re-parsed and compared at the individual source-assertion level using an audit of 624 assertion–model rows. We measured reconstruction of original relationships and recoverability of assertion identity, provenance, evidence mode, directness, and contextual text. We separately performed field-deletion ablation, inspected clinical context-variation candidates, and verified an authentic pySHACL Core validation run and ten deliberately malformed controls. Eight development competency questions were retained as unscored demonstrations; no human-derived reference answers were constructed.

**Results:** The graphs contained 207, 1,501, and 2,733 distinct triples for M1, M2, and M3, respectively. All 208 input relationship rows could be located in each representation, although two clinical assertions collapsed into one SPO in M1. Individual assertion identities and source links were recoverable for 0/208, 208/208, and 208/208 input rows for M1, M2, and M3. Evidence mode, directness, and contextual text were recoverable for 0/208, 0/208, and 208/208 rows, respectively. Three clinical topic-level groups involving seven assertions exhibited context-dependent differences requiring expert review, not confirmed biological contradiction. Official pySHACL 0.40.2 returned conformity on the project’s 34-triple SHACL shapes graph, with zero validation violations; all ten intentional structural errors were detected. An independently adjudicated expert gold standard was unavailable (0/45 candidate review cases).

**Conclusions:** First-class evidence assertions and contextual qualifiers are a reproducible way to preserve source identity and interpretation-relevant metadata in a heterogeneous herbal knowledge graph. The observed capability improvements are design-dependent representation results and require larger graph storage. They do not demonstrate superior answer accuracy, stronger therapeutic evidence, or validated contradictions. A future, source-disjoint, expert-adjudicated evaluation is necessary before comparative semantic or clinical claims can be made.

**Keywords:** herbal medicine; knowledge graph; RDF; provenance; PROV-O; SHACL; evidence assertions; ontology evaluation; representation fidelity; Thai traditional medicine

## 1. Introduction

Traditional herbal knowledge is not a homogeneous set of binary facts. A prescription formula may identify a named medicinal material but leave preparation details unspecified. A phytochemical review may associate an ingredient with a compound without reporting that compound in the specific medicinal preparation used in a clinical study. An isolated-molecule receptor assay, a preparation-level functional assay, and a human endpoint study support different kinds of inferences, even when their graphical objects or target labels coincide. This creates a representational problem: an unqualified relationship such as *herb—contains—compound* or *compound—acts on—target* may be easier to search than to interpret responsibly.

Knowledge graphs provide graph-based identifiers and relations that can integrate heterogeneous sources (Hogan et al., 2021). RDF, in particular, separates relations into explicit triples, but the RDF data model does not itself require a publication locator, preparation condition, source-specific assertion identity, or epistemic qualifier. The W3C PROV-O ontology provides a standardized language for representing provenance relations, while the Shapes Constraint Language (SHACL) defines a formal mechanism for checking data graphs against expected graph patterns (World Wide Web Consortium [W3C], 2013, 2017). The FAIR Guiding Principles similarly emphasize reusable metadata and qualified inter-resource references rather than treating data availability alone as a guarantee of data quality (Wilkinson et al., 2016).

Yet a graph can pass structural tests while retaining misleading labels, conflating distinct studies, or omitting important contextual dimensions. Therefore, structural conformance, deterministic representation retention, historical source verification, and independent answer evaluation must be treated as different outcomes. In the Thai herbal project, prior methodological work assembled a frozen V3 corpus integrating four evidence channels. This corpus had also been represented historically using different projection versions; older manuscript claims about graph sizes and source registries are not substituted for reproducible results from the present freeze.

We investigated three increasingly qualified RDF representations: (M1) a naive SPO baseline, (M2) a provenance-aware representation with explicit assertion resources, and (M3) an evidence-centric representation that additionally stores evidence mode, interpretive directness, contextual source text, original status, and limitations. The choice of features reflects specific deficiencies in the information retained by simple SPO statements; it is not intended to provide three independently optimized prediction systems.

The primary research question was: **Which source-level properties survive the mapping from 208 frozen evidence assertions to these three RDF models?** Secondary questions concerned the trade-off in RDF graph size, recovery of multiple source claims sharing the same SPO, sensitivity to removal of context/provenance qualifiers, and structural conformity to a published project-specific SHACL profile. An exploratory, development-only set of competency questions illustrates the kinds of queries that require evidence qualifiers. Because no independent expert adjudication exists, we do not test a hypothesis that M3 produces more accurate scientific answers than M1 or M2.

## 2. Materials and Methods

### 2.1 Study design and frozen source corpus

This was a retrospective, deterministic representation- and integrity-audit study using one previously curated, frozen ThaiHerb EvidenceKG V3 source table. The source dataset was immutable during evaluation, contained 208 distinct assertion identifiers, and had SHA-256 `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`. The four channels were formula/documentary membership (71), source-reported herbal chemistry (100), pharmacology-target (30), and clinical evidence (seven). Source records referenced 45 distinct identifiers. These are source identifiers in a curated project registry; they are not equivalent to 45 independently verified full-text studies.

Each source row contained an assertion identifier, subject and object labels/IDs, a predicate/topic, evidence mode, directness or direction, source identifier, a source locator or context statement, an original annotation/status, and a limitation or finding. The frozen projection did not expand the 71 original V3 formula assertions to the 74 memberships in a different Paper 2 dataset version. All seven clinical assertions lack original canonical object IDs and retain source-grounded text rather than receiving invented biomedical concept IDs. The difference in source versions is treated as a freeze boundary, not silently reconciled during analysis.

### 2.2 Representation models

**M1 — naive SPO.** The original subject and object terms were connected by the source predicate directly. Identical triples were merged under RDF set semantics. This model prioritizes simple graph traversal, but no source-level assertion identifier, evidence mode, or source locator accompanies an edge.

**M2 — provenance-aware assertion nodes.** Each row became a first-class `EvidenceAssertion` resource with a stable `dcterms:identifier`, typed subject/predicate/object fields, evidence channel, and `prov:wasDerivedFrom` source link. The source-document node is typed as a project `SourceDocument`. These are RDF encoding properties, not independently curated proof of the source content.

**M3 — contextualized evidence assertions.** M3 retained the M2 core and added project properties for `evidenceMode`, `directness`, `contextText`, `objectLabel`, `originalStatus`, optional `limitationText`, and flags for noncanonical clinical objects. The values were carried from the frozen annotation table; the projection did not automatically verify every label against full text or convert every context phrase into normalized ontology entities.

All three graphs were parsed using RDFLib. The graphs contained 207 (M1), 1,501 (M2), and 2,733 (M3) distinct RDF triples. These measured graph sizes describe the current version, not the historical V3 graph sizes described in earlier draft documents. The graph stores are semantically distinct by construction, and their triple counts should not be interpreted as a controlled study of query engine optimization or prediction power.

### 2.3 Structural fidelity metrics

For each of the 208 original assertion rows and each model, we attempted to recover the corresponding subject–predicate–object relationship, then tested whether the graph explicitly retained the following: (a) the original assertion identifier; (b) source provenance; (c) evidence mode; (d) the directness/direction label; and (e) contextual source text. We also recorded original status, optional limitation text, and an explicit flag for uncanonicalized clinical objects. This produced 624 (208 × 3) deterministic audit records.

For M1, relationship presence was tested by direct RDF triple membership using the corresponding terms in the M3 projection. For M2/M3, relationship presence was tested through the subject, predicate, and object properties on the assertion resource, rather than through a direct SPO triple. Accordingly, the relationship measure represents **recoverability of the input relation**, not identical graph traversal syntax. For M1, the same single triple can satisfy two source rows if they share the same SPO; therefore, row-level relation recoverability can equal 208 even when unique triples equal 207.

Field-retention denominators were the 208 source rows; `limitationText` was optional and assessed as a separate availability measure. Structural fields present on assertions do not establish that their factual content is correct. The metrics were computed as complete-corpus counts, not estimates from independent random samples; consequently, no confidence intervals or significance tests were applied to model-defined capability differences.

### 2.4 Qualifier deletion and semantic boundary checks

We performed a deterministic property-deletion sensitivity analysis in M3 by omitting source provenance, evidence mode, directness, or context text, each separately and once jointly. We then counted the remaining recoverable qualifier fields over all 208 assertion nodes. This is an engineering intervention intended to confirm dependency on metadata design; it is not a test that readers or language models would answer correctly with or without these properties.

Clinical evidence statements were grouped by `(subject_id, predicate_or_topic)`. Candidate review groups were selected when at least two distinct source assertions shared that topic but had more than one `directness_or_direction` label. We preserved population, preparation, treatment duration, comparator, endpoint, and other context strings to aid review. A differing label was **not** automatically declared a biological contradiction. Material identity cases involving fruit versus gall or seed versus aril were treated as additional semantic caution examples, not proven inferences in a normalized material ontology.

### 2.5 SHACL Core evaluation

An authentic, completed GitHub Actions run executed official `pySHACL` version 0.40.2 using RDFLib 7.6.0 and Python 3.11.18, with the frozen M3 graph and the project-specific 34-triple SHACL shapes graph. Validation used SHACL Core with no entailment, no advanced features, and no simulated replacement for the standards engine. The project profile required exactly one literal identifier; subject and predicate IRIs; one object; a channel literal; and a provenance IRI pointing to a typed `SourceDocument`. A standard RDF validation report and runtime metadata were saved. Ten distinct artificial graph mutations targeted missing required properties, node-kind mismatches, missing source class, and excess identifiers. The runner failed closed on undetected mutations.

Passing this selected SHACL profile is not a claim that all scientifically relevant requirements are modeled. In particular, the profile does not ensure the chemical source is primary, verify a plant-part term, test a standardized dose constraint, confirm a drug-target binding assay, or resolve disagreements between clinical sources.

### 2.6 Competency questions and confirmatory benchmark eligibility

Eight previously authored development competency questions cover taxonomy, medicinal material/preparation, formula membership/version, chemistry, target directness, clinical context, potential context discordance, and safety/regulatory uncertainty. The archived query engine produced 24 model-specific development outputs (eight × three). Those outputs were retained only to demonstrate differences in graph-query expressiveness and appropriate abstention; they are not independent test results or human-graded answers.

A separate review file contains 45 proposed cases (32 earlier development questions, 11 post hoc external analytical positives, and two contextual traps). None has two genuinely independent completed reviewer assessments and adjudicated gold (0/45). The external analytical positives are insufficient as a source-disjoint confirmatory test because they were selected after observing the development system and lack a representative set of expert-confirmed negative examples. Accordingly, we report **no** answer accuracy, citation precision, semantic recall, false-support rate, agreement coefficient, or external generalizability estimate. An independently scored protocol is specified as future work.

### 2.7 Reproducibility, testing, and analysis plan

All counts were generated by rerunning an independent Python audit against the frozen CSV and the three TTL graphs. Assertions are enumerated without requiring any external network access. Outputs include a 624-row assertion-level CSV, model-level and evidence-channel summaries, one SPO collision audit, a three-group clinical context queue, qualifier ablation, and a 24-row development query index. The repository contains the validation script, tests, original input hashes, and machine-readable results. The historical authentic pySHACL run is linked with its original CI log and artifact; we did not repeat an unavailable local pySHACL package with a substitute library and claim a new conformance run.

## 3. Results

### 3.1 Corpus and graph dimensions

The frozen corpus comprised 71 formula, 100 chemistry, 30 pharmacology-target, and seven clinical assertions (total, 208) linked to 45 distinct source identifiers. Among the pharmacology-target records, 26 were annotated as direct compound-target assertions, three as functional target associations, and one as a preparation-target assertion. These provenance roles were source-table annotations; the current analysis did not re-adjudicate the underlying biological assays. The M1, M2, and M3 graphs contained 207, 1,501, and 2,733 unique triples, respectively (Table 1, Figure 2). M3 thus had approximately 13.20 times the RDF triple count of M1 and 1.82 times that of M2.

**Table 1. Frozen corpus, graph size, and recovery of original source-assertion information**

| Attribute | M1 naive SPO | M2 provenance-aware | M3 evidence-centric |
|---|---:|---:|---:|
| Distinct RDF triples | 207 | 1,501 | 2,733 |
| Input relationship rows recoverable | 208/208 | 208/208 | 208/208 |
| Source assertion IDs recoverable | 0/208 | 208/208 | 208/208 |
| Source provenance recoverable | 0/208 | 208/208 | 208/208 |
| Evidence mode recoverable | 0/208 | 0/208 | 208/208 |
| Evidence directness/direction recoverable | 0/208 | 0/208 | 208/208 |
| Context text recoverable | 0/208 | 0/208 | 208/208 |
| Limitation text recoverable | 0/208 | 0/208 | 185/208 |
| Noncanonical clinical object flagged | 0/7 | 0/7 | 7/7 |

*Note.* All denominators refer to frozen source assertions. Recoverability describes RDF encoding only and must not be interpreted as source quality, biomedical correctness, or independent answer accuracy. For the noncanonical flag, the denominator is the seven clinical records. M1 relationship recovery is row-based despite one duplicated SPO edge.

### 3.2 Preservation of identity, provenance, and context

All 208 original relationships could be recovered in all three representations under the model-specific decoding procedure. However, the identities of the original source assertions and their provenance were absent from M1, present for 208/208 source rows in M2, and present for 208/208 in M3 (Figure 1). M3 additionally retained all 208 evidence mode, directness, context text, and original status values. The 23 absent optional limitation-text values were not imputed.

The difference arises directly from the data models: M1 does not encode assertion identifiers, M2 does not encode contextual qualifiers, and M3 does. Therefore, these results are meaningful as an audit of **information retained under projection**, but would be circular if used as a significance test of M3's superior general scientific accuracy. The 45 source IDs represent linked project-source entities, not per-assertion verified primary-full-text citations.

### 3.3 Loss of source-level uniqueness under naive SPO encoding

The frozen corpus contained 207 distinct SPOs for 208 input assertions. The sole collision involved `CLIN005` and `CLIN006`, which shared the same subject, predicate, and object but were associated with different clinical sources and contextual interpretations. M1 encoded them as one triple, while M2 and M3 retained two assertion resources. The corresponding clinical context strings reported different populations and dosing conditions, including a short-term study and a chronic dosing study. The collision demonstrates loss of **source-specific evidence identity**, not proof that the studies contradict one another or that either result is correct.

### 3.4 Clinical context variation and need for expert assessment

Three topic-level groups spanned all seven clinical assertions (Table 2; Figure 4). These concerned ginger in chemotherapy-related nausea/vomiting (two source assertions), garlic and LDL cholesterol (two), and ginger/platelet aggregation (three). The clinical direction or synthesis labels differed within each group. All three groups were classified as **review candidates** requiring independent assessment of medicinal preparation, dose, population, study design, comparator, and endpoint. No formal contradiction or therapeutic conclusion was assigned.

**Table 2. Clinical source-context review candidates (not validated contradictions)**

| Subject and topic | Assertion IDs | Sources / assertions | Review interpretation |
|---|---|---:|---|
| Ginger: chemotherapy-induced nausea/vomiting | CLIN001; CLIN002 | 2 / 2 | Different supportive and no-additional-benefit annotations; check population and regimen |
| Garlic: LDL cholesterol | CLIN003; CLIN004 | 2 / 2 | Opposite annotations; evaluate trial population, preparation and follow-up |
| Ginger: platelet aggregation | CLIN005; CLIN006; CLIN007 | 3 / 3 | Short-term inhibition, chronic null result, and review synthesis differ in study context |

*Note.* The source dataset's clinical outcome objects are textual rather than canonical biomedical endpoint identifiers. Topic alignment is a curator-derived grouping and should not be treated as an independently verified outcome synonym mapping.

### 3.5 Qualifier ablation and development competency queries

Removing each M3 evidence qualifier caused the corresponding recoverable field to fall from 208/208 to 0/208 while leaving unremoved fields recoverable. Removing source provenance, evidence mode, directness, and context together eliminated all four categories (Figure 3). This is a deterministic dependency check, not a causal demonstration that source information increases answer quality. The model retained its source assertion rows and relation terms despite loss of these qualifiers.

The eight previously defined competency questions produced 24 archived development outputs. Edge discovery was available from all three models for questions about formula membership and reported chemistry. Only representations containing provenance returned per-assertion sources. The question about direct pharmacological action could be qualified using M3's directness field; queries requiring material parts could not be fully answered by any model because the frozen source graph lacked the required canonical material identifiers. All three models appropriately avoided asserting regulatory approval in a graph that did not represent regulatory authorization evidence. These illustrative outcomes were not compared against an independent human reference set.

### 3.6 Authentic SHACL Core validation

The completed GitHub Actions run passed official pySHACL Core validation for the project-specific constraint shapes. The runtime report identified 208 frozen M3 assertion resources, 2,733 data triples, a 34-triple shapes graph, `sh:conforms = true`, and zero violation results. The validator detected all ten planted structural violations, including missing identifiers, missing source/provenance, malformed node kinds, absent source typing, and duplicate identifiers. The complete validation output, environment version, source hashes, GitHub run ID, and artifact were preserved as machine-readable and human-readable evidence.

### 3.7 Benchmark readiness and unresolved evidence-quality issues

The blinded review register contains 45 entries but zero independently adjudicated gold labels. Consequently, the protocol disallows a reported independent accuracy comparison across M1, M2, and M3. Moreover, the source corpus includes phytochemical assertions whose original citations have not uniformly been confirmed against primary compound-specific full text; some are review-based. Seven clinical object identifiers are intentionally uncanonicalized. The existing contextual qualifiers are often literal strings rather than normalized plant part, preparation, dose, comparator, and population nodes. These represent bounded data-model limitations rather than exceptions to the measured SHACL result.

## 4. Discussion

### 4.1 Principal contribution: preserving the identity of evidence, not merely relationships

The most important finding is that a naive SPO projection of the frozen Thai herbal corpus retained 207 unique relationships but did not retain recoverable per-source evidence identity. Moving to explicit assertion resources preserved source separation and `prov:wasDerivedFrom` lineage. Adding contextual qualifiers then made evidence mode and interpretive directness available for source-specific review. This architecture is consistent with provenance-aware semantic-web principles: the meaning and trustworthiness of a claim depend not only on its graph relation, but on which source made the claim and under what conditions it was reported (W3C, 2013; Wilkinson et al., 2016).

The study provides a concrete example, the CLIN005–CLIN006 collision, in which two distinct sources become graphically indistinguishable under naive SPO modeling. A source-aware representation can prevent that information loss even without yet resolving the scientific interpretation of the two studies. The evidence-centric representation allows a curator or automated tool to surface source differences rather than silently collapsing them.

### 4.2 Why these results are not independent answer-accuracy improvements

Retention counts are calculated from properties explicitly present or absent in each model. The 208/208 contextual retrieval result for M3 therefore reflects a successful serialization choice, not a blinded model superiority experiment. Neither clinical benefit nor safety follows from graph conformance; a perfectly structured graph can faithfully encode a false or weakly supported source claim. Similarly, the eight development competency questions were known to the project before the present audit. Their 24 outputs demonstrate query mechanics but cannot support confirmatory accuracy comparisons or inferential statistical tests. Such a comparison requires an independent outcome-definition protocol, gold answers adjudicated by real experts, and a prospectively locked, source-disjoint evaluation set.

### 4.3 Graph complexity and interpretability trade-offs

M3 stored 2,733 triples compared with 207 in M1. The greater representational richness comes with larger serialization and additional graph-query complexity. Our analysis did not measure server-level storage, distributed query planning, or operational latency under standardized database deployments, so graph-size ratios should not be mistaken for a measured runtime overhead. However, they highlight the cost of supporting audit trails and contextual metadata. A future deployment should benchmark operational throughput and user-facing retrieval experience separately from semantic correctness.

### 4.4 Clinical contradiction is a review task

All seven clinical evidence assertions could be grouped into three topics showing differing original evidence-direction labels. Differences in population, exposure, duration, or endpoint can explain apparent opposition without a direct logical contradiction. M3 retains the original contextual text to support this comparison, but the current V3 graph does not formally encode enough standardized trial attributes to determine contradiction automatically. A scientifically defensible contradiction engine should distinguish (a) equivalent context and incompatible effect statements, (b) heterogeneous conditions producing apparently different outcomes, and (c) indeterminate comparisons pending additional source review. No present group was adjudicated into category (a).

### 4.5 SHACL as a testable structural contract

The completed official pySHACL run is stronger evidence than custom Python assertions alone. It produced a recognized SHACL validation report and correctly rejected ten planted faults. Yet the current shapes profile is intentionally narrow: it checks the presence and types of a small set of properties, not comprehensive botanical or clinical semantics. For future versions, new SHACL shapes should cover material identities, specified medicinal plant part and preparation, typed assay context, target relation type, stable canonical identifiers, and controlled vocabularies. These new shapes must be versioned and separately tested rather than retroactively declared supported by this run (W3C, 2017).

### 4.6 Relationship to Paper 2

Paper 2 evaluated internal robustness, source sensitivity, and representation stability for a 20-herb/10-formula embedding study. The present Paper 3 addresses a different methodological object: preservation of evidence-assertion identity and provenance across RDF representations, and standards-based structural constraints. Paper 3 uses 71 frozen V3 formula membership assertions, whereas the later Paper 2 freeze included 74 curated memberships. These versions were not merged in order to avoid changing the 208-assertion evidence projection. To avoid duplicate publication, neither manuscript should present shared source inventory as an independent new sample or reuse figures as if they were separate experiments.

### 4.7 Limitations

This was a single, modestly sized, project-curated corpus (208 assertions, 45 source identifiers), and the historical source review quality varies across channels. Context is carried largely as free text and has not been fully normalized to standard clinical and botanical ontologies. The current three-way comparison is structurally predetermined by projection design; no significance test of field presence is justified. The SHACL shapes graph contains only 34 triples and tests a subset of intended semantic constraints. The 10 negative controls are engineered faults, not an exhaustive conformance suite. The eight competency questions were developmental, and the 45 proposed independent-review cases have zero adjudicated gold answers. The 11 external analytical examples were selected post hoc and should not be used as confirmatory external validation. Finally, this work does not assess harms, interventions, clinical effectiveness, regulatory authorization, or query latency under production conditions.

### 4.8 Next validation steps before a stronger comparative claim

Before claiming that M3 answers herbal questions more accurately, the study team should lock a representative source-disjoint test corpus with positive, negative, and ambiguous questions; select reviewers with documented expertise; gather two blinded reviews and independent adjudication; define unit-of-analysis and denominator rules; record systems' outputs before opening gold labels; and report answer support, citation correctness, hallucination/unsupported claims, abstention appropriateness, and latency with paired uncertainty estimates. The same source snapshots, retrieval permissions, answer templates and latency environment should be applied across all three models. A separate source-level primary-text audit is also needed for claims used in clinical interpretation. Until then, a narrower claim of reproducible representation and structural integrity is the scientifically appropriate conclusion.

## 5. Conclusion

Within a frozen collection of 208 Thai herbal evidence assertions, an evidence-centric RDF representation retained assertion identifiers, source provenance, evidence roles, and context metadata that a naive SPO graph could not express. A provenance-aware intermediate model preserved source identity but not the same contextual qualifiers. An authentic pySHACL Core run confirmed structural conformity to the project's declared profile and correctly detected ten deliberately malformed graphs. These results support the technical feasibility and reproducible auditability of an evidence-qualified herbal knowledge graph. They do **not** establish independent scientific answer accuracy, validated biological contradictions, clinical effectiveness, safety, or external generalizability. A prospective, adjudicated source-disjoint evaluation remains essential for these stronger claims.

## Declarations and research transparency

**Ethical review:** The present computational work uses bibliographic and already assembled non-person-identifiable source assertions; authors must confirm any institutional research ethics determination before submission. No participant-level clinical records were analyzed here.

**Funding:** To be completed by the authors; no grant is inferred.

**Competing interests:** To be declared by all authors.

**Author contributions:** To be provided and approved by the actual researchers.

**Data availability:** The frozen, versioned RDF, assertion CSV, shapes graph, tests, supplementary results, and provenance log are distributed in the project research archive. Redistribution rights for third-party cited full-text material must be checked separately; the package does not assert permission to reproduce copyrighted publications. Source dataset fingerprint: `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`.

**Code availability:** The reproducible structural audit and plotting scripts are provided with the versioned package. Official pySHACL proof: https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018 .

**Role of generative AI:** AI assistance was used for scripting, analysis organization, visualizations, and manuscript drafting. It did not supply independent expert gold labels or replace source-level scientific adjudication. Authors must independently verify and approve the final content.

## References (APA 7th edition)

Allemang, D., Hendler, J., & Gandon, F. (2020). *Semantic web for the working ontologist: Effective modeling for linked data, RDFS, and OWL* (3rd ed.). Association for Computing Machinery. https://doi.org/10.1145/3382097

Hogan, A., Blomqvist, E., Cochez, M., d'Amato, C., de Melo, G., Gutierrez, C., Kirrane, S., Labra Gayo, J. E., Navigli, R., Neumaier, S., Ngonga Ngomo, A.-C., Polleres, A., Rashid, S. M., Rula, A., Schmelzeisen, L., Sequeda, J., Staab, S., & Zimmermann, A. (2021). Knowledge graphs. *ACM Computing Surveys, 54*(4), Article 71. https://doi.org/10.1145/3447772

Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J. J., Appleton, G., Axton, M., Baak, A., Blomberg, N., Boiten, J.-W., Bonino da Silva Santos, L., Bourne, P. E., Brookes, A. J., Clark, T., Crosas, M., Dillo, I., Dumon, O., Edmunds, S., Evelo, C. T., Finkers, R., Gonzalez-Beltran, A., ... Mons, B. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data, 3*, Article 160018. https://doi.org/10.1038/sdata.2016.18

World Wide Web Consortium. (2013, April 30). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/

World Wide Web Consortium. (2017, July 20). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/

## Figure captions

**Figure 1.** Deterministic retrieval of source-assertion properties from three frozen RDF projections. All bars are field-retention counts, not answer-accuracy rates.

**Figure 2.** Distinct RDF triple count by representation; graph-size increases are not runtime measurements.

**Figure 3.** Sensitivity to deletion of selected M3 evidence qualifiers; removal of a field deterministically makes it unrecoverable.

**Figure 4.** Clinical topic groups requiring context-aware expert review, rather than adjudicated contradictions.

## Supplementary material

Supplementary files include `P3_ASSERTION_AUDIT_624.csv`, `P3_MODEL_CAPABILITY_SUMMARY.csv`, `P3_CHANNEL_CAPABILITY_SUMMARY.csv`, `P3_SPO_COLLISION_AUDIT.csv`, `P3_CLINICAL_CONTEXT_VARIATION.csv`, `P3_CONTEXT_ABLATION.csv`, `P3_DEVELOPMENT_CQ_24_SUMMARY.csv`, `P3_V11_EXPERIMENT_SUMMARY.json`, the frozen RDF and source assertions, the authentic SHACL validation report, and the unfilled expert-review case template.
