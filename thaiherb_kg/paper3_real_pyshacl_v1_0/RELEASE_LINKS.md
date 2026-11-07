# ThaiHerb KG: Evidence v1.2 / authentic SHACL v1.0

Research release date: **2026-11-07**. GitHub code-only branches; complete reproducible data/outputs on Google Drive.

## Verified files
- [Paper 2 v1.2 folder](https://drive.google.com/drive/folders/1AnsSCuKrOsXvGC7_HB0dz572tUuLQsh2)
- [Paper 3 v1.0 folder](https://drive.google.com/drive/folders/1jsISD7_FZ6_chM8kAMSCC0w0E4D2Jvda)
- [Paper 2 complete archive](https://drive.google.com/file/d/1gMwgrf9OK9zYv3OUZ83hcyd4MG5RBRIp/view)
- [Paper 3 complete archive](https://drive.google.com/file/d/1lfY5rALeuIQIMZ756QdvZcYjZCrNYJX4/view)
- [Combined reproducible archive](https://drive.google.com/file/d/17yXrYg9J5072Io2_ictRJJwjyaF3JpIh/view)
- [Scientific validity report in Thai (DOCX)](https://drive.google.com/file/d/1qDBDj3EuYEI11KurQQerkI-O9mPnd8uT/view)
- [Interactive evidence and validation dashboard](https://drive.google.com/file/d/1V2vws_DkPCZxXHj28UZ4xhNCczmcSSln/view)

Three full ZIPs were downloaded back from Drive, matched SHA256 `fa4897a711531d3f1cec5a00872bed06406c132c6585209e91e718d59fcfeda6`, and each archive passed 39/39 internal manifest checks. Clean extraction: `17 passed` pytest; browser interactive smoke passed.

## Authentic pySHACL (validated)
- Official [successful workflow run 42362561018](https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018)
- [Original artifact 13569434536](https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018/artifacts/13569434536)
- pySHACL v0.40.2, RDFLib v7.6.0, 208 frozen V3 assertions, M3 2733 triples, 34-triple shapes profile, **0 violations**, **10/10 planted negative controls detected**, `sh:conforms=true`.
- The **authentic** JSON, Turtle report, human-readable report and negative-control CSV are inside all full archives. No simulated SHACL conformance.

## Honest scientific limits
1. Original 100 phytochemical assertions were source-screened; **only 5 original-source primary experimental full-text verified**, not 100.
2. Official pySHACL Core **PASS**, confined to project-specific structural profile.
3. **0 expert-adjudicated gold labels**. 45 blinded-review candidates remain unsigned and unscored. AI is not a substitute for independent human experts.
4. Original 83-to-35 class crosswalk **not recovered**. A provisional **31-family new** name-based mapping is non-equivalent and unadjudicated.
5. New **11 positive analytical examples from 3 DOI-disjoint sources** are **post-hoc development pilot**, not an independently held-out, prospective test; no comparative accuracy calculated.

Earlier frozen sources and repo `main` remain unchanged.
