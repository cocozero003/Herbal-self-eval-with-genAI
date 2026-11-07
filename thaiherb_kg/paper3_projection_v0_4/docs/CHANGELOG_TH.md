# CHANGELOG: ThaiHerb P2 v0.6 / P3 v0.4

- ยึด frozen Paper 2 v0.5 100 chemical assertions และ Paper 3 V3 208 assertions โดยไม่แก้ข้อมูลต้นฉบับ.
- ตรวจ source exact table จริงเฉพาะ P. retrofractum 5 รายการ; ตั้งสถานะอีก 95 รายการเป็น NOT_VERIFIED ต่อไป.
- ตรวจชื่อบทความเพิ่มเติมสำหรับ ginger, Terminalia chebula และ Curcuma โดยแยก bibliographic check จาก claim-specific review.
- สร้าง RDF M1/M2/M3 จาก 208 claims เดียวกัน และพบ SPO collision ของ CLIN005/CLIN006.
- สร้างชุดคำถาม benchmark หมวดละ 1 แถวเป็น template เปล่า โดยไม่สร้าง expert gold.
- เพิ่มรหัสทดสอบ structural negative controls และตัวเรียก pySHACL ที่คืน NOT_RUN ถ้าติดตั้งไม่ได้.
- จัดทำ HTML dashboard สองฉบับที่อ่านได้โดยไม่ต้องเชื่อมอินเทอร์เน็ต.
