# ThaiHerb Paper 2 v1.4 — ต้นฉบับบทความวิจัย

วันที่ 7 พฤศจิกายน 2569 | สถานะ: Author-review manuscript (ยังไม่ใช่ฉบับรับรองให้ส่งวารสาร)

## การปรับเป้าหมายบทความ

ชื่อเรื่อง: **Internal Robustness, Data-Source Sensitivity, and Representation Stability of Herbal Knowledge Embeddings: A Reproducible Study of 20 Thai Medicinal Herbs and 10 Traditional Formulas**

เนื้อหาพิสูจน์ความเสถียรของ embeddings ต่อ random seed และการเปลี่ยนข้อมูล ตั้งเป้าทำนาย **การปรากฏร่วมในตำรับที่กันไว้ทดสอบ** ไม่ใช่ผลด้านเภสัชวิทยาหรือประสิทธิผลทางคลินิก

## สิ่งที่อยู่ในชุดงาน

- Word manuscript ภาษาอังกฤษ มีบทคัดย่อ, Introduction, Methods, Results, Discussion, Conclusion, Declarations และ References (APA 7)
- Markdown ฉบับแก้ไขบน GitHub ได้
- 4 tables และ 4 figures จากผล Paper 2 v1.3 จริง
- JSON สำหรับยืนยันตัวเลขหลักและระบุขอบเขตของการศึกษานี้

## ความเห็นผู้แก้ไขต้นฉบับที่สำคัญ

1. การประเมิน LOFO แบบครบ 190 คู่มี 6 folds; อีก 4 folds เหลือ 171 คู่ ต้องไม่รวมกันโดยไม่อธิบาย
2. Bootstrap ช่วงความเชื่อมั่นที่สุ่มซ้ำระดับสูตรตำรับเป็นเพียง exploratory เพราะมี 6 สูตรตำรับในชุด complete-fold
3. Chemistry 100 claims เป็นชุดที่คัดเลือกไว้ ไม่ใช่สารทั้งหมด; original-source primary full-text verified ยัง 5/100 เท่านั้น
4. การรัน 20 random seeds ไม่ได้เพิ่มจำนวนสูตรตำรับอิสระ
5. ไม่มีการกู้คืน class mapping 35 กลุ่มเดิม; 31-family จัดเป็น sensitivity analysis เท่านั้น
6. ไม่มี expert biological gold หรือการทดสอบ external generalizability แบบ confirmatory
7. ต้องให้ผู้วิจัยยืนยันผู้แต่ง ที่สังกัด แหล่งทุน ผลประโยชน์ทับซ้อน สิทธิ์ข้อมูล และรายละเอียดตามรูปแบบวารสารก่อน submission

## ข้อมูลต้นฉบับและการทำซ้ำ

ข้อมูลการคำนวณทั้งหมดอยู่ใน [Paper 2 v1.3 Full Research Package](https://drive.google.com/file/d/1CLSvyUsF_8GEDgRhtYlVLMAAD3PWdXmE/view) และแยก source code ใน [GitHub branch v1.3](https://github.com/cocozero003/Herbal-self-eval-with-genAI/tree/thaiherb-p2-internal-robustness-v1.3-20261107)

ผลนี้เป็น **internal computational robustness** ไม่ใช่การยืนยันเชิงคลินิก
