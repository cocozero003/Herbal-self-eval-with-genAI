"""Generate integrity dashboards, review templates and editorial report for Paper 2.

All computational figures come from CSVs; no fictitious reviewer ratings.
"""
import csv,hashlib,json,itertools,random,statistics
from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';DOC=ROOT/'docs';HTML=ROOT/'dashboard';M=ROOT/'manuscript'
for p in (DOC,HTML,M):p.mkdir(exist_ok=True)
def rows(name):
 with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def table(items,keys):
 return '| '+' | '.join(keys)+' |\n| '+ ' | '.join(['---']*len(keys))+' |\n'+'\n'.join('| '+' | '.join(str(r.get(k,'')) for k in keys)+' |' for r in items)+'\n'
def write(name,arr):
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)

m=json.loads((OUT/'foundation_manifest.json').read_text());base=rows('lofo_baseline_summary.csv');folds=rows('formula_heldout_eligibility_10.csv');source=rows('leave_one_source_out_20.csv');prune=rows('exact_chemistry_panel_pruning_8.csv');cross=rows('formula_id_crosswalk_10.csv');graph=rows('cooc_pair_weights_190.csv');chem=rows('exact_compound_pairs_190.csv');lofo=rows('lofo_graph_sensitivity_20rows.csv')

# Independent human ratings deliberately blank: no model scores and no labels from training.
data=json.loads((ROOT/'data/paper2_bootstrap_v3_proxy.json').read_text());herbs={x['id']:x for x in data['herbs']};pairs=list(itertools.combinations(sorted(herbs),2))
case=[]
for a,b in pairs:
 c='P2-'+hashlib.sha256(('THAIHERB20-REVIEWER-20261107|'+a+'|'+b).encode()).hexdigest()[:14].upper()
 case.append({'case_id':c,'herb_a_id':a,'herb_b_id':b,'herb_a_th':herbs[a]['thai'],'herb_b_th':herbs[b]['thai'],'herb_a_botanical':herbs[a]['scientific'],'herb_b_botanical':herbs[b]['scientific']})
write('BLINDED_REVIEW_CASE_KEY_INTERNAL_190.csv',case)
for reviewer,seed in [('R1',2323),('R2',2424)]:
 ordered=case.copy();random.Random(seed).shuffle(ordered)
 write('BLINDED_EXPERT_'+reviewer+'_190.csv',[{**r,'reviewer':reviewer,'chemical_similarity_grade_0_1_2_or_NA':'','formula_context_grade_0_1_2_or_NA':'','independent_external_evidence_url':'','page_table_exact_locator':'','plant_part_preparation_match_Y_N_U':'','review_confidence':'','review_notes':''} for r in ordered])
write('EXPERT_ADJUDICATION_BLANK_190.csv',[{'case_id':r['case_id'],'rater1_chemistry':'','rater2_chemistry':'','adjudicated_chemistry':'','rater1_formula':'','rater2_formula':'','adjudicated_formula':'','independent_source_confirmed_Y_N_U':'','source_url':'','evidence_locator':'','adjudication_reason':''} for r in case])

singleton=[x for x in data['herbs'] if int(x['formula_count'])==1]
nrare=sum(float(x['positive_npmi'])>0 and int(x['support'])==1 for x in graph)
mean_prune=statistics.mean(float(x['rank_spearman_vs_all5']) for x in prune)
meanprev=statistics.mean(float(x['heldout_pair_prevalence']) for x in folds if x['full_190_pair_eligible']=='1')
current=next(x for x in base if x['model']=='PairSupport')

