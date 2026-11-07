# Paper 2 — Robustness Foundation v0.3 (ThaiHerb20)

**วันที่:** 7 พฤศจิกายน 2569  
**สถานะ:** SOURCE/BASELINE ROBUSTNESS COMPLETE ON V3-DERIVED PROXY; ORIGINAL 35-CLASS CHEM/CORE REPLICATION NOT COMPLETE

## Executive summary

เริ่ม Paper 2 ได้โดยไม่ต้องรอ independent biological validation ของ Paper 1 เพราะโจทย์หลักของ Paper 2 คือ robustness, source/selection dependence และการพัฒนา benchmark ที่ไม่รั่วข้อมูล ส่วน independent expert benchmark ของ Paper 2 จะเป็นการประเมินในระยะถัดไป และ **ยังไม่ได้รับคะแนนจากผู้เชี่ยวชาญจริง**

Baseline ตรวจจากชุด V3-derived: 20 สมุนไพร, 10 ตำรับ, 71 membership assertions, 100 chemistry assertions, 83 compound IDs, 190 herb pairs, 82 positive NPMI edges. สารเคมี 35 classes และ archived 20-seed 190-pair vectors ใน Paper 2 manuscript เดิม **ยังไม่มีไฟล์ที่ตรวจยืนยันได้**. โค้ดนี้จึงไม่อ้างว่าเป็น exact original embedding replication.

## 1. Source integrity และ crosswalk

- 10 ตำรับที่ใช้ใน Paper 2 สามารถจับคู่ F01–F10 กับ Paper 1 source-reviewed snapshot ได้ โดยสมุนไพร 10 ชนิดแรกมี presence ตรงกับข้อมูล Paper 1 ในทุกสูตร
- ความสัมพันธ์ของสมุนไพรที่เพิ่ม H11–H20 ยังอยู่ในสถานะ **V3-derived, not primary independently adjudicated**; ต้องตรวจต้นฉบับทั้งส่วนที่พบและส่วนที่ไม่พบ
- ต้องแยก 200 formula-herb matrix cells เป็นชั้น legacy (100) และ added (100) ไม่รายงานว่า 200 cells ผ่าน primary audit เท่ากัน
- Source IDs เคมี 20 แหล่ง มีแหล่งหลักเพียงหนึ่งต่อสมุนไพรทุกชนิด; source-holdout 20/20 ทำให้สมุนไพรอย่างน้อยหนึ่งชนิดไม่มีข้อมูลเคมี จึงไม่สามารถเปรียบเทียบครบ 190 คู่ได้อย่างเท่าเทียม
- จำนวน positive-NPMI edges ที่ support เพียง 1 ตำรับ: **38/82**; ค่านี้สะท้อนความไวของ NPMI ใน corpus ขนาดเล็ก

## 2. Leave-One-Formula-Out coverage

กันสูตรตำรับออกทีละหนึ่งสูตรและสร้าง Cooc scores ใหม่จากอีกเก้าสูตรโดยไม่มีสูตรทดสอบใน training IDs; ผลลัพธ์คือคู่สมุนไพรที่อยู่ในสูตรทดสอบร่วมกัน ไม่ใช่ความคล้ายคลึงทางชีววิทยา การเลือกสมุนไพรและสูตรจาก corpus เดียวกันยังเป็น selection bias.

- ประเมินเต็ม 190 คู่ได้ **6/10** folds
- Cold-start folds: **F02 (H07), F03 (H18), F05 (H20), F07 (H19)**
- Mean prevalence ใน 6 folds ที่มี coverage ครบ = **0.1053**

| Formula | Eligible | Unseen herbs | Positive pairs |
| --- | --- | --- | --- |
| F01_DTAM2566 | 1 | - | 36 |
| F02_DTAM2566 | 0 | H07 | 21 |
| F03_DTAM2566 | 0 | H18 | 28 |
| F04_DTAM2566 | 1 | - | 28 |
| F05_DTAM2566 | 0 | H20 | 36 |
| F06_DTAM2566 | 1 | - | 10 |
| F07_DTAM2566 | 0 | H19 | 28 |
| F08_DTAM2566 | 1 | - | 28 |
| F09_DTAM2566 | 1 | - | 15 |
| F10_DTAM2566 | 1 | - | 3 |


