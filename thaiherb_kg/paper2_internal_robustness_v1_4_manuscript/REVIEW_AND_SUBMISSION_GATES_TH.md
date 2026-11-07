# Paper 2 — รายงานตรวจความพร้อมก่อนส่งวารสาร (Author Review)

**เวอร์ชันต้นฉบับ:** v1.4 manuscript development จากผลเชิงคำนวณ v1.3, 7 พฤศจิกายน 2569  
**ประเภทบทความ:** Original research — computational internal robustness; ไม่ใช่ clinical or pharmacological validation

## เนื้อหาที่เสร็จแล้ว

- ต้นฉบับภาษาอังกฤษฉบับเต็ม 4,700+ คำ มี Abstract, Introduction, Methods, Results, Discussion, Conclusion, References แบบ APA 7, research transparency declarations
- ตาราง 2 ตาราง ประกอบด้วย 9 perturbation conditions และ LOFO 8 ranking methods (6 full folds, 4 partial folds)
- รูป 4 รูปจากผล v1.3 ได้แก่ seed stability, perturbation, LOFO AP และ cold-start coverage
- ตรวจตัวเลขสำคัญกับ CSV ต้นทางของ v1.3 ผ่านใน `MANUSCRIPT_NUMERIC_AUDIT.json`
- ยืนยันชื่อหนังสืออ้างอิงทางราชการจากภาพปก PDF ต้นฉบับ ไม่สร้างชื่อหนังสือขึ้นใหม่
- DOCX ผ่านการ render และตรวจดูแต่ละหน้าจนครบ 11 หน้า

## ข้อจำกัดทางวิทยาศาสตร์ที่ยังต้องรักษา

1. ผล AP/AUROC วัด co-membership ในตำรับที่กันไว้ ไม่ใช่ความคล้ายคลึงทางเภสัชวิทยาหรือ clinical outcomes
2. ข้อมูลมีเพียง 10 selected formula documents; 6 full folds, 4 cold-start folds ไม่อาจแทนความหลากหลายของตำรับทั่วประเทศไทย
3. ข้อมูลเคมี 100 assertions มี original-source primary full text verified เพียง 5; การใช้สาร 5 รายการต่อสมุนไพรเป็นการคัดเลือก ไม่ใช่ exhaustive chemical composition
4. Historical 35-class mapping ไม่พบ; 31-family sensitivity ไม่เท่ากับการ replicate ontology เดิม
5. ไม่มี independent biological expert gold และ pilot 11 positives ไม่เหมาะกับ confirmatory external AP/AUROC
6. Percentile cluster bootstrap resamples สูตรตำรับเพียง 6 รายการใน full stratum; ช่วงความเชื่อมั่นเป็น exploratory ไม่ใช่การยืนยัน hypothesis
7. Paper 2 and Paper 3 source snapshot อาจต่างกัน 74 vs 71 formula memberships; ห้ามรวมตัวเลขข้าม frozen version

## ขั้นตอนที่ผู้เขียนต้องตรวจจริงก่อน submission

- ใส่ชื่อผู้เขียน ตำแหน่ง สังกัด และยืนยัน authorship / corresponding author
- Confirm contributor statements, funding, conflict of interest, use-of-AI declaration และ research ethics/exemption ตามเกณฑ์สถาบัน
- อ่าน References ทั้งหมดจากต้นฉบับเผยแพร่ โดยเฉพาะเอกสารราชการภาษาไทย ตรวจ publisher attribution และการตีพิมพ์ปี 2566
- ตรวจตารางตำรับต้นฉบับ กรณีชนิดสมุนไพร–ส่วนที่ใช้ที่ยังเป็น species-level mapping
- เลือกวารสารและปรับ word limit, abstract format, article type, tables/figure resolution, referencing style
- ตรวจซ้ำว่าส่วนเชิงสถิติเรียกว่า exploratory formula-cluster bootstrap เสมอ
- เมื่อมี independent expert gold จึงค่อยตีความความแม่นยำทางชีวภาพและ external validity ในงานแยก ไม่เพิ่มคำกล่าวอ้างในบทความนี้

**Research stage:** Full author-review manuscript complete; NOT journal-submission certified until the author checks above.