report=f'''# Paper 2 — Robustness Foundation v0.3 (ThaiHerb20)

**วันที่:** 7 พฤศจิกายน 2569  
**สถานะ:** SOURCE/BASELINE ROBUSTNESS COMPLETE ON V3-DERIVED PROXY; ORIGINAL 35-CLASS CHEM/CORE REPLICATION NOT COMPLETE

## Executive summary

เริ่ม Paper 2 ได้โดยไม่ต้องรอ independent biological validation ของ Paper 1 เพราะโจทย์หลักของ Paper 2 คือ robustness, source/selection dependence และการพัฒนา benchmark ที่ไม่รั่วข้อมูล ส่วน independent expert benchmark ของ Paper 2 จะเป็นการประเมินในระยะถัดไป และ **ยังไม่ได้รับคะแนนจากผู้เชี่ยวชาญจริง**

Baseline ตรวจจากชุด V3-derived: 20 สมุนไพร, 10 ตำรับ, 71 membership assertions, 100 chemistry assertions, 83 compound IDs, 190 herb pairs, 82 positive NPMI edges. สารเคมี 35 classes และ archived 20-seed 190-pair vectors ใน Paper 2 manuscript เดิม **ยังไม่มีไฟล์ที่ตรวจยืนยันได้**. โค้ดนี้จึงไม่อ้างว่าเป็น exact original embedding replication.

## 1. Source integrity และ crosswalk

- 10 ตำรับที่ใช้ใน Paper 2 สามารถจับคู่ F01–F10 กับ Paper 1 source-reviewed snapshot ได้ โดยสมุนไพร 10 ชนิดแรกมี presence ตรงกับข้อมูล Paper 1 ในทุกสูตร
- ความสัมพันธ์ของสมุนไพรที่เพิ่ม H11–H20 ยังอยู่ในสถานะ **V3-derived, not primary independently adjudicated**; ต้องตรวจต้นฉบับทั้งส่วนที่พบและส่วนที่ไม่พบ
- ต้องแยก 200 formula-herb matrix cells เป็นชั้น legacy (100) และ added (100) ไม่รายงานว่า 200 cells ผ่าน primary audit เท่ากัน
- Source IDs เคมี 20 แหล่ง มีแหล่งหลักเพียงหนึ่งต่อสมุนไพรทุกชนิด; source-holdout 20/20 ทำให้สมุนไพรอย่างน้อยหนึ่งชนิดไม่มีข้อมูลเคมี จึงไม่สามารถเปรียบเทียบครบ 190 คู่ได้อย่างเท่าเทียม
- จำนวน positive-NPMI edges ที่ support เพียง 1 ตำรับ: **{nrare}/{sum(float(x['positive_npmi'])>0 for x in graph)}**; ค่านี้สะท้อนความไวของ NPMI ใน corpus ขนาดเล็ก

## 2. Leave-One-Formula-Out coverage

กันสูตรตำรับออกทีละหนึ่งสูตรและสร้าง Cooc scores ใหม่จากอีกเก้าสูตรโดยไม่มีสูตรทดสอบใน training IDs; ผลลัพธ์คือคู่สมุนไพรที่อยู่ในสูตรทดสอบร่วมกัน ไม่ใช่ความคล้ายคลึงทางชีววิทยา การเลือกสมุนไพรและสูตรจาก corpus เดียวกันยังเป็น selection bias.

- ประเมินเต็ม 190 คู่ได้ **6/10** folds
- Cold-start folds: **F02 (H07), F03 (H18), F05 (H20), F07 (H19)**
- Mean prevalence ใน 6 folds ที่มี coverage ครบ = **{meanprev:.4f}**

{table([{'Formula':x['heldout_formula'],'Eligible':x['full_190_pair_eligible'],'Unseen herbs':x['cold_start_herbs'] or '-','Positive pairs':x['heldout_positive_pairs']} for x in folds],['Formula','Eligible','Unseen herbs','Positive pairs'])}

## 3. Task-specific baseline benchmark

การประเมินนี้ใช้ simple baselines โดยยัง **ไม่ได้เทียบกับต้นฉบับ Cooc/Chem/Core Word2Vec 20-seed** เพราะต้นฉบับ class map และ vectors ไม่ได้ถูกกู้คืน. ข้อมูลเคมีที่ทดสอบใช้ exact compound IDs เท่านั้น ไม่ได้อนุมาน chemical classes.

{table([{'Model':r['model'],'Mean AP':r['mean_average_precision'],'95% fold bootstrap':r['fold_bootstrap_low']+'–'+r['fold_bootstrap_high'],'AUROC':r['mean_auroc'],'P@10':r['mean_p10']} for r in base],['Model','Mean AP','95% fold bootstrap','AUROC','P@10'])}

PairSupport Mean AP = **{current['mean_average_precision']}**, AUROC = **{current['mean_auroc']}**. รายงาน uncertainty ใช้ bootstrap ตามสูตรเพียง 6 folds (3,000 ครั้ง) เป็น **exploratory ไม่ใช่ confirmatory CI**.

## 4. Chemistry panel robustness

Randomly removing one of the five chemistry assertions per herb (eight reproducible panels) gives a **mean rank Spearman of {mean_prune:.3f}** on exact-compound Jaccard rankings. This is not the original Chem embedding ablation and does not demonstrate chemical truth.

{table([{'Replicate':r['replicate'],'Rank rho':round(float(r['rank_spearman_vs_all5']),3),'Top-10 overlap':r['top10_overlap']} for r in prune],['Replicate','Rank rho','Top-10 overlap'])}

## 5. Scientific interpretation

- Robustness of score ranking is not independent validity. Formula edges are documentary records, not biological or clinical truth.
- Original source-held-out chemistry **cannot be fully evaluated** when removing any one of 20 original chemistry sources isolates a herb. The correct outcome is BLOCKED, not zero-valued or randomly initialized similarity.
- The 10 extra herbs were selected conditional on occurrence in the same formula corpus and source availability; thus a within-corpus holdout is not an independent external corpus.
- The 35 chemical-class original mapping is missing. A 35-class taxonomy invented after examining the model would be a different experiment.
- Non-cooccurrence in a formula is not evidence of pharmacological dissimilarity.

## 6. Next scientific gates

1. Independently verify H11–H20 × F01–F10 (100 cells) using complete official formula tables and record source pages/ingredient names.
2. Recover original 35 compound-class mapping and training parameters or produce a **new** source-validated class dataset under a distinctly versioned study.
3. Generate frozen model comparison with Cooc/Chem/Core (20 seeds), balanced input budgets, degree and exact-chemistry baselines, and source/corpus held-out evaluation.
4. Acquire an independent formula corpus with precommitted eligibility rules, not post-hoc herbs/formulas chosen from training set.
5. Obtain genuine blinded expert labels from two reviewers for 190 pairs, adjudicate disagreement, and report agreement and source disjointness. Templates are present but **all ratings are blank**.

## References (APA 7)

Brière, G., Stosskopf, T., Loire, B., & Baudot, A. (2026). Benchmarking the impact of data leakage on the performance of knowledge graph embedding models for biomedical link prediction. *Bioinformatics, 42*(8), btag608. https://doi.org/10.1093/bioinformatics/btag608

Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). *ข้อมูลรายการอ้างอิงผลิตภัณฑ์สมุนไพรสำหรับผลิตภัณฑ์สมุนไพรที่ขอจดแจ้ง: ประเภทตำรับยาแผนไทย ฉบับ พ.ศ. 2566*. Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf

**Technical status:** Source/benchmark foundation only. **Not manuscript submission ready.**
'''
(DOC/'PAPER2_V03_RESEARCH_REPORT_TH.md').write_text(report,encoding='utf-8')
(M/'PAPER2_METHODS_RESULTS_ADDENDUM_EN.md').write_text(f'''# Paper 2 — Robustness foundation (v0.3): author-review addendum

**Scientific status:** An exploratory V3-derived proxy-data analysis; not a replication of the archived 35-class Chem/Core model. Results must be distinguished from the earlier 20-herb manuscript.

**Aim:** To establish source-integrity boundaries and leakage-aware structural baselines before extending the 20-herb knowledge graph. This work does not require biological validation of the preceding 10-herb feasibility paper.

**Methods:** We audited 20 herbs, ten formula codes, 71 formula membership assertions, and 100 curated herb–compound assertions. A 20×10 membership matrix was cross-checked against a single-curator ten-herb source review. Leave-one-source-out audit tracked chemistry coverage. For internal leave-one-formula-out benchmarking, each of ten formulas was completely omitted from training and full 190-pair evaluation was restricted to folds with all herbs represented by the remaining nine formulas. We tested PairSupport, DegreeProduct, PositiveNPMI, exact-compound Jaccard and IDF-weighted exact-compound Jaccard. Outcome labels indicate co-occurrence in withheld formulas, not independently graded biological similarity. Eight seed-locked 4-of-5 compound-panel deletion experiments assessed exact-compound rank sensitivity.

**Results:** Twenty distinct chemical source IDs each exclusively supported one focal herb; removing any one source isolated that herb. Four of ten formula-holdout folds exhibited previously unseen herbs. In the six eligible folds, PairSupport achieved mean AP {current['mean_average_precision']} (mean AUROC {current['mean_auroc']}). Exact-compound-only Jaccard was inferior on the held-out formula-cooccurrence task; this does not test chemical accuracy. Mean Spearman rank agreement across eight 4/5 chemistry panels was {mean_prune:.3f}. Positive NPMI edges were 82/190, with {nrare} edges supported by only one formula.

**Interpretation:** This analysis identifies source concentration and cold-start risks in the preselected small formula corpus. No independent external validation or recovery of the original 35-class chemistry ontology has occurred. The reported 20-seed Cooc/Chem/Core values from the original manuscript should not be replaced with these descriptive baseline results.

**Conclusion:** Proceed to source-verifying expanded formulas, recovering class mappings, and preregistering an independent corpus benchmark. Author review and independent adjudication are outstanding.
''',encoding='utf-8')

