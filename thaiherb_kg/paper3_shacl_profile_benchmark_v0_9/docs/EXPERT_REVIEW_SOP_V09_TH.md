# SOP สำหรับ Independent Expert Review — Paper 3

**หลักการ:** ใช้ผู้ประเมินจริงอย่างน้อยสองคน โดยไม่เห็นผลโมเดลอื่นและไม่เห็นคำตอบของอีกคนก่อนเสร็จรอบแรก คำตอบที่ AI สร้างไม่ใช่ independent gold

## ขั้นตอน

1. ตรวจคุณสมบัติและ conflict of interest ของผู้ทบทวนแต่ละราย เก็บ reviewer ID แบบไม่เปิดเผยชื่อในข้อมูลเผยแพร่
2. กำหนด inclusion/exclusion criteria ของ 32 competency questions และตรวจว่าโจทย์แต่ละข้อถามข้อมูลที่ชุดต้นฉบับรองรับจริง รวมถึงคงข้อที่ต้องงดตอบเมื่อหลักฐานไม่เพียงพอ
3. ล็อกชุดคำถามและแหล่งข้อมูลล่วงหน้า ไม่ดึงบทความที่ผู้วิจัยใช้พัฒนาโมเดลเข้ามาปะปนชุด holdout
4. Reviewer 1 และ Reviewer 2 อ่านแหล่งเดิม independently บันทึก gold response, citation IDs, evidence sufficiency, source/date, reviewer confidence, และ rationale
5. Adjudicator แยกต่างหากดูเฉพาะกรณีที่เห็นต่าง แล้วบันทึก final adjudicated gold พร้อม audit trail
6. Lock model outputs M1/M2/M3 ภายใต้ dataset/model settings เดียวกัน สุ่มรหัสลำดับคำตอบก่อนให้ blind assessor ตรวจ
7. ให้คะแนน answer_correct, citation_correct, evidence_complete และ abstention_appropriate เป็น 0/1 ตาม rubric ที่ผู้วิจัยประกาศไว้ล่วงหน้า
8. เมื่อตรวจครบเท่านั้นจึงใช้ `src/blind_benchmark_v09.py` สำหรับ paired metrics, McNemar exact และ bootstrap CI

## ข้อห้าม

ห้ามใช้ ChatGPT คนเดียวเป็น reviewer สองคนเพื่อรายงาน inter-rater reliability อิสระ ห้ามเติมค่าที่ไม่มีใน original source ห้ามเลือก threshold หรือคัดเฉพาะโจทย์ที่ M3 ตอบได้ดีหลังเห็นผล

## Files

- Template gold reviewer: `results/P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv`
- Three-model blind scores: `results/P3_V09_BLINDED_SCORING_TEMPLATE_96.csv`
- Scoring gate: `results/P3_V09_BENCHMARK_GATE_REPORT.json`
