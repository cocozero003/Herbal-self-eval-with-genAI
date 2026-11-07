# Restricted research inputs and reproducibility

This public repository contains **code and review protocols only**, not the full formula/chemistry research dataset, copyrighted manuscripts, or source PDF. Obtain the authorized **Paper 1 AI-Evidence Review v0.5** ZIP from:

https://drive.google.com/drive/folders/1h9pGMTpOT5_jBpI0O54nWOFSOMfckGs-

To rerun, extract the full ZIP preserving its folder structure, install `requirements.txt`, then run `python run_all_v05.py` and `python -m pytest -q tests`.

Required from the full ZIP: `data/paper1_bootstrap_v3_proxy.json` and the archived `results/BASELINE_v04_18class_cosines.csv` and other intermediate outputs used for the 18-to-19 candidate taxonomy comparison. Code on this branch alone is **not** a complete redistributable dataset.

Scientific caveats: 19 candidate chemical classes have the same **count** as the reported 19 original classes, **not** proven identical class definitions. Original source row-by-row compound–herb locators, archived walks/vectors and independent expert labels remain unavailable. Compound identity matches are candidates until verified for precise structure, plant part and specimen. Original manuscript results have not been overwritten.

The v0.3 erroneous deletion of three F05 formula memberships is retracted: the official ingredient table continues onto its next page.
