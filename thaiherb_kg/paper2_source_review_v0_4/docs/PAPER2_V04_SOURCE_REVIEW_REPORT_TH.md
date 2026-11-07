# ThaiHerb Paper 2 — Source-Reviewed Graph Robustness v0.4

**วันที่:** 7 พฤศจิกายน 2569  
**สถานะ:** AI-assisted source review + new 20-seed exact-compound reconstruction; **not** original Paper 2 35-class replication; **not** independent expert validation.

## ข้อค้นพบที่สำคัญ

กราฟ Paper 2 v0.3 นำสูตรตำรับจาก V3 มาใช้รวม **71** memberships แต่เมื่อทบทวนสูตรที่เลือกทั้ง 10 ตำรับจากหนังสือทางการ DTAM/อย. พ.ศ. 2566 และตรวจ H11–H20 ทุกคู่ พบ F09 ยาวิสัมพยาใหญ่ขาดสมุนไพร **H11 สมอไทย, H15 เทียนดำ และ H17 ว่านน้ำ** จำนวน 3 เส้น จึงสร้างกราฟ projection ระดับ botanical species ใหม่ **74** memberships โดยไม่เปลี่ยนต้นฉบับ v0.3.

**ความแตกต่างด้าน species vs medicinal material:** F08 ยามหาจักรใหญ่มี *โกฐพุงปลา* ซึ่งเป็น gall จาก *Terminalia chebula* ไม่ใช่เนื้อผล *สมอไทย* แม้ species-level projection จะเชื่อม H11 ในสูตรนั้นก็ตาม. F01 มีเนื้อผลสมอไทยและโกฐพุงปลาในสูตรเดียว; F09 มีสมอไทยและสมอเทศจาก species เดียว. ลูกจันทน์ (เมล็ด) และดอกจันทน์ (เยื่อหุ้มเมล็ด) มาจาก species เดียวกันแต่เป็นคนละเครื่องยา. ความแตกต่างนี้ถูกบันทึกใน review matrix ไม่ใช้แทน therapeutic equivalence.

## วิธีตรวจข้อมูล

- ตรวจ 10 สูตรจากตารางส่วนประกอบในหนังสือ DTAM/อย. และอ่านหน้าต่อเนื่องโดยไม่ตัดรายการท้ายตาราง
- H11–H20: ตรวจ 100 cells ครบทั้ง presence และ absence ในสูตรที่เลือก โดยบันทึก printed pages และ PDF pages
- H01–H10: รับช่วงจาก Paper 1 source-reviewed snapshot (single-curator) ไม่อ้างว่าตรวจอิสระซ้ำสองคน
- แยก canonical botanical species ออกจาก medicinal material; ไม่อนุมานว่าพืชต่างส่วนหรือเตรียมต่างวิธีใช้แทนกันได้
- เครื่องมือและผู้ตรวจ: ChatGPT-assisted, single-curator documentary audit, **ไม่มี blind human adjudication**

## ผลกระทบต่อกราฟ

| ตัวชี้วัด | ผล |
|---|---:|
| Membership ก่อนตรวจ | 71 |
| Membership ระดับ species หลังตรวจ | 74 |
| Material-projection sensitivity (ตัด F08/H11 gall) | 73 |
| คู่สมุนไพรทั้งหมด | 190 |
| คู่ที่ NPMI เปลี่ยนจากการแก้ F09 | 37 |
| Rank Spearman original-vs-corrected NPMI | 0.973895 |
| Rank Spearman species-vs-material variant NPMI | 0.969504 |
| Positive NPMI edges เดิม/ใหม่ | 82 / 82 |

กรณี material-level ข้างต้นเป็น sensitivity illustration ของ F08/H11 เท่านั้น ไม่ใช่กราฟของรายการเครื่องยาทั้งหมดที่แยกส่วนพืชครบแล้ว.

## โมเดลใหม่ 20 seeds (ไม่ใช้ chemical classes)

9 models × 20 seeds = **180 model fits**. แบบ Cooc ใช้ NPMI sampling หรือการปรับด้วย support/degree; Chem-Exact ใช้ herb–exact-compound–herb motif (H–C–H) เท่านั้น; Core-Exact ผสม Cooc และ Chem ด้วย walk count 25:75, 50:50, 75:25. ทุกโมเดลมี 20 สมุนไพร, Word2Vec skip-gram 32 dimensions, window=5, negative samples=5, epochs=15, 60 walks/herb, 1 worker. ไม่มี class bridge H–C–K–C–H ของ manuscript เดิม.

