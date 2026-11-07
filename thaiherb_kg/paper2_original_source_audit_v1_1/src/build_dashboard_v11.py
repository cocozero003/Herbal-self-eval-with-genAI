"""Build an offline auditable browser dashboard with local embedded data."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'
DEST=ROOT/'dashboard'/'ThaiHerb_SourceAndValidation_v11_v09.html'

def load_csv(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def build():
    claims=load_csv(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
    sources=load_csv(RESULTS/'P2_SOURCE_TYPE_AUDIT_20_v11.csv')
    taxa=load_csv(RESULTS/'P2_TAXON_SYNONYM_2_v11.csv')
    q=load_csv(RESULTS/'P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv')
    gate=json.loads((RESULTS/'P3_V09_BENCHMARK_GATE_REPORT.json').read_text(encoding='utf-8'))
    shapes=json.loads((RESULTS/'P3_V09_SHACL_PROFILE_STATUS.json').read_text(encoding='utf-8'))
    data={'claims':claims,'sources':sources,'taxa':taxa,'questions':q,'benchmark':gate,'shape':shapes}
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
    html=r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>ThaiHerb KG | Evidence and validation research release</title>
<style>
:root{--bg:#f4f6f9;--ink:#182638;--sub:#5f7184;--border:#d9e0e8;--navy:#15395a;--blue:#17679c;--white:#fff;--pale:#e9f1fa;--green:#186f53;--amber:#a66b0c;--red:#aa4c4c}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}header{background:linear-gradient(110deg,#103452,#1d5978);color:#fff;padding:27px max(calc((100vw - 1220px)/2),28px)}h1{margin:3px 0;font-size:29px;letter-spacing:-.7px}header p{margin:8px 0 0;max-width:950px;color:#dceaf3}main{max-width:1220px;padding:26px 23px 80px;margin:auto}.eyebrow{font-size:12px;letter-spacing:1.2px;text-transform:uppercase;font-weight:700;color:#8cbacb}nav{display:flex;flex-wrap:wrap;gap:8px;border-bottom:1px solid var(--border);padding-bottom:12px;margin-bottom:18px}nav button{font:inherit;border:1px solid var(--border);background:white;color:var(--navy);padding:10px 18px;border-radius:8px;cursor:pointer;font-weight:650}nav button.active{color:#fff;background:var(--navy);border-color:var(--navy)}.metrics{display:grid;grid-template-columns:repeat(4,minmax(140px,1fr));gap:12px;margin:0 0 16px}.metric{border:1px solid var(--border);border-radius:11px;background:white;padding:16px;box-shadow:0 2px 8px #102f4810}.metric span{display:block;color:var(--sub);font-size:13px}.metric strong{display:block;font-size:29px;letter-spacing:-.9px}.panel{background:white;border:1px solid var(--border);border-radius:12px;padding:19px;margin:15px 0;box-shadow:0 2px 7px #0c1d2c08}.panel h2{font-size:20px;margin:0 0 7px}.muted{color:var(--sub)}.controls{display:flex;flex-wrap:wrap;gap:9px;margin:14px 0}.controls input,.controls select{font:inherit;min-width:155px;background:white;border-radius:8px;border:1px solid #c6d0da;padding:10px;flex:1}.controls input{flex:2;min-width:220px}table{width:100%;border-collapse:collapse;table-layout:fixed}th,td{border-bottom:1px solid #e5e9ed;padding:10px 9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#eff3f7;color:#344d60;font-size:12px;text-transform:uppercase;letter-spacing:.3px}td{font-size:13px}.scroll{overflow:auto;max-height:680px;border-radius:8px;border:1px solid var(--border)}td a{color:var(--blue);text-decoration:underline}.flag{display:inline-block;border-radius:20px;background:#e5eef8;color:#164b72;font-weight:650;padding:3px 8px;font-size:11px;overflow-wrap:normal}.flag.grey{background:#ebedf0;color:#596a7a}.flag.yellow{background:#fff3d9;color:#8b5e0b}.flag.green{background:#e3f4eb;color:#166448}.bar{height:10px;background:#e6edf4;border-radius:8px;overflow:hidden;margin:6px 0}.fill{height:100%;background:var(--blue)}.twocol{display:grid;grid-template-columns:1fr 1fr;gap:14px}.notice{background:#fff8e8;border-left:4px solid #c89427;padding:12px 14px;border-radius:4px;margin:13px 0}.actions{display:flex;gap:12px;flex-wrap:wrap}.actions button{padding:8px 12px;background:#fff;border:1px solid #9eb0c2;color:#143b60;border-radius:6px;cursor:pointer}.actions button:hover{background:#eaf4fc}.hidden{display:none}.group{padding:12px 0;border-bottom:1px solid #ebeff4}.group:last-child{border-bottom:0}.group strong{font-size:17px}.caption{font-size:13px;color:var(--sub)}.small{font-size:12px}.wrap{white-space:normal;max-width:250px}.nobreak{white-space:nowrap}footer{color:var(--sub);font-size:13px;padding-top:12px}@media(max-width:800px){.metrics{grid-template-columns:repeat(2,minmax(140px,1fr))}.twocol{grid-template-columns:1fr}h1{font-size:22px}th,td{font-size:12px;padding:7px}table{min-width:920px}}
</style></head><body>
<header><div class="eyebrow">Thai Herbal Knowledge Graph | Research release</div>
<h1>Evidence Traceability &amp; RDF Validation</h1>
<p>Paper 2 v1.1 / Paper 3 v0.9. Audited source types and material-dependent qualifiers are distinguished from primary experimental results. This is a development research audit, not clinical or expert scientific validation.</p>
</header><main>
<nav aria-label="Dashboard views"><button class="active" data-tab="claims" onclick="showTab('claims')">Chemical evidence</button><button data-tab="sources" onclick="showTab('sources')">Source registry</button><button data-tab="taxon" onclick="showTab('taxon')">Taxon &amp; process</button><button data-tab="graph" onclick="showTab('graph')">RDF integrity</button><button data-tab="review" onclick="showTab('review')">Blind benchmark</button></nav>
<section id="tab-claims">
  <div class="metrics" id="cards"></div>
  <div class="panel"><h2>Original-source claim screening</h2><p class="muted">Status describes the level of documentary support inspected for each fixed assertion. An unresolved location is not evidence of absence.</p>
    <div class="controls"><input id="search" type="search" placeholder="Find herb, source, compound or assertion ID" aria-label="Search chemical claims" oninput="drawClaims()"/>
    <select id="grade" onchange="drawClaims()" aria-label="Filter evidence grade"><option value="">All evidence grades</option></select>
    <select id="herb" onchange="drawClaims()" aria-label="Filter species"><option value="">All herbs</option></select></div>
    <div class="actions"><button onclick="downloadFiltered()">Export filtered CSV</button><span class="caption" id="filteredCount"></span></div>
    <div class="scroll"><table><thead><tr><th style="width:9%">Claim</th><th style="width:20%">Herb / species</th><th style="width:15%">Compound</th><th style="width:22%">Screen grade</th><th style="width:22%">Exact source locator / context</th><th style="width:12%">Source</th></tr></thead><tbody id="claimRows"></tbody></table></div>
  </div>
</section>
<section class="hidden" id="tab-sources">
 <div class="panel"><h2>20 original publications screened</h2><p class="muted">Publication type is a source-level property; a review can support a secondary synthesis, but it cannot be recast as a new laboratory assay.</p>
 <div class="scroll"><table><thead><tr><th style="width:17%">Source ID</th><th style="width:18%">Publication type</th><th style="width:26%">Bibliography</th><th style="width:29%">Scope limitations</th><th style="width:10%">Link</th></tr></thead><tbody id="sourceRows"></tbody></table></div></div>
</section>
<section class="hidden" id="tab-taxon">
 <div class="metrics"><div class="metric"><span>Verified synonym crosswalks</span><strong>2</strong></div><div class="metric"><span>Plant/process-specific primary abstracts</span><strong>10</strong></div><div class="metric"><span>Original legacy chemical classes recovered</span><strong>0</strong></div><div class="metric"><span>Human independent reviewer decisions</span><strong>0</strong></div></div>
 <div class="panel"><h2>Taxonomic names and material/process context</h2><div id="taxaList"></div><div class="notice">For H19, the reported concinnosides were isolated after alkaline hydrolysis of pod saponin fractions. Do not infer intact compound occurrence in every untreated pod or formulation.</div></div>
</section>
<section class="hidden" id="tab-graph">
 <div class="metrics"><div class="metric"><span>Locked source assertions</span><strong>208</strong></div><div class="metric"><span>M1 / M2 / M3 RDF triples</span><strong>207 / 1,501 / 2,733</strong></div><div class="metric"><span>Local subset violations</span><strong id="violations">0</strong></div><div class="metric"><span>Synthetic negative controls detected</span><strong id="negative">7 / 7</strong></div></div>
 <div class="twocol"><div class="panel"><h2>SHACL constraint checks</h2><p>The local checker reads the actual SHACL shapes and tests the six constraint kinds used by this release. It is <strong>not</strong> a complete SHACL Core validator.</p><div class="notice">pySHACL Core engine: <strong>NOT RUN</strong>. Do not treat a local-subset pass as standards-wide conformance.</div></div>
 <div class="panel"><h2>Representation integrity</h2><p><strong>M1</strong>: 207 distinct SPO statements from 208 assertions; collapses one clinical relationship pair.</p><p><strong>M2</strong>: assertion IDs and source links can be recovered.</p><p><strong>M3</strong>: additional evidence mode, directness, context and limitation attributes. These are structural, not QA accuracy results.</p></div></div>
</section>
<section class="hidden" id="tab-review">
 <div class="metrics"><div class="metric"><span>Prepared candidate questions</span><strong>32</strong></div><div class="metric"><span>Model response assessment slots</span><strong>96</strong></div><div class="metric"><span>Adjudicated expert gold answers</span><strong>0</strong></div><div class="metric"><span>Comparative answer accuracy reported</span><strong>None</strong></div></div>
 <div class="panel"><h2>Independent blinded benchmark gate</h2><div class="notice">Confirmatory scoring is blocked until both independent reviewers supply decisions, conflicts are checked, gold is adjudicated and frozen model responses are evaluated without exposure to the comparator.</div>
 <p class="muted">The next-stage ZIP includes a paired-score evaluator, exact McNemar testing and paired bootstrap. Synthetic examples exist in unit tests only and are not treated as experimental evidence.</p>
 <div class="scroll"><table><thead><tr><th style="width:14%">Case ID</th><th style="width:18%">Category</th><th style="width:54%">Draft competency question</th><th style="width:14%">Gold status</th></tr></thead><tbody id="reviewRows"></tbody></table></div></div>
</section>
<footer>Frozen source: ThaiHerb Paper 2 v0.5 chemistry 100 and Paper 3 V3 208. All screening decisions are AI-assisted and should be independently audited before publication.</footer>
</main><script id="data" type="application/json">__PAYLOAD__</script><script>
'use strict';
const db=JSON.parse(document.getElementById('data').textContent);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const grades=['PRIMARY_FULLTEXT_EXPERIMENT','PRIMARY_ABSTRACT_EXPERIMENT','PRIMARY_ABSTRACT_PROCESS_DEPENDENT','SECONDARY_FULLTEXT_REVIEW','UNRESOLVED_CLAIM_LOCATOR'];
const gradeColor=g=>g.startsWith('PRIMARY_FULLTEXT')?'green':g.startsWith('PRIMARY_ABSTRACT')?'yellow':g.startsWith('SECONDARY')?'':'grey';
let filtered=[];
function showTab(name){for(const id of ['claims','sources','taxon','graph','review'])document.getElementById('tab-'+id).classList.toggle('hidden',id!==name);for(const el of document.querySelectorAll('nav button')){el.classList.toggle('active',el.dataset.tab===name);} }
function drawCards(){let counts={};for(const row of db.claims)counts[row.original_source_claim_screen_grade]=(counts[row.original_source_claim_screen_grade]||0)+1;const items=[['All claims',db.claims.length],['Primary full text',counts.PRIMARY_FULLTEXT_EXPERIMENT||0],['Primary abstract only',(counts.PRIMARY_ABSTRACT_EXPERIMENT||0)+(counts.PRIMARY_ABSTRACT_PROCESS_DEPENDENT||0)],['Review-level mention',counts.SECONDARY_FULLTEXT_REVIEW||0]];document.getElementById('cards').innerHTML=items.map(([label,value])=>`<div class="metric"><span>${esc(label)}</span><strong>${value}</strong></div>`).join('');}
function drawClaims(){let query=document.getElementById('search').value.trim().toLowerCase(),grade=document.getElementById('grade').value,herb=document.getElementById('herb').value;filtered=db.claims.filter(r=>(!grade||r.original_source_claim_screen_grade===grade)&&(!herb||r.herb_id===herb)&&(!query||[r.assertion_id,r.herb_id,r.scientific_name_locked,r.compound_locked,r.source_id_locked,r.locator].join(' ').toLowerCase().includes(query)));
 document.getElementById('filteredCount').textContent=`${filtered.length} / ${db.claims.length} claims`;
 document.getElementById('claimRows').innerHTML=filtered.map(r=>`<tr><td class="nobreak"><strong>${esc(r.assertion_id)}</strong><div class="caption">${esc(r.herb_id)}</div></td><td>${esc(r.scientific_name_locked)}</td><td>${esc(r.compound_locked)}</td><td><span class="flag ${gradeColor(r.original_source_claim_screen_grade)}">${esc(r.original_source_claim_screen_grade)}</span></td><td class="wrap">${esc(r.locator||'Claim-specific source location unresolved')}<div class="caption">${esc(r.material_process_context)}</div></td><td><a href="${esc(r.source_type_url)}" target="_blank" rel="noopener noreferrer">${esc(r.source_id_locked)}</a><div class="caption">${esc(r.source_type_screened)}</div></td></tr>`).join('');}
function fill(){drawCards();let s=document.getElementById('grade');for(const g of grades)s.add(new Option(g.replace(/_/g,' '),g));s=document.getElementById('herb');for(const id of [...new Set(db.claims.map(x=>x.herb_id))]){const r=db.claims.find(x=>x.herb_id===id);s.add(new Option(`${id} ${r.scientific_name_locked}`,id));}drawClaims();document.getElementById('sourceRows').innerHTML=db.sources.map(r=>`<tr><td><strong>${esc(r.source_id)}</strong></td><td>${esc(r.screened_source_type)}</td><td>${esc(r.bibliography)}</td><td>${esc(r.source_scope_note)}</td><td><a href="${esc(r.source_url)}" rel="noopener noreferrer" target="_blank">Open source</a></td></tr>`).join('');document.getElementById('taxaList').innerHTML=db.taxa.map(r=>`<div class="group"><strong>${esc(r.herb_id)} — ${esc(r.accepted_name)}</strong><p>Older paper name: <em>${esc(r.name_in_older_source)}</em></p><p>${esc(r.relationship)} — <a target="_blank" rel="noopener noreferrer" href="${esc(r.url)}">${esc(r.authority)}</a></p><p class="muted">${esc(r.note)}</p></div>`).join('');document.getElementById('violations').textContent=db.shape.original_dataset_subshape_violations;document.getElementById('negative').textContent=db.shape.negative_controls_detected+' / '+db.shape.negative_controls_total;document.getElementById('reviewRows').innerHTML=db.questions.map(r=>`<tr><td>${esc(r.case_id)}</td><td>${esc(r.category)}</td><td>${esc(r.question)}</td><td><span class="flag grey">${esc(r.independent_gold_available)}</span></td></tr>`).join('');}
function downloadFiltered(){let keys=['assertion_id','herb_id','scientific_name_locked','compound_locked','source_id_locked','source_type_screened','original_source_claim_screen_grade','locator','material_process_context','source_type_url'];let rows=[keys,...filtered.map(r=>keys.map(k=>r[k]||''))];let csv=rows.map(r=>r.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(',')).join('\r\n');let blob=new Blob([new Uint8Array([0xEF,0xBB,0xBF]),csv],{type:'text/csv;charset=utf-8'});let url=URL.createObjectURL(blob);let a=document.createElement('a');a.href=url;a.download='thaiherb_screened_claims_v11.csv';a.click();URL.revokeObjectURL(url)}
fill();
</script></body></html>'''
    DEST.parent.mkdir(exist_ok=True)
    DEST.write_text(html.replace('__PAYLOAD__',payload),encoding='utf-8')
    return {'path':str(DEST),'claims':len(claims),'sources':len(sources),'questions':len(q),'bytes':DEST.stat().st_size}
if __name__=='__main__':print(json.dumps(build(),indent=2))
