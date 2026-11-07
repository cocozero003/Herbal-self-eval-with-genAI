"""Create transparent, source-reviewed Paper 2 v0.4 report and offline dashboard."""
from __future__ import annotations
import csv, json, html, statistics, itertools, hashlib, zipfile
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'results';DOC=ROOT/'docs';DASH=ROOT/'dashboard';M=ROOT/'manuscript';DATA=ROOT/'data'
for p in (DOC,DASH,M):p.mkdir(exist_ok=True)
def csvrows(name):
 with (O/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save(name,rows):
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def fmt(n):return f'{float(n):.3f}'
def mdtable(rs,keys):return '| '+' | '.join(keys)+' |\n| '+' | '.join('---' for _ in keys)+' |\n'+'\n'.join('| '+' | '.join(str(r.get(k,'')) for k in keys)+' |' for r in rs)
a=json.loads((DATA/'paper2_bootstrap_v3_proxy.json').read_text());b=json.loads((DATA/'paper2_source_reviewed_species_v04.json').read_text());m=json.loads((O/'RELEASE_MANIFEST.json').read_text())
from reanalyse import cooc_pairs
ids=[h['id'] for h in b['herbs']];old=cooc_pairs(a['formulas'],ids);new=cooc_pairs(b['formulas'],ids)
mat=json.loads((DATA/'paper2_source_reviewed_species_v04.json').read_text())
partial=json.loads(json.dumps(b));f8=next(x for x in partial['formulas'] if x['id']=='F08_DTAM2566');f8['herbs'].remove('H11')
part=cooc_pairs(partial['formulas'],ids)
impact=[]
for x,y,z in zip(old,new,part):
 impact.append({'herb_a':x['herb_a'],'herb_b':x['herb_b'],'old_support':x['support'],'new_support':y['support'],'old_npmi':round(x['npmi'],6),'corrected_species_npmi':round(y['npmi'],6),
 'strict_material_variant_npmi':round(z['npmi'],6),'npmi_change_after_primary_audit':round(y['npmi']-x['npmi'],6),'evidence_not_biological_similarity':1})
save('BEFORE_AFTER_NPMI_190.csv',impact)
npmi_rho=float(spearmanr([x['npmi'] for x in old],[z['npmi'] for z in new]).statistic)
material_rho=float(spearmanr([x['npmi'] for x in new],[z['npmi'] for z in part]).statistic)
metrics={'original_formula_memberships':sum(len(x['herbs']) for x in a['formulas']),'corrected_formula_memberships':sum(len(x['herbs']) for x in b['formulas']),
 'strict_material_projected_memberships':sum(len(x['herbs']) for x in partial['formulas']),
 'old_new_npmi_rank_spearman':round(npmi_rho,6), 'species_material_npmi_rank_spearman':round(material_rho,6),
 'pairs_changed_npmi_after_source_correction':sum(abs(x['npmi']-y['npmi'])>1e-10 for x,y in zip(old,new)),
 'old_positive_npmi':sum(x['positive_npmi']>0 for x in old),'new_positive_npmi':sum(x['positive_npmi']>0 for x in new),'part_variant_positive_npmi':sum(x['positive_npmi']>0 for x in part),
 'old_new_positive_edge_overlap':len({(x['herb_a'],x['herb_b']) for x in old if x['positive_npmi']>0}&{(x['herb_a'],x['herb_b']) for x in new if x['positive_npmi']>0})}
(O/'SOURCE_CORRECTION_IMPACT.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
models=csvrows('SEED_REPEATABILITY_20SEEDS.csv');pert=csvrows('PERTURBATION_COMPARISON_20SEEDS.csv');fl=csvrows('LOFO_COVERAGE_10.csv');base=csvrows('LOFO_STRUCTURAL_BASELINES.csv');matrix=csvrows('NEW_HERBS_SOURCE_REVIEW_100.csv');corr=csvrows('FORMULA_MEMBERSHIP_CORRECTIONS.csv')
base_summary=[]
for name in sorted({x['model'] for x in base}):
 rs=[x for x in base if x['model']==name]
 base_summary.append({'method':name,'eligible_folds':len(rs),'mean_ap':round(statistics.mean(float(x['average_precision']) for x in rs),6),'mean_auroc':round(statistics.mean(float(x['auroc']) for x in rs),6),'not_external_validation':1})
save('LOFO_SUMMARY_AFTER_SOURCE_AUDIT.csv',base_summary)
report=f'''# ThaiHerb Paper 2 — Source-Reviewed Graph Robustness v0.4

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
| Membership ก่อนตรวจ | {metrics['original_formula_memberships']} |
| Membership ระดับ species หลังตรวจ | {metrics['corrected_formula_memberships']} |
| Material-projection sensitivity (ตัด F08/H11 gall) | {metrics['strict_material_projected_memberships']} |
| คู่สมุนไพรทั้งหมด | 190 |
| คู่ที่ NPMI เปลี่ยนจากการแก้ F09 | {metrics['pairs_changed_npmi_after_source_correction']} |
| Rank Spearman original-vs-corrected NPMI | {metrics['old_new_npmi_rank_spearman']} |
| Rank Spearman species-vs-material variant NPMI | {metrics['species_material_npmi_rank_spearman']} |
| Positive NPMI edges เดิม/ใหม่ | {metrics['old_positive_npmi']} / {metrics['new_positive_npmi']} |

กรณี material-level ข้างต้นเป็น sensitivity illustration ของ F08/H11 เท่านั้น ไม่ใช่กราฟของรายการเครื่องยาทั้งหมดที่แยกส่วนพืชครบแล้ว.

## โมเดลใหม่ 20 seeds (ไม่ใช้ chemical classes)

9 models × 20 seeds = **180 model fits**. แบบ Cooc ใช้ NPMI sampling หรือการปรับด้วย support/degree; Chem-Exact ใช้ herb–exact-compound–herb motif (H–C–H) เท่านั้น; Core-Exact ผสม Cooc และ Chem ด้วย walk count 25:75, 50:50, 75:25. ทุกโมเดลมี 20 สมุนไพร, Word2Vec skip-gram 32 dimensions, window=5, negative samples=5, epochs=15, 60 walks/herb, 1 worker. ไม่มี class bridge H–C–K–C–H ของ manuscript เดิม.

{mdtable([{'Model':x['model'],'Mean rank rho':x['mean'],'SD':x['sd'],'Min':x['min'],'Max':x['max']} for x in models],['Model','Mean rank rho','SD','Min','Max'])}

ค่าความสม่ำเสมอเป็นค่า Spearman เฉลี่ยจากการเปรียบเทียบ seed pairs {20*19//2} คู่ต่อโมเดล; seed pairs ไม่ใช่ตัวอย่างอิสระเชิงสถิติ. ค่าสูง **ไม่พิสูจน์ biological correctness**.

## Robustness / Graph perturbations

{mdtable([{'Variant':x['variant'],'Baseline':x['baseline'],'Rank rho':x['mean_ranking_spearman'],'Top10':x['top10_overlap']} for x in pert],['Variant','Baseline','Rank rho','Top10'])}

Cooc-Support2 ทำให้การจัดอันดับเปลี่ยนมากเมื่อบางเส้น NPMI มี support เพียงหนึ่งสูตร; Spearman อาจได้รับผลจาก ties ในกราฟที่ sparse. Chem-ExactPrune4 เป็นการตัด 1 จาก 5 compounds ต่อสมุนไพรด้วย panel เดียวกันทุก seed — sensitivity เชิง curation เท่านั้น ไม่ใช่ความถูกต้องของสารเคมี.

## LOFO หลังแก้สูตร

{mdtable(base_summary,['method','eligible_folds','mean_ap','mean_auroc'])}

Eligible folds = **{sum(int(x['all_190_pairs_evaluable']) for x in fl)} จาก 10**; H07, H18, H20, H19 ยังคง cold start ในแต่ละสูตรของตน. Outcome เป็นการปรากฏร่วมกันในสูตรที่ถือออก จากแหล่ง compendium เดียว ไม่ใช่ external biological similarity. ไม่ใช้ class-based chemical model เข้าร่วม LOFO เพราะ original 35-class mapping ไม่มี.

## ข้อจำกัดและ release gates

1. ไม่พบ original 35 chemical-class mapping จึงไม่สามารถ exact-replay original Chem/Core 20-seed results; Chem-Exact / Core-Exact เป็นโมเดลคนละรุ่น
2. Chemistry assertions 100 รายการมาจาก V3-derived selected proxy แหล่งหลักหนึ่งรายการต่อสมุนไพร 20 ชนิด ยังไม่มีการตรวจ primary full text ราย assertion
3. ไม่มี external source-disjoint corpus หรือ independent expert gold labels 190 คู่; ไม่รายงาน predictive biological accuracy
4. สมุนไพรที่เลือก 20 ชนิดและตำรับ 10 สูตรไม่ใช่ sample แบบสุ่ม; เอกสารทั้งหมดมาจาก source compendium เดียว
5. Formulas เป็น presence projection ไม่ได้เข้ารหัสปริมาณหรือเครื่องยาเต็มสูตร; material-specific graph ยังไม่สมบูรณ์
6. งานตรวจครั้งนี้เป็น AI-assisted single-curator; ต้องให้ผู้เขียนตรวจรับ botanical normalization, plant part และ source accuracy ก่อน submission

## References (APA 7)

Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. Ministry of Public Health. {b['source_pdf']}

Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. *Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 135–144. https://doi.org/10.1145/3097983.3098036

**ยังไม่พร้อมส่งตีพิมพ์:** ผลเป็น exploratory internal robustness ที่ provenance ดีขึ้นแล้ว แต่การรับรองความถูกต้องทางชีววิทยาและการ generalize ยังไม่เสร็จ.
'''
(DOC/'PAPER2_V04_SOURCE_REVIEW_REPORT_TH.md').write_text(report,encoding='utf-8')
methods=f'''# Paper 2 — v0.4 source-audited robustness and 20-seed model reconstruction

## Editorial status
Reanalysis of 20-herb selected pilot, NOT replication of unavailable 35-class archive. Source review on 100 added-herb/formula cells is single-curator, ChatGPT-assisted. Human-independent adjudication and an external source-disjoint validation set are not available.

## Methods
An official 2023 compendium was consulted for all ten selected formulas, reading complete ingredient-table continuations. Formula memberships were projected to the botanical-species level, while documented variation in medicinal material (e.g., *Terminalia chebula* fruit/pericarp versus gall; *Myristica fragrans* seed versus aril) was recorded rather than merged at medicinal-material level. Three omitted herb–formula memberships were restored to F09 and a frozen 74-membership species snapshot was prepared. All 100 H11–H20 membership cells carry official printed-page locators.

Nine embedding variants were compared over 20 preselected random seeds with Word2Vec skip-gram, dimension 32, window five, negative samples five, 15 epochs and one worker. Cooc walks used NPMI weights with support and degree alternatives; Chem walks used H–C–H exact compound paths, and Core variants mixed them at 25/75, 50/50 and 75/25 walk counts. No compound class labels were supplied or inferred. Each model yielded 190 unordered herb-pair cosine scores per seed. Computational repeatability was the mean of 190 dependent seed-pair Spearman correlations; edge perturbation compared mean cosine ranking and top-ten overlap. Held-out formula co-occurrence was evaluated by structural baselines on folds with all herbs represented in training.

## Main findings

- Formula memberships: 71 V3-derived vs 74 source-reviewed species-level. Source correction: F09 + H11, H15, H17.
- Mean original-versus-source-corrected NPMI rank correlation: {metrics['old_new_npmi_rank_spearman']}; {metrics['pairs_changed_npmi_after_source_correction']}/190 pairs changed score.
- Cooc-NPMI stability: {next(x['mean'] for x in models if x['model']=='Cooc-NPMI')}; Chem-Exact: {next(x['mean'] for x in models if x['model']=='Chem-Exact')}; Core-Exact50: {next(x['mean'] for x in models if x['model']=='Core-Exact50')}.
- Eligible full 190-pair LOFO folds: 6/10; expert biological labels and external source-disjoint tests absent.

## Interpretation
The expanded panel exposes substantive data-selection and medicinal-part normalization risks. Source-corrected Cooc paths and class-free exact-chemistry paths are trainable and repeatable, but the new chemical channel is not comparable to the original manuscript's compound-class walks. No claims of predictive superiority, pharmacological relevance, therapeutic interchangeability, efficacy or safety are supported.

## Citations
Official Thai herbal formula compendium (2023): {b['source_pdf']}. metapath2vec (Dong et al., 2017), DOI:10.1145/3097983.3098036.
'''
(M/'PAPER2_V04_METHODS_RESULTS_ADDENDUM_EN.md').write_text(methods,encoding='utf-8')
readme=f'''# ThaiHerb Paper 2 — Source-Reviewed Robustness v0.4

**2026-11-07 — internal reproducible research package.** Not original Paper 2 replication, not biological validation.

## What's new from v0.3

- An AI-assisted, single-curator audit of all 100 H11–H20 × F01–F10 cells against complete official ingredient tables with printed-page locators.
- Three source-verified F09 memberships restored: H11, H15, H17. Species-level formula total: 71 → **74**; V3 raw data preserved.
- Special handling of species-versus-medicinal material, especially *Terminalia chebula* gall vs fruit and *Myristica fragrans* aril vs seed.
- New **class-free** Cooc, Chem-Exact (H–C–H), Core-Exact 20-seed reanalysis; 9 configurations × 20 seeds = 180 model fits.
- Before/after NPMI audit, 190-pair mean embeddings, six perturbation comparisons, and LOFO structural baselines.
- No artificial recovery of the original 35 chemical classes, no fabricated independent expert scores.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run.py
```

Data required under `data/` in **the authorized full ZIP**: `paper2_bootstrap_v3_proxy.json`, `paper1_formula_reviewed_snapshot.json`. The script regenerates `paper2_source_reviewed_species_v04.json`, result CSVs and integrity tests. Public GitHub contains code and documentation, not these research data archives.

## Main outputs

- `results/NEW_HERBS_SOURCE_REVIEW_100.csv`
- `results/FORMULA_MEMBERSHIP_CORRECTIONS.csv`
- `results/SOURCE_REVIEW_FORMULA_ASSERTIONS_74.csv`
- `results/ALL_EMBEDDING_SCORES_9MODELS_20SEEDS.csv` (34,200 rows)
- `results/SEED_REPEATABILITY_20SEEDS.csv`
- `results/BEFORE_AFTER_NPMI_190.csv`
- `results/SOURCE_CORRECTION_IMPACT.json`
- `results/RELEASE_MANIFEST.json`
- `dashboard/Paper2_SourceReview_v0.4.html`
- `manuscript/PAPER2_V04_METHODS_RESULTS_ADDENDUM_EN.md`
- `docs/PAPER2_V04_SOURCE_REVIEW_REPORT_TH.md`

## Research boundary

- Original 35 classes and archived original model vectors are NOT available; Chem-Exact and Core-Exact are different algorithms with different information channels from original Chem/Core.
- No independent external formula set and no expert biological similarity gold labels.
- Do not use v0.3's 71-membership data and v0.4's 74-membership metrics in a single figure without explicitly labeling cohorts.
- The species projection is NOT a preparation/part-specific ingredient graph. Special-material notes require expert review.
- Official source: {b['source_pdf']}
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
(ROOT/'data/README.md').write_text('Research proxy inputs reside in the authorized Full ZIP on project Google Drive. Do not copy original formulas, sources or copyright-protected content into public code repositories. Original 35 chemical classes and human expert gold standards are unavailable.\n',encoding='utf-8')
# Local standalone, offline interactive dashboard.
dashboard_data={'meta':m,'impact':metrics,'models':models,'perturb':pert,'folds':fl,'baselines':base_summary,'matrix':matrix,'corrections':corr,'graph':impact,'pair_means':csvrows('MEAN_PAIR_SIMILARITIES.csv')}
payload=json.dumps(dashboard_data,ensure_ascii=False).replace('</','<\\/')
style='''*{box-sizing:border-box}body{font-family:system-ui,"Noto Sans Thai",sans-serif;background:#f3f6f8;color:#203344;margin:0;font-size:14px}main{max-width:1280px;margin:auto;padding:20px}.hero{background:#213d53;color:white;border-radius:14px;padding:28px}.hero h1{font-size:26px;margin:8px 0}.hero p{color:#e2ecf4}.warning{padding:14px;background:#fff5e4;border-left:4px solid #b3822e;margin:15px 0}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.card,.panel{background:white;border:1px solid #dde5eb;border-radius:11px;padding:18px}.card strong{font-size:24px;display:block}.card small{color:#637784}nav{margin:18px 0;display:flex;gap:6px;flex-wrap:wrap}button,input,select{font:inherit;border:1px solid #c3d1dc;border-radius:6px;padding:9px 11px;background:white;color:#17384d}button{cursor:pointer}button.active{background:#275d77;color:white}.panel{display:none}.panel.active{display:block}.scroll{overflow:auto;max-height:540px;border:1px solid #e1e7ed;border-radius:8px}table{border-collapse:collapse;width:100%;font-size:12px}th,td{border-bottom:1px solid #e8edf1;padding:8px;text-align:left}th{background:#e9f1f7;white-space:nowrap;position:sticky;top:0}.barline{display:flex;gap:12px;align-items:center;margin:12px 0}.barname{width:185px}.track{flex:1;height:13px;background:#ebf2f6;border-radius:5px;overflow:hidden}.fill{height:100%;background:#3e849f}.value{width:75px;text-align:right}.tools{display:flex;gap:8px;margin:15px 0;flex-wrap:wrap}.muted{color:#667889;font-size:12px}footer{padding:20px 0;color:#667889}@media(max-width:700px){.cards{grid-template-columns:repeat(2,1fr)}main{padding:10px}.hero{padding:17px}.barname{width:130px;font-size:11px}table{min-width:700px}}'''
script='''const data=window.P2DATA;function esc(v){return String(v??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;')}function tbl(rows,cols){return '<div class="scroll"><table><thead><tr>'+cols.map(c=>'<th>'+esc(c[1])+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+cols.map(c=>'<td title="'+esc(r[c[0]])+'">'+esc(r[c[0]])+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>'}function show(id,b){document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('active',x.id===id));document.querySelectorAll('nav button').forEach(x=>x.classList.remove('active'));b.classList.add('active')}function init(){document.querySelector('#bars').innerHTML=data.models.map(m=>'<div class="barline"><span class="barname">'+esc(m.model)+'</span><div class="track"><div class="fill" style="width:'+Math.max(0,Math.min(100,Number(m.mean)*100))+'%"></div></div><span class="value">'+Number(m.mean).toFixed(3)+'</span></div>').join('');document.querySelector('#modelsTable').innerHTML=tbl(data.models,[['model','Method'],['mean','Mean rho'],['sd','SD'],['min','Min'],['max','Max']]);document.querySelector('#pertTable').innerHTML=tbl(data.perturb,[['variant','Variant'],['baseline','Baseline'],['mean_ranking_spearman','Rank rho'],['top10_overlap','Top-10 overlap']]);document.querySelector('#lofoTable').innerHTML=tbl(data.folds,[['heldout_formula','Formula'],['all_190_pairs_evaluable','Eligible'],['cold_start_herbs','Cold-start'],['positive_pairs','Positive dyads']]);document.querySelector('#baselineTable').innerHTML=tbl(data.baselines,[['method','Method'],['mean_ap','Mean AP'],['mean_auroc','Mean AUROC'],['eligible_folds','Folds']]);document.querySelector('#correctionsTable').innerHTML=tbl(data.corrections,[['formula_id','Formula'],['herb_id','Herb'],['thai_name','Name'],['prior_v03_present','v0.3'],['source_reviewed_species_present','v0.4'],['official_printed_pages','Page']]);function updateMatrix(){const q=document.querySelector('#q').value.toLowerCase(),f=document.querySelector('#formula').value;const a=data.matrix.filter(x=>(f==='all'||x.formula_id===f)&&Object.values(x).join(' ').toLowerCase().includes(q));document.querySelector('#matrixTable').innerHTML=tbl(a,[['formula_id','Formula'],['herb_id','Herb'],['thai_name','Thai name'],['source_reviewed_species_present','Species present'],['official_printed_pages','Printed pages'],['special_material_note','Material note']]);}document.querySelector('#q').addEventListener('input',updateMatrix);document.querySelector('#formula').addEventListener('change',updateMatrix);updateMatrix();document.querySelector('#graphTable').innerHTML=tbl(data.graph,[['herb_a','A'],['herb_b','B'],['old_support','Old support'],['new_support','New support'],['old_npmi','Old NPMI'],['corrected_species_npmi','v0.4 NPMI'],['strict_material_variant_npmi','Material variant']]);function updatePairs(){const q=document.querySelector('#pairSearch').value.toLowerCase(),f=document.querySelector('#modelSelect').value;const a=data.pair_means.filter(x=>(f==='all'||x.model===f)&&(x.herb_a+' '+x.herb_b).toLowerCase().includes(q)).slice(0,450);document.querySelector('#pairTable').innerHTML=tbl(a,[['model','Model'],['herb_a','A'],['herb_b','B'],['mean_cosine','Mean cosine'],['sd_cosine','SD']])}document.querySelector('#modelSelect').innerHTML='<option value="all">All models</option>'+data.models.map(x=>'<option>'+esc(x.model)+'</option>').join('');document.querySelector('#pairSearch').addEventListener('input',updatePairs);document.querySelector('#modelSelect').addEventListener('change',updatePairs);updatePairs();document.querySelectorAll('nav button').forEach(b=>b.addEventListener('click',()=>show(b.dataset.tab,b)));}document.addEventListener('DOMContentLoaded',init);'''
page=f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ThaiHerb20 Paper 2 v0.4</title><style>{style}</style></head><body><main><div class="hero"><small>THAIHERB20 | PAPER 2 | VERSION 0.4</small><h1>Source-Reviewed Robustness and Embedding Stability</h1><p>Primary documentary formula audit, 20-seed class-free embedding benchmarks, explicit evidence limits.</p></div><div class="warning"><b>Scientific boundary:</b> The original 35 chemical classes were not recovered. Chem-Exact and Core-Exact are new models, not the original Paper 2 chemical-class walks. Source-review is AI-assisted; expert biological gold labels and external validation are not available.</div><div class="cards"><div class="card"><strong>74</strong><small>Species-level formula memberships</small></div><div class="card"><strong>3</strong><small>F09 corrected missing edges</small></div><div class="card"><strong>180</strong><small>Model fits (9 x 20 seeds)</small></div><div class="card"><strong>100/100</strong><small>Added-herb formula cells reviewed</small></div></div><nav><button class="active" data-tab="summary">Overview</button><button data-tab="audit">100-cell source audit</button><button data-tab="models">Seed stability</button><button data-tab="sensitivity">Perturbations</button><button data-tab="lofo">Held-out formulas</button><button data-tab="pairs">190-pair scores</button><button data-tab="limits">Limitations</button></nav><section class="panel active" id="summary"><h2>Updated model stability</h2><div id="bars"></div><p><b>Formula correction:</b> F09 gained H11, H15, and H17 from official source tables. The prior 71-membership proxy is retained as a historical baseline, not overwritten. Positive-NPMI edges: {metrics['old_positive_npmi']} prior, {metrics['new_positive_npmi']} reviewed; {metrics['pairs_changed_npmi_after_source_correction']} herb-pair NPMI values changed.</p><p>Some species nodes collapse different materia medica: for example, Terminalia chebula gall and fruit are not identical herbal materials.</p></section><section class="panel" id="audit"><h2>Source audit: 10 formulas x 10 added herbs</h2><div class="tools"><input id="q" placeholder="Search formula, herb, note"><select id="formula"><option value="all">All formulas</option>{''.join(f'<option value="{html.escape(fid)}">{html.escape(fid)}</option>' for fid in sorted({r['formula_id'] for r in matrix}))}</select></div><div id="matrixTable"></div><h2>Corrections from the prior projection</h2><div id="correctionsTable"></div></section><section class="panel" id="models"><h2>Seed-to-seed ranking agreement</h2><div id="modelsTable"></div><p class="muted">190 correlations per method are dependent pairings of the same 20 random seeds. This is repeatability, not biological validity.</p></section><section class="panel" id="sensitivity"><h2>Graph and panel perturbations</h2><div id="pertTable"></div><h2>Before and after source correction</h2><div id="graphTable"></div></section><section class="panel" id="lofo"><h2>Leave-one-formula-out coverage</h2><div id="lofoTable"></div><h2>Structural baselines only</h2><div id="baselineTable"></div><p class="muted">Outcome is documentary co-occurrence in the held-out formula, not chemical or pharmacological similarity.</p></section><section class="panel" id="pairs"><h2>190 pairs per method: mean cosine across 20 seeds</h2><div class="tools"><select id="modelSelect"></select><input id="pairSearch" placeholder="Search herb IDs"></div><div id="pairTable"></div></section><section class="panel" id="limits"><h2>Research limits and next scientific gates</h2><p>The formulas are from one purposively selected official source. Chemical occurrences are V3-derived selections, often one source per herb. The original 35-class mapping and original Chem/Core vectors are not available. No independently adjudicated external corpus or human review labels exist. The full compound class schema and medicinal-material preparations cannot be inferred from these figures.</p><p>Next stages: source-verify individual chemical occurrences, obtain source-disjoint external formula documents, and perform a preregistered paired evaluation. Expert review must be independently conducted rather than generated from model predictions.</p></section><footer>ThaiHerb Paper 2, v0.4. Offline static data dashboard with client-side filtering. No external services or tracking.</footer></main><script>window.P2DATA={payload};</script><script>{script}</script></body></html>'''
(DASH/'Paper2_SourceReview_v0.4.html').write_text(page,encoding='utf-8')
# Short polished Word editorial report.
d=Document();section=d.sections[0];section.top_margin=Inches(.7);section.bottom_margin=Inches(.65)
style0=d.styles['Normal'];style0.font.name='Calibri';style0.font.size=Pt(10);style0.paragraph_format.space_after=Pt(5)
for style_name in ('Title','Heading 1','Heading 2'):
 st=d.styles[style_name];st.font.name='Calibri';st.font.color.rgb=RGBColor(25,65,85)
d.add_heading('ThaiHerb Paper 2: Source-Reviewed Robustness',0)
d.add_paragraph('Version 0.4 | 7 November 2026 | Computational research report',style='Subtitle')
d.add_paragraph('Scientific status: source-reviewed species-level formula reconstruction and 20-seed class-free embeddings. Not a replication of the original 35-class model, not external biological validation.',style='Intense Quote')
d.add_heading('1. What changed from v0.3?',1)
d.add_paragraph('The 20-herb, 10-formula V3-derived projection was audited against the complete ingredient tables in the official DTAM/Thai FDA compendium. All 100 added-herb × formula presence/absence cells were checked by an AI-assisted single curator. Three omitted F09 memberships were restored: H11 (Terminalia chebula), H15 (Nigella sativa) and H17 (Acorus calamus). The reviewed species-level total is 74, compared with 71 in the earlier proxy. The original archive is retained.')
d.add_paragraph('Species-versus-material distinctions matter. In F08 the Terminalia chebula botanical match is a gall (Ko Thung Pla), not Somo Thai fruit; Myristica fragrans aril and seed are also distinct medicinal materials. These mappings are flagged rather than treated as therapeutic substitutes.')
d.add_heading('2. Before/after source audit',1)
t=d.add_table(rows=1,cols=2);t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
for c,v in zip(t.rows[0].cells,['Metric','Result']):c.text=v
for row in [('Original memberships','71'),('Corrected species-level memberships','74'),('NPMI pairs changed',str(metrics['pairs_changed_npmi_after_source_correction'])),('Old/new NPMI rank Spearman',str(metrics['old_new_npmi_rank_spearman'])),('Species-only vs illustrative strict-material rank rho',str(metrics['species_material_npmi_rank_spearman']))]:
 cc=t.add_row().cells
 for c,v in zip(cc,row):c.text=v
d.add_heading('3. Twenty-seed computational reanalysis',1)
d.add_paragraph('Nine controlled model configurations were trained under 20 random seeds (180 model fits). All methods used 32-dimensional skip-gram Word2Vec. The chemical channel was explicitly exact-compound H-C-H without compound classes; it is not equivalent to the original manuscript’s H-C-K-C-H channel.')
t=d.add_table(rows=1,cols=3);t.style='Light Shading Accent 1'
for c,v in zip(t.rows[0].cells,['Method','Mean seed-rank rho','SD']):c.text=v
for row in models:
 cc=t.add_row().cells
 for c,v in zip(cc,[row['model'],fmt(row['mean']),fmt(row['sd'])]):c.text=v
d.add_heading('4. What the results support',1)
d.add_paragraph('The revised graph and class-free channel walks can be trained reproducibly. Cooc rank stability does not imply external predictive validity; chemistry rank instability under compound pruning reflects selected-panel sensitivity. Complete-pair formula LOFO remains evaluable in only six of ten folds due to cold-start herbs. No claim of biological or therapeutic similarity is justified.')
d.add_heading('5. Outstanding scientific gates',1)
for x in ['Recover original 35-class chemical ontology or design a new independently verified mapping with a new version identity.','Review herb-compound assertions individually with primary full-text locators and plant part/preparation matching.','Build a source-disjoint external formula test corpus with fixed eligibility criteria.','Have independent human experts review blinded herb-pair labels and medicinal-material distinctions.','Obtain author sign-off before combining this reanalysis with the original Paper 2 manuscript.']:
 d.add_paragraph(x,style='List Number')
d.add_heading('References',1)
d.add_paragraph('Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566. Ministry of Public Health. '+b['source_pdf'])
d.add_paragraph('Dong, Y., Chawla, N. V., & Swami, A. (2017). metapath2vec: Scalable representation learning for heterogeneous networks. Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 135–144. https://doi.org/10.1145/3097983.3098036')
d.save(M/'Paper2_SourceReviewed_Robustness_v0.4.docx')
print('Generated reports',len(report),'dashboard',len(page),'Word',M/'Paper2_SourceReviewed_Robustness_v0.4.docx')