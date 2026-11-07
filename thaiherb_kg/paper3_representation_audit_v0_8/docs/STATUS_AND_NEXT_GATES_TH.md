# รายงานสถานะ ThaiHerb KG — Paper 2 v1.0 / Paper 3 v0.8

วันที่ 7 พฤศจิกายน 2569

## งานที่รันและตรวจยืนยันได้

1. ตรวจ schema และ input SHA-256 จาก archive ล่าสุด ก่อนสร้าง release ต่อเนื่อง
2. เพิ่มหลักฐานจากการทดลองปฐมภูมิของ *Coriandrum sativum* 5 assertions ในทะเบียน corroboration แยกจาก original source โดยเก็บ Table 3/4, เทคนิควิเคราะห์, บริบท commercial fruit essential oil และตัวหารของตัวเลข
3. สร้างระเบียนเตือนบริบทการอ้างอิง *Plumbago indica* 5 assertions จากบทนำกับตารางผลทดลอง โดยไม่ระบุว่าไม่พบสารจากการตรวจที่ยังไม่ครบ
4. สร้าง 100-row audit ledger โดยไม่มีการเปลี่ยน disposition เดิม
5. วิเคราะห์การคงข้อมูลของ M1/M2/M3 624 รายการ ตรวจ 208 assertions เท่ากัน พบ 1 SPO collapse ที่เกี่ยวกับ CLIN005/CLIN006
6. สร้าง HTML dashboard ออฟไลน์ มีแท็บค้นหา/กรองข้อมูล และทดสอบการทำงานด้วย Chromium

## ขอบเขตข้อสรุป

- 5/100 เป็นจำนวนที่ผ่าน original-source primary full-text matching จากรอบก่อน; 9 claims มีหลักฐาน corroboration จากแหล่งอื่นเพิ่มเติม (ไม่ใช่ต้นฉบับเดียวกัน)
- ตัวเลข 0/208 vs 208/208 ของ representation fields เกิดจากความแตกต่างของ schema ไม่ใช่ผลประเมินคุณภาพของคำตอบ AI
- `pySHACL` ยังติดตั้งไม่ได้จากระบบนี้: SHACL Core `NOT_RUN`
- ข้อมูล clinical 7 รายการขาด canonical object ID; เก็บเป็น text/context แทนการสร้าง IRI วิทยาศาสตร์ปลอม
- ไม่มี expert gold หรือ external source-disjoint test set ตามการ preregistration จึงไม่อ้าง model superiority หรือ generalizability
- ชุดงานนี้สำเร็จในระดับ research engineering / author review เท่านั้น ไม่ใช่ manuscript-ready validation

## สิ่งที่ยังต้องทำเพื่อปิด publication gates

1. ผู้เชี่ยวชาญตรวจ 95 original-source chemistry assertions ที่ไม่ผ่าน primary full-text match อย่างครบถ้วน
2. ค้นต้นฉบับ 35 chemical classes หรือประกาศ candidate taxonomy ใหม่ที่ไม่เทียบเท่ากับของเดิม
3. พัฒนา genuinely independent external held-out corpus โดยตัดความซ้ำกับแหล่งที่ใช้พัฒนาโมเดล
4. ติดตั้งและรัน `pySHACL` จริง พร้อมเก็บ positive/negative RDF reports
5. ผู้ทบทวนจริงสองคนให้คะแนน 32+ competency questions และ adjudicate gold ก่อนวิเคราะห์ model accuracy

การที่ gates เหล่านี้ยังค้าง ไม่ใช่เหตุผลให้เติมค่า p-value คะแนนหรือการรับรองสมมติลงในรายงาน
