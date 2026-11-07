# รายงานสถานะงานวิจัย Thai Herbal Knowledge Graph — Paper 1–3

**ข้อมูลถึงวันที่ 7 พฤศจิกายน 2569 (2026-11-07)**  
**สถานะเอกสาร:** Portfolio progress review / release index; ไม่ใช่หลักฐานอนุมัติส่งตีพิมพ์

## Executive summary

โครงการมีต้นฉบับบทความสำหรับผู้ร่วมวิจัยตรวจทานครบ **3 ฉบับ** โดยมีขอบเขตแยกกัน: **Paper 1** พิสูจน์ความเป็นไปได้เชิงคำนวณในชุดสมุนไพร 10 ชนิด, **Paper 2** วิเคราะห์ความทนทานและความอ่อนไหวต่อแหล่งข้อมูลในชุดสมุนไพร 20 ชนิด และ **Paper 3** ตรวจความครบถ้วนของการแทนข้อมูล RDF/provenance และ SHACL conformance ทั้งสามฉบับอยู่ในสถานะ **Author-review**, ยังไม่ได้รับการรับรองจากผู้เขียนและยังไม่ได้ส่งวารสาร

| Paper | เวอร์ชัน | คำถามวิจัยหลัก | สิ่งที่พิสูจน์ได้ | สิ่งที่ยังพิสูจน์ไม่ได้ |
|---|---|---|---|---|
| 1. ThaiHerb10 Feasibility | v0.8 | แยก Cooc/Chem/Core และสร้าง embedding ได้หรือไม่ | ทำ computational feasibility reanalysis ได้และรันซ้ำได้ | ไม่ใช่ exact historical replication; ไม่มี original 19-class mapping หรือ independent biological gold |
| 2. ThaiHerb20 Robustness | v1.4 (manuscript), v1.3 (results) | ความเสถียรต่อ seeds / perturbations / source holdout / formula holdout | internal robustness และ LOFO ของ documentary co-membership | external generalizability, biological/clinical validity; original 35-class mapping ยังไม่กู้คืน |
| 3. Evidence-centric RDF KG | v1.1 | M1/M2/M3 รักษา assertion/provenance/context แตกต่างกันอย่างไร | RDF representation fidelity, SHACL Core project-profile PASS | independent semantic answer accuracy, clinical contradiction adjudication, expert gold |

## Paper 1 — Ten-herb computational feasibility

**ชื่อบทความ:** *Evidence-channel-specific graph embeddings for Thai herbal medicine: A reproducible ten-herb computational feasibility reanalysis*  
**รุ่นล่าสุด:** v0.8 Publication Finalization (author review)

- Dataset: สมุนไพร 10, ตำรับ 10, 46 herb–formula memberships, 45 คู่สมุนไพร, 23 positive-NPMI edges; chemistry proxy 30 herb-compound assertions, 25 compound names และ candidate 19 classes.
- วิธีการ: 13 configurations × 10 seeds = 130 model fits; 5,850 herb-pair scores. ผล mean seed-pair Spearman: Cooc-NPMI 0.932159, Chem-candidate19 0.909170, Core-candidate19 0.739359, Cooc-support/degree 0.962278.
- Sensitivity: pruning chemistry เหลือ 2 จาก 3 compounds ต่อสมุนไพร เปลี่ยน mean rank correlation เหลือ 0.036495.
- **ข้อจำกัด:** เป็น reanalysis จาก V3-derived proxy ไม่ใช่การกู้คืนเวกเตอร์/walk corpus และ original 19-class mapping ของ pilot ก่อนหน้า ผลเก่าที่รายงาน Cooc 0.946, Chem 0.977, Core 0.945 เป็นคนละรัน ห้ามผสมตัวเลขในตารางเดียวโดยไม่แยก dataset version. ไม่มี independent expert gold.
- QA ที่รายงานไว้ใน release: 10/10 automated checks และหลักฐาน clean replay ภายใต้สภาพแวดล้อมเดียวกัน.
- **ผลลัพธ์ที่เหมาะจะตีพิมพ์:** 10-herb computational methods feasibility พร้อมความเปราะบางต่อหลักฐานและข้อจำกัดของ corpus ขนาดเล็ก.

## Paper 2 — Internal robustness, data-source sensitivity and representation stability

**ชื่อบทความ:** *Internal Robustness, Data-Source Sensitivity, and Representation Stability of Herbal Knowledge Embeddings: A Reproducible Study of 20 Thai Medicinal Herbs and 10 Traditional Formulas*  
**รุ่นล่าสุด:** v1.4 Full Manuscript; อ้างอิง experiment freeze v1.3