## 3. Task-specific baseline benchmark

การประเมินนี้ใช้ simple baselines โดยยัง **ไม่ได้เทียบกับต้นฉบับ Cooc/Chem/Core Word2Vec 20-seed** เพราะต้นฉบับ class map และ vectors ไม่ได้ถูกกู้คืน. ข้อมูลเคมีที่ทดสอบใช้ exact compound IDs เท่านั้น ไม่ได้อนุมาน chemical classes.

| Model | Mean AP | 95% fold bootstrap | AUROC | P@10 |
| --- | --- | --- | --- | --- |
| PairSupport | 0.253147 | 0.144998–0.369372 | 0.728453 | 0.266667 |
| DegreeProduct | 0.226841 | 0.123766–0.349756 | 0.667526 | 0.216667 |
| PositiveNPMI | 0.237752 | 0.129191–0.337189 | 0.654383 | 0.316667 |
| ExactCompoundJaccard | 0.114693 | 0.066595–0.161124 | 0.477069 | 0.1 |
| ExactCompoundIDFJaccard | 0.121666 | 0.071912–0.168563 | 0.478412 | 0.133333 |


PairSupport Mean AP = **0.253147**, AUROC = **0.728453**. รายงาน uncertainty ใช้ bootstrap ตามสูตรเพียง 6 folds (3,000 ครั้ง) เป็น **exploratory ไม่ใช่ confirmatory CI**.

## 4. Chemistry panel robustness

Randomly removing one of the five chemistry assertions per herb (eight reproducible panels) gives a **mean rank Spearman of 0.792** on exact-compound Jaccard rankings. This is not the original Chem embedding ablation and does not demonstrate chemical truth.

| Replicate | Rank rho | Top-10 overlap |
| --- | --- | --- |
| 1 | 0.812 | 7 |
| 2 | 0.812 | 8 |
| 3 | 0.812 | 4 |
| 4 | 0.836 | 7 |
| 5 | 0.651 | 4 |
| 6 | 0.836 | 9 |
| 7 | 0.787 | 8 |
| 8 | 0.787 | 8 |


## 5. Scientific interpretation

- Robustness of score ranking is not independent validity. Formula edges are documentary records, not biological or clinical truth.
- Original source-held-out chemistry **cannot be fully evaluated** when removing any one of 20 original chemistry sources isolates a herb. The correct outcome is BLOCKED, not zero-valued or randomly initialized similarity.
- The 10 extra herbs were selected conditional on occurrence in the same formula corpus and source availability; thus a within-corpus holdout is not an independent external corpus.
- The 35 chemical-class original mapping is missing. A 35-class taxonomy invented after examining the model would be a different experiment.
- Non-cooccurrence in a formula is not evidence of pharmacological dissimilarity.

## 6. Next scientific gates

1. Independently verify H11–H20 × F01–F10 (100 cells) using complete official formula tables and record source pages/ingredient names.
2. Recover original 35 compound-class mapping and training parameters or produce a **new** source-validated class dataset under a distinctly versioned study.
3. Generate frozen model comparison with Cooc/Chem/Core (20 seeds), balanced input budgets, degree and exact-chemistry baselines, and source/corpus held-out evaluation.
4. Acquire an independent formula corpus with precommitted eligibility rules, not post-hoc herbs/formulas chosen from training set.
5. Obtain genuine blinded expert labels from two reviewers for 190 pairs, adjudicate disagreement, and report agreement and source disjointness. Templates are present but **all ratings are blank**.

## References (APA 7)

Brière, G., Stosskopf, T., Loire, B., & Baudot, A. (2026). Benchmarking the impact of data leakage on the performance of knowledge graph embedding models for biomedical link prediction. *Bioinformatics, 42*(8), btag608. https://doi.org/10.1093/bioinformatics/btag608

Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง: ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

**Technical status:** Source/benchmark foundation only. **Not manuscript submission ready.**
