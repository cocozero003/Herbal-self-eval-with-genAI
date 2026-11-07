"""Build one offline, source-identifiable research audit dashboard."""
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results'
OUT=ROOT/'dashboard'
OUT.mkdir(exist_ok=True)
def read(name):
 with (RES/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
data={'summary':json.loads((RES/'P3_V11_EXPERIMENT_SUMMARY.json').read_text(encoding='utf-8')),
      'models':read('P3_MODEL_CAPABILITY_SUMMARY.csv'),
      'assertions':read('P3_ASSERTION_AUDIT_624.csv'),
      'clinical':read('P3_CLINICAL_CONTEXT_VARIATION.csv'),
      'ablation':read('P3_CONTEXT_ABLATION.csv'),
      'development':read('P3_DEVELOPMENT_CQ_24_SUMMARY.csv')}
js=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
html='''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ThaiHerb Paper 3: Evidence-Centric RDF Research Audit</title>
<style>
:root{--ink:#172b43;--muted:#596b7b;--bg:#f4f7fa;--line:#dbe3e9;--accent:#205e83;--panel:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Arial,"Noto Sans",sans-serif}
header{background:#123149;color:#fff;padding:28px max(22px,calc((100vw - 1160px)/2));}
header h1{font-size:26px;margin:4px 0 10px}header p{font-size:14px;max-width:890px;line-height:1.6;color:#dfeaf2}
main{max-width:1160px;margin:0 auto;padding:22px}
nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}button.tab{border:1px solid #cbd8e0;background:white;border-radius:8px;padding:10px 15px;color:var(--ink);cursor:pointer}
button.tab.active{background:#205e83;color:#fff;border-color:#205e83}section{display:none}section.active{display:block}
.panel{background:white;border:1px solid var(--line);padding:19px;border-radius:12px;margin:12px 0;box-shadow:0 2px 12px #dbe5ef40}.layout{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.metric strong{display:block;font-size:31px;margin-bottom:6px}.metric span{color:var(--muted);font-size:13px}
.tablewrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:12px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}th{background:#e8f1f7;position:sticky;top:0}td{vertical-align:top;line-height:1.5}
label{font-size:13px;color:var(--muted)}select,input{border:1px solid #b7c8d7;background:white;color:var(--ink);padding:9px 11px;border-radius:8px;font-size:13px}input{min-width:260px}h2{margin-top:0;font-size:20px}h3{font-size:15px}.muted{color:var(--muted);line-height:1.6;font-size:13px}
.barrow{display:flex;gap:14px;align-items:center;margin:12px 0}.barlabel{width:175px;font-size:12px}.track{height:19px;background:#e9eef2;border-radius:6px;flex:1;overflow:hidden}.fill{height:19px;background:#2c7198}.val{width:62px;text-align:right;font-variant-numeric:tabular-nums;font-size:12px}
footer{font-size:12px;color:var(--muted);padding:14px 5px 26px}code{font-family:Consolas,monospace;font-size:12px}
</style></head><body><header><h1>ThaiHerb EvidenceKG — Paper 3</h1>
<p>Reproducible representation-fidelity and provenance audit, not an expert-graded semantic accuracy study. Frozen 208 assertions across four evidence channels; authentic official pySHACL CI evidence preserved.</p></header>
<main><nav><button class="tab active" data-tab="overview">Overview</button><button class="tab" data-tab="assertions">Assertion audit</button><button class="tab" data-tab="clinical">Clinical context</button><button class="tab" data-tab="development">Development queries</button><button class="tab" data-tab="limitations">Scientific gates</button></nav>
<section id="overview" class="active"><div id="metrics" class="layout"></div><div class="panel"><h2>Recovered fields by RDF model</h2><div class="tablewrap"><table id="modeltable"></table></div><h3>Provenance recoverability (of 208)</h3><div id="bars"></div><p class="muted">Changes in retained fields are directly caused by what each representation stores. Do not interpret these ratios as predictive performance.</p></div></section>
<section id="assertions"><div class="panel"><h2>Original assertion-by-model matrix</h2><p class="muted">Each source assertion appears once per representation. Search by ID or evidence channel; filter by model.</p><label>Model: <select id="model"><option value="all">All</option><option>M1</option><option>M2</option><option>M3</option></select></label> &nbsp;<label>Search: <input id="q" placeholder="Assertion ID or channel" autocomplete="off"></label><p class="muted" id="nrecords"></p><div class="tablewrap"><table id="audittable"></table></div></div></section>
<section id="clinical"><div class="panel"><h2>Clinical evidence context-variation review queue</h2><p class="muted">These are candidate differences. No clinical contradiction has been adjudicated and absence of source verification does not establish falsehood.</p><div class="tablewrap"><table id="clinicaltable"></table></div></div></section>
<section id="development"><div class="panel"><h2>Eight development competency questions, 24 model-specific outputs</h2><p class="muted">Development-only diagnostics — not independent expert-gold answer accuracy.</p><div class="tablewrap"><table id="devtable"></table></div></div></section>
<section id="limitations"><div class="panel"><h2>Validation boundaries</h2><p><strong>Structural SHACL Core:</strong> PASS with official pySHACL 0.40.2, zero violations, 10/10 seeded negative controls.</p><p><strong>Expert gold:</strong> 0/45 independently adjudicated cases. Confirmatory semantic accuracy NOT MEASURED.</p><p><strong>Clinical canonical IDs:</strong> 7 original clinical object IDs missing, preserved as text with explicit flags.</p><p><strong>Source verification:</strong> source references are not equivalent to independent verification of 100 chemical assertions.</p><p><strong>Material ontology:</strong> plant part, dose, preparation and assay context not completely normalized.</p><p><strong>M1–M3 comparison:</strong> representation capabilities by design; no statistical superiority inference.</p><p><a href="https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018">Official SHACL CI evidence</a></p></div></section>
<footer>Source: frozen P3 V3 data, SHA-256 59f91465413937b2ecbd58d8726fd691f965db76fa8377026933169fbb081774. Author-review technical research.</footer></main>
<script>const DATA=__DATA__;
function safe(v){return String(v??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');}
function table(id,rows,cols){let h='<thead><tr>'+cols.map(c=>'<th>'+safe(c[1])+'</th>').join('')+'</tr></thead><tbody>';h+=rows.map(r=>'<tr>'+cols.map(c=>'<td>'+safe(r[c[0]])+'</td>').join('')+'</tr>').join('')+'</tbody>';document.getElementById(id).innerHTML=h;}
document.getElementById('metrics').innerHTML=[['Assertions',208],['Source IDs',45],['M3 triples',2733],['Clinical review groups',3],['Expert gold',0]].map(x=>'<div class="panel metric"><strong>'+x[1]+'</strong><span>'+x[0]+'</span></div>').join('');
const mods=DATA.models;
table('modeltable',mods,[['model','Model'],['rdf_triples','Triples'],['edge_recoverable','Relations'],['id','IDs'],['provenance','Source'],['evidence_mode','Mode'],['directness','Directness'],['context','Context']]);
document.getElementById('bars').innerHTML=mods.map(m=>'<div class="barrow"><span class="barlabel">'+m.model+'</span><div class="track"><div class="fill" style="width:'+(100*Number(m.provenance)/208)+'%"></div></div><span class="val">'+m.provenance+'/208</span></div>').join('');
function audit(){const m=document.getElementById('model').value;const q=document.getElementById('q').value.toLowerCase().trim();const x=DATA.assertions.filter(a=>(m==='all'||a.model===m)&&(!q||(a.assertion_id+' '+a.channel).toLowerCase().includes(q)));document.getElementById('nrecords').textContent='Showing '+x.length+' of '+DATA.assertions.length+' records';table('audittable',x.slice(0,624),[['assertion_id','Assertion'],['channel','Channel'],['model','Model'],['edge_recoverable','Relation'],['id','ID'],['provenance','Source'],['evidence_mode','Mode'],['directness','Directness'],['context','Context']]);}
document.getElementById('q').addEventListener('input',audit);document.getElementById('model').addEventListener('change',audit);audit();
table('clinicaltable',DATA.clinical,[['subject_id','Herb'],['topic','Clinical topic'],['assertion_ids','Assertion IDs'],['n_distinct_sources','Sources'],['directions','Divergent annotations'],['independent_adjudication','Gold status']]);
table('devtable',DATA.development,[['case_id','Case'],['category','Category'],['model','Model'],['query_status','Archived status'],['edge_count','Edges'],['citations_from_rdf','Sources']]);
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('section').forEach(s=>s.classList.toggle('active',s.id===b.dataset.tab));}));
</script></body></html>'''.replace('__DATA__',js)
(OUT/'ThaiHerb_Paper3_EvidenceKG_Research_Explorer.html').write_text(html,encoding='utf-8')
print('Built',len(html),'characters')
