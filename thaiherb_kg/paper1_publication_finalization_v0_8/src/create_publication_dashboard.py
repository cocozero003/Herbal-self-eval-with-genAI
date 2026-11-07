"""Single-file offline Research QA dashboard. No external scripts or credentials."""
from pathlib import Path
import json,csv,html
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';OUT=ROOT/'dashboard'
OUT.mkdir(exist_ok=True)
def rows(name):
 with (R/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
data={
 'seed':rows('seed_repeatability_13models.csv'),
 'pert':rows('perturbation_sensitivity_10comparisons.csv'),
 'original':rows('ORIGINAL_MANUSCRIPT_VS_V08_REANALYSIS.csv'),
 'gates':rows('PUBLICATION_READINESS_GATES.csv'),
 'families':rows('botanical_family_descriptive_3models.csv'),
 'lofo':rows('model_comparison_cluster_bootstrap.csv'),
 'manifest':json.loads((R/'reanalysis_manifest.json').read_text()),
 'replay':json.loads((R/'REPLAY_VERIFICATION.json').read_text()),
}
payload=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
style=r'''*{box-sizing:border-box}body{margin:0;background:#f3f6f7;color:#193644;font:14px/1.55 Arial,'Noto Sans Thai',sans-serif}main{max-width:1200px;margin:auto;padding:22px}header{padding:32px;background:#173f51;color:#fff;border-radius:16px}h1{font-size:28px;margin:7px 0}header p{max-width:840px;color:#dfedf3;margin:6px 0}header small{color:#b4d0dd}nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}button,input,select{font:inherit;padding:10px 13px;border:1px solid #aec4ce;border-radius:7px;background:#fff;color:#193644}button{cursor:pointer}button.active{background:#246078;color:#fff}.tab{display:none}.tab.active{display:block}.panel,.stat{background:#fff;border:1px solid #dbe7eb;border-radius:12px;padding:19px;margin:12px 0}.notice{border-left:4px solid #af711a;background:#fff7e7;padding:14px 18px;margin:18px 0}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.stat{margin:0}.stat strong{font-size:26px;display:block}.stat span{color:#61737b;font-size:12px}.scroll{max-height:610px;overflow:auto}.tools{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}table{border-collapse:collapse;width:100%;font-size:12.5px}th,td{text-align:left;padding:9px;border-bottom:1px solid #e7eef0}th{position:sticky;top:0;background:#eaf2f5;white-space:nowrap}.row{display:flex;align-items:center;gap:12px;margin:9px 0}.row label{width:170px;flex-shrink:0}.bar{height:12px;background:#e8f0f3;border-radius:6px;flex:1;overflow:hidden}.fill{height:100%;background:#4a879f}.val{width:58px;text-align:right;font-variant-numeric:tabular-nums}.muted{font-size:12px;color:#647b86}.warning{color:#8c590a}footer{font-size:12px;color:#55717e;margin:20px 0}@media(max-width:700px){main{padding:10px}header{padding:22px}h1{font-size:22px}.grid{grid-template-columns:repeat(2,1fr)}.stat strong{font-size:22px}table{min-width:660px}.row label{width:116px;font-size:11px}}'''
script=r'''
const d=window.RESEARCH_DATA;
const esc=x=>String(x??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
const to3=x=>Number(x).toFixed(3);
function tab(id,btn){document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x.id===id));document.querySelectorAll('nav button').forEach(x=>x.classList.remove('active'));btn.classList.add('active')}
function makeTable(rows,cols){return `<div class="scroll"><table><thead><tr>${cols.map(k=>`<th>${esc(k[1])}</th>`).join('')}</tr></thead><tbody>${rows.map(x=>`<tr>${cols.map(k=>`<td title="${esc(x[k[0]])}">${esc(x[k[0]])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`}
function init(){
  document.querySelector('#fitbars').innerHTML=[...d.seed].filter(x=>['Cooc-NPMI','Chem-Candidate19','Core-Candidate19','Cooc-Combined'].includes(x.model)).map(r=>`<div class="row"><label>${esc(r.model)}</label><div class="bar"><div class="fill" style="width:${100*Number(r.rank_rho_mean)}%"></div></div><div class="val">${to3(r.rank_rho_mean)}</div></div>`).join('');
  document.querySelector('#modelSummary').innerHTML=makeTable(d.seed,[['model','Model'],['rank_rho_mean','Mean rho'],['rank_rho_sd_population','SD'],['rank_rho_min','Min'],['rank_rho_max','Max']]);
  document.querySelector('#pert').innerHTML=makeTable(d.pert,[['perturbation','Perturbation'],['baseline','Compared to'],['mean_rank_spearman','Rank rho'],['top5_overlap_mean_vectors','Top-5 shared'],['mean_absolute_cosine_shift','Cosine shift']]);
  document.querySelector('#original').innerHTML=makeTable(d.original,[['original_manuscript_label','Analysis'],['archived_manuscript_value','Original report'],['fresh_reanalysis_value','New reanalysis'],['identity','Equivalence status']]);
  document.querySelector('#gate').innerHTML=makeTable(d.gates,[['gate','Gate'],['requirement','Requirement'],['status','Status'],['comment','Notes']]);
  document.querySelector('#lofo').innerHTML=makeTable([...d.lofo].sort((a,b)=>Number(b.mean_average_precision)-Number(a.mean_average_precision)),[['method','Model'],['mean_average_precision','Mean AP'],['mean_auroc','AUROC'],['eligible_folds','Folds']]);
  const q=document.querySelector('#search');q.addEventListener('input',()=>{const term=q.value.toLowerCase();document.querySelector('#modelSummary').innerHTML=makeTable(d.seed.filter(x=>x.model.toLowerCase().includes(term)),[['model','Model'],['rank_rho_mean','Mean rho'],['rank_rho_sd_population','SD'],['rank_rho_min','Min'],['rank_rho_max','Max']]);});
}
document.addEventListener('DOMContentLoaded',init);
'''
page=f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ThaiHerb Paper1 v0.8 Research Review</title><style>{style}</style></head><body><main><header><small>THAIHERB / PAPER 1 / RESEARCH REANALYSIS v0.8</small><h1>Publication Readiness and Evidence-Channel Feasibility</h1><p>Ten-herb pilot: coherent computational reanalysis, scientific limits and original-result reconciliation.</p></header>
<div class="notice"><strong>Scientific boundary:</strong> The candidate 19 chemical classes are not the recovered original class archive. This dashboard reports a new V3-derived reconstruction, not an exact replay of the historical Paper 1 results. Formula holdout is not independent biological validation.</div>
<div class="grid"><div class="stat"><strong>10</strong><span>Focal herbs and formulas</span></div><div class="stat"><strong>30</strong><span>Herb–compound claims</span></div><div class="stat"><strong>130</strong><span>Model fits / 10 seeds</span></div><div class="stat"><strong>10/10</strong><span>Automated tests</span></div></div>
<nav><button class="active" onclick="tab('overview',this)">Summary</button><button onclick="tab('models',this)">Model stability</button><button onclick="tab('sensitivity',this)">Perturbations</button><button onclick="tab('reconcile',this)">Original vs new</button><button onclick="tab('external',this)">Validation</button><button onclick="tab('publish',this)">Readiness</button></nav>
<section id="overview" class="tab active panel"><h2>What can be concluded?</h2><p>It is computationally feasible to construct separate formula and phytochemical evidence-channel embeddings for the selected ten-herb graph. The new training pipeline reruns 13 model variants across 10 seeds and successfully reproduces the computational outputs within the version-frozen runtime.</p><p><strong>What cannot be concluded:</strong> The model does not establish therapeutic equivalence, clinical effectiveness or biological relevance. The original archived chemical class mapping and embeddings are not accessible; an author-approved publication decision has not been recorded.</p><h3>Seed-rank correlations</h3><div id="fitbars"></div></section>
<section id="models" class="tab panel"><h2>Seed repeatability (new proxy only)</h2><div class="tools"><input id="search" placeholder="Filter model name"></div><div id="modelSummary"></div></section>
<section id="sensitivity" class="tab panel"><h2>Graph-construction sensitivity</h2><p class="muted">Spearman of ten-seed mean rank vectors. Large changes reflect curation and graph topology sensitivity, not a clinical conclusion.</p><div id="pert"></div></section>
<section id="reconcile" class="tab panel"><h2>Original manuscript compared with new calculations</h2><p class="warning">Different class mapping and unavailable original vectors mean these must NOT be described as identical experiments.</p><div id="original"></div></section>
<section id="external" class="tab panel"><h2>Internal formula holdout (v0.7 supplement)</h2><p>The task tests whether herb pairs appear together in a withheld formula from the same selected compendium. PairSupport outperformed the embeddings on this task, and one fold was blocked due to a cold-start herb. No independent expert ratings have been supplied.</p><div id="lofo"></div></section>
<section id="publish" class="tab panel"><h2>Research release gates</h2><div id="gate"></div><p class="muted">Automated tests and exact replay provide computational integrity only. Original pilot reproducibility, full-text chemical adjudication and coauthor signoff remain open.</p></section>
<footer>Generated 2026-11-07 | Offline single-file research view | No remote resources, model inference or tracking</footer></main><script>window.RESEARCH_DATA={payload};</script><script>{script}</script></body></html>'''
(OUT/'Paper1_Publication_Readiness_v08.html').write_text(page,encoding='utf-8')
print('saved',len(page))