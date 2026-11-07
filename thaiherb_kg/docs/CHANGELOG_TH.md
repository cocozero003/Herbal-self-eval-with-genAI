# บันทึกการปรับปรุง ThaiHerb KG v0.2 — 7 พฤศจิกายน 2569

## Stage 0 — Data integrity
- เก็บ snapshot แยก Paper 1/2/3 พร้อม SHA-256 และ crosswalk
- ตรวจชุด assertion ซ้อนกัน โดย **ไม่ถือว่า assertion ID ตรงกันพิสูจน์เอกสารต้นฉบับตรงกัน**

## Stage 1 — Paper 1
- คำนวณ positive NPMI ใหม่จากข้อมูลที่มี (10 herbs, 10 formulas)
- เปรียบเทียบ Original NPMI, support-k=2, degree correction, combined
- ทดลอง leave-one-formula-out (LOFO) บน **edge ranks** ไม่อ้างเป็นผล embedding หรือ biological validation
- คงผล experiment 2026-11-06 เป็นงาน exploratory แยกจาก manuscript

## Stage 2 — Paper 2
- ขยาย ablation วิธีเดิมเป็น 20 herbs และ 190 pairs
- ตรวจ formula support; คำนวณ chemistry Jaccard และ IDF-weighted Jaccard เฉพาะ compound IDs ที่มี
- ยังไม่ใช่ molecular fingerprint/Tanimoto และไม่ใช่ source-independent gold-standard evaluation

## Stage 3 — Paper 3
- ตรวจ missing canonical IDs, source references และ locator ของ 208 assertions
- ส่งออก RDF โดยไม่ invent ID ของ clinical endpoints ที่ไม่มี
- สร้าง contradiction adjudication queue จาก 4 review candidates และ blank competency-question benchmark 8 categories
- ยัง **ไม่ได้รัน pySHACL** ในสภาพแวดล้อมนี้ และยังไม่มี expert benchmark

## ขั้นตรวจรับงานก่อนตีพิมพ์
1. Retrieve original documents and row-level source citations.
2. Freeze source snapshots and exact methods/versions.
3. Pre-register paired metrics and blind expert questions.
4. Run independent tests; report effect sizes, confidence intervals and failure cases.
5. Preserve the original baseline and mark all sensitivity results as additional analyses.

## Scientific release gating (สำคัญ)
- กราฟ Paper 3 ขนาด 1,497 triples เป็น **projection ที่สร้างใหม่จาก 201 assertions** ไม่ใช่กราฟ 5,148 triples ต้นฉบับ V3
- ฐานรายการ sources ของ UI subset มี **45 source IDs** ขณะที่ร่างต้นฉบับกล่าวถึง 67 evidence sources; ต้องตรวจเหตุผลของความต่างก่อนสรุปครบถ้วน
- Chemistry assertions 100 แถวมี source locator แบบไม่ระบุหน้า/ตารางระดับสารแบบสม่ำเสมอ ส่วน Clinical 7 แถวไม่มี canonical object ID
- pySHACL ไม่สามารถติดตั้งใน runtime นี้เนื่องจากไม่มีการเชื่อมต่อ package index จึงระบุสถานะ **NOT RUN** ไม่รายงาน SHACL passed
- ผู้เชี่ยวชาญยังไม่ได้ทำ annotation หรือ adjudication; blank templates ใช้สำหรับเริ่มกระบวนการเท่านั้น
