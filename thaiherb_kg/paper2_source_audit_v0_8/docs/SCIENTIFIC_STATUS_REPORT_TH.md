# รายงานความก้าวหน้า ThaiHerb KG — Paper 2 v0.8 / Paper 3 v0.6

**วันที่:** 7 พฤศจิกายน 2569  
**สถานะ:** Research-development release; ยังไม่พร้อมอ้างการตรวจสอบความถูกต้องทางชีววิทยาหรือการเปรียบเทียบสมรรถนะ M1/M2/M3

## 1. สถานะ Paper 2

ใช้ข้อมูล Herb–Compound จากรุ่น v0.7 ที่มี **100 assertions / 83 internal compound identifiers / 20 source studies** คงเดิม และเพิ่มทะเบียนประเภทแหล่งหลักฐาน 20 แหล่ง (`P2_SOURCE_TYPE_AUDIT_20.csv`) โดยแบ่งเป็นบทความทบทวนเฉพาะพืช 12 แหล่ง, งานทบทวนระดับสกุล 3 แหล่ง และการศึกษาต้นฉบับหรือรายงานการวิเคราะห์ต้นฉบับ 5 แหล่ง ทั้งนี้ ประเภทบทความ **ไม่เท่ากับ** การยืนยันองค์ประกอบเคมีรายสาร

ระดับหลักฐานราย assertion ตามการตรวจที่สามารถพิสูจน์ได้:

| ระดับ | จำนวน | ข้อจำกัด |
|---|---:|---|
| PRIMARY_FULLTEXT_MATCH | 5 | *Piper retrofractum*: ตรวจ Table 3 ของ Luca et al. (2021); ไม่ได้รับรอง canonical structure หรือฤทธิ์ทางคลินิก |
| PRIMARY_ABSTRACT_ONLY | 5 | *Zingiber montanum*: ใช้ข้อมูลบทคัดย่อของ Verma et al. (2018) เท่านั้น |
| PRIMARY_ABSTRACT_AFTER_HYDROLYSIS | 5 | *Acacia concinna* (ชื่อเดิมของ *Senegalia rugata*): concinnosides A–E หลัง alkaline hydrolysis; **ห้าม** อ้างว่าเป็นสารอิสระในฝักที่ยังไม่ได้ผ่านกระบวนการ |
| SECONDARY_ABSTRACT_NAME_MATCH | 9 | *Piper nigrum* 5 และ *Ocimum tenuiflorum* 4 จากบทคัดย่อของบทความทบทวน ไม่ใช่ผลจากห้องทดลองของผู้เขียนทบทวน |
| SECONDARY_ONLY | 10 | ขิง 5 และกระเทียม 5; หลักฐาน secondary review ที่ได้รายงานไว้ใน v0.7 |
| NOT_VERIFIED | 66 | ไม่มีตำแหน่งหลักฐานรายสารที่ตรวจครบเพียงพอ |

**ข้อค้นพบสำคัญ:** แหล่ง DOI 10.1039/C6RA27830B เป็นงานทบทวน *Alpinia* หลาย species, DOI 10.3390/molecules28207117 เป็นงานทบทวน *Acorus* genus และ DOI 10.3390/nu10091196 เป็นงานทบทวน Curcuma spp.; ไม่อนุมาน presence ของ 15 species–compound assertions จากการมีชื่อ genus ในบทความเพียงอย่างเดียว

สำหรับ **H11** ต้องแยกผลของ *Terminalia chebula* fruit จากวัสดุแบบ insect gall และ **H13** ต้องแยก *Myristica fragrans* seed จาก aril; วัสดุต่างชนิดไม่ถือว่าเทียบเท่ากันโดยอัตโนมัติ

**สิ่งที่ยังขาด:** original 35-class chemical map, การตรวจ PubChem CID / ChEBI ที่ยืนยันในบริบทสารและ isomer, source-disjoint external validation, reviewer 2 คนและ adjudicated gold, และการทำ sensitivity/retraining ที่ใช้ข้อมูล frozen ซึ่งผ่าน source audit แล้ว

## 2. สถานะ Paper 3

ข้อมูล V3 **208 assertions** คงเดิม (`P3_V3_208_LOCKED.csv`, SHA-256: `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`), ได้แก่ formula 71, chemistry 100, pharmacology-target 30 และ clinical 7