| Model | Mean rank rho | SD | Min | Max |
| --- | --- | --- | --- | --- |
| Cooc-NPMI | 0.968781 | 0.006219 | 0.947989 | 0.984597 |
| Cooc-Support | 0.974039 | 0.005124 | 0.955295 | 0.984969 |
| Cooc-Combined | 0.974486 | 0.004982 | 0.960624 | 0.986383 |
| Cooc-Support2 | 0.93497 | 0.019651 | 0.872827 | 0.980714 |
| Chem-Exact | 0.757706 | 0.030515 | 0.665156 | 0.845065 |
| Chem-ExactPrune4 | 0.735085 | 0.033095 | 0.63074 | 0.81742 |
| Core-Exact50 | 0.69269 | 0.036329 | 0.604759 | 0.790569 |
| Core-Exact25 | 0.700512 | 0.032356 | 0.595605 | 0.780675 |
| Core-Exact75 | 0.637356 | 0.075171 | 0.446708 | 0.792492 |

ค่าความสม่ำเสมอเป็นค่า Spearman เฉลี่ยจากการเปรียบเทียบ seed pairs 190 คู่ต่อโมเดล; seed pairs ไม่ใช่ตัวอย่างอิสระเชิงสถิติ. ค่าสูง **ไม่พิสูจน์ biological correctness**.

## Robustness / Graph perturbations

| Variant | Baseline | Rank rho | Top10 |
| --- | --- | --- | --- |
| Cooc-Support | Cooc-NPMI | 0.995519 | 10 |
| Cooc-Combined | Cooc-NPMI | 0.995624 | 10 |
| Cooc-Support2 | Cooc-NPMI | 0.408583 | 9 |
| Chem-ExactPrune4 | Chem-Exact | 0.78658 | 4 |
| Core-Exact25 | Core-Exact50 | 0.963009 | 9 |
| Core-Exact75 | Core-Exact50 | 0.876081 | 7 |

Cooc-Support2 ทำให้การจัดอันดับเปลี่ยนมากเมื่อบางเส้น NPMI มี support เพียงหนึ่งสูตร; Spearman อาจได้รับผลจาก ties ในกราฟที่ sparse. Chem-ExactPrune4 เป็นการตัด 1 จาก 5 compounds ต่อสมุนไพรด้วย panel เดียวกันทุก seed — sensitivity เชิง curation เท่านั้น ไม่ใช่ความถูกต้องของสารเคมี.

## LOFO หลังแก้สูตร

| method | eligible_folds | mean_ap | mean_auroc |
| --- | --- | --- | --- |
| DegreeProduct | 6 | 0.260688 | 0.68485 |
| PairSupport | 6 | 0.290904 | 0.742631 |
| PositiveNPMI | 6 | 0.300768 | 0.675456 |

Eligible folds = **6 จาก 10**; H07, H18, H20, H19 ยังคง cold start ในแต่ละสูตรของตน. Outcome เป็นการปรากฏร่วมกันในสูตรที่ถือออก จากแหล่ง compendium เดียว ไม่ใช่ external biological similarity. ไม่ใช้ class-based chemical model เข้าร่วม LOFO เพราะ original 35-class mapping ไม่มี.

## ข้อจำกัดและ release gates

1. ไม่พบ original 35 chemical-class mapping จึงไม่สามารถ exact-replay original Chem/Core 20-seed results; Chem-Exact / Core-Exact เป็นโมเดลคนละรุ่น
2. Chemistry assertions 100 รายการมาจาก V3-derived selected proxy แหล่งหลักหนึ่งรายการต่อสมุนไพร 20 ชนิด ยังไม่มีการตรวจ primary full text ราย assertion
3. ไม่มี external source-disjoint corpus หรือ independent expert gold labels 190 คู่; ไม่รายงาน predictive biological accuracy
4. สมุนไพรที่เลือก 20 ชนิดและตำรับ 10 สูตรไม่ใช่ sample แบบสุ่ม; เอกสารทั้งหมดมาจาก source compendium เดียว
5. Formulas เป็น presence projection ไม่ได้เข้ารหัสปริมาณหรือเครื่องยาเต็มสูตร; material-specific graph ยังไม่สมบูรณ์
6. งานตรวจครั้งนี้เป็น AI-assisted single-curator; ต้องให้ผู้เขียนตรวจรับ botanical normalization, plant part และ source accuracy ก่อน submission

## References (APA 7)

Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. *Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 135–144. https://doi.org/10.1145/3097983.3098036

**ยังไม่พร้อมส่งตีพิมพ์:** ผลเป็น exploratory internal robustness ที่ provenance ดีขึ้นแล้ว แต่การรับรองความถูกต้องทางชีววิทยาและการ generalize ยังไม่เสร็จ.
