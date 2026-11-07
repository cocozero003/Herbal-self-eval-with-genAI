"""Build a single-file offline evidence integrity and RDF projection explorer."""
from pathlib import Path
import json
import csv
from html import escape

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'
OUTPUT=ROOT/'dashboard/ThaiHerb_EvidenceAndRepresentation_v10_v08.html'

def read(name):
    with (RESULTS/name).open(newline='',encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def build():
    blocks={
        'claims':read('P2_ALL_CLAIMS_AUDIT_LEDGER_100_v10.csv'),
        'new':read('P2_ADDITIONAL_PRIMARY_CORROBORATION_5_v10.csv'),
        'context':read('P2_SOURCE_CONTEXT_WARNINGS_PLUMBAGO_5_v10.csv'),
        'retention':read('P3_RDF_CAPABILITY_SUMMARY_v08.csv'),
        'collisions':read('P3_SPO_COLLISION_GROUPS_v08.csv'),
        'cases':read('P3_EXPERT_REVIEW_READY_UNFILLED_32_v08.csv'),
    }
    status=json.loads((RESULTS/'P2_P3_V10_V08_STATUS.json').read_text(encoding='utf-8'))
    data=json.dumps({'blocks':blocks,'status':status},ensure_ascii=False).replace('</','<\\/')
    html='''<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ThaiHerb Evidence Audit | Paper 2 v1.0 & Paper 3 v0.8</title>
<style>
:root{font-family:Inter,system-ui,'Noto Sans Thai',sans-serif;color:#1c2832;background:#f5f8f9}*{box-sizing:border-box}body{margin:0}header{background:#102a35;color:#fff;padding:32px max(24px,calc((100vw - 1240px)/2))}h1{font-size:clamp(24px,3vw,35px);margin:5px 0 10px}h2{font-size:19px;margin:8px 0 15px}p{line-height:1.6}.sub{color:#b8cbd2;font-size:14px}main{max-width:1240px;margin:22px auto;padding:0 18px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0}.metric{background:white;border:1px solid #dde6e9;border-radius:13px;padding:19px}.num{font-size:29px;font-weight:750;color:#167c7a}.metric small{color:#647780}nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}nav button{background:#fff;border:1px solid #cad8dd;padding:10px 15px;color:#304854;border-radius:9px;cursor:pointer;font-size:14px}nav button.sel{background:#145b65;color:white;border-color:#145b65}.panel{display:none;background:white;border:1px solid #dfe8eb;border-radius:14px;padding:22px;margin:12px 0 24px}.panel.on{display:block}.note{font-size:13px;color:#55707b;background:#eff6f8;border-left:3px solid #5c8d9d;padding:10px 15px;margin:16px 0}.warning{background:#fff6ef;border-color:#d18b52;color:#7c4622}.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}.toolbar input,.toolbar select{border-radius:8px;border:1px solid #bacbd1;background:#fff;padding:10px 12px;font-size:14px;min-width:190px}table{border-collapse:collapse;width:100%;font-size:12.5px}thead{position:sticky;top:0;background:#edf4f6}th,td{text-align:left;padding:11px;border-bottom:1px solid #e7eef0;vertical-align:top;overflow-wrap:anywhere}th{font-size:12px;color:#315362}.tablewrap{overflow:auto;max-height:630px;border:1px solid #e4e9ec;border-radius:9px}a{color:#126c89}footer{color:#698087;font-size:12px;padding:20px 0 45px}.caption{color:#66808a;font-size:12px}pre{overflow:auto;white-space:pre-wrap;background:#f4f6f7;padding:10px;border-radius:7px}@media(max-width:760px){.metrics{grid-template-columns:repeat(2,1fr)}header{padding:25px 20px}.panel{padding:15px}}
</style></head><body>
<header><div class="sub">Thai Herbal Knowledge Graph | Research engineering release | 7 November 2026</div><h1>Evidence integrity & representation audit</h1><div class="sub">Paper 2 v1.0 / Paper 3 v0.8 · Source-specific corroboration and 208-assertion RDF retention</div></header>
<main><section class="metrics"><div class="metric"><div class="num">100</div><small>Original chemical assertions</small></div><div class="metric"><div class="num">9</div><small>Claims with separate corroboration (4 prior + 5 new)</small></div><div class="metric"><div class="num">624</div><small>Representation audit rows</small></div><div class="metric"><div class="num">0</div><small>Independent expert gold cases</small></div></section>
<div class="note warning"><strong>Scientific boundary.</strong> Only 5 of the original-source chemical assertions have source-specific PRIMARY_FULLTEXT_MATCH status. Nine independent-source corroborations do not validate the original citations or constitute a prespecified external benchmark. The 0/208 and 208/208 comparison measures RDF field retention, NOT answer correctness. pySHACL Core NOT RUN.</div>
<nav aria-label="Dashboard sections"><button class="sel" data-tab="claims">Claim ledger</button><button data-tab="new">New primary source</button><button data-tab="context">Context warnings</button><button data-tab="retention">RDF retention</button><button data-tab="cases">Expert review queue</button></nav>
<section class="panel on" id="claims"><h2>Herb-compound assertions: original source remains immutable</h2><p>Filter all 100 claims by herb, compound, source ID or archived source status.</p><div class="toolbar"><input id="qclaims" aria-label="Search claims" placeholder="Search herb, compound or source"><select id="fclaims" aria-label="Filter corroboration"><option value="all">All claims</option><option value="new">New corroboration</option><option value="previous">Prior corroboration</option><option value="none">No corroboration</option></select></div><div class="tablewrap"><table id="tclaims"></table></div><p class="caption" id="nclaims"></p></section>
<section class="panel" id="new"><h2>Primary analytical corroboration: commercial coriander fruit essential oil</h2><p>Satyal & Setzer (2020), <a target="_blank" rel="noopener noreferrer" href="https://doi.org/10.1177/1934578X20933067">DOI 10.1177/1934578X20933067</a>. The percentage ratios for terpinen-4-ol represent <b>enantiomer fractions</b>, not compound abundance. No clinical inference.</p><div class="tablewrap"><table id="tnew"></table></div></section>
<section class="panel" id="context"><h2>Source context risk: Plumbago indica</h2><p>Original 2022 article introduction discusses prior literature. Table 1 original LC-MS/MS requires additional claim-by-claim checking; the source is not blanket proof that every archived compound was measured in that experiment.</p><div class="tablewrap"><table id="tcontext"></table></div></section>
<section class="panel" id="retention"><h2>Deterministic RDF representation capabilities</h2><p>All models receive the same frozen 208 assertions. Structural property counts are not accuracy, usefulness, or medical validity.</p><div class="tablewrap"><table id="tretention"></table></div><div class="note"><strong>SPO collisions:</strong> One duplicate triple maps CLIN005 and CLIN006 into the same M1 SPO. M2 and M3 preserve both assertion identities with their sources. M3 also explicitly flags seven clinical claims lacking canonical outcome IDs.</div></section>
<section class="panel" id="cases"><h2>32 development competency questions</h2><p>Questions remain without two independent human ratings or adjudication. Confirmation metrics are not available.</p><div class="toolbar"><input id="qcases" aria-label="Search competency questions" placeholder="Search questions and categories"></div><div class="tablewrap"><table id="tcases"></table></div><div class="note warning">SHACL Core requires actual pySHACL execution on the frozen graph. No conformity report is claimed by this dashboard.</div></section>
<footer>Offline HTML; reads embedded audit tables only. No network request or automatic modification of source data. Source citations, frozen manifests and code are distributed in the reproducibility ZIP.</footer></main>
<script id="audit-data" type="application/json">__DATA__</script><script>
const DB=JSON.parse(document.getElementById('audit-data').textContent);
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function render(id,items,cols){let el=document.getElementById(id);el.innerHTML='<thead><tr>'+cols.map(x=>'<th>'+esc(x[1])+'</th>').join('')+'</tr></thead><tbody>'+items.map(row=>'<tr>'+cols.map(x=>'<td>'+esc(row[x[0]])+'</td>').join('')+'</tr>').join('')+'</tbody>';}
const cs=DB.blocks.claims;
const colsClaims=[['assertion_id','ID'],['herb','Species'],['compound','Compound'],['original_source_id','Original source'],['original_source_disposition','Original status'],['prior_additional_corrob','Prior independent'],['new_additional_corrob','New independent'],['human_gold','Gold']];
function refreshClaims(){let needle=document.getElementById('qclaims').value.toLowerCase();let mode=document.getElementById('fclaims').value;let selected=cs.filter(r=>Object.values(r).join(' ').toLowerCase().includes(needle)&& (mode==='all'||(mode==='new'&&r.new_additional_corrob==='1')||(mode==='previous'&&r.prior_additional_corrob==='1')||(mode==='none'&&r.new_additional_corrob==='0'&&r.prior_additional_corrob==='0')));render('tclaims',selected,colsClaims);document.getElementById('nclaims').textContent=selected.length+' of '+cs.length+' claims';}
render('tnew',DB.blocks.new,[['assertion_id','ID'],['compound','Compound'],['exact_source_locator','Study locator'],['method','Method'],['reported_value','Value'],['units_and_denominator','Denominator'],['source_test_eligibility','Benchmark eligibility']]);
render('tcontext',DB.blocks.context,[['assertion_id','ID'],['compound','Compound'],['source_material','Material in study'],['decision','Review status'],['source_claim_warning','Reason']]);
render('tretention',DB.blocks.retention,[['model','Model'],['source_assertion_denominator','Assertions'],['rdf_triples','Triples'],['individual_assertion_id_recoverable','IDs'],['source_id_traceable','Sources'],['evidence_mode_recoverable','Evidence mode'],['directness_recoverable','Directness'],['source_context_text_recoverable','Context'],['clinical_missing_canonical_id_flag','Uncanonicalized clinical IDs']]);
let caseCols=[['case_id','ID'],['category','Category'],['question','Question'],['eligible_for_blind_scoring','Eligible'],['independent_gold_available','Gold available']];
function refreshCases(){const needle=document.getElementById('qcases').value.toLowerCase();render('tcases',DB.blocks.cases.filter(x=>Object.values(x).join(' ').toLowerCase().includes(needle)),caseCols);}
for (let b of document.querySelectorAll('nav button')) b.addEventListener('click',()=>{document.querySelectorAll('nav button').forEach(x=>x.classList.remove('sel'));document.querySelectorAll('.panel').forEach(x=>x.classList.remove('on'));b.classList.add('sel');document.getElementById(b.dataset.tab).classList.add('on');});
document.getElementById('qclaims').addEventListener('input',refreshClaims);document.getElementById('fclaims').addEventListener('change',refreshClaims);document.getElementById('qcases').addEventListener('input',refreshCases);refreshClaims();refreshCases();
</script></body></html>'''
    OUTPUT.write_text(html.replace('__DATA__',data),encoding='utf-8')
    return {'dashboard':str(OUTPUT),'bytes':OUTPUT.stat().st_size,'blocks':{k:len(v) for k,v in blocks.items()}}

if __name__=='__main__':
    print(json.dumps(build(),indent=2))
