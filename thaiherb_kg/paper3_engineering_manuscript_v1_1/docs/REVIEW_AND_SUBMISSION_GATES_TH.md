# Paper 3 v1.1 — สถานะการส่งบทความและสิ่งที่ต้องตรวจรับรอง

**ทำเสร็จใน ChatGPT:** สร้าง manuscript ภาษาอังกฤษฉบับเต็ม; ตรวจ 208 source assertions; เปรียบเทียบ M1/M2/M3 แบบ structural ด้วย 624 records; ทำ qualifier ablation; ตรวจ clinical-context queue; รวมผล pySHACL Core ที่รันจริงและผ่านบน GitHub Actions; ทดสอบโค้ดและ dashboard; ตรวจ layout Word.

**เงื่อนไขที่ผ่าน:**
- Frozen corpus SHA-256 ตรงกับ V3: `59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774`.
- M1/M2/M3 = 207/1,501/2,733 triples; recuperability counts 208/208 edges ทุกแบบ, source IDs 0/208/208 และ evidence context 0/0/208.
- pySHACL Core v0.40.2 ตรวจ shape profile โครงการผ่านจริง: 0 violations, negative controls 10/10. อ้าง CI: https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018 .
- ตารางและรูปตรงกับ computed CSV; เอกสาร Word ผ่าน render และตรวจหน้ากระดาษ.

**ข้อจำกัดที่ยังไม่สามารถใช้ ChatGPT ปิดแทนมนุษย์ได้:**
- Independent expert-adjudicated gold: 0/45. ต้องมีผู้ทรงคุณวุฒิที่มีตัวตนจริงสองคนทำ blind review และบุคคล adjudicate ด้วยหลักฐานก่อนวัด answer accuracy.
- ข้อมูล clinical 7 รายการยังเป็นข้อความ ไม่มี canonical object IDs ใน original source freeze; ไม่สามารถแอบเติมตัวระบุหรืออ้างว่าความขัดแย้ง 3 กลุ่มได้รับการตัดสินแล้ว.
- การตรวจ primary/fulltext ทุก chemistry assertion ไม่ได้ครบจากการมี source ID เท่านั้น.
- SHACL Core profile ที่ทดสอบเป็น structural contract เฉพาะ ไม่ใช่การรับรองความครบถ้วนของศัพท์ plant part/preparation/assay หรือความถูกต้องของ clinical conclusion.

**คำแนะนำสำหรับส่งวารสาร:** ใช้หัวข้อ engineering representation/fidelity/SHACL ที่ตรงกับหลักฐานปัจจุบัน ไม่ใช้หัวข้อ `improved answer accuracy` หรือ `validated clinical contradictions`. ขอความเห็นผู้ร่วมวิจัยเรื่องทบทวน source ราย assertion, ความต่างกับ Paper 2 และ Declaration ก่อน submission.
