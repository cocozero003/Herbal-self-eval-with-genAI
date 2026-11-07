# Paper 1 — Evidence Qualification, Source Independence และ Source-Holdout Sensitivity (v0.6)

**วันที่:** 7 พฤศจิกายน 2569  
**สถานะ:** AI-assisted literature corroboration + exploratory computational experiment; **ไม่ใช่ independent expert adjudication** และ **ไม่ใช่การทำซ้ำผล original Chem/Core แบบตรงกันทุกขั้นตอน**

## 1. เหตุผลและคำถามวิจัย

Paper 1 เดิมแสดงความเป็นไปได้ในการแสดงความคล้ายคลึงของสมุนไพร 10 ชนิดผ่าน Cooc/Chem/Core แต่กราฟเคมี v0.5 ประกอบด้วย 30 herb–compound assertions จากชุด V3-proxy ซึ่งไม่ใช่ไฟล์ chemistry inputs ดั้งเดิมที่ผ่านการตรวจต้นฉบับครบถ้วน ข้อจำกัดสำคัญคือจำนวนแหล่งอ้างอิงอิสระต่อสมุนไพรต่ำ ทำให้ seed stability อาจปิดบังความเปราะบางต่อการหายไปของแหล่งข้อมูล

วัตถุประสงค์เฉพาะการทดลองรอบนี้คือ (1) จัดทำทะเบียนแหล่งอ้างอิงเพิ่มเติมแบบมีบริบทสมุนไพร/ส่วนที่ใช้/การเตรียมตัวอย่าง (2) ตรวจระดับความพึ่งพาแหล่งข้อมูล (3) วัดความเปลี่ยนแปลงของอันดับ embedding จากการนำ original-source ID ออกทีละแหล่ง โดยไม่ยืนยันว่าแหล่งข้อมูลที่ค้นเพิ่มเป็น independent test gold standard

## 2. ข้อมูลและเกณฑ์ตรวจ

- **Locked source:** v0.5 V3-derived chemistry proxy, 30 assertions, 25 ชื่อสาร, 10 สมุนไพร; ห้ามสลับกับ original Paper 1 chemistry panel โดยไม่มีหลักฐาน
- **Original bibliographic ledger:** 12 source IDs; 8/10 สมุนไพรมี original source เพียงหนึ่งรายการ
- **External corroboration:** ทบทวนแหล่งเปิดเผยต่อสาธารณะเพิ่มเติม 12 แหล่ง และผูกกับ assertion เฉพาะที่ข้อความใน abstract/หน้าบทความสนับสนุนได้; ได้ 23/30 assertions ที่มี candidate corroboration ใหม่ ไม่ใช่ 23 independently validated findings
- **Identity vs occurrence:** PubChem CID ใช้กับตัวตนสารเท่านั้น ไม่ใช่หลักฐานว่าสารพบในสมุนไพรหรือผลิตภัณฑ์ใด
- **Expert standard:** ช่อง expert labels 45 คู่ใน benchmark ยังคงว่าง; ไม่มีการสร้างผู้ประเมินมนุษย์เทียม

การพิจารณาแบ่งแหล่งเป็น primary analytical / primary isolation / government monograph / systematic review และแบ่งระดับการรองรับตามความตรงของ species, cultivar, plant part, processing และ chemical identity; ทั้งหมดเป็นการจัดประเภทแบบ AI-assisted provisional review ไม่ใช่ final full-text expert adjudication

## 3. การทดลอง

### 3.1 Source coverage audit

นับ original source IDs ที่ใช้รองรับ chemistry assertions แต่ละชนิด การพบสามสารจากบทความเดียวให้ **source count = 1** ไม่ใช่ 3 งานวิจัยอิสระ

### 3.2 Leave-one-source-out (LOSO) eligibility

สำหรับ original source ID ทั้ง 12 รายการ กำจัด assertion ทั้งหมดที่อ้าง source ID นั้น แล้วตรวจว่าสมุนไพรแต่ละชนิดยังมีข้อมูลเคมีอย่างน้อยหนึ่งรายการหรือไม่ หากสมุนไพรใดขาดข้อมูลเคมีหมด จะ **BLOCK** การเปรียบเทียบ embedding ของทั้ง 45 คู่ ไม่เติมข้อมูลแบบสังเคราะห์และไม่จัดอันดับสมุนไพรที่ไม่มีเคมี

