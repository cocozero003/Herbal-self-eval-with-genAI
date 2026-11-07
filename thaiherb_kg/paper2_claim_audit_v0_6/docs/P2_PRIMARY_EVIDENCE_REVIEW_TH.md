# Paper 2 v0.6 — รายงานตรวจหลักฐานสารเคมีรายข้อ

วันที่ตรวจ: 7 พฤศจิกายน 2569

## ขอบเขตและวิธีการ

1. ใช้ P2 v0.5 `P2_CHEM_EVIDENCE_100.csv` เป็นฐานข้อมูล frozen 100 assertions ไม่แก้ original archived assertion ID.
2. สืบค้นและอ่านต้นฉบับ Luca et al. (2021), *Antioxidants*, 10(10), article 1642, DOI 10.3390/antiox10101642, โดยระบุตำแหน่ง **Section 3.1, Table 3, คอลัมน์ P. retrofractum**.
3. ตรวจข้อมูล `compound label`, `species`, `part`, `extract`, `source locator` และค่าปริมาณเท่าที่ต้นฉบับรายงาน; ไม่แปลงชื่อสารเป็น CID โดยอาศัยชื่อเพียงอย่างเดียว.
4. อนุมัติเฉพาะสถานะการพบสารในสารสกัดของการศึกษานี้ (`PRIMARY_FULLTEXT_MATCH`) ไม่อนุมัติ pharmacological or clinical validity; การตรวจทำแบบ AI-assisted single-curator ไม่มี independent reviewer.

## รายการที่ตรวจพบในงานต้นฉบับจริง

| Assertion | Compound | Reported level, mg PE/g extract | Source locator |
|---|---|---:|---|
| CA006 | piperine | 93.86 ± 0.13 | Table 3, *P. retrofractum* |
| CA007 | pellitorine | 206.95 ± 0.22 | Table 3, *P. retrofractum* |
| CA008 | piperlongumine | 14.19 ± 0.14 | Table 3, *P. retrofractum* |
| CA009 | piperolein B | 2.70 ± 0.01 | Table 3, *P. retrofractum* |
| CA010 | guineensine | 29.73 ± 0.05 | Table 3, *P. retrofractum* |

**หมายเหตุ:** PE เป็นการรายงานเป็น *piperine equivalents* ตามหัวตาราง ไม่ใช่ mg ของสารแต่ละชนิดโดยตรง และไม่ใช่ mg/g ผลสมุนไพรแห้ง. ตัวอย่างต้นฉบับคือ **dried fruits (peppercorns)** สกัดด้วย methanol และวัดด้วย LC-based analytical profiling. ดังนั้น **ห้ามเทียบปริมาณดังกล่าวกับส่วนหรือวิธีเตรียมอื่นโดยตรง**.

อ้างอิงและตำแหน่งตรวจ: https://pmc.ncbi.nlm.nih.gov/articles/PMC8533580/ (Methods 2.1, Results 3.1, Table 3); https://doi.org/10.3390/antiox10101642

## ผลการควบคุมข้อมูล

- **5/100:** มีหลักฐานจากต้นฉบับเฉพาะสารและ species ที่ตรวจตามตารางงานวิจัย.
- **95/100:** ยังคง `NOT_VERIFIED`; ไม่ใช่การสรุปว่าไม่พบสาร.
- `SRC_GINGER`: Mao et al. (2019) ตรวจพบข้อมูล bibliographic ว่าเป็น review ใน *Foods*, 8(6), 185. ยังไม่ตรวจ compound-level ทั้ง 5.
- `SRC_CHEBULA`: Wang et al. (2024) ตรวจ metadata ว่าเป็น review ที่มุ่งเน้นผล *Terminalia chebula*. ยังไม่ตรวจ compound-level ทั้ง 5.
- `SRC_CURCUMA`: Dosoky & Setzer (2018) เป็นบทความเรื่องน้ำมันหอมระเหยของ **หลายชนิดในสกุล Curcuma**; การยืนยันการเกิดสารใน **C. aromatica** ทั้ง 5 ต้องใช้ species-specific table evidence. ยังไม่ใช่การพิสูจน์ว่า claims ผิด.

## สิ่งที่ยังต้องทำ

ตรวจแหล่งอ้างอิงทีละแหล่งและสารทีละรายการอีก 95 assertions; บันทึก exact page/table, botanical part, sample/extract, assay, quantity, DOI; แยก source-reviewed direct measurements และ reviews; ตรวจ canonical structure/isomer/salt/CID ในขั้นแยกต่างหาก. ถ้า source ไม่ตรงให้ `WRONG_CONTEXT` พร้อมเหตุผล ไม่ย้ายเป็น `PRIMARY_FULLTEXT_MATCH`.

## References (APA 7)

Dosoky, N. S., & Setzer, W. N. (2018). Chemical composition and biological activities of essential oils of *Curcuma* species. *Nutrients, 10*(9), 1196. https://doi.org/10.3390/nu10091196

Luca, S. V., Gaweł-Bęben, K., Strzępek-Gomółka, M., Czech, K., Trifan, A., Zengin, G., Korona-Glowniak, I., Minceva, M., Gertsch, J., & Skalicka-Woźniak, K. (2021). Insights into the phytochemical and multifunctional biological profile of spices from the genus *Piper*. *Antioxidants, 10*(10), 1642. https://doi.org/10.3390/antiox10101642

Mao, Q.-Q., Xu, X.-Y., Cao, S.-Y., Gan, R.-Y., Corke, H., Beta, T., & Li, H.-B. (2019). Bioactive compounds and bioactivities of ginger (*Zingiber officinale* Roscoe). *Foods, 8*(6), 185. https://doi.org/10.3390/foods8060185

Wang, C., Zhang, H., Wang, X., Wang, X., Li, X., Li, C., Wang, Y., & Zhang, M. (2024). Comprehensive review on fruit of *Terminalia chebula*: Traditional uses, phytochemistry, pharmacology, toxicity, and pharmacokinetics. *Molecules, 29*(23), 5547. https://doi.org/10.3390/molecules29235547
