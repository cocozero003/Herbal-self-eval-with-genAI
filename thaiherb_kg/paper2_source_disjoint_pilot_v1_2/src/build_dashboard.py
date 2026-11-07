"""Create a fully offline research evidence dashboard; nothing simulated as PASS."""
import csv,json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'results'

def rows(n):
    with open(DATA/n,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

claims=rows('P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv')
external=rows('P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv')
taxonomy=rows('P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv')
sources=rows('P2_EXTERNAL_SOURCE_REGISTRY_V12.csv')
review=rows('P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv')
shacl_runtime=json.loads((DATA/'P3_PYSHACL_CORE_RUNTIME.json').read_text(encoding='utf-8'))
shacl_ok=(shacl_runtime.get('status')=='PASS' and shacl_runtime.get('baseline_conforms') is True and shacl_runtime.get('negative_controls_detected')==10)
shacl_status=('PASS / official pySHACL '+str(shacl_runtime.get('engine_version','')) if shacl_ok else 'NOT VERIFIED')

css="""
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:#172334;background:#f6f8fa}
*{box-sizing:border-box}body{margin:0}header{padding:26px 5%;background:#142d45;color:#fff}
header h1{font-size:25px;margin:0 0 9px} header p{opacity:.9;margin:0}
main{max-width:1260px;margin:auto;padding:22px 18px}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:12px}
.metric{background:#fff;border:1px solid #dfe6ed;border-radius:10px;padding:16px}
.metric b{display:block;font-size:25px;color:#243f67}.metric small{font-size:12px;color:#4e5d71}
nav{display:flex;gap:7px;overflow-x:auto;margin:18px 0;flex-wrap:wrap}
nav button{background:#fff;color:#233a50;border:1px solid #cad6e1;border-radius:7px;padding:10px 13px;cursor:pointer}
nav button.active{background:#233e5c;color:#fff}
section{display:none;background:#fff;border:1px solid #d9e4eb;border-radius:10px;padding:18px;margin-bottom:18px}
section.active{display:block}.filter{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
input,select{padding:9px;border:1px solid #bccbd7;border-radius:6px;min-width:160px}
.tablewrap{width:100%;overflow:auto;max-height:550px;border:1px solid #e1e7ed}
table{border-collapse:collapse;width:100%;font-size:13px}th{position:sticky;top:0;background:#e8eff5;text-align:left;z-index:1}
th,td{padding:9px 10px;border-bottom:1px solid #edf0f4;vertical-align:top;white-space:normal;max-width:360px}
tr:nth-child(even){background:#f8fafc}a{color:#265b88;overflow-wrap:anywhere}.note{background:#f2f5f9;padding:13px;border-left:3px solid #5c7d9f;margin:13px 0;line-height:1.5}
.pass{color:#237343}.blocked{color:#9d4d20}.nowrap{white-space:nowrap}
"""
js="""
const sourceData = __DATA__;
const views = [
 ['claims',['assertion_id','herb_id','compound_locked','original_source_claim_screen_grade','new_source_id_pipe','original_source_url_locked']],
 ['external',['case_id','scientific_name','compound','plant_part','reported_peak_area_percent','source_id','eligibility','source_url']],
 ['taxonomy',['archive_compound_label','reconstructed_family_id','status','original_35class_recovered','postprocessing_context']],
 ['sources',['source_id','doi','study_class','part','assay','prior_development_overlap','primary_eligible','url']],
 ['review',['case_id','stratum','question','source_disjoint','benchmark_ready','reason']]
];
function el(tag, attrs, content){const e=document.createElement(tag);for(const [k,v] of Object.entries(attrs||{})){if(k==='class')e.className=v;else e.setAttribute(k,v);}if(content!=null)e.textContent=String(content);return e;}
function tableFor(key){const spec=views.find(v=>v[0]===key);const fields=spec[1];const rows=sourceData[key];const search=document.getElementById('search-'+key).value.toLowerCase();const status=document.getElementById('status-'+key)?.value||'';const target=document.getElementById('count-'+key);const list=rows.filter(row=>(!search||JSON.stringify(row).toLowerCase().includes(search))&&(!status||JSON.stringify(row).includes(status)));
 target.textContent=list.length+' / '+rows.length+' records';let table=document.createElement('table'),head=document.createElement('thead'),tr=document.createElement('tr');fields.forEach(f=>tr.appendChild(el('th',{},f)));head.appendChild(tr);table.appendChild(head);let tbody=document.createElement('tbody');list.slice(0,500).forEach(row=>{let r=document.createElement('tr');fields.forEach(f=>{let td=document.createElement('td');let value=row[f]||'';if(f.endsWith('_url_locked')||f==='source_url'||f==='url'){if(value.startsWith('https://')){let a=el('a',{href:value,target:'_blank',rel:'noopener noreferrer'},value);td.appendChild(a);}else td.textContent=value;}else td.textContent=value;r.appendChild(td);});tbody.appendChild(r);});table.appendChild(tbody);const container=document.getElementById('table-'+key);container.replaceChildren(table);}
function openTab(key){document.querySelectorAll('section').forEach(e=>e.classList.toggle('active',e.id===key));document.querySelectorAll('nav button').forEach(e=>e.classList.toggle('active',e.dataset.tab===key));for(const [v] of views){if(v===key)tableFor(key);}}
for(const [key,fields] of views){const div=document.getElementById('table-'+key);document.getElementById('search-'+key).addEventListener('input',()=>tableFor(key));}
document.querySelectorAll('nav button').forEach(b=>b.addEventListener('click',()=>openTab(b.dataset.tab)));openTab('claims');
"""

panels=[]
for key,title,description in [
('claims','100 original-source claims','Original-source status is never promoted by later evidence.'),
('external','11 post-hoc GC-MS pilot observations','Positive-only source-specific records; not independent scientific accuracy.'),
('taxonomy','83 compounds / 31 proposed chemical families','New preliminary assignment, not the unrecovered historical 35 classes.'),
('sources','External source registry and exclusions','Previously used coriander publication excluded from independent validation.'),
('review','45 unfilled independent reviewer candidates','Expert reviewer and adjudicated gold cells are blank.')]:
    panels.append(f'<section id="{key}"><h2>{html.escape(title)}</h2><p>{html.escape(description)}</p><div class="filter"><input id="search-{key}" aria-label="Filter {key}" placeholder="Filter by name, ID, source"><span id="count-{key}"></span></div><div class="tablewrap" id="table-{key}"></div></section>')

payload=json.dumps(dict(claims=claims,external=external,taxonomy=taxonomy,sources=sources,review=review),ensure_ascii=False).replace('</','<\\/')
page='''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ThaiHerb KG v1.2/v1.0 Evidence Integrity</title><style>'''+css+'''</style></head><body><header><h1>ThaiHerb KG — Source Integrity and Validation Gates</h1><p>Paper 2 v1.2 / Paper 3 v1.0. Research evidence audit, not a clinical recommendation.</p></header><main><div class="metrics"><div class="metric"><b>100</b><small>Original chemistry claims</small></div><div class="metric"><b>5</b><small>Original source primary full-text matches</small></div><div class="metric"><b>11</b><small>Post-hoc external analyte observations</small></div><div class="metric"><b>83 / 31</b><small>Compound labels / candidate families</small></div><div class="metric"><b>0</b><small>Independent adjudicated gold cases</small></div><div class="metric"><b>{html.escape(shacl_status)}</b><small>Authentic pySHACL Core project profile</small></div></div><div class="note"><b>Release gates:</b> Original 35-class archive not recovered. Human independent gold pending. SHACL Core status derives from actual GitHub Actions log and downloaded artifact: <a href="https://github.com/cocozero003/Herbal-self-eval-with-genAI/actions/runs/42362561018" target="_blank" rel="noopener noreferrer">verified workflow run</a>. Positive-only data is not an accuracy benchmark.</div><nav>'''+''.join(f'<button data-tab="{k}">{k.title()}</button>' for k in ['claims','external','taxonomy','sources','review'])+'''</nav>'''+''.join(panels)+'''<p><small>All source URLs are public. The original 208-assertion V3 input was not altered. No reviewer labels were generated.</small></p></main><script>'''+js.replace('__DATA__',payload)+'''</script></body></html>'''
page=page.replace('{html.escape(shacl_status)}',html.escape(shacl_status))
result=ROOT/'dashboard/ThaiHerb_EvidenceAndValidation_v12_v10.html'
result.parent.mkdir(exist_ok=True)
result.write_text(page,encoding='utf-8')
print(result, result.stat().st_size)