- Dataset: สมุนไพร 20, ตำรับ 10, 74 herb–formula memberships ใน v1.3 freeze, 190 คู่สมุนไพร, chemistry claims 100 รายการ (83 compound identifiers). Original primary full-text verification 5/100 ข้อกล่าวอ้าง; อย่าสรุปว่า 95 รายการผิด.
- Archived baseline: 9 configurations × 20 seeds = 180 fits, 34,200 pairwise similarity scores. ภายหลังทดลอง perturbations, leave-one-formula-out (LOFO), source holdout, provisional taxonomy และ material sensitivity.
- Seed repeatability (ตาม v1.3): Cooc-NPMI 0.969, Chem-Exact 0.758, Core-Exact50 0.693. Chemical pruning เหลือ 4/5, 3/5, 2/5 สาร ทำให้ rank correlation ≈0.606, 0.261, 0.048 ตามลำดับ.
- **LOFO ที่ไม่มี cold start 6 folds:** mean AP PositiveNPMI 0.300768; PairSupport 0.290904; Cooc-NPMI train-only 0.275481; Core-Exact50 0.168405; Chem-Exact 0.138927. อีก 4 folds มี cold start และต้องรายงาน coverage ต่างกัน.
- Paired formula-cluster bootstrap (6 complete folds): Δ AP (Core-Exact50 − PairSupport) ≈ −0.1225, exploratory 95% CI ประมาณ [−0.208, −0.050]. ตัวชี้วัดอ้างอิง **formula co-membership** เท่านั้น ไม่ใช่ biological similarity.
- Chemical source holdout 20 แหล่ง × 5 seeds ทำให้คะแนนคำนวณได้ 171/190 คู่ = 90% coverage ต่อ holdout; ห้าม impute ค่าที่ไม่มีหลักฐาน.
- **ข้อจำกัด:** original chemical 35-class mapping ไม่พบ, taxonomy ใหม่ 31 groups เป็นเพียง reconstruction/sensitivity, external source-disjoint pilot 11 รายการเป็น post-hoc positives ไม่ใช่ confirmatory benchmark; ไม่สามารถอ้าง generalizability หรือ efficacy.
- QA ที่รายงานไว้ใน release: 23/23 automated tests, 87/87 manifest items, clean ZIP rerun ของห้า result summaries และ browser smoke test.
- **ผลลัพธ์ที่เหมาะจะตีพิมพ์:** reproducible internal robustness and data-source sensitivity study พร้อม negative findings ว่า Core ไม่ได้เหนือกว่า Cooc สำหรับการทำนาย documentary formula co-membership.

## Paper 3 — Evidence-centric RDF representation and structural conformance

**ชื่อบทความ:** *An Evidence-Centric RDF Knowledge Graph for Thai Herbal Medicine: Reproducible Evaluation of Representation Fidelity, Provenance, and SHACL Conformance*  
**รุ่นล่าสุด:** v1.1 Full Manuscript; เชื่อม pySHACL v1.0 จริง

- Frozen dataset: 208 assertions (formula 71, chemistry 100, pharmacology-target 30, clinical 7). **ต่างจาก Paper 2 ที่มี 74 formula memberships ในรุ่น freeze ของตน** — ห้ามนำจำนวนมาสลับกัน.
- Graph sizes: M1 Naive SPO = 207 triples; M2 Provenance-aware = 1,501 triples; M3 Evidence-centric = 2,733 triples. M1 มีหนึ่ง SPO collision ระหว่าง CLIN005/006.
- Source assertion recovery: M1/M2/M3 = 0/208/208; provenance = 0/208/208; evidence mode/directness/context = 0/0/208. จำนวนข้อมูลที่เก็บได้มากขึ้นเป็น property ของ representation ไม่ใช่ semantic QA accuracy.
- `pySHACL` v0.40.2 รันจริงใน GitHub Actions สำเร็จ: M3 ผ่าน project-specific SHACL Core profile, 0 violations, 10/10 planted negative controls detected. **ไม่ใช่การพิสูจน์ความจริงของข้อมูลเคมี/คลินิก.**
- สามกลุ่ม clinical-context variation จาก 7 clinical assertions เป็น review candidates (ไม่ใช่ contradictions ที่รับรองแล้ว); 8 development competency questions, 24 query outputs **ไม่ใช่ independent benchmark**.
- **ข้อจำกัด:** 0 expert-adjudicated semantic gold labels, source-disjoint confirmatory accuracy ยังไม่มี, clinical object IDs และ plant-part/preparation contexts บางส่วนยังไม่ normalized.
- QA ที่รายงานไว้ใน release: 14/14 tests, 40/40 manifest checks, clean rerun, browser 5 tabs และ 624 assertion-model audit records.
- **ผลลัพธ์ที่เหมาะจะตีพิมพ์:** RDF engineering/methods contribution เรื่อง provenance, assertion-level retention, contextual qualifiers และ structural validation.

## เส้นแบ่งวัตถุประสงค์และความซ้ำซ้อนของบทความ

