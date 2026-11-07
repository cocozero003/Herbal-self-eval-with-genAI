# ข้อเสนอการแก้บทความ Paper 1 ตาม Source Audit

## ข้อค้นพบ

การตรวจต้นฉบับเอกสาร DTAM/อย. พ.ศ. 2566 พบ false-positive 3 ความสัมพันธ์ในข้อมูลสูตรตำรับที่สร้างกลับจาก V3 สำหรับ F05 (ยาประสะว่านนางคำ ชนิดผง, หน้าพิมพ์ 161) ขิง ดีปลี พริกไทย ไม่อยู่ในตารางตัวยาสำคัญของฉบับที่เลือก แต่มีการใส่ในกราฟที่ใช้เป็นข้อมูลสาธิต Paper 1 ของโครงการ

ข้อค้นพบนี้ **ยังไม่ใช่หลักฐานว่า manuscript Paper 1 ฉบับส่งพิจารณาเคยใช้ข้อมูลผิดนั้น** เพราะไม่มีไฟล์ import และ training source ต้นฉบับให้ตรวจตรงกัน ต้นฉบับรายงาน 46 membership และ 23 positive-NPMI ซึ่งเป็นจำนวนเดียวกับ proxy แต่ตัวเลขรวมเท่ากันไม่ได้ยืนยัน identity ของแต่ละแถว

## คำที่ควรใช้

- "V3-derived reconstructed projection" แทน "original Paper 1 dataset" สำหรับผลวิเคราะห์ v0.3
- "partial source-correction sensitivity" แทน "corrected gold graph" จนกว่า 100 membership decisions (10 สูตร × 10 herbs) ผ่านการตรวจครบ
- "Cooc embedding reimplementation" แทน "reproduction of original published vectors"
- "source-document discrepancy in downstream proxy" แทน "error in manuscript" จนมีหลักฐานยืนยันการใช้ข้อมูลชุดเดียวกัน

## การเปรียบเทียบเพื่ออภิปราย

- ข้อมูล proxy 46 memberships / 23 positive edges เปลี่ยนเป็น 43 / 24 หลังแก้เฉพาะ F05 (3 false positives)
- อันดับ NPMI 45 คู่มี Spearman rho 0.9056 และ Top-5 overlap 3/5
- Matching 10-seed Cooc experiment มีอันดับก่อน/หลังเฉลี่ย Spearman rho 0.7675 (Original NPMI) ถึง 0.8056 (Combined)
- ไม่ควรแปลผลเป็น improvement of biological validity โดยไม่มี independent gold labels

## เอกสารที่ต้องจัดทำเพิ่มก่อนส่งต้นฉบับ

1. Source registry แบบ row-level สำหรับ formula memberships ทั้ง positive/negative
2. Source registry / compound class table สำหรับ original chemical panel
3. Protocol และ code ที่ rebuild Cooc, Chem, Core ได้โดย seed/parameter lock
4. Evaluation on independently adjudicated herb-pair pairs; absence of a link means not curated, not proof of absence
