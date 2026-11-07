# Recheck: original 35-class archive candidate

Source archive: `ThaiHerb20_Paper2_WebApp_v1.zip` (historical original WebApp), SHA-256 `84eea279e05a7fd1a1ba30cc6e8f7d3b73bf39740c79bf1ae07ae4e11e6bccf3`.

Inspected 26 ZIP members, including `data/processed/paper2_bootstrap.json`, `data/thaiherb20.sqlite3`, HTML/JS source and documentation. The bootstrap stores 83 compound records and the summary field `n_compound_classes_reported = 35`. However, the 83 compound records in this bootstrap do not include a recoverable original class label map. The archived SQLite tables (`metadata`, `herbs`, `formulas`, `compounds`, `assertions`, `sources`, `pairs`, `cooc`, `published`, `annotations`, `audit`) also do not contain a dedicated chemical-class mapping table.

**Audit conclusion for this examined archive only:** no original 35-class *assignment map* was recovered. A manuscript summary reporting 35 categories is not the map, and a new taxonomy with the same category count would not reconstruct the historical taxonomy. Status: `NOT_RECOVERED_FROM_THIS_ARCHIVE`. Other unexamined private archives remain possible.
