# ThaiHerb20 Paper 2 v1.3: ผลทดลอง Robustness และการประเมินความพร้อมตีพิมพ์

**วันที่:** 7 พฤศจิกายน 2569  
**สถานะ:** Internal computational robustness completed; external/generalizability validation incomplete.

## วัตถุประสงค์การทดลองที่รันจริง

ประเมินความเสถียรของ Co-occurrence, Chemical-Exact และ Core-Exact embeddings ต่อ random seeds, การลบ chemical assertions, การปรับ threshold, การถอดตำรับ และการถอดแหล่งอ้างอิง โดยใช้ snapshot ที่ล็อกไว้ของ 20 สมุนไพร, 10 ตำรับ, 74 species-level formula memberships และ chemical assertions 100 รายการ (compound identifiers 83).

### ผลหลัก

- ทำซ้ำ Cooc-NPMI จาก archive seed 11 ได้ตรงระดับความต่างสูงสุด 4.99×10⁻⁹.
- ใช้ผล archive 9 configurations × 20 seeds = 180 fits ที่ได้รับการตรวจ SHA-256 และทำ numerical replay; ไม่แอบอ้างว่า fit ใหม่ทั้ง 180 ในรอบนี้.
- รัน perturbation 9 variants × 20 seeds = 180 paired tests; ผล ranking Spearman เฉลี่ยของ Chem-Prune3 เทียบ Chem-Exact = 0.261; Chem-Prune2 = 0.048.
- LOFO ครบ 10 ตำรับ: 6 folds ไม่มี cold-start มี 190 คู่ต่อ fold; 4 folds ต้องตัด 19 คู่และเหลือ 171 คู่ต่อ fold.
- สำหรับ 6 complete folds: PositiveNPMI AP 0.301, PairSupport AP 0.291, Cooc-NPMI-TrainOnly AP 0.275, Core-Exact50-TrainOnly AP 0.168, Chem-Exact AP 0.139.
- ผลต่าง Mean AP (Core−PairSupport) = -0.122 มี 95% paired formula-bootstrap CI จาก 4,000 resamples, ไม่ตีความเป็นผลยืนยันสมมติฐาน.
- Source holdout 20 แหล่ง × 5 seeds: การตัด 1 source หมายถึงขาดข้อมูลเคมีสมุนไพร 1 ชนิด จึงเหลือ 171/190 คู่ (90% coverage), ไม่เติมค่าคาดเดาคู่ที่ไม่มีข้อมูล.
- สำรวจ taxonomy ที่สร้างขึ้นใหม่ 31 families สำหรับ 83 สาร (ไม่ใช่ original 35 classes); Chem-Family31 mean rank correlation 0.502 เทียบ Exact. Material-specific counterfactual F08/H11 มี rank correlation 0.958 เทียบ species-level.

## ประเด็นที่ต้องไม่สรุปเกินหลักฐาน

1. Label ที่ใช้คำนวณ AP/AUROC คือการปรากฏร่วมใน **ตำรับเอกสารที่กันไว้** ไม่ใช่หลักฐานความคล้ายคลึงทางชีวภาพ ประสิทธิผลหรือความปลอดภัย.
2. PairSupport และ NPMI ไม่ใช้ Word2Vec seeds ส่วน Cooc และ Core ต้องฝึกใหม่โดยใช้เฉพาะ 9 ตำรับ train เพื่อป้องกัน label leakage.
3. External pilot 11 observations จาก 3 DOI ไม่ซ้ำกับรายการ DOI เดิม แต่เป็น positive-only post-hoc selection จึง **ไม่คำนวณ confirmatory external AP/AUROC**.
4. Original-source chemistry primary full-text verification ยังได้ 5/100; สารอีก 95 ไม่ใช่หลักฐานว่าไม่มีสาร แต่ยังไม่ครบระดับยืนยันดังกล่าว.
5. Original 35-class mapping ยังไม่พบ; 31-family reconstruction ไม่เทียบเท่ากับ historical 35-class. ไม่มี independent expert gold.
6. Confidence intervals ใช้ resampling ระดับตำรับ 6 หรือ 4 clusters; seed ไม่ใช่ biological sample อิสระ จึงเป็น descriptive/exploratory interval เท่านั้น.

## ข้อสรุปที่เขียนใน Abstract ได้

"Within a selected 20-herb, 10-formula documentary corpus, co-occurrence measures yielded higher mean average precision than the tested exact-chemical and mixed embeddings for leave-one-formula-out co-membership retrieval. Chemical pruning produced marked ranking instability and leaving out a source removed chemical coverage for one herb (19 of 190 pairs). These internal findings do not establish biological validity or cross-source generalizability."

## ข้อสรุปที่ยังเขียนไม่ได้

- Core embedding เหนือกว่า Cooc/Chem ในความถูกต้องทางเภสัชวิทยา
- Robustness ภายนอกกับข้อมูลสมุนไพรทั่วประเทศไทยพิสูจน์แล้ว
- กลุ่มเคมี 35 class ตามต้นฉบับกู้คืนได้สมบูรณ์
- 11 external positives มีความเทียบเท่ากับ blinded test หรือมี true negatives

**เกณฑ์ปิด Paper 2 สำหรับบทความ:** อาจส่งเป็น *internal robustness/sensitivity study* เมื่อผู้เขียนยอมรับขอบเขตเป้าหมายดังกล่าวและตรวจคุณภาพ source mapping; แต่หากใช้ชื่อเรื่องที่อ้าง external generalizability ต้องมี prospective, disjoint external test with independent adjudication.
