from pathlib import Path
import json,sys
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'src'))
from formula_audit import verify
from model_reanalysis import train
source=root/'data/paper1_bootstrap_v3_proxy.json'
snapshot,pairs,manifest=verify(source,root/'results')
d=json.loads(source.read_text());chem=[x for x in d['assertions'] if x['assertion_type']=='ChemistryOccurrenceAssertion']
sumry=train(snapshot,chem,root/'results')
print(json.dumps({'formula_audit':manifest,'models':sumry},ensure_ascii=False,indent=2))