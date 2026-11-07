# Paper 2 v0.7 — Evidence-claim adjudication staging report

## ขอบเขต

งานรอบนี้ขยาย Paper 2 v0.6 เฉพาะการตรวจหลักฐานที่แหล่งตีพิมพ์ระบุสารต่อชนิดพืช ข้อมูลอ้างอิงที่ใช้เป็น frozen `P2_CHEM_EVIDENCE_100_v05_LOCKED.csv` และผล v0.6 โดยไม่ได้เปลี่ยน species/projection หรืออ้างว่าได้รับ independent human review

## ผลการจัดระดับหลักฐาน

| Category | Count | Meaning |
|---|---:|---|
| PRIMARY_FULLTEXT_MATCH | 5 | Luca et al. (2021) Table 3; *Piper retrofractum*, methanolic dried-fruit extract, LC-DAD piperine equivalents |
| PRIMARY_ABSTRACT_ONLY | 5 | Verma et al. (2018), *Zingiber montanum* rhizome hydrodistilled essential oil, GC-MS/GC-FID; values come from published abstract only |
| SECONDARY_ONLY | 10 | Five *Allium sativum* constituents in Shang et al. (2019); five *Zingiber officinale* constituents or derivatives in Mao et al. (2019); reviews, no primary source-specific mass confirmations |
| NOT_VERIFIED | 80 | No claim-specific source adjudication performed in this stage |

**การจำแนก source-disposition ไม่ใช่ gold label.** PRIMARY_ABSTRACT_ONLY ยังไม่ผ่าน full-text table audit; SECONDARY_ONLY ไม่อาจใช้พิสูจน์ concentration, medicinal material, canonical isomer, metabolite isolation หรือประสิทธิผลทางคลินิก. All 100 chemical structure mappings and historical 35-class map remain separately unadjudicated.

### รายละเอียดไพล CA021–CA025

Verma et al. (2018) รายงาน GC-FID/GC-MS ของน้ำมันหอมระเหยจากเหง้าไพลที่ได้จาก hydrodistillation และให้ **ช่วงสัดส่วนใน essential oil** ตาม abstract: sabinene 13.5–38.0%, DMPBD 20.6–35.3%, terpinen-4-ol 9.0–31.3%, gamma-terpinene 1.1–4.8%, beta-phellandrene 1.0–4.4%. ไม่สามารถเทียบเป็นความเข้มข้นจากเนื้อเหง้าหรือสารสกัดด้วยตัวทำละลายชนิดอื่นได้.

### รายละเอียดกระเทียม CA016–CA020

Shang et al. (2019), abstract and section 2, ระบุ alliin, allicin, diallyl sulfide, diallyl disulfide, ajoene ชัดเจนในฐานะส่วนประกอบของ garlic ข้อมูลนี้เป็น review ที่รวมหลาย study และการแปรรูปหลายแบบ ไม่ใช่การตรวจวัดตัวอย่างชุดเดียวกัน.

### รายละเอียดขิง CA001–CA005

Mao et al. (2019) กล่าวถึง 6-gingerol, 6-shogaol, zingerone, 6-paradol และ zingiberene ในบริบท constituent/bioactivity review. โดยเฉพาะ 6-paradol อาจเป็น derivative และ/หรือสารที่ใช้ในการทดลองที่อ้างอิงต่อ จึงไม่ระบุเป็นผลตรวจพบเชิงปริมาณใน fresh medicinal rhizome. ต้องตาม primary experiments ก่อนขึ้นระดับ primary evidence.

## APA 7 references (verified bibliographic identity, not all full-text analytical tables)

Luca, S. V., et al. (2021). *Piper* species chemical profiling and bioactivity. *Antioxidants, 10*(10), 1642. https://doi.org/10.3390/antiox10101642 [Title/authors abbreviated here; use primary publisher metadata before final manuscript]

Mao, Q.-Q., Xu, X.-Y., Cao, S.-Y., Gan, R.-Y., Corke, H., Beta, T., & Li, H.-B. (2019). Bioactive compounds and bioactivities of ginger (*Zingiber officinale* Roscoe). *Foods, 8*(6), 185. https://doi.org/10.3390/foods8060185

Shang, A., et al. (2019). Bioactive compounds and biological functions of garlic (*Allium sativum* L.). *Foods, 8*(7), 246. https://doi.org/10.3390/foods8070246 [Complete author list to reconcile before submission]

Verma, R. S., Joshi, N., Padalia, R. C., Singh, V. R., Goswami, P., Verma, S. K., Iqbal, H., Chanda, D., Verma, R. K., Darokar, M. P., Chauhan, A., & Kandwal, M. K. (2018). Chemical composition and antibacterial, antifungal, allelopathic and acetylcholinesterase inhibitory activities of cassumunar-ginger. *Journal of the Science of Food and Agriculture, 98*(1), 321–327. https://doi.org/10.1002/jsfa.8474

## P2 ยังไม่ผ่าน publication gates

1. Compound identity/canonical structure/isomer/mixture map ยังไม่มี independent source-supported structure audit.
2. Full text จากงานไพลและ primary studies สำหรับ review assertions ยังไม่ตรวจครบ.
3. Original 35 class archive และ source-disjoint chemical/expert dataset ยังไม่พบ.
4. Species projection กับ material/preparation graph ยังแยกไม่ได้ครบ ไม่ใช้ H11 gall เป็น fruit หรือ H13 aril เป็น seed โดยอัตโนมัติ.
