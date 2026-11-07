from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from audit_paper1 import CHECKED_FORMULA_MEMBERS,FORMULA_CROSSWALK,main,npmi,weights,spearman

def test_formula_names_anchored():
    assert len(FORMULA_CROSSWALK)==10
    assert all(f[-1] for f in FORMULA_CROSSWALK)
    assert next(f for f in FORMULA_CROSSWALK if f[0]=='F05_DTAM2566')[3]==161

def test_original_formula_mismatch():
    assert CHECKED_FORMULA_MEMBERS['F05_DTAM2566','H01'][0] is False
    assert CHECKED_FORMULA_MEMBERS['F05_DTAM2566','H02'][0] is False
    assert CHECKED_FORMULA_MEMBERS['F05_DTAM2566','H03'][0] is False
    assert CHECKED_FORMULA_MEMBERS['F05_DTAM2566','H05'][0] is True
    assert CHECKED_FORMULA_MEMBERS['F05_DTAM2566','H10'][0] is True

def test_report_scope(tmp_path):
    r=main(ROOT/'data/paper1_bootstrap_v3_proxy.json',tmp_path)
    assert r['counts']['original_memberships']==46
    assert r['counts']['corrected_scenario_memberships']==43
    assert r['counts']['not_row_verified']==32
    assert r['audit_status'].startswith('PARTIAL')
    assert len(list(__import__('csv').DictReader(open(tmp_path/'npmi_original_vs_partially_corrected_45pairs.csv',encoding='utf-8-sig'))))==45

def test_weight_positive():
    d=json.loads((ROOT/'data/paper1_bootstrap_v3_proxy.json').read_text())
    p=npmi(d['formulas'],[h['id'] for h in d['herbs']]);assert sum(z[2]>0 for z in p.values())==23
    for m in ['original_npmi','support_k2','degree_05','combined']:
        assert all(v>=0 for v in weights(p,m).values())

def test_rank_corr_ties():
    assert abs(spearman([1,1,2,3],[1,1,2,3])-1)<1e-9