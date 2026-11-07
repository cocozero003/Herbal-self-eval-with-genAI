# ThaiHerb Paper 1 — Held-Out Formula Validation & Independent Expert Benchmark Protocol (v0.7)

**วันที่จัดทำ:** 7 พฤศจิกายน 2569  
**สถานะ:** INTERNAL OUT-OF-SAMPLE PROXY VALIDATION COMPLETED; INDEPENDENT EXPERT VALIDATION **NOT** COMPLETED  
**โครงการ:** ThaiHerb10 Paper 1 — Feasibility of evidence-channel graph representations

## บทสรุปผู้บริหาร

การวิเคราะห์ Paper 1 v0.7 เปรียบเทียบ baseline กับ Cooc/Chem/Core บนโจทย์ใหม่คือ *การจัดอันดับคู่สมุนไพรที่พบร่วมกันในตำรับที่กันไว้* โดยใช้สูตรตำรับจากชุดที่ทบทวนเอกสารแล้วจำนวน 10 ตำรับ (สมุนไพรเป้าหมาย 10 ชนิด) และไม่ใช้สูตรทดสอบในการสร้างความสัมพันธ์ของ Cooc โมเดลที่มีความซับซ้อนมากขึ้นไม่ได้ให้ผลเหนือ PairSupport baseline บนโจทย์นี้ ผลไม่ใช่การประเมินความคล้ายคลึงทางชีววิทยาหรือทางคลินิก

การทดลอง F02 ต้องแยกออกจากการเปรียบเทียบครบ 45 คู่ เนื่องจาก H07 (กะเพราแดง) ปรากฏเฉพาะในตำรับดังกล่าว ทำให้ไม่มีข้อมูล Cooc สำหรับ H07 ใน 9 ตำรับฝึก นี่เป็นข้อมูล cold-start ที่สำคัญ มิใช่ค่าที่ควรเติมด้วยค่า embedding สุ่ม

## 1. คำถามวิจัย

1. โมเดล Cooc, Chem, Core สามารถจัดอันดับคู่สมุนไพรที่ปรากฏร่วมในตำรับที่ไม่เคยเห็นในชุดฝึกได้เพียงใด?
2. Graph embedding มีประโยชน์เหนือ baseline แบบจำนวนครั้งที่ปรากฏร่วม (PairSupport) หรือไม่?
3. ผลประเมินเปลี่ยนแปลงเท่าใดเมื่อไม่แยกสูตรทดสอบออกจาก training data และเกิด data leakage?
4. ระบบพร้อมประเมิน herb-pair similarity ด้วย blinded independent experts แล้วหรือไม่?

## 2. ข้อมูลและข้อจำกัด

- Formula layer: 10 ตำรับ, 10 สมุนไพร, 46 Herb–Formula memberships ในกลุ่มสมุนไพรเป้าหมาย, 45 คู่สมุนไพรทั้งหมด
- การยืนยันชั้นสูตรเป็นการตรวจโดยผู้ตรวจหนึ่งรายโดยใช้เอกสาร DTAM/อย. พ.ศ. 2566; ยังไม่มี adjudication อิสระ
- Chemistry: 30 herb–compound assertions / 25 compound names จาก V3-derived proxy, candidate class 19 กลุ่มที่ยังไม่ยืนยันว่าเหมือนต้นฉบับ Paper 1
- ไม่พบ original Paper 1 walk corpora, chemistry class archive และ trained vectors
- Literature corroboration v0.5–v0.6 มี post-hoc source selection จึง **ไม่ถือเป็น independent gold standard**

## 3. การทดลอง

### 3.1 Leave-One-Formula-Out (LOFO)

ในแต่ละ fold เก็บหนึ่งสูตรไว้เป็นชุดทดสอบและใช้เก้าสูตรที่เหลือสร้าง Cooc graph ตั้งแต่ต้น จากนั้นสร้างลำดับคะแนนสำหรับ 45 คู่ด้วยโมเดลต่อไปนี้: DegreeProduct, PairSupport, ClassJaccard, Cooc-NPMI, Cooc-Support, Cooc-Degree, Cooc-Combined, Chem-Proxy และ Core-Proxy

**Outcome:** คู่สมุนไพรสองชนิดปรากฏร่วมกันในสูตรทดสอบ (1) หรือไม่ปรากฏร่วมกันในสูตรนั้น (0) โดย 0 **ไม่ใช่** ป้ายว่าไม่มีความคล้ายคลึงทางเคมีหรือเภสัชวิทยา

