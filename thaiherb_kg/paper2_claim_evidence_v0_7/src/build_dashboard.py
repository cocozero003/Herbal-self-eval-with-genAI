"""Generate no-network searchable audit and model query explorer."""
from __future__ import annotations
import json
from pathlib import Path
try:
    from .stage_next import ROOT, RES, readcsv
except ImportError:
    from stage_next import ROOT, RES, readcsv


def build_dashboard():
    p2=readcsv(RES/'P2_CHEM_EVIDENCE_100_v07.csv')
    p3=readcsv(RES/'P3_V05_ENGINE_OUTPUTS_24.csv')
    sources=readcsv(RES/'P2_V07_EVIDENCE_SOURCE_REGISTRY.csv')
    data=json.dumps({'chem':p2,'queries':p3,'sources':sources},ensure_ascii=False).replace('</','<\\/')
    html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ThaiHerb Evidence Integrity and Query Research</title>
<style>
:root {--bg:#f4f6f8;--paper:#fff;--line:#dce2e8;--ink:#142334;--muted:#647487;--accent:#204d68}
*{box-sizing:border-box}body{background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,Segoe UI,Arial,sans-serif;margin:0}
header{background:#182b3c;color:white;padding:26px max(20px,calc((100% - 1240px)/2))}
header h1{margin:0;font-size:26px} header p{margin:8px 0 0;color:#ced7df}
main{max-width:1240px;padding:20px;margin:0 auto}.nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.nav button{border:1px solid var(--line);border-radius:7px;background:white;color:var(--ink);padding:10px 17px;cursor:pointer}
.nav button.selected{background:var(--accent);color:#fff}.panel{background:var(--paper);border:1px solid var(--line);border-radius:11px;padding:20px;margin-bottom:16px}
h2{font-size:20px;margin:0 0 12px}h3{margin:0 0 7px}.muted{color:var(--muted)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.kpi{border:1px solid var(--line);border-radius:9px;padding:14px;background:white}.kpi strong{font-size:24px;display:block}
.filters{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px}input,select{font:inherit;border:1px solid #bcc7d1;border-radius:7px;padding:9px;background:#fff;max-width:100%}
.filters input{flex:1;min-width:200px}.filters select{min-width:180px}.scroll{overflow:auto;max-height:600px}
table{border-collapse:collapse;width:100%;font-size:13px}th{background:#edf1f5;position:sticky;top:0;white-space:nowrap;text-align:left}
th,td{padding:10px;border-bottom:1px solid #e4e9ed;vertical-align:top}
a{color:#17658b;word-break:break-all}tr:hover{background:#f7f9fa}
.status{font-size:12px;display:inline-block;border:1px solid #cbd4de;padding:2px 8px;border-radius:20px;white-space:nowrap}
.detail{white-space:pre-wrap;overflow:auto;background:#f5f7f9;padding:14px;border-radius:7px;max-height:370px}
footer{color:var(--muted);padding:26px 0}
@media(max-width:650px){main{padding:12px}header{padding:20px}th,td{padding:7px}}
</style></head><body>
<header><h1>ThaiHerb Knowledge Graph Research Explorer</h1>
<p>Paper 2 v0.7 and Paper 3 v0.5 — source-reviewed development. No independent expert gold, external accuracy, or SHACL Core conformance claim.</p></header>
<main><nav class="nav"><button class="selected" data-tab="chem">Paper 2 — Chemical source audit</button>
<button data-tab="query">Paper 3 — RDF query engine</button><button data-tab="registry">Sources and methods</button></nav>
<section id="chem"><div class="kpis" id="stats"></div><div class="panel"><h2>100 evidence assertions</h2>
<p class="muted">PRIMARY_ABSTRACT_ONLY and SECONDARY_ONLY are not equivalent to primary experimental full-text verification.</p>
<div class="filters"><input id="searchChem" placeholder="Search herb, compound, source or assertion ID" aria-label="Search chemicals">
<select id="level"><option value="">All evidence statuses</option><option>PRIMARY_FULLTEXT_MATCH</option><option>PRIMARY_ABSTRACT_ONLY</option><option>SECONDARY_ONLY</option><option>NOT_VERIFIED</option></select></div>
<p class="muted" id="chemCount"></p><div class="scroll"><table><thead><tr><th>ID</th><th>Herb</th><th>Compound</th><th>Evidence status</th><th>Primary/secondary locator</th><th>Source</th></tr></thead><tbody id="chemRows"></tbody></table></div></div></section>
<section id="query" hidden><div class="kpis"><div class="kpi"><strong>208</strong>Frozen V3 assertions</div><div class="kpi"><strong>207</strong>M1 distinct triples</div><div class="kpi"><strong>1,501</strong>M2 triples</div><div class="kpi"><strong>2,733</strong>M3 triples</div></div>
<div class="panel"><h2>24 deterministic query outputs</h2><p class="muted">Eight competency question development cases, three RDF projections. This is structural retrieval, not adjudicated accuracy.</p>
<div class="filters"><select id="cqCase"></select><select id="cqModel"><option>M1</option><option>M2</option><option>M3</option></select></div>
<div id="answer"></div><h3>Returned source records</h3><pre class="detail" id="recordDetail"></pre></div></section>
<section id="registry" hidden><div class="panel"><h2>Source registry</h2><div id="sourceRows"></div></div><div class="panel"><h2>Research gates</h2><p>The 208 original V3 assertions remain immutable. Material and preparation are not normalized into canonical material nodes. PySHACL Core could not run in this environment, and all human-review/gold labels remain empty.</p>
<p>No distinction in graph representation establishes therapeutic efficacy, safety, interchangeability, or regulatory authorization.</p></div></section>
<footer>Reproducible research engineering preview. AI-assisted source review and model query outputs require scientific adjudication before publication.</footer></main>
<script>
const store = DATA_PLACEHOLDER;
function el(tag,text){const n=document.createElement(tag);n.textContent=String(text??'');return n}
function clear(node){while(node.firstChild)node.removeChild(node.firstChild)}
const chem=store.chem, qa=store.queries;
for(const button of document.querySelectorAll('[data-tab]'))button.addEventListener('click',()=>{
 for(const b of document.querySelectorAll('[data-tab]'))b.classList.toggle('selected',b===button);
 for(const id of ['chem','query','registry'])document.getElementById(id).hidden=id!==button.dataset.tab;
});
const levels=['PRIMARY_FULLTEXT_MATCH','PRIMARY_ABSTRACT_ONLY','SECONDARY_ONLY','NOT_VERIFIED'];
for(const lvl of levels){const k=el('div','');k.className='kpi';const v=el('strong',chem.filter(r=>r.v07_review_level===lvl).length);k.append(v,el('span',lvl.replaceAll('_',' ')));document.getElementById('stats').appendChild(k)}
function renderChem(){const term=document.getElementById('searchChem').value.toLowerCase(),status=document.getElementById('level').value;
 const chosen=chem.filter(r=>(!status||r.v07_review_level===status)&&[r.assertion_id,r.herb_scientific_name,r.compound_label,r.source_id].join(' ').toLowerCase().includes(term));
 document.getElementById('chemCount').textContent=`Showing ${chosen.length} of ${chem.length} assertions`;
 const body=document.getElementById('chemRows');clear(body);
 for(const r of chosen){const tr=document.createElement('tr');for(const v of [r.assertion_id,r.herb_scientific_name,r.compound_label,r.v07_review_level,r.v07_source_locator||'Unverified',r.source_id]){
 const td=el('td',v);tr.append(td)}body.appendChild(tr)} }
document.getElementById('searchChem').addEventListener('input',renderChem);
document.getElementById('level').addEventListener('change',renderChem);renderChem();
const cases=[...new Set(qa.map(x=>x.case_id))];const caseSelect=document.getElementById('cqCase');
for(const id of cases){const row=qa.find(x=>x.case_id===id);const opt=el('option',`${id} — ${row.category}: ${row.question}`);opt.value=id;caseSelect.appendChild(opt)}
function renderQuery(){const row=qa.find(x=>x.case_id===caseSelect.value&&x.model===document.getElementById('cqModel').value);
 const out=document.getElementById('answer');clear(out);
 if(!row)return;out.appendChild(el('h3',row.question));out.appendChild(el('p',`Status: ${row.status}`));out.appendChild(el('p',`Graph edges: ${row.edge_count} | Distinct assertion IDs: ${row.distinct_assertion_ids} | Source IDs: ${row.source_ids||'Unavailable'}`));
 out.appendChild(el('p',row.qualification||'No additional qualification encoded.'));document.getElementById('recordDetail').textContent=JSON.stringify(JSON.parse(row.returned_records_json),null,2)}
caseSelect.addEventListener('change',renderQuery);document.getElementById('cqModel').addEventListener('change',renderQuery);renderQuery();
const sourcePanel=document.getElementById('sourceRows');for(const s of store.sources){const p=document.createElement('p');p.append(el('strong',s.source_id+' — '+s.level+' '));const a=el('a',s.doi||s.evidence_url);a.href=s.evidence_url;a.target='_blank';a.rel='noopener noreferrer';p.appendChild(a);p.append(el('div',s.context));sourcePanel.appendChild(p)}
</script></body></html>'''
    (ROOT/'dashboard'/'ThaiHerb_P2v07_P3v05_EvidenceExplorer.html').write_text(html.replace('DATA_PLACEHOLDER',data),encoding='utf-8')
if __name__=='__main__':build_dashboard()