# Offline dashboard with no external libraries, no icons or emoji in JS.
exhibit={'manifest':m,'summary':base,'folds':folds,'source':source,'pruning':prune,'crosswalk':cross,'graph':graph,'chem':chem,'lofo':lofo}
js=json.dumps(exhibit,ensure_ascii=False).replace('</','<\\/')
html='''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ThaiHerb Paper 2 v0.3 | Robustness</title><style>
:root{font-family:system-ui,'Noto Sans Thai',sans-serif;color:#172c39;background:#f5f7fa}*{box-sizing:border-box}body{margin:0}.layout{max-width:1270px;margin:auto;padding:26px}header{background:#17384b;border-radius:16px;color:white;padding:30px}h1{font-size:28px;margin:8px 0}header p{color:#dcebf2}.notice{background:#fff4da;padding:15px;border-left:4px solid #ab7217;margin:20px 0;border-radius:6px}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.kpi,.panel{background:white;border:1px solid #dce5eb;border-radius:12px;padding:19px}.kpi strong{font-size:28px;display:block}.kpi span{color:#607480;font-size:12px}nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}button,input{font:inherit;border:1px solid #b4c4ce;background:white;padding:9px 13px;border-radius:8px}button{cursor:pointer}button.active{background:#14516d;color:white;border-color:#14516d}.tab{display:none}.tab.active{display:block}h2{font-size:20px;margin:0 0 15px}.panel p{line-height:1.7}.scroll{max-height:580px;overflow:auto;border:1px solid #e2eaf0;border-radius:8px}table{width:100%;border-collapse:collapse;font-size:12px}th,td{text-align:left;padding:10px;border-bottom:1px solid #e9eef1}th{background:#edf3f7;position:sticky;top:0;white-space:nowrap}td{max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.barrow{display:flex;align-items:center;gap:9px;margin:12px 0}.barrow span{width:185px}.bar{flex:1;background:#e9f1f6;height:15px;border-radius:6px}.fill{height:100%;background:#3185a8;border-radius:6px}.num{width:56px;text-align:right}.search{margin:12px 0;width:100%;max-width:410px}.foot{font-size:12px;color:#607784;margin-top:25px}@media(max-width:740px){.layout{padding:12px}.kpis{grid-template-columns:repeat(2,1fr)}header{padding:20px}h1{font-size:23px}.barrow span{width:125px;font-size:11px}table{min-width:720px}}
</style></head><body><main class="layout"><header><div>THAIHERB 20 / PAPER 2 / v0.3</div><h1>Robustness &amp; Evidence Integrity</h1><p>Source concentration, formula holdout, structural baselines and chemistry-panel perturbation</p></header><section class="notice"><b>Scientific boundary:</b> V3-derived proxy, not exact original Paper 2 archive. No recovered 35-class taxonomy, no external corpus, no human expert ratings. Holdout measures withheld-formula cooccurrence only.</section><div class="kpis"><div class="kpi"><strong>20</strong><span>Herbs</span></div><div class="kpi"><strong>82</strong><span>Positive NPMI edges</span></div><div class="kpi"><strong>6/10</strong><span>LOFO folds with full 190-pair coverage</span></div><div class="kpi"><strong>20/20</strong><span>Chemistry source-holdout coverage failures</span></div></div><nav><button class="active" data-tab="summary">Overview</button><button data-tab="folds">Formula heldouts</button><button data-tab="sources">Source risk</button><button data-tab="chem">Chemistry</button><button data-tab="cross">Formula crosswalk</button><button data-tab="limits">Limitations</button></nav><section class="panel tab active" id="summary"><h2>Baseline ranking on eligible formula holdouts</h2><div id="bars"></div><div id="summarytable"></div><p>PairSupport ranks past co-occurrence in nine training formulas. The target label is documentary pair co-occurrence in the omitted formula, not a clinical or biological label. Six folds are available; fold-bootstrap intervals are exploratory.</p></section><section class="panel tab" id="folds"><h2>Cold-start and graph sensitivity</h2><div id="foldtable"></div><h2 style="margin-top:20px">Graph rank sensitivity</h2><div id="lofotable"></div></section><section class="panel tab" id="sources"><h2>Leave-one-chemical-source-out</h2><p>Each of 20 sources supports a single herb in the imported panel; removing any one source leaves at least one focal herb without chemical evidence. All 20 full-pair chemistry holdouts are blocked.</p><div id="sourceTable"></div></section><section class="panel tab" id="chem"><h2>Exact-compound similarity (no class bridges)</h2><input class="search" id="findChem" placeholder="Search herb ID or compound ID"><div id="chemTable"></div><h2 style="margin-top:20px">Random 4-of-5 compound deletion</h2><div id="pruneTable"></div></section><section class="panel tab" id="cross"><h2>Ten formula-ID crosswalks</h2><p>Legacy H01–H10 presence agrees with Paper 1 single-curator source projection. Newly added H11–H20 remain unverified against full official formula tables.</p><div id="crossTable"></div></section><section class="panel tab" id="limits"><h2>Interpretation</h2><p>The 10 formula records and 20 herbs are purposively selected from a single official compendium. This is an internal record-level holdout only. Absence of formula cooccurrence is not biological dissimilarity. Exact compound overlap does not imply pharmacological effects. The original 35 class annotations and complete embeddings have not been recovered. No reviewer labels are present; blind forms remain intentionally empty.</p></section><div class="foot">ThaiHerb Paper 2 v0.3. Scientific status: exploratory, source-reviewed foundation; not external biological validation.</div></main><script>window.RESEARCH_DATA=__DATA__;</script><script>
const d=window.RESEARCH_DATA;const esc=x=>String(x??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');function makeTable(a,cols){return `<div class="scroll"><table><thead><tr>${cols.map(x=>`<th>${esc(x[1])}</th>`).join('')}</tr></thead><tbody>${a.map(r=>`<tr>${cols.map(x=>`<td title="${esc(r[x[0]])}">${esc(r[x[0]])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`};function init(){const sorted=[...d.summary].sort((a,b)=>Number(b.mean_average_precision)-Number(a.mean_average_precision));document.querySelector('#bars').innerHTML=sorted.map(r=>`<div class="barrow"><span>${esc(r.model)}</span><div class="bar"><div class="fill" style="width:${100*Number(r.mean_average_precision)}%"></div></div><div class="num">${Number(r.mean_average_precision).toFixed(3)}</div></div>`).join('');document.querySelector('#summarytable').innerHTML=makeTable(sorted,[['model','Baseline'],['mean_average_precision','Mean AP'],['mean_auroc','Mean AUROC'],['fold_bootstrap_low','AP CI low'],['fold_bootstrap_high','AP CI high']]);document.querySelector('#foldtable').innerHTML=makeTable(d.folds,[['heldout_formula','Heldout'],['full_190_pair_eligible','Eligible'],['cold_start_herbs','Cold-start herbs'],['heldout_positive_pairs','Positive pairs']]);document.querySelector('#lofotable').innerHTML=makeTable(d.lofo,[['heldout_formula','Heldout'],['comparison_measure','Measure'],['spearman_all_190_pairs','Spearman'],['top10_overlap','Top10 overlap']]);document.querySelector('#sourceTable').innerHTML=makeTable(d.source,[['removed_chemistry_source','Removed source'],['removed_assertions','Removed edges'],['unrepresented_herb_ids','Lost herb'],['eligible_for_complete_190pair_chemistry_comparison','Eligible']]);document.querySelector('#pruneTable').innerHTML=makeTable(d.pruning,[['replicate','Replicate'],['rank_spearman_vs_all5','Spearman'],['top10_overlap','Top10 overlap']]);document.querySelector('#crossTable').innerHTML=makeTable(d.crosswalk,[['formula_id','ID'],['paper1_title_th','Thai formula'],['legacy_10herb_match','Legacy match'],['new_10herb_source_reviewed','Added 10 source-reviewed'],['paper2_imported_source_locator','Imported locator']]);function chemistry(){let q=document.querySelector('#findChem').value.trim().toLowerCase();document.querySelector('#chemTable').innerHTML=makeTable(d.chem.filter(r=>Object.values(r).join(' ').toLowerCase().includes(q)).slice(0,190),[['herb_a','Herb A'],['herb_b','Herb B'],['shared_compounds','Shared compounds'],['compound_jaccard','Jaccard'],['compound_idf_jaccard','IDF Jaccard'],['shared_compound_ids','Shared IDs']])}document.querySelector('#findChem').addEventListener('input',chemistry);chemistry();document.querySelectorAll('nav button').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('nav button').forEach(z=>z.classList.remove('active'));b.classList.add('active');document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x.id===b.dataset.tab));}));}document.addEventListener('DOMContentLoaded',init);
</script></body></html>'''.replace('__DATA__',js)
(HTML/'Paper2_Robustness_v0.3.html').write_text(html,encoding='utf-8')