**Training segregation:** กราฟ Cooc และคู่ที่นำไปคำนวณคะแนนใช้เพียง 9 สูตร ไม่มีสูตรทดสอบอยู่ใน training IDs; chemistry V3-derived proxy เป็นชุดคงที่และไม่ได้มาจากสูตรที่ถูกถือออก แต่ยังมีความเสี่ยงจากการเลือกข้อมูลและแหล่งหลักฐาน

**Coverage gate:** Fold F02 ถูกจำแนกเป็น `COLD_START_UNREPRESENTED_HERB` เพราะ H07 ไม่มีข้อมูล Cooc ในเก้าสูตรฝึก ไม่ใช้สูตรนี้ในการเปรียบเทียบ 45 คู่อย่างยุติธรรม เหลือ 9 eligible folds

**Seed control:** ใช้ seeds เดียวกันจำนวน 10 ค่าในการสร้าง embeddings; สำหรับแต่ละ fold นำค่า cosine ของสิบ seeds มาเฉลี่ยก่อนคำนวณค่า AUROC, Average Precision, P@5 และ nDCG@5; ไม่ปรับ hyperparameters ด้วยผลทดสอบ

### 3.2 ความไม่แน่นอนและ Negative Controls

- รายงาน mean AP ต่อสูตร (macro average) และ 95% percentile interval จากการ bootstrap *ตามสูตร* 3,000 ครั้ง จำนวน cluster = 9 จึงเป็นค่า exploratory
- เปรียบเทียบความต่าง AP แบบ paired sign-flip ที่ระดับสูตร; ยังไม่ปรับ multiplicity และห้ามอ้างนัยสำคัญเชิงยืนยัน
- Permutation control: สลับ label ภายในแต่ละสูตร 2,000 ครั้ง โดยเก็บจำนวนบวก/ลบแต่ละสูตรคงเดิม เพื่อดูว่าคะแนนจริงสูงกว่า label-null หรือไม่
- Leakage oracle: จงใจรวมสูตรทดสอบเข้า PairSupport เพื่อแสดงผลการประเมินผิดพลาดเมื่อละเมิด train/test separation; ห้ามถือว่า oracle เป็น candidate model ที่ถูกต้อง

## 4. ผล

| Model | Mean AP | 95% clustered bootstrap CI | Mean AUROC | Mean P@5 |
|---|---:|---:|---:|---:|
| PairSupport | 0.419 | 0.234–0.620 | 0.690 | 0.467 |
| Cooc-NPMI | 0.395 | 0.223–0.573 | 0.599 | 0.400 |
| Cooc-Support | 0.372 | 0.215–0.545 | 0.579 | 0.356 |
| Cooc-Degree | 0.362 | 0.195–0.548 | 0.597 | 0.378 |
| DegreeProduct | 0.356 | 0.195–0.539 | 0.683 | 0.422 |
| Cooc-Combined | 0.349 | 0.207–0.512 | 0.582 | 0.378 |
| Core-Proxy | 0.292 | 0.146–0.455 | 0.467 | 0.289 |
| Chem-Proxy | 0.275 | 0.145–0.423 | 0.484 | 0.289 |
| ClassJaccard | 0.239 | 0.128–0.368 | 0.509 | 0.333 |

Mean label prevalence (eligible folds) = **0.183**. Constant-score AP baseline = prevalence. ผล permutation ของ PairSupport พบ observed AP = **0.419**, mean label-null AP ≈ **0.229**, และ permutation p (exploratory) ≈ **0.00050** โดยเปรียบเทียบกับ label-null ภายในสูตร มิใช่ independent external relevance standard

**Data leakage diagnostic:** Proper PairSupport mean AP = **0.419**; invalid oracle ที่ใส่ held-out formula เข้า training ได้ mean AP = **0.543** (+0.124) ยืนยันว่า baseline ที่เห็นผลดีต้องประเมินด้วย split ที่ถูกต้อง

### การตีความ

- การจัดอันดับจาก raw formula support มีผลดีกว่า embedding ที่ทดลองในโจทย์ *held-out formula co-occurrence* นี้ ทั้งที่ Chem/Core ยังอาจมีประโยชน์กับโจทย์อื่น การทดลองนี้ไม่ได้ทดสอบ biological similarity ที่มี label อิสระ
- ค่า seed stability สูงใน v0.4–v0.5 ไม่ควรใช้เป็นคำตอบแทน predictive validity และไม่ยืนยันความถูกต้องของหลักฐาน
- เนื่องจากมีเพียง 9 fold ที่ประเมินได้ และสูตรจากเอกสารชุดเดียวกัน confidence intervals จึงกว้างและความสามารถทั่วไปยังจำกัด
- การทดสอบเปรียบเทียบกับ PairSupport ต้องไม่ตีความเป็นความแตกต่างเชิงสถิติที่ยืนยันแล้ว เพราะไม่มี pre-registered confirmatory design และมีหลาย models

