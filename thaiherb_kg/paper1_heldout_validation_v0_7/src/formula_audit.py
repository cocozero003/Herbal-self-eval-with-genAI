"""Source-reviewed 10x10 Thai formula projection.

Manually transcribed from the complete ingredient tables of DTAM/FDA (2023).
This is the chosen ten-herb *projection*; full formula ingredient tables are
not redistributed. Audit is single-curator, model-assisted, not independent.
"""
from __future__ import annotations
import csv, json, itertools, hashlib, math
from pathlib import Path

SOURCE_URL = 'https://www.dtam.moph.go.th/wp-content/uploads/dtam-publicdoc/2024/dtam-pbd0002.pdf'
# Complete DTAM/FDA B.E. 2566 ingredient tables. Printed page numbers; PDF zero index is printed page + 8.
# All 10 focal botanicals considered for each complete formula table.
# Status is CURATOR_REVIEWED not INDEPENDENTLY_ADJUDICATED.
FORMULAS = [
    ('F01_DTAM2566','ยาธาตุบรรจบ','ชนิดผง',(1,2),('H01','H02','H09'),22),
    ('F02_DTAM2566','ยาประสะกะเพรา','ชนิดผง',(27,28),('H07','H10','H08','H04','H01','H02','H03'),9),
    ('F03_DTAM2566','ยาไฟประลัยกัลป์','ชนิดผง',(122,123),('H10','H06','H05','H04','H01','H02','H03'),14),
    ('F04_DTAM2566','ยาประสะไพล','ชนิดผง',(143,144),('H05','H04','H01','H02','H03','H10'),12),
    ('F05_DTAM2566','ยาประสะว่านนางคำ','ชนิดผง',(161,162),('H05','H10','H01','H02','H03'),14),
    ('F06_DTAM2566','ยาปลูกไฟธาตุ','ชนิดแคปซูล',(164,165),('H03','H01','H02','H10'),11),
    ('F07_DTAM2566','ยาแก้ไอ ขับเสมหะ สูตร 2','ชนิดผง',(240,241),('H04','H09','H08','H02','H03'),15),
    ('F08_DTAM2566','ยามหาจักรใหญ่','ชนิดผง',(49,51),('H04','H09','H08'),25),
    ('F09_DTAM2566','ยาวิสัมพยาใหญ่','ชนิดผง',(71,72),('H02','H09','H01'),19),
    ('F10_DTAM2566','ยาทาพระเส้น','ชนิดผง',(386,387),('H04','H06','H03'),10),
]


def write_csv(path, rows, headers=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not rows and not headers:return
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=headers or list(rows[0]));w.writeheader();w.writerows(rows)


def npmi(formulas,ids):
    """NPMI over independent formula records (not individual herbs)."""
    n=len(formulas)
    sets={h:{f['id'] for f in formulas if h in f['herbs']} for h in ids}
    o=[]
    for a,b in itertools.combinations(ids,2):
        support=len(sets[a]&sets[b]);v=0.0
        if 0<support<n:
            p=support/n
            v=math.log(p/((len(sets[a])/n)*(len(sets[b])/n)))/-math.log(p)
        o.append({'herb_a':a,'herb_b':b,'support':support,'npmi':v,'positive_npmi':max(v,0.0)})
    return o


def verify(data_path,output):
    d=json.loads(Path(data_path).read_text(encoding='utf8'))
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    ids=[h['id'] for h in d['herbs']]; assert len(ids)==10
    matrix=[];cross=[];formula_rows=[]
    for fid,th,form,(p1,p2),present,all_n in FORMULAS:
        orig=next(f for f in d['formulas'] if f['id']==fid)
        present=set(present); projected=set(orig['herbs'])
        assert present==projected,(fid,'DIFF',present-projected,projected-present)
        cross.append({'formula_id':fid,'official_name':th,'form':form,'printed_page_start':p1,'printed_page_end':p2,'pdf_page_zero_index_start':p1+8,'pdf_page_zero_index_end':p2+8,'source_url':SOURCE_URL,'ingredient_table_total_rows':all_n,'review_method':'manual review of complete source ingredient table','reviewer_independence':'not_independently_adjudicated'})
        formula_rows.append({'id':fid,'title':th,'dosage_form':form,'source_url':SOURCE_URL,'printed_pages':[p1,p2],'herbs':list(orig['herbs']),'status':'curator_source_reviewed'})
        for h in d['herbs']:
            exists=h['id'] in present
            matrix.append({'formula_id':fid,'formula_name':th,'herb_id':h['id'],'herb_name_th':h['thai'],'scientific_name':h['scientific'],'source_verified_presence':int(exists),'previous_projection_presence':int(h['id'] in projected),'agreement':1,'source_locator':f'DTAM/FDA B.E.2566, printed pp. {p1}-{p2}, section 2.1, ingredient table','source_url':SOURCE_URL,'review_status':'source_reviewed_single_curator','independent_expert_verified':0})
    write_csv(out/'formula_herb_100_matrix.csv',matrix)
    write_csv(out/'formula_source_crosswalk.csv',cross)
    snapshot={'dataset_label':'Paper1_focal_herb_formula_projection_v0.4','status':'SOURCE_TABLE_REVIEWED_SINGLE_CURATOR_NOT_INDEPENDENTLY_ADJUDICATED','source':SOURCE_URL,'origin':'V3 derived projection reconciled to DTAM FDA 2566 complete formula tables','herbs':d['herbs'],'formulas':formula_rows}
    (out/'formula_reviewed_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf8')
    pairs=npmi(formula_rows,ids)
    write_csv(out/'npmi_45pairs.csv',[{**r,'npmi':round(r['npmi'],8),'positive_npmi':round(r['positive_npmi'],8)} for r in pairs])
    npositive=sum(r['positive_npmi']>0 for r in pairs)
    manifest={'original_formula_records':len(formula_rows),'curator_reviewed_formula_tables':10,'herb_formula_matrix_cells':len(matrix),'present_memberships':sum(r['source_verified_presence'] for r in matrix),'absent_memberships':sum(1-r['source_verified_presence'] for r in matrix),'dataset_projection_matches_source_tables':True,'positive_npmi_edges':npositive,'total_herb_pairs':len(pairs),'source_verification':'manual source table check, NOT independent adjudication','original_paper1_training_archive_matched':False,'withdraw_v0_3_three_edge_deletion':True,'why_v0_3_invalid':'F05 formula ingredients extend to printed page 162; ginger, Java long pepper and black pepper are present in rows 10,12,13','chemistry_original_19_classes_unavailable':True,'source_pdf_url':SOURCE_URL,'input_sha256':hashlib.sha256(Path(data_path).read_bytes()).hexdigest()}
    (out/'audit_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    return snapshot,pairs,manifest

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--input',default='data/paper1_bootstrap_v3_proxy.json');ap.add_argument('--out',default='results')
    a=ap.parse_args();print(json.dumps(verify(a.input,a.out)[2],ensure_ascii=False,indent=2))