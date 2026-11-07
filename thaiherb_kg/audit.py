"""Check frozen snapshots, cross-paper integrity, input source and hashes."""
import json,hashlib,csv,collections
from pathlib import Path
from shared import load_json,sha256
ROOT=Path(__file__).resolve().parent

def run():
    names=['paper1_bootstrap.json','paper2_bootstrap.json','paper3_ui_subset.json','paper3_assertions.csv']
    manifest={'release':'v0.2','purpose':'audited frozen snapshots, NOT independently confirmed original research datasets',
        'files':{name:{'sha256':sha256(ROOT/'data'/name),'bytes':(ROOT/'data'/name).stat().st_size} for name in names}}
    a,b,c=[load_json(ROOT/'data'/name) for name in names[:3]]
    for name,d in [('paper1',a),('paper2',b),('paper3',c)]:
        assert len(d['herbs'])==({'paper1':10,'paper2':20,'paper3':20}[name])
        if name!='paper3':
            assert len(d['formulas'])==10
            assert len(d['pairs']) in (45,190)
    p1=set(h['id'] for h in a['herbs']);p2=set(h['id'] for h in b['herbs'])
    assert p1<=p2
    p1_assert={r['assertion_id'] for r in a['assertions']}
    p2_assert={r['assertion_id'] for r in b['assertions']}
    p3_assert={r['assertion_id'] for r in c['assertions']}
    assert p1_assert<=p2_assert<=p3_assert
    manifest['crosswalk']={'paper1_herbs_subset_paper2':True,
       'p1_shared_assertion_ids_with_p2':len(p1_assert&p2_assert),
       'p2_shared_assertion_ids_with_p3':len(p2_assert&p3_assert),
       'warning':'Matching assertion IDs across projections is not a source-document equivalence audit.'}
    (ROOT/'docs/SOURCE_AUDIT.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
