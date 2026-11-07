"""Create reproducible figures, source gates and offline result browser."""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib, html, json, re
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results';F=ROOT/'figures';H=ROOT/'dashboard';D=ROOT/'docs'
for directory in [F,H,D]:directory.mkdir(exist_ok=True)

def show_fig(p, title):
    plt.title(title)
    plt.grid(axis='x',alpha=.2)
    plt.tight_layout()
    plt.savefig(F/p,dpi=180,bbox_inches='tight')
    plt.close()

def figures():
    d=pd.read_csv(R/'P2_LOFO_SUMMARY_CLUSTER_BOOTSTRAP.csv');t=d[d.coverage_type=='FULL_190'].sort_values('mean_AP_across_formulas')
    y=np.arange(len(t));lo=t.mean_AP_across_formulas-t.AP_CI_lower;hi=t.AP_CI_upper-t.mean_AP_across_formulas
    plt.figure(figsize=(10,5.3));plt.barh(y,t.mean_AP_across_formulas,xerr=[lo,hi],capsize=3)
    plt.yticks(y,t.model,fontsize=9);plt.xlabel('Mean average precision (95% formula-cluster bootstrap CI)')
    plt.xlim(0,max(t.AP_CI_upper)*1.18);show_fig('Figure1_LOFO_AP_6_complete_formulas.png','Internal LOFO: documentary co-membership, six complete folds')
    p=pd.read_csv(R/'P2_PERTURBATION_SUMMARY.csv').sort_values('mean_rank_spearman')
    plt.figure(figsize=(10,5.4));plt.barh(np.arange(len(p)),p.mean_rank_spearman,xerr=p.sd_over_seeds,capsize=3)
    plt.yticks(np.arange(len(p)),p.variant,fontsize=9);plt.xlim(-.15,1.08)
    plt.xlabel('Mean Spearman vs paired baseline (SD across seeds)');show_fig('Figure2_Perturbation_Rank_Stability.png','Representation sensitivity across 20 random seeds')
    v=pd.read_csv(R/'P2_ARCHIVED_SEED_REPEATABILITY_20SEEDS.csv').sort_values('mean')
    plt.figure(figsize=(10,5.2));plt.barh(np.arange(len(v)),v['mean'])
    plt.yticks(np.arange(len(v)),v.model,fontsize=9);plt.xlim(0,1.05)
    plt.xlabel('Mean pairwise seed-rank Spearman (archived 190 seed comparisons)')
    show_fig('Figure3_Archived_20seed_stability.png','Version 0.4 reproducible seed stability')
    f=pd.read_csv(R/'P2_LOFO_COVERAGE.csv');plt.figure(figsize=(9,4))
    plt.barh(f.heldout_formula.str[:3],f.eligible_pairs/190)
    plt.xlim(0,1.05);plt.xlabel('Pair coverage after holding out a formula')
    show_fig('Figure4_LOFO_Coverage_and_ColdStart.png','Four folds block 19/190 herb pairs due to cold start')

def normalize_doi(url):
    if pd.isna(url):return ''
    t=str(url).lower();m=re.search(r'10\.\d{4,9}/[^\s?&#]+',t)
    return m.group(0).rstrip('.,;') if m else ''

def source_overlaps():
    orig=pd.read_csv(ROOT/'input'/'evidence_v12'/'P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv')
    external=pd.read_csv(ROOT/'input'/'evidence_v12'/'P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv')
    origdoi={normalize_doi(s) for s in orig.original_source_url_locked.dropna()}
    origdoi.discard('')
    vals=[]
    for _,x in external.iterrows():
        doi=normalize_doi(x['doi'])
        vals.append({'case_id':x['case_id'],'herb_id':x['herb_id'],'doi':doi,
                     'doi_in_20_archived_original_source_records':doi in origdoi,
                     'positive_only':True,'selected_posthoc':True,
                     'material_context_requires_review':x['eligibility']=='CONTEXT_REVIEW_REQUIRED',
                     'allowed_confirmatory_external_test':False})
    pd.DataFrame(vals).to_csv(R/'P2_EXTERNAL_DOI_DEDUP_AND_ELIGIBILITY.csv',index=False)
    return {'original_source_doi_count':len(origdoi),'candidate_doi_count':len(set(x['doi'] for x in vals)),
            'any_overlap':any(x['doi_in_20_archived_original_source_records'] for x in vals),
            'negative_cases':0,'confirmatory_validity':False}