1. **Paper 1 (feasibility):** unit = 10 focal herbs / document-derived co-occurrence & chemical evidence channels; endpoint = feasibility และ seed-repeatability ของ reconstructed embeddings.
2. **Paper 2 (robustness):** unit = herb-pair rankings / formula holdout; endpoint = perturbation stability, source coverage, documentary co-membership AP. ไม่ใช้ผลชุด P1 เป็น independent external test.
3. **Paper 3 (representation):** unit = evidence assertions / RDF graph; endpoint = retention of source metadata, SHACL conformance และ design trade-off. ไม่ใช้ AP จาก P2 เป็นผลลัพธ์ของ M3.

ทั้งสาม Paper ใช้ project provenance ร่วมกันบางส่วน ผู้เขียนต้องเปิดเผยที่มาของ corpus, รุ่นที่ freeze, การใช้ร่วมกันของสมุนไพร/ตำรับ, และความแตกต่างของจุดประสงค์ เพื่อลดความเสี่ยง duplicate publication / salami slicing.

## ตารางสิ่งที่ยังต้องปิดก่อน submission

| รายการ | Paper 1 | Paper 2 | Paper 3 |
|---|---|---|---|
| ต้นฉบับครบเพื่อ author review | ใช่ (v0.8) | ใช่ (v1.4) | ใช่ (v1.1) |
| ผลคำนวณทดสอบซ้ำภายใน | ใช่ ตามขอบเขต release | ใช่ (v1.3) | ใช่ + SHACL CI |
| ห้ามอ้าง clinical/biological validation | ใช่ | ใช่ | ใช่ |
| ข้อมูล/วิธีการที่ต้องรับรอง | Candidate 19 classes และ source qualification | Primary chemistry evidence, original 35 classes หรือเปลี่ยน taxonomy อย่างเปิดเผย | Clinical contexts และ semantic benchmark ที่ยังไม่มี gold |
| เอกสารผู้เขียน/ทุน/COI/ethics/data sharing | รอผู้เขียนรับรอง | รอผู้เขียนรับรอง | รอผู้เขียนรับรอง |
| สถานะส่งวารสาร | **ยังไม่ส่ง; author review** | **ยังไม่ส่ง; author review** | **ยังไม่ส่ง; author review** |

## Release links — Google Drive / GitHub

### Paper 1 (v0.8)
- Google Drive folder: https://drive.google.com/drive/folders/11ZhI1j3fpmYS9KixG5E_1pw03pqC5fIe
- Manuscript DOCX: https://drive.google.com/file/d/12B73v_SNQlF8UBnnzt7oT7xGPtE_xCiE/view
- Full ZIP: https://drive.google.com/file/d/1HZYlxuI36gbg2d5E_jzanedT3LXJ2sLd/view
- GitHub: https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p1-publication-finalization-v0.8-20261107

### Paper 2 (v1.4 + v1.3 experiment)
- Google Drive manuscript: https://drive.google.com/drive/folders/18tDTgmaFvoRGlEBCSrS4ENbUJwdIrXpU
- Manuscript DOCX: https://drive.google.com/file/d/1ShjDlOqowNkavMJnMY_xoXjrlubH_z8m/view
- Reproducible experiment ZIP: https://drive.google.com/file/d/1CLSvyUsF_8GEDgRhtYlVLMAAD3PWdXmE/view
- GitHub: https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p2-manuscript-internal-robustness-v1.4-20261107

### Paper 3 (v1.1 + authentic SHACL)
- Google Drive folder: https://drive.google.com/drive/folders/1bp-UKpXrDDMCpBiNt8370MC-KnGBNBAm
- Manuscript DOCX: https://drive.google.com/file/d/18Wlx3lA5EsK-UE6mwLQjPHH7cJzssOaK/view
- Reproducible full ZIP: https://drive.google.com/file/d/123i4IuxLSuk1G5Vtej0orZHZOpPLHbKg/view
- GitHub: https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p3-engineering-manuscript-v1.1-20261107
- SHACL CI evidence: https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018

## แนะนำการดำเนินการต่อแบบไม่เปลี่ยนผลการทดลอง

- **อันดับแรก:** ผู้เขียนยืนยันการใช้ reanalysis สำหรับ P1, ตรวจความถูกต้อง source claims และข้อจำกัด P2, ตรวจ ontology context/claims P3 พร้อมระบุ author contributions, funding, conflict of interest และ data availability.
- **ขั้นสอง:** ตรวจ manuscript ของแต่ละ Paper ต่อวารสารที่เหมาะสม และเพิ่ม cross-paper overlap disclosure ใน Methods / cover letter.
- **ขั้นสาม:** สำหรับบทความที่ต้องการอ้าง biological validity หรือ semantic QA superiority ต้องพัฒนา independent expert-adjudicated gold / preregistered external benchmark แยก ไม่ใช่ขยายข้อสรุปจากผล internal tests.

**การจัดทำรายงานรวมนี้เป็นการตรวจสอบและสรุปข้อมูลเดิม ไม่มีการรันการทดลองใหม่หรือเปลี่ยนผลที่ freeze ไว้ และไม่ได้ยืนยันว่ามีการส่งบทความต่อวารสารแล้ว**
