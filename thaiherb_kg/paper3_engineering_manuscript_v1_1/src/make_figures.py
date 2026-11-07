"""Prepare deterministic figures from original RDF audit CSV files."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results'; OUT=ROOT/'figures'; OUT.mkdir(exist_ok=True)
def read(name):
    with (RES/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
S={x['model']:x for x in read('P3_MODEL_CAPABILITY_SUMMARY.csv')}
features=['edge_recoverable','id','provenance','evidence_mode','directness','context']
labels=['SPO relation','Assertion ID','Source link','Evidence mode','Directness','Context']
xs=np.arange(len(labels));width=.25
fig,ax=plt.subplots(figsize=(11,5.2))
for i,m in enumerate(('M1','M2','M3')):
 vals=[int(S[m][k]) for k in features]
 bars=ax.bar(xs+(i-1)*width,vals,width,label=m)
 for b,v in zip(bars,vals):
  if v>0:ax.text(b.get_x()+b.get_width()/2, v+3,str(v),ha='center',va='bottom',fontsize=7)
ax.set_xticks(xs,labels,rotation=15,ha='right');ax.set_ylim(0,238)
ax.set_ylabel('Recoverable original assertions (of 208)');ax.set_title('Figure 1. Representation fidelity on the frozen V3 corpus')
ax.legend(frameon=False);fig.tight_layout();fig.savefig(OUT/'Figure1_Representation_Fidelity.png',dpi=190);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.4))
ms=['M1','M2','M3'];ys=[int(S[x]['rdf_triples']) for x in ms]
bars=ax.bar(ms,ys)
for b,y in zip(bars,ys):ax.text(b.get_x()+b.get_width()/2,y+45,f'{y:,}',ha='center')
ax.set_title('Figure 2. RDF serialization size by model');ax.set_ylabel('Distinct RDF triples');ax.set_ylim(0,3150)
ax.text(.01,-.18,'Storage size reflects chosen representation; not answer accuracy.',transform=ax.transAxes,fontsize=9)
fig.tight_layout();fig.savefig(OUT/'Figure2_Graph_Size.png',dpi=190);plt.close(fig)

A=read('P3_CONTEXT_ABLATION.csv')
feat=['source_recoverable','evidence_mode_recoverable','directness_recoverable','context_recoverable']
lab=['Source','Evidence mode','Directness','Context']
mat=np.array([[int(row[k])/208 for k in feat] for row in A])
fig,ax=plt.subplots(figsize=(9.7,4.7))
im=ax.imshow(mat,aspect='auto',vmin=0,vmax=1)
ax.set_yticks(range(len(A)),[a['ablation'].replace('_',' ') for a in A]);ax.set_xticks(range(4),lab)
for i in range(mat.shape[0]):
 for j in range(mat.shape[1]):ax.text(j,i,f'{mat[i,j]:.0%}',ha='center',va='center',fontsize=9,color='black' if mat[i,j]<.8 else 'white')
ax.set_title('Figure 3. Qualifier ablation: deterministic information loss')
fig.colorbar(im,ax=ax,label='Recoverable fraction');fig.tight_layout();fig.savefig(OUT/'Figure3_Qualifier_Ablation.png',dpi=190);plt.close(fig)

C=read('P3_CLINICAL_CONTEXT_VARIATION.csv')
fig,ax=plt.subplots(figsize=(9,4))
short=['Ginger: nausea/vomiting','Ginger: platelet','Garlic: LDL cholesterol']
by={(x['subject_id'],x['topic']):x for x in C}
order=[by[('H01','chemotherapy-induced nausea and vomiting')],by[('H01','platelet aggregation')],by[('H04','LDL cholesterol')]]
bars=ax.barh(short,[int(x['n_assertions']) for x in order]);ax.invert_yaxis();ax.set_xlim(0,3.8)
for b,v in zip(bars,order):ax.text(b.get_width()+.07,b.get_y()+b.get_height()/2,str(v['n_assertions']),va='center')
ax.set_xlabel('Source assertions, not contradictions confirmed');ax.set_title('Figure 4. Clinical context-variation review candidates')
fig.tight_layout();fig.savefig(OUT/'Figure4_Clinical_Context_Candidates.png',dpi=190);plt.close(fig)
print('Saved',len(list(OUT.glob('Figure*.png'))),'figures')