- พบ **45 source IDs** ใน CSV; ตัวเลข historical reference registry **67** ยังไม่ได้มีต้นฉบับครบให้ cross-check ว่าแตกต่างเพราะการคัด subset หรือรายการตกหล่น
- Clinical assertions **7 รายการ** ไม่มี canonical object ID; ระบบเก็บคำอธิบายเดิมเป็น literal ไม่สร้าง IRI ทางการแพทย์ขึ้นมาเอง
- Chemistry assertions **100 รายการ** ยังมี source-locator audit queue; ไม่มีหลักฐานเฉพาะสารจาก M3 ที่ทำให้ได้ผ่านทั้งหมดอัตโนมัติ
- M1 มี **207 distinct triples**, M2 มี **1,501**, M3 มี **2,733** (v0.5 baseline) โดยพบ 1 SPO collision ระหว่าง CLIN005/CLIN006 ซึ่งเป็นการสูญเสีย assertion identity เมื่อยุบ subject–predicate–object ไม่ใช่ผลยืนยันความขัดแย้งทางคลินิก
- มีคำถามพัฒนาระบบ **8 คำถาม × 3 models = 24 deterministic RDF-query outputs**; ยังไม่มีคะแนน accuracy, CI, F1 หรือ reviewer agreement เพราะไม่มี adjudicated gold

## 3. การทดสอบและขอบเขตคำว่า PASS

`pytest` และ HTML browser smoke test ที่รันในสภาพแวดล้อมนี้มีความหมายด้านการทำงานของโค้ดและความสอดคล้องข้อมูลเท่านั้น ทั้งนี้ `pySHACL` ไม่สามารถติดตั้งผ่าน package index ของสภาพแวดล้อมนี้ได้ จึงตั้ง `SHACL_CORE = NOT_RUN`; การผ่าน custom constraints ไม่อาจแทนการผ่านมาตรฐาน SHACL Core

## 4. เงื่อนไขก่อน Manuscript-ready

- Paper 2 ต้องตรวจ 66 compound assertions ที่เหลือพร้อม page/table และ primary-source origin หรือแยกออกเป็น restricted reconstruction; บทความสามารถเขียนเป็น internal robustness study โดยจำกัด scope ถ้าไม่มี source-disjoint external benchmark
- Paper 3 ต้องรัน pySHACL จริงบน graph เดิมและ defect tests ทั้ง 4 กรณี; ตรวจ 7 clinical canonical objects และ source registry; สร้างคำถาม **prospectively โดยผู้เชี่ยวชาญจริง** แล้วใช้ two-blind review/adjudication จึงเริ่ม paired M1/M2/M3 accuracy benchmark ได้
- Paper 1/2/3 ต้องมี editorial overlap control และ human author approval ก่อนส่งวารสาร

## 5. เอกสารอ้างอิงหลัก (APA 7)

Ashokkumar, K., Murugan, M., Dhanya, M. K., Pandian, A., & Warkentin, T. D. (2021). Phytochemistry and therapeutic potential of black pepper [*Piper nigrum* (L.)] essential oil and piperine: A review. *Clinical Phytoscience, 7*, Article 52. https://doi.org/10.1186/s40816-021-00292-2

Bhattarai, K., Bhattarai, R., Pandey, R. D., Paudel, B., & Bhattarai, H. D. (2024). A comprehensive review of the phytochemical constituents and bioactivities of *Ocimum tenuiflorum*. *The Scientific World Journal, 2024*, Article 8895039. https://doi.org/10.1155/2024/8895039

Gafur, M. A., Obata, T., Kiuchi, F., & Tsuda, Y. (1997). Acacia concinna saponins. I. Structures of prosapogenols, concinnosides A–F, isolated from the alkaline hydrolysate of the highly polar saponin fraction. *Chemical & Pharmaceutical Bulletin, 45*(4), 620–625. https://doi.org/10.1248/cpb.45.620

Sommer, A. (2026). *pySHACL* (Version 0.40.2) [Computer software]. https://pypi.org/project/pyshacl/

World Wide Web Consortium. (2017). *Shapes constraint language (SHACL)*. https://www.w3.org/TR/shacl/