## 5. Independent expert benchmark — สถานะจริง

สร้างแบบประเมิน 2 ชุด (R1/R2) มีลำดับคู่ไม่เหมือนกันและไม่มี model scores จำนวน 45 คู่สมุนไพร โดยแยกการให้คะแนน **chemistry** และ **formula-context** เป็น 0, 1, 2, NA รวมทั้งบันทึก source, precise locator, material/plant part/preparation และสถานะ independence ของแหล่งข้อมูล  **ยังไม่มีผู้เชี่ยวชาญให้คะแนนจริง**; adjudication จึงว่างและสคริปต์ประเมินจะรายงาน `BLOCKED_GOLD_LABELS_INCOMPLETE`

คำนิยามที่ต้องใช้สำหรับความเชื่อถือได้ของ gold standard: ผู้ประเมินอย่างน้อยสองรายเป็นมนุษย์จริง ประเมินแยกกันโดยไม่เห็นคะแนนโมเดล; ใช้เอกสารที่ไม่ซ้ำข้อมูลที่ป้อนโมเดลหรือข้อมูลที่ใช้เลือกสมุนไพร; ระบุหลักฐานชนิดพืชและส่วนของพืช; ให้ผู้พิจารณาที่สามตัดสินข้อขัดแย้งแล้วบันทึกเหตุผล หากข้อมูลไม่เพียงพอให้ NA ไม่ใช่ 0

**ไฟล์:** `BLINDED_EXPERT_R1_45.csv`, `BLINDED_EXPERT_R2_45.csv`, `ADJUDICATION_TEMPLATE_45.csv`, `CASE_KEY_INTERNAL_45.csv`, `expert_evaluation_gate.json`.

## 6. ข้อเสนอเพื่อปรับ Paper 1 Manuscript

1. แยก original 10-herb feasibility results ออกจาก LOFO v0.7 ซึ่งเป็น post-hoc extension; อย่าเขียนผล v0.7 ทับผลตีพิมพ์เดิม
2. เพิ่มหัวข้อ **Task-Specific Predictive Validation and Leakage Controls** โดยระบุโจทย์เป็น held-out formula co-occurrence ไม่ใช่ biological/pharmacological similarity
3. เพิ่มตาราง baseline PairSupport และ DegreeProduct เพราะโมเดลใหม่ต้องพิสูจน์ประโยชน์เหนือวิธีพื้นฐาน
4. แสดง cold-start F02 อย่างโปร่งใส (ไม่แอบทิ้ง fold ที่ผลไม่ดี) และรายงาน CI bootstrap ที่ระดับสูตร
5. ให้แยกผล expert ratings จนกว่าจะมี independent adjudication; อย่าทำ label จาก ChatGPT แล้วอ้างเป็น expert gold
6. ยืนยัน compound class ontology เดิม 19 กลุ่มและ original training vectors/walks หรือระบุว่าการ reanalysis เป็น reconstruction

## 7. แนวทางต่อไป

**Gate A: External corpus (ยังไม่เสร็จ):** เพิ่มสูตรจากแหล่งที่ต่างจาก compendium ที่ใช้สร้างกราฟและตรวจชื่อสมุนไพร/สูตร/ส่วนของพืช; ปิดข้อมูลการเลือก model ก่อนเปิด test corpus

**Gate B: Independent chemistry expert labels (ยังไม่เสร็จ):** เก็บคะแนน 45 คู่โดยสอง reviewer, ตรวจ source disjointness, Cohen's weighted kappa และ adjudication; เมื่อครบแล้วคำนวณ nDCG@10, Spearman เทียบแบบ paired และเผยแพร่ review protocol

**Gate C: Manuscript scientific signoff (ยังไม่เสร็จ):** primary full-text row verification, original chemistry taxonomy, study-specific reproducibility and transparent limitation statement

## References (APA 7)

Brière, G., Stosskopf, T., Loire, B., & Baudot, A. (2026). Benchmarking the impact of data leakage on the performance of knowledge graph embedding models for biomedical link prediction. *Bioinformatics, 42*(8), btag608. https://doi.org/10.1093/bioinformatics/btag608

Department of Thai Traditional and Alternative Medicine & Thai Food and Drug Administration. (2023). *Official Thai herbal formula compendium (B.E. 2566)* [Official reference publication]. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

> หมายเหตุ: ชื่อหน่วยงานและชื่อเรื่องในรายการอ้างอิงเอกสารไทยต้องตรวจสอบกับหน้าปกและข้อมูลทางบรรณานุกรมจริงก่อน manuscript finalization; รายการนี้ใช้เป็น working citation