# Short structured Word technical report, not a full paper/claimed gold.
d=Document();sec=d.sections[0];sec.top_margin=Inches(.52);sec.bottom_margin=Inches(.5)
styles=d.styles;styles['Normal'].font.name='Calibri';styles['Normal'].font.size=Pt(9)
styles['Normal'].paragraph_format.space_after=Pt(3)
styles['Title'].font.name='Calibri';styles['Title'].font.size=Pt(19)
d.add_heading('ThaiHerb Paper 2: Robustness Foundation',0)
p=d.add_paragraph('Version 0.3 | 7 November 2026 | V3-derived research proxy');p.style='Subtitle'
d.add_paragraph('Scientific status: exploratory source integrity and internal formula-holdout baseline; NOT external biological validation or an exact reproduction of the archived 35-class model.',style='Intense Quote')
d.add_heading('1. Scope and source-integrity gates',level=1)
for s in [f"20 herbs; ten formulas; 71 focal formula memberships; 100 chemistry assertions; 83 unique compounds; 190 possible herb pairs; 82 positive-NPMI edges.","All ten legacy H01–H10 formula projections match the Paper 1 single-curator crosswalk. Added herbs H11–H20 are not independently source-adjudicated.","The 35 chemical-class annotations and original 190-pair embedding vectors are missing; full original Chem/Core replication is blocked.","Chemistry source fragility: 20 of 20 leave-one-source-out tests remove the only chemistry source for one focal herb."]:
 d.add_paragraph(s,style='List Bullet')
