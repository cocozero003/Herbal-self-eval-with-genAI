"""Create genuine score-blinded cases for TWO reviewers; never synthesize their labels."""
import csv,hashlib,itertools,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';OUT=ROOT/'results'
d=json.loads((DATA/'paper1_bootstrap_v3_proxy.json').read_text(encoding='utf-8'))
herbs={h['id']:h for h in d['herbs']}
pairs=list(itertools.combinations(sorted(herbs),2))
assert len(pairs)==45
rows=[]
for a,b in pairs:
    caseid='P1-'+hashlib.sha256(('P1-v07-case-salt-20261107|'+a+'|'+b).encode()).hexdigest()[:12].upper()
    rows.append({'case_id':caseid,'herb_a_id':a,'herb_b_id':b,'herb_a_th':herbs[a]['thai'], 'herb_b_th':herbs[b]['thai'],
                 'herb_a_scientific':herbs[a]['scientific'],'herb_b_scientific':herbs[b]['scientific']})
assert len({r['case_id'] for r in rows})==45

def write(name,arr):
 with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)

# Reviewer spreadsheets contain NO model scores, NPMI, experimental ranks, or heldout outcome labels.
for reviewer in ('R1','R2'):
    x=rows.copy()
    random.Random(4101 if reviewer=='R1' else 4202).shuffle(x)
    records=[{**r,'reviewer_id':reviewer,'chemistry_similarity_grade_0_1_2_or_NA':'',
      'formula_context_similarity_grade_0_1_2_or_NA':'',
      'evidence_primary_url':'','evidence_page_section_table':'',
      'independent_of_paper1_training_sources_Y_N_U':'',
      'matched_botanical_part_preparation_Y_N_U':'',
      'rater_confidence_low_moderate_high':'','rater_notes':''} for r in x]
    write('BLINDED_EXPERT_'+reviewer+'_45.csv',records)
write('CASE_KEY_INTERNAL_45.csv',rows)
write('ADJUDICATION_TEMPLATE_45.csv',[{'case_id':r['case_id'],'expert1_chemistry':'','expert2_chemistry':'',
 'adjudicated_chemistry_0_1_2_or_NA':'','expert1_formula_context':'','expert2_formula_context':'',
 'adjudicated_formula_context_0_1_2_or_NA':'','adjudicator_comment':'','evidence_url':'','evidence_locator':'',
 'source_independence_accepted_Y_N_U':'','independent_expert_validation_completed':'NO'} for r in rows])
(OUT/'expert_benchmark_status.json').write_text(json.dumps({'cases':45,'reviewers_required':2,'blind_to_model_scores':True,
 'reviewer_labels_populated':False,'adjudicated_labels_populated':False,'independent_gold_available':False,
 'reviewer_identity_or_credentials_provided':False,'evaluation_blocked_without_genuine_labels':True},indent=2),encoding='utf-8')
print('Generated 2 blinded forms, case key and blank adjudication for',len(rows),'dyads')