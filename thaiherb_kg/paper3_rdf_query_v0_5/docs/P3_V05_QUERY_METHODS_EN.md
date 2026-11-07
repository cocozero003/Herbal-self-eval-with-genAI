# Paper 3 v0.5 — RDF-only query engine development report

## Study state

The immutable 208-assertion V3 snapshot is **unchanged**. Three RDF projections from version v0.4 are used: M1 consists of naive subject-predicate-object edges, M2 has assertion and source identity, and M3 retains context, evidence mode and directness as **source text**, not normalized material/dose ontology. The present stage implements queries against the actual RDF graphs and tests model capability **without** reference answers or adjudicated gold.

## Deterministic competency-question development

Eight cases cover taxonomy, medicinal material/preparation, formula/version, chemistry, target directness, clinical context, candidate discordance and unknown safety/regulatory data. Exactly the same input case specification is executed against M1/M2/M3. Records in `P3_V05_ENGINE_OUTPUTS_24.csv` are *development-only outputs*, not adjudicated predictions or accuracy labels. The query engine does not see any gold labels; all reviewer/gold columns are empty.

For the platelet aggregation example, three distinct clinical assertions exist in V3, but two studies (CLIN005/CLIN006) share a subject-predicate-object tuple. M1 returns two *distinct objects* while M2 and M3 each return the three assertion instances. M2 can cite their source identities; only M3 carries raw context and direction text. This is a representation/capability diagnostic and **not** proof of superior clinical reasoning, source correctness or semantic answer accuracy.

Queries requiring canonical plant material, exact preparation or regulatory authorization abstain. M3 directness reports the archived assertion's directness field; this does **not** independently validate molecular binding experiments.

## SHACL and controls

`src/validate_shacl.py` retains an actual pySHACL Core validator with four constructed negative controls (missing provenance, duplicate object, source type and missing subject). The authoring Python container could not install pySHACL because outbound package resolution failed; the tool was not executed and the SHACL Core state stays `NOT_RUN_DEPENDENCY_UNAVAILABLE`. Prior custom checks are only implementation regression controls. A GitHub Action can install pySHACL on a networked runner; conformance must be read from the actual CI result before any pass claim.

## Formal benchmark plan

Retain 8 competency categories, freeze a prospectively sourced case set, obtain two genuine blinded reviews and adjudicate; only then run a locked paired M1/M2/M3 benchmark. Primary endpoint: semantic answer correctness including justified abstention. Secondary endpoints: answer coverage, citation correctness, provenance traceability, material fidelity, direct/functional target discrimination, overclaims and latency. No test evaluation, inferential statistics, expert agreement or real accuracy results are available in this stage.

## References

World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/

World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/

Sommer, A. (n.d.). *pySHACL* [Computer software]. https://github.com/RDFLib/pySHACL
