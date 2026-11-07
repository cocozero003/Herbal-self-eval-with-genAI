"""Paper 1 primary-source integrity review and bounded counterfactual impact test.

Primary bibliography: DTAM/Thai FDA B.E. 2566 formula compendium.
Full PDF not bundled; official source URL and reviewed PDF page locators recorded.
This file NEVER labels partially reviewed data as completely verified.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
import math
import statistics
from copy import deepcopy
from datetime import date
from pathlib import Path

PUBLIC_PDF = 'https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf'
FROZEN_REVIEW_DATE = '2026-11-07'
# Compendium table-of-contents mapping; PDF index = printed page + 8 (directly checked on pp.1, 143, 161).
FORMULA_CROSSWALK = [
    ('F01_DTAM2566', 'ยาธาตุบรรจบ', 'ชนิดผง', 1, 'formula_membership_checked'),
    ('F02_DTAM2566', 'ยาประสะกะเพรา', 'ชนิดผง', 27, 'toc_only'),
    ('F03_DTAM2566', 'ยาไฟประลัยกัลป์', 'ชนิดผง', 122, 'toc_and_body_name_variant'),
    ('F04_DTAM2566', 'ยาประสะไพล', 'ชนิดผง', 143, 'formula_membership_checked'),
    ('F05_DTAM2566', 'ยาประสะว่านนางคำ', 'ชนิดผง', 161, 'formula_membership_checked_discrepancy'),
    ('F06_DTAM2566', 'ยาปลูกไฟธาตุ', 'ชนิดแคปซูล', 164, 'toc_only'),
    ('F07_DTAM2566', 'ยาแก้ไอ ขับเสมหะ สูตร 2', 'ชนิดผง', 240, 'toc_only'),
    ('F08_DTAM2566', 'ยามหาจักรใหญ่', 'ชนิดผง', 49, 'toc_only'),
    ('F09_DTAM2566', 'ยาวิสัมพยาใหญ่', 'ชนิดผง', 71, 'toc_only'),
    ('F10_DTAM2566', 'ยาทาพระเส้น', 'ชนิดผง', 386, 'toc_only'),
]
# Only instances directly reviewed against displayed original source tables.
# Document pages are not the same as displayed PDF pages; page printed +8 = PDF zero-index.
CHECKED_FORMULA_MEMBERS = {
 ('F01_DTAM2566','H01'):(True,2,'source body table, entry 10, ginger'),
 ('F01_DTAM2566','H02'):(True,2,'source body table, entry 12, Java long pepper'),
 ('F01_DTAM2566','H09'):(True,1,'source body table, entry 4, clove'),
 ('F04_DTAM2566','H05'):(True,143,'source body table, entry 1, plai'),
 ('F04_DTAM2566','H04'):(True,143,'source body table, entry 2, garlic'),
 ('F04_DTAM2566','H01'):(True,143,'source body table, entry 5, ginger'),
 ('F04_DTAM2566','H02'):(True,143,'source body table, entry 6, Java long pepper'),
 ('F04_DTAM2566','H03'):(True,143,'source body table, entry 8, black pepper'),
 ('F04_DTAM2566','H10'):(True,143,'source body table, entry 9, kaffir lime'),
 ('F05_DTAM2566','H05'):(True,161,'source body table, entry 4, plai'),
 ('F05_DTAM2566','H10'):(True,161,'source body table, entry 5, kaffir lime'),
 ('F05_DTAM2566','H01'):(False,161,'not in complete ingredient table, ginger'),
 ('F05_DTAM2566','H02'):(False,161,'not in complete ingredient table, Java long pepper'),
 ('F05_DTAM2566','H03'):(False,161,'not in complete ingredient table, black pepper'),
}
SEEDS = [11,23,37,41,53,67,79,83,97,101]
METHODS = ['original_npmi','support_k2','degree_05','combined']


def sha256(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def csv_write(path,rows,fields=None):
    if not rows:return
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=fields or list(rows[0]));writer.writeheader();writer.writerows(rows)


def npmi(formulas, ids):
    n=len(formulas)
    members={i:{f['id'] for f in formulas if i in f['herbs']} for i in ids}
    out={}
    for a,b in itertools.combinations(ids,2):
        support=len(members[a] & members[b])
        x=0.
        if support>0 and support<n and members[a] and members[b]:
            p=support/n
            x=math.log(p/((len(members[a])/n)*(len(members[b])/n)))/-math.log(p)
        out[(a,b)]=(support,x,max(0.,x))
    return out


def rank(values):
    pairs=sorted(enumerate(values), key=lambda x:x[1]);r=[0.]*len(values);n=len(values);i=0
    while i<n:
        j=i+1
        while j<n and pairs[j][1]==pairs[i][1]:j+=1
        avg=(i+1+j)/2
        for k in range(i,j):r[pairs[k][0]]=avg
        i=j
    return r


def spearman(x,y):
    if len(x)!=len(y) or len(x)<2:return None
    rx,ry=rank(x),rank(y)
    mx,my=statistics.mean(rx),statistics.mean(ry)
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
    return num/den if den else None


def weights(npmi_data,method):
    deg={n:sum(z[2]>0 and n in pair for pair,z in npmi_data.items()) for p in npmi_data for n in p}
    out={}
    for (a,b), (support,raw,positive) in npmi_data.items():
        val=positive
        if positive>0 and method in ('support_k2','combined'):val*=support/(support+2.)
        if positive>0 and method in ('degree_05','combined'):val/=(deg[a]*deg[b])**.25
        out[(a,b)]=val
    return out


def main(data_path,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    dat=json.loads(Path(data_path).read_text(encoding='utf-8'))
    herbs=dat['herbs'];ids=[h['id'] for h in herbs];name={h['id']:h['thai'] for h in herbs}
    assert len(ids)==10 and len(dat['formulas'])==10
    crosswalk=[]
    for fid,title,form,pg,status in FORMULA_CROSSWALK:
        assert any(f['id']==fid for f in dat['formulas'])
        crosswalk.append({'formula_id':fid,'official_name':title,'dosage_form':form,'official_printed_page':pg,
                'pdf_zero_index_start_page':pg+8,'source_url':PUBLIC_PDF,
                'status':status,'verification_date':FROZEN_REVIEW_DATE,
                'note':('Contents uses variant spelling ยาไฟประสะกัลป์ while body says ยาไฟประลัยกัลป์.' if fid=='F03_DTAM2566' else '')})
    csv_write(output/'formula_id_crosswalk.csv',crosswalk)
    member_rows=[]
    for f in dat['formulas']:
        for h in f['herbs']:
            checked=CHECKED_FORMULA_MEMBERS.get((f['id'],h))
            member_rows.append({'formula_id':f['id'],'herb_id':h,'herb_name':name[h],
                'original_projection_present':1,
                'primary_source_status':('confirmed_present' if checked[0] else 'contradicted_absent') if checked else 'not_row_verified',
                'official_printed_page':checked[1] if checked else '',
                'official_pdf_zero_index':checked[1]+8 if checked else '',
                'evidence_note':checked[2] if checked else 'Membership not yet reviewed against original source table',
                'official_source_url':PUBLIC_PDF})
    csv_write(output/'formula_membership_review.csv',member_rows)
    corrected=deepcopy(dat)
    removed=[]
    for f in corrected['formulas']:
        for herb in list(f['herbs']):
            row=CHECKED_FORMULA_MEMBERS.get((f['id'],herb))
            if row and row[0] is False:
                f['herbs'].remove(herb)
                removed.append({'formula_id':f['id'],'herb_id':herb,'herb':name[herb], 'why':'ingredient absent from official printed page 161'})
    csv_write(output/'source_contradicted_projection_rows.csv',removed)
    assert len(removed)==3
    assert len(member_rows)==46
    assert sum(x['primary_source_status']=='confirmed_present' for x in member_rows)==11
    assert sum(x['primary_source_status']=='contradicted_absent' for x in member_rows)==3
    assert sum(x['primary_source_status']=='not_row_verified' for x in member_rows)==32
    # Partial correction means NOT publication freeze, only a bounded sensitivity scenario.
    (output/'paper1_partial_source_correction.json').write_text(
       json.dumps({'status':'PARTIAL_REVIEW_NOT_FROZEN',
           'input_sha256':sha256(data_path), 'origin':'V3-derived formula projection used in Paper 1 app',
           'source_url':PUBLIC_PDF, 'source_access':'inspected official PDF online; source PDF bytes not included',
           'review_coverage':{'confirmed':11,'contradicted':3,'not_row_verified':32},
           'manuscript_counts_are_not_revalidated':True,
           'formulas':corrected['formulas']},ensure_ascii=False,indent=2),encoding='utf8')
    before=npmi(dat['formulas'],ids); after=npmi(corrected['formulas'],ids)
    assert len(before)==45 and len(after)==45
    compared=[]
    for a,b in itertools.combinations(ids,2):
        original=before[(a,b)];candidate=after[(a,b)]
        r={'herb_a':a,'herb_b':b,'herb_a_th':name[a],'herb_b_th':name[b],
           'support_before':original[0],'support_after_partial_correction':candidate[0],
           'npmi_before':round(original[1],8),'npmi_after_partial_correction':round(candidate[1],8),
           'delta_npmi':round(candidate[1]-original[1],8),
           'edge_before':int(original[2]>0),'edge_after':int(candidate[2]>0),
           'affected':int(original[0]!=candidate[0] or abs(original[1]-candidate[1])>1e-10)}
        for m in METHODS:
            r['w_'+m+'_before']=round(weights(before,m)[(a,b)],8)
            r['w_'+m+'_after']=round(weights(after,m)[(a,b)],8)
        compared.append(r)
    csv_write(output/'npmi_original_vs_partially_corrected_45pairs.csv',compared)
    npmis1=[z[2] for z in before.values()];npmis2=[z[2] for z in after.values()]
    metric_rows=[]
    for m in METHODS:
        w1=weights(before,m);w2=weights(after,m)
        v1=list(w1.values());v2=list(w2.values())
        top1=set(sorted(w1,key=w1.get,reverse=True)[:5]);top2=set(sorted(w2,key=w2.get,reverse=True)[:5]);
        metric_rows.append({'method':m,'edge_rank_spearman_original_vs_partial':round(spearman(v1,v2),8),
            'top5_overlap_count':len(top1&top2),'top5_jaccard':round(len(top1&top2)/len(top1|top2),8),
            'positive_edges_before':sum(x>0 for x in v1),'positive_edges_after':sum(x>0 for x in v2)})
    csv_write(output/'weighting_effect_of_source_correction.csv',metric_rows)
    chem=[a for a in dat['assertions'] if a['assertion_type']=='ChemistryOccurrenceAssertion']
    chemistry_flags=[{'assertion_id':a['assertion_id'],'herb_id':a['subject_id'],
         'compound':a['object_label'],'source_id':a['source_id'],
         'locator':a['source_locator_or_context'],
         'review_status':'V3 subset only; original Paper 1 row identity and compound class not verified',
         'priority':'HIGH'} for a in chem]
    csv_write(output/'chemistry_30_source_gaps.csv',chemistry_flags)
    report={
       'audit_status':'PARTIAL_SOURCE_REVIEW_NOT_A_PUBLICATION_DATA_FREEZE',
       'review_date':FROZEN_REVIEW_DATE,'input_sha256':sha256(data_path),'official_source_url':PUBLIC_PDF,
       'counts':{'original_memberships':len(member_rows),'confirmed_present':11,'contradicted_absent':3,
                 'not_row_verified':32,'corrected_scenario_memberships':sum(len(f['herbs']) for f in corrected['formulas']),
                 'positive_npmi_before':sum(v[2]>0 for v in before.values()),
                 'positive_npmi_after':sum(v[2]>0 for v in after.values()),
                 'pair_support_changed':sum(r['support_before']!=r['support_after_partial_correction'] for r in compared),
                 'pair_npmi_changed':sum(r['affected'] for r in compared),
                 'chemistry_rows_needing_source_match':len(chem)},
       'edge_rank_spearman_npmi_before_after':spearman(npmis1,npmis2),
       'methods':metric_rows,
       'limitations':[
          'Other 32 projected memberships have not been matched against source ingredient tables.',
          'Official PDF title and page locations do not prove row-level membership validation.',
          'Original Paper 1 30-herb-compound and 19-class data are not accessible as an independently verified input export.',
          'Study correlations reported in manuscript are not recalculated here; this is a source-correction sensitivity, not an embedding validation.',
          'Corrected scenario cannot be called frozen or ground truth until all 46 rows and absent rows checked independently.',
       ]}
    (output/'audit_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    return report

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser()
 parser.add_argument('--data',default='data/paper1_bootstrap_v3_proxy.json')
 parser.add_argument('--out',default='results')
 args=parser.parse_args()
 print(json.dumps(main(args.data,args.out),indent=2,ensure_ascii=False))