d.add_heading('2. Internal formula-holdout benchmarks',level=1)
d.add_paragraph('Six of ten folds retain all focal herbs in training. Four folds are blocked by unseen H07, H18, H20 or H19. Outcome is pair membership within the withheld formula, not a biological similarity standard.')
t=d.add_table(rows=1,cols=4);t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
for cell,val in zip(t.rows[0].cells,['Baseline','Mean AP','95% fold CI','Mean AUROC']):cell.text=val
for r in sorted(base,key=lambda r:-float(r['mean_average_precision'])):
 cc=t.add_row().cells
 for cell,v in zip(cc,[{'PositiveNPMI':'Positive NPMI','DegreeProduct':'Degree product','ExactCompoundJaccard':'Exact Jaccard','ExactCompoundIDFJaccard':'Exact IDF Jaccard'}.get(r['model'],r['model']),f"{float(r['mean_average_precision']):.3f}",f"{float(r['fold_bootstrap_low']):.3f}–{float(r['fold_bootstrap_high']):.3f}",f"{float(r['mean_auroc']):.3f}"]):cell.text=v
d.add_heading('3. Exact-compound perturbation',level=1)
d.add_paragraph(f'Eight randomized 4/5 compound panels achieved mean rank Spearman {mean_prune:.3f} relative to the 5/5 exact-compound Jaccard baseline. This does not estimate class-based Chem embedding robustness.')
d.add_heading('4. Interpretation and next gates',level=1)
for s in ['Verify added-herb membership across all ten complete official formula ingredient tables.','Recover the original 35-class chemistry mapping or version a new independently source-reviewed mapping.','Develop paired Cooc/Chem/Core 20-seed embedding comparisons with degree/support baselines.','Define a genuinely external, source-disjoint corpus and secure two blinded human expert assessments.','Do not merge this new exploratory data with historical manuscript numbers as if they were the same experiment.']:
 d.add_paragraph(s,style='List Number')
d.add_heading('References',level=1)
d.add_paragraph('Brière, G., Stosskopf, T., Loire, B., & Baudot, A. (2026). Benchmarking the impact of data leakage on the performance of knowledge graph embedding models for biomedical link prediction. Bioinformatics, 42(8), btag608. https://doi.org/10.1093/bioinformatics/btag608')
d.add_paragraph('Department of Thai Traditional and Alternative Medicine, & Thai Food and Drug Administration. (2023). Reference information for herbal products for notification: Thai traditional medicine formulations (B.E. 2566). Ministry of Public Health. https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf')
d.save(M/'Paper2_Research_Starting_Report_v0.3.docx')
print('Generated report, docx and offline dashboard')