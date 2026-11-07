"""Forbid independent accuracy claims until real independent reviewers adjudicate.

Human identities and adjudication records must be added explicitly by the study
team. No development candidate or post-hoc source panel may pass this gate.
"""
import csv, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def score_allowed(path):
    with open(path,encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    if not rows:return {'score_allowed':False,'reason':'EMPTY_GOLD'}
    missing=[]
    for row in rows:
        fields=('reviewer1_name','reviewer1_score','reviewer1_signature','reviewer2_name','reviewer2_score','reviewer2_signature','adjudicator_name','adjudicated_gold','adjudication_date')
        if any(not row.get(f,'').strip() for f in fields):missing.append(row['case_id'])
        elif row['reviewer1_name']==row['reviewer2_name']:missing.append(row['case_id'])
        elif row.get('stratum','')!='PROSPECTIVE_INDEPENDENT_HELDOUT':missing.append(row['case_id'])
    return {'score_allowed':len(missing)==0,'records':len(rows),'blocked_cases':missing,
            'reason':'NOT_INDEPENDENTLY_ADJUDICATED_OR_DEVELOPMENT_ONLY' if missing else 'REQUIRES_HUMAN_IDENTITY_VERIFICATION_BEFORE_RELEASE'}
if __name__=='__main__':
    print(json.dumps(score_allowed(ROOT/'results/P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv'),indent=2))