### 3.3 Paired-seed model sensitivity

ใช้เฉพาะ source holdouts ที่ผ่านเกณฑ์ coverage; รันโมเดล Chem-Proxy และ Core-Proxy ชุด class candidate 19 กลุ่มจาก v0.5 แบบจับคู่ 10 seeds ก่อน–หลังตัดแหล่งหลักฐาน คำนวณ Spearman rho ของอันดับ cosine 45 คู่ และ Top-5 overlap; รายงานผลเป็น *exploratory ranking sensitivity* เท่านั้น

## 4. ผลการทดลอง

| รายการ | ผล |
|---|---:|
| Herb–compound original assertions | 30 |
| Distinct original source IDs | 12 |
| สมุนไพรที่พึ่ง original source เดียว | 8/10 |
| Assertion ที่เพิ่ม candidate corroboration URL | 23/30 |
| External studies/monographs catalogued | 12 |
| LOSO source tests | 12 |
| LOSO ที่ต้อง BLOCK เพราะสมุนไพรไม่มีเคมีเหลือ | 8 |
| LOSO ที่รัน Chem/Core ได้โดยมีข้อมูลครบ | 4 |
| Paired model/seed comparisons | 80 |

**การทดลอง sensitivity (ค่าเฉลี่ย 10 seeds):**

| Removed original source | Chem rank rho | Core rank rho | Chem Top-5 overlap | Core Top-5 overlap |
|---|---:|---:|---:|---:|
| DMSC_Garlic | 0.9113 | 0.7364 | 4.2 | 4.1 |
| DMSC_PiperRetrofractum | 0.7212 | 0.6560 | 4.0 | 3.6 |
| PubChem_DiallylSulfide | 0.9172 | 0.8065 | 4.5 | 4.6 |
| Retroframides2023 | 0.9129 | 0.7243 | 4.6 | 4.2 |

เมื่อเอา DMSC_PiperRetrofractum ออกจากเดิม ข้อมูลดีปลีเหลือเพียงสารที่อ้างอิง Retroframides2023; อันดับของ Chem/Core เปลี่ยนมากสุดในชุด LOSO ที่ผ่านเกณฑ์ครบทุกสมุนไพร

## 5. ประเด็นการตีความที่ต้องระวัง

**5.1 Garlic — processing effect:** รายการ diallyl sulfide (CA018) มีงาน GC-MS ในกระเทียมที่กลั่นเป็นน้ำมันระเหยรองรับ ไม่ควรอนุมานว่าอยู่ในกานกระเทียมสดด้วยความเข้มข้นเดียวกัน ส่วน allicin ไม่เสถียรและการเตรียมตัวอย่างเปลี่ยน constituent profile

**5.2 Holy basil — red cultivar:** งานวิเคราะห์ O. tenuiflorum สายพันธุ์ R มีผลวัด eugenol โดยตรง แต่หลักฐาน rosmarinic acid และ oleanolic acid ที่อ้างเพิ่มเป็นระดับ species ไม่ใช่ red cultivar โดยตรง

**5.3 Licorice — botanical authentication:** HPLC ของ Glycyrrhizae Radix ที่ตรวจ glycyrrhizin, liquiritin และ liquiritigenin ไม่จำเป็นต้องพิสูจน์ว่าแต่ละตัวอย่างเป็น Glycyrrhiza glabra L. โดยตรง

**5.4 Kaffir lime — stereochemistry:** การรายงาน D-limonene จาก GC-MS ไม่อนุญาตให้เติม PubChem CID แบบเจาะจง stereoisomer ให้กับต้นฉบับที่เขียนเพียง limonene

**5.5 Piper:** piperlongumine และ piperlonguminine เป็นสารต่างชนิด ห้ามใช้เป็น synonyms ของกันและกัน การศึกษาที่อ้างถึง P. longum ก็ไม่เท่ากับหลักฐานของ P. retrofractum

**5.6 Exploratory stats:** ค่าความสัมพันธ์จาก 10 seeds เป็นผลซ้ำภายในชุดข้อมูลเดียวกัน ไม่ใช่ตัวอย่างอิสระ 10 ชุด จึงไม่ใช้ค่า p ที่ปฏิบัติต่อ seeds ว่าเป็น independent biological replicates

## 6. ข้อสรุป

แหล่งหลักฐานเคมีของ 8/10 สมุนไพรมีความเปราะบางต่อการนำแหล่งต้นทางออกเพียงรายการเดียว อันเป็นเหตุให้ไม่สามารถทำ LOSO embedding แบบครบ 45 คู่ได้ใน 8/12 กรณี การเพิ่มแหล่ง literature corroboration ในรอบนี้ช่วยให้ตรวจข้อกล่าวอ้างเชิงบริบทได้มากขึ้น แต่ **ไม่ได้ทำให้กลายเป็น independent model validation** และไม่ได้กู้ 19 chemical classes หรือ embedding archive ของ Paper 1 เดิม

สำหรับต้นฉบับ Paper 1 ควรรายงานผลนี้เป็น post-hoc source-dependence and provenance audit และไม่เปลี่ยน primary outcome เดิมโดยอัตโนมัติ ควรมี independent formula/chemistry re-curation และ blinded pair assessment ก่อนอ้าง biological validity

## 7. เอกสารที่เกิดขึ้นใน v0.6

- `results/v06/assertion_evidence_qualification_30.csv` — evidence qualification ราย assertion
- `results/v06/new_public_study_registry_12.csv` — บรรณานุกรมแหล่งหลักฐานเพิ่มเติม
- `results/v06/herb_source_independence_10.csv` — source redundancy รายสมุนไพร
- `results/v06/leave_one_source_out_12.csv` — coverage breakdown แบบ LOSO
- `results/v06/source_holdout_embedding_eligibility_12.csv` — เกณฑ์รัน/งดรัน
- `results/v06/source_holdout_embedding_eligible_10seeds.csv` — 80 paired runs
- `results/v06/source_holdout_model_summary.csv` — aggregate descriptive statistics
- `dashboard/Paper1_Source_Independence_v0.6.html` — offline interactive
- `manuscript/Paper1_v0.6_Evidence_Qualification_Addendum.docx` — manuscript addendum (separate, not replacing original)

## 8. แหล่งข้อมูลที่ตรวจสอบได้ (selected APA 7 / metadata pending where not yet independently verified)

- Ashokkumar, K., et al. (2021). Phytochemistry and therapeutic potential of black pepper *Piper nigrum* essential oil and piperine: A review. *Clinical Phytoscience, 7*, Article 52. https://doi.org/10.1186/s40816-021-00292-2
- Janssen, A. M., & Scheffer, J. J. (1985). Acetoxychavicol acetate, an antifungal component of *Alpinia galanga*. *Planta Medica, 51*(6), 507–511. https://doi.org/10.1055/s-2007-969577
- Lee, S., et al. (2007). Liquid chromatographic determination of 6-, 8-, 10-gingerol, and 6-shogaol in ginger (*Zingiber officinale*) as the raw herb and dried aqueous extract. *Journal of AOAC International, 90*(5), 1219–1226. https://pubmed.ncbi.nlm.nih.gov/17955965/
- Wang, Y.-C., & Yang, Y.-S. (2007). Simultaneous quantification of flavonoids and triterpenoids in licorice using HPLC. *Journal of Chromatography B, 850*(1–2), 392–399. https://doi.org/10.1016/j.jchromb.2006.12.032
- World Wide Web Consortium. (2013). *PROV-O: The PROV ontology*. https://www.w3.org/TR/prov-o/
- World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/

**สำหรับแหล่งอีก 12 รายการและรายละเอียด exact source locator ให้ใช้ URL ใน `new_public_study_registry_12.csv` ร่วมกับบทความต้นฉบับ บรรณานุกรมนี้ไม่ใช่ final validated APA 7 bibliography ของบทความหลัก**

## 9. Gate สำหรับการตีพิมพ์

**ยังไม่ผ่าน publication-grade evidence freeze:** ยังต้องมี (1) original 30-row panel / class mapping confirmation (2) primary full-text source and plant part locators (3) independent human botanical/pharmacognosy adjudication (4) unbiased herb-pair gold labels and split preserving source independence. ไม่มีการแทนที่ gate เหล่านี้ด้วยคำตอบของ ChatGPT
