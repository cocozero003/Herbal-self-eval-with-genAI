# สถานะการปิด 4 Scientific Validation Gates — 7 พฤศจิกายน 2569

## Gate 1: Source-specific primary full text — ยังไม่ครบตามคำขอ

ตรวจทะเบียน original citations ทั้ง 100 assertions ด้วยเกณฑ์แยกประเภทหลักฐาน 5 primary full-text experimental source matches, 15 primary abstract mentions (ในนี้ 5 มีบริบท hydrolysis), 19 review source locators, 61 unresolved source/compound locators. การตรวจครบทุกรายการไม่เท่ากับการยืนยันหลักฐานเชิงทดลองครบ 100 รายการ ต้นฉบับอ้าง review จะไม่สามารถเปลี่ยนให้เป็น original primary article ได้โดยไม่เปลี่ยนแหล่งอ้างอิง. การตรวจเพิ่มเติม 11 observations เป็นอีกชุดอ้างอิง แยกออกจาก original source ทั้งหมด.

## Gate 2: SHACL Core — ผ่านจริงเฉพาะ shape profile ที่ใช้

GitHub Actions https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018 รัน official pySHACL v0.40.2 สำเร็จเมื่อ 7 พ.ย. 2569. สถานะ `PASS`, `sh:conforms = true`, 0 violations, 208 assertions, M3 2733 triples, shapes 34 triples และ negative controls 10/10. ผลจาก JSON/TTL ใน ZIP เป็น artifact จริงที่ดาวน์โหลดกลับจาก GitHub ไม่ใช่ผลจำลอง. ผลการผ่าน SHACL เป็น structural conformance ไม่ใช่ scientific validity.

## Gate 3: Independent expert gold — ยังทำแทนมนุษย์ไม่ได้

มี review candidate 45 กรณี: 32 development questions, 11 new external positive observations, 2 context traps. ยังไม่มี expert reviewer 1, reviewer 2, adjudicator ลงชื่อพร้อมวันที่, independent source blindness หรือ adjudicated gold. ระบบจึงบล็อกการคำนวณ accuracy/precision/recall ของ M1/M2/M3 ในฐานะ confirmatory benchmark. ห้ามบันทึกคำตอบของ ChatGPT สองรอบว่าเป็น independent human review.

## Gate 4: Original 35 classes + external source-disjoint — ยังไม่ปิดเชิงการรับรอง

ไม่มี 83-to-original-35 archive crosswalk ในไฟล์ที่ตรวจได้ จึงห้ามอ้าง exact replication. New 31-family chemical grouping is a deliberately new, non-equivalent, provisional name-based working taxonomy. ต้องตรวจ molecular structure, isomers, mixtures, processing transformations, authoritative ontology และผู้เชี่ยวชาญก่อนการใช้อ้างผล.

External pilot 11 records มี DOI ไม่ซ้ำ citation เดิม แยกต้นทางจาก development แต่ถูกเลือกหลังทราบเป้าหมายและมีเพียง positive cases จึงไม่ผ่านเกณฑ์ confirmatory prospective external test. ต้องล็อก benchmark ล่วงหน้า, เพิ่ม negative/counterexamples ที่แท้จริง, ทำ source-lineage exclusion, รับ expert gold จากคนจริง แล้วจึงคำนวณ paired M1/M2/M3 metrics.

## ผลงานส่งมอบ

CSV original 100, new pilot 11, compounds 83/31, review casebook 45, RDF M1/M2/M3, official pySHACL runtime JSON, authentic TTL validation report, 10 negative controls, code, CI workflow, offline HTML dashboard, verification manifest และเอกสารทบทวนของผู้วิจัย.