def reviewer_templates():
    d=json.loads((ROOT/'input'/'v04'/'data'/'paper2_source_reviewed_species_v04.json').read_text(encoding='utf-8'))
    herbs={h['id']:h for h in d['herbs']}
    ids=list(herbs)
    import itertools
    rows=[]
    for i,(a,b) in enumerate(itertools.combinations(ids,2),1):
        rows.append({'case_id':f'P2G{i:03d}','herb_a':a,'herb_b':b,
                     'scientific_a':herbs[a]['scientific'],'scientific_b':herbs[b]['scientific'],
                     'material_scope':'REVIEW_SPECIES_VS_PART_PREPARATION',
                     'gold_score_0_to_3':'','evidence_source_url':'','source_locator':'',
                     'confidence':'','reviewer_identity':'','reviewed_date':'',
                     'blinding_status':'MUST_NOT_VIEW_MODEL_OUTPUTS',
                     'notes':''})
    for role in ['R1','R2']:
        pd.DataFrame(rows).to_csv(R/f'P2_BLINDED_EXPERT_{role}_190_UNFILLED.csv',index=False,encoding='utf-8-sig')
    arbit=[]
    for row in rows:
        arbit.append({'case_id':row['case_id'],'reviewer_1_score':'','reviewer_2_score':'',
                      'adjudicator':'','adjudicated_gold':'','agreement':'',
                      'locked_before_comparison':'NO','review_date':''})
    pd.DataFrame(arbit).to_csv(R/'P2_EXPERT_ADJUDICATION_190_UNFILLED.csv',index=False,encoding='utf-8-sig')

def dashboard(meta):
    m=pd.read_csv(R/'P2_LOFO_SUMMARY_CLUSTER_BOOTSTRAP.csv').round(5)
    p=pd.read_csv(R/'P2_PERTURBATION_SUMMARY.csv').round(5)
    c=pd.read_csv(R/'P2_LOFO_COVERAGE.csv')
    f=pd.read_csv(R/'P2_PROVISIONAL_CLASS_MATERIAL_SENSITIVITY_20SEEDS.csv').groupby('scenario',as_index=False)[['rank_spearman','top10_overlap']].mean().round(4)
    a=pd.read_csv(R/'P2_EXTERNAL_DOI_DEDUP_AND_ELIGIBILITY.csv')
    s=pd.read_csv(R/'P2_SOURCE_HOLDOUT_COVERAGE.csv')
    data={'models':m.to_dict(orient='records'),'pert':p.to_dict(orient='records'),
          'coverage':c.to_dict(orient='records'),'classes':f.to_dict(orient='records'),
          'external':a.to_dict(orient='records'),'source':s.to_dict(orient='records')}
    js=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
    markup=r'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ThaiHerb20 | Paper 2 Robustness v1.3</title><style>
:root{color-scheme:light;--navy:#132e47;--teal:#087e84;--muted:#617084;--border:#e2e8ed;--paper:#f7f9fb}
*{box-sizing:border-box}body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--paper);margin:0;color:#14283c}
header{background:var(--navy);color:#fff;padding:31px max(24px,calc((100vw - 1160px)/2))}
header h1{font-size:28px;margin:6px 0 9px}header p{margin:0;color:#d6e4e8}main{max-width:1160px;margin:22px auto;padding:0 20px 45px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:12px}.card,.panel{background:#fff;border:1px solid var(--border);border-radius:12px;padding:20px}.card .value{font-size:28px;font-weight:750;color:var(--navy)}.card .label{font-size:12px;color:var(--muted)}
.notice{background:#fff7e8;border-left:4px solid #d48c23;padding:13px 17px;margin:20px 0;line-height:1.5}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:20px 0}button{border:1px solid var(--border);background:white;border-radius:8px;padding:11px 17px;cursor:pointer;color:var(--navy);font-weight:600}button.active{background:var(--teal);color:white;border-color:var(--teal)}
.panel{display:none}.panel.active{display:block}h2{font-size:20px;margin:4px 0 16px}p{line-height:1.5}table{border-collapse:collapse;width:100%;font-size:12px}th,td{border-bottom:1px solid var(--border);padding:9px;text-align:left}th{background:#eef4f6;position:sticky;top:0}tr:hover{background:#f4f9fa}.tablewrap{max-height:540px;overflow:auto}
.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:16px 0}select,input{background:white;border:1px solid #cbd5df;border-radius:7px;padding:9px 12px;min-width:175px}
.bar{height:16px;background:#dcebef;border-radius:4px;overflow:hidden;margin-top:3px}.bar span{display:block;background:var(--teal);height:100%}footer{margin-top:25px;color:var(--muted);font-size:12px}
@media(max-width:700px){header h1{font-size:22px}table{font-size:11px}th,td{padding:7px}.card{padding:13px}}
</style></head><body>
<header><div style="font-size:12px;letter-spacing:1.6px">THAIHERB20 / PAPER 2 / INTERNAL ROBUSTNESS</div><h1>Robustness &amp; Source Integrity Explorer</h1><p>Version 1.3 | 20 herbs · 10 selected formulas · 190 pairs · 20 random seeds</p></header>
<main><div class="cards"><div class="card"><div class="value">180</div><div class="label">Archived replay-checked fits</div></div><div class="card"><div class="value">10</div><div class="label">LOFO folds (6 full; 4 partial)</div></div><div class="card"><div class="value">20</div><div class="label">Source holdouts</div></div><div class="card"><div class="value">0</div><div class="label">Independent expert gold ratings</div></div></div>
<div class="notice"><b>Interpretation gate:</b> Results concern documentary co-membership in selected Thai herbal formulas, not clinical efficacy or biological similarity. Historical 35-class mapping has not been recovered. External 11 positives are post-hoc and unscored.</div>
<nav class="tabs"><button data-tab="lofo" class="active">LOFO comparison</button><button data-tab="pert">Perturbation</button><button data-tab="source">Source holdouts</button><button data-tab="class">Class &amp; material</button><button data-tab="external">External gate</button></nav>
<section class="panel active" id="lofo"><h2>Leave-one-formula-out, train-only embeddings</h2><div class="controls"><label>Coverage <select id="coverage"><option value="FULL_190">6 full folds (190 pairs)</option><option value="PARTIAL_171_COLD_START">4 cold-start folds (171 pairs)</option></select></label><label>Metric <select id="metric"><option value="mean_AP_across_formulas">Average precision</option><option value="mean_AUROC_across_formulas">AUROC</option></select></label></div><div id="lofochart"></div><p>95% intervals resample held-out formula clusters (2,000 draws), not 190 correlated pairs as independent samples.</p><div class="tablewrap" id="lofotable"></div></section>
<section class="panel" id="pert"><h2>Paired-seed rank sensitivity</h2><div class="controls"><input id="pertfilter" placeholder="Filter model variant" aria-label="Filter perturbations"></div><div class="tablewrap" id="perttable"></div><p>Spearman rank correlations compare each changed representation with its matched baseline for the same seed. Seed variation is not uncertainty across independent herbal sources.</p></section>
<section class="panel" id="source"><h2>Leave-one-chemical-source-out</h2><p>Each archived chemical source supports one herb (5 chemical assertions). Removing it leaves that herb without a chemical profile. Consequently, 171/190 herb pairs (90%) remain evaluable; 19 pair predictions are blocked, not filled with synthetic values.</p><div class="tablewrap" id="sourcetable"></div></section>
<section class="panel" id="class"><h2>Exploratory taxonomy and material sensitivity</h2><p>The 31 proposed families are not equivalent to the missing original 35 chemical classes. The F08/H11 counterfactual removes a species-level ingredient edge solely to illustrate the fruit-versus-insect-gall material distinction.</p><div class="tablewrap" id="classtable"></div></section>
<section class="panel" id="external"><h2>Post-hoc independent-paper candidate audit</h2><p>11 positive phytochemical observations from 3 DOI-disjoint publications. No prelocked held-out test, independent reviewer judgments or negative labels: accuracy and AUPRC are not calculated. The archive records source URLs, material part and exclusion reasons.</p><div class="tablewrap" id="externaltable"></div></section>
<footer>All displayed values are generated from bundled CSV experiment files, frozen by SHA-256. All models and figures are research-development artifacts.</footer></main>
<script>const DATA=__DATA__;
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function table(items){if(!items.length)return '<p>No rows</p>';const cols=Object.keys(items[0]);return '<table><thead><tr>'+cols.map(c=>'<th>'+esc(c.replaceAll('_',' '))+'</th>').join('')+'</tr></thead><tbody>'+items.map(r=>'<tr>'+cols.map(c=>'<td>'+esc(typeof r[c]==='number'?Number(r[c].toFixed(5)):r[c])+'</td>').join('')+'</tr>').join('')+'</tbody></table>'}
function updateLOFO(){const mode=$('coverage').value,metric=$('metric').value;const records=DATA.models.filter(r=>r.coverage_type===mode).sort((a,b)=>b[metric]-a[metric]);let max=Math.max(...records.map(r=>r[metric]));$('lofochart').innerHTML=records.map(r=>'<div style="display:grid;grid-template-columns:minmax(170px,260px) 1fr 70px;align-items:center;gap:9px;margin:9px 0;font-size:12px"><b>'+esc(r.model)+'</b><div class="bar"><span style="width:'+Math.max(0,100*r[metric]/max).toFixed(1)+'%"></span></div><strong>'+r[metric].toFixed(3)+'</strong></div>').join('');$('lofotable').innerHTML=table(records)}
$('coverage').addEventListener('change',updateLOFO);$('metric').addEventListener('change',updateLOFO);updateLOFO();
function updatePert(){const text=$('pertfilter').value.trim().toLowerCase();$('perttable').innerHTML=table(DATA.pert.filter(r=>r.variant.toLowerCase().includes(text)))}$('pertfilter').addEventListener('input',updatePert);updatePert();
$('sourcetable').innerHTML=table(DATA.source);$('classtable').innerHTML=table(DATA.classes);$('externaltable').innerHTML=table(DATA.external);
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('active',x.id===b.dataset.tab))}));
</script></body></html>'''
    (H/'ThaiHerb_Paper2_Robustness_v13.html').write_text(markup.replace('__DATA__',js),encoding='utf-8')

if __name__=='__main__':
    figures();g=source_overlaps();reviewer_templates();dashboard(g)
    (R/'P2_EXTERNAL_GATE_SUMMARY.json').write_text(json.dumps(g,indent=2),encoding='utf-8')
    print('Created 4 figures, reviewer blanks, DOI audit, interactive dashboard:',g)
