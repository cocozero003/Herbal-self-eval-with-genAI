# ขั้นตอนตรวจรับข้อมูล Paper 1 ก่อนการ Freeze

## Gate 1: Formula source integrity (ยังไม่ผ่าน)

1. ตรวจเอกสารทางการ DTAM/อย. พ.ศ. 2566 ที่ https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf
2. จับคู่ F01–F10 กับชื่อสูตร **และรูปแบบยา** ตามหน้าเอกสาร ไม่อาศัยลำดับหมายเลขที่สร้างขึ้นใน pipeline เพียงอย่างเดียว
3. เทียบสมุนไพรเป้าหมายทั้ง **10 ชนิดสำหรับทุกสูตร** ไม่ใช่ตรวจเฉพาะ 46 เส้นที่บันทึกไว้ เพราะอาจมีทั้ง false-positive และ false-negative edges
4. เก็บ locator แยกหน้าพิมพ์/เลขหน้า PDF และชื่อวิทยาศาสตร์จากสูตรต้นฉบับ รวมส่วนของพืช; บันทึกผลว่าพบ/ไม่พบ/กำกวม และ reviewer/source checksum
5. ตรวจรูปแบบแคปซูล/ผง/เม็ด/ลูกกลอนที่ต่างกันว่าใช้สูตรแม่บทเดียวกันจริงหรือไม่
6. ตรวจ alias ยาไฟประลัยกัลป์ / ยาไฟประสะกัลป์ จากสารบัญและเนื้อหา โดยไม่ auto-normalize ก่อน adjudication
7. จัดทำ source-backed coverage 100 สูตร–สมุนไพร (10x10) แล้วลงชื่อผู้ตรวจอย่างอิสระ; แก้ไขเฉพาะ verified rows

## Gate 2: Chemistry provenance (ยังไม่ผ่าน)

- กู้ original 30 Herb–Compound records และ 19 CompoundClass assignments จากอาร์ไคฟ์ต้นฉบับ ไม่ใช้ V3 3-per-herb proxy แทนโดยอัตโนมัติ
- เพิ่ม DOI/URL, table/page/figure, plant part, preparation, analytical method, compound ID และ evidence type ต่อแถว
- แยก compounds observed in material ออกจาก compounds mentioned in a review; หลีกเลี่ยงการอนุมาน exposure/efficacy
- บันทึก reviewer decision, timestamp, data-license status, record SHA และ source manifest

## Gate 3: Models & validation (ยังไม่ผ่าน)

- Freeze source corpus with source checksums; archive all intermediate transforms
- รัน Cooc/Chem/Core ตาม parameters และ random seeds ใน manuscript
- เปรียบเทียบ NPMI vs support/degree adjustment พร้อม external task validity และ source-perturbation effect
- ใช้ชุด pairs ประเมินที่ไม่รั่วไหลจาก formula/chemistry input และแสดง uncertainties จาก corpus size
- เก็บ seed-wise 45-pair vectors และ full source-level dependency graph

## Gate 4: Publication decisions

- คงค่าดั้งเดิมในบทความเป็น manuscript-reported ไม่แก้ให้ตรง proxy โดยอัตโนมัติ
- เมื่อมี original verified freeze ให้ rerun pipeline แล้วรายงานการเปลี่ยนแปลงแบบ transparent correction / supplementary analysis
- ไม่ใช้วลีว่า "source verified", "biologically validated" หรือ "reproduced original embeddings" หากไม่มีหลักฐานตรงกัน

## Paper 2–3 dependencies

- Paper 2 ต้องยืนยันการไม่ปะปนกันของ formula versions และ source class mappings ก่อนแปลผลการเปลี่ยน weighting
- Paper 3 ควรนำ false-positive F05 และ alias F03 เป็น negative-control cases ของ provenance/document-consistency validation
