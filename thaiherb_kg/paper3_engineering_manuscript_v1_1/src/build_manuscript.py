"""Create an author-review Word manuscript from the frozen Markdown text."""
from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/'manuscript'
MARKDOWN=MAN/'Paper3_EvidenceCentric_KG_Full_Manuscript.md'
OUT=MAN/'Paper3_EvidenceCentric_KG_Full_Manuscript.docx'
MD=MARKDOWN.read_text(encoding='utf-8')

D=Document()
sec=D.sections[0]
sec.top_margin=Inches(.82);sec.bottom_margin=Inches(.77)
sec.left_margin=Inches(.85);sec.right_margin=Inches(.8)
sec.header_distance=Inches(.32);sec.footer_distance=Inches(.38)

st=D.styles['Normal'];st.font.name='Aptos';st.font.size=Pt(9.6)
st.font.color.rgb=RGBColor(37,48,60)
st.paragraph_format.line_spacing=1.13
st.paragraph_format.space_after=Pt(6)
for sty,size,bef,after in [('Title',19,0,10),('Heading 1',13.5,13,6),('Heading 2',10.8,10,4),('Heading 3',9.6,7,3)]:
 s=D.styles[sty];s.font.name='Aptos Display' if sty in ['Title','Heading 1'] else 'Aptos';s.font.size=Pt(size)
 s.font.bold=True;s.font.color.rgb=RGBColor(26,57,84)
 s.paragraph_format.space_before=Pt(bef);s.paragraph_format.space_after=Pt(after)
 s.paragraph_format.keep_with_next=True

hdr=sec.header.paragraphs[0];hdr.text='THAIHERB KNOWLEDGE GRAPH   |   PAPER 3   |   AUTHOR REVIEW'
hdr.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for x in hdr.runs:x.font.size=Pt(7.4);x.font.color.rgb=RGBColor(100,110,121)
ftr=sec.footer.paragraphs[0];ftr.alignment=WD_ALIGN_PARAGRAPH.RIGHT
run=ftr.add_run('Evidence-centric RDF methods study  |  Page ');run.font.size=Pt(7.5)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');ftr._p.append(fld)

styles={'abstract':False,'references':False,'section':None}

def inline(text,paragraph):
    # Lightweight formatting; no external Markdown parser dependency.
    parts=re.split(r'(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+`)',text)
    for s in parts:
        if not s:continue
        bold=s.startswith('**') and s.endswith('**')
        ital=s.startswith('*') and s.endswith('*') and not bold
        code=s.startswith('`') and s.endswith('`')
        content=s[2:-2] if bold else (s[1:-1] if ital or code else s)
        run=paragraph.add_run(content)
        run.bold=bold;run.italic=ital
        if code:run.font.name='Consolas';run.font.size=Pt(8)

def label_caption(text):
    p=D.add_paragraph()
    p.style='Normal';p.alignment=WD_ALIGN_PARAGRAPH.LEFT;p.paragraph_format.space_before=Pt(4)
    p.paragraph_format.space_after=Pt(10)
    for span in re.split(r'(\*\*.*?\*\*)',text):
        if span.startswith('**') and span.endswith('**'):
            r=p.add_run(span[2:-2]);r.bold=True;r.font.size=Pt(8.5)
        else:
            r=p.add_run(span);r.italic=True;r.font.size=Pt(8.5)
    return p

def table(lines):
    clean=[]
    for line in lines:
        l=[x.strip() for x in line.strip('|').split('|')]
        if all(re.fullmatch(r':?-{3,}:?',x.replace(' ','')) for x in l):continue
        clean.append(l)
    if not clean:return
    n=len(clean[0]);t=D.add_table(rows=1,cols=n);t.style='Light Shading Accent 1'
    t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    widths=[Inches(2.9),Inches(1.15),Inches(1.15),Inches(1.15)] if n==4 else ([Inches(1.5),Inches(1.3),Inches(.8),Inches(2.65)] if n==4 else [Inches(6.1/n)]*n)
    if n==4 and len(clean)>6:widths=[Inches(2.65),Inches(1.2),Inches(1.2),Inches(1.2)]
    if n==4 and len(clean)<=6:widths=[Inches(1.55),Inches(1.1),Inches(.75),Inches(2.8)]
    for j,cell in enumerate(t.rows[0].cells):
        cell.width=widths[j];cell.text=clean[0][j]
    for rowvals in clean[1:]:
        cells=t.add_row().cells
        for j,v in enumerate(rowvals):cells[j].text=re.sub(r'\*\*|\*','',v)
    for ri,row in enumerate(t.rows):
        for j,cell in enumerate(row.cells):
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cell.width=widths[j]
            for p in cell.paragraphs:
                p.paragraph_format.space_after=Pt(1);p.paragraph_format.space_before=Pt(1)
                for run in p.runs:
                    run.font.size=Pt(7.8 if len(clean)>7 else 8.2)
                    if ri==0:run.font.bold=True
        if ri==0:
            trPr=row._tr.get_or_add_trPr();elm=OxmlElement('w:tblHeader');elm.set(qn('w:val'),'true');trPr.append(elm)
    D.add_paragraph().paragraph_format.space_after=Pt(1)

def add_fig(name, caption):
    fn=ROOT/'figures'/name
    p=D.add_paragraph();p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(2)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run();r.add_picture(str(fn),width=Inches(6.18))
    label_caption(caption)

figs={
 '### 3.1 Corpus and graph dimensions': ('Figure2_Graph_Size.png','Figure 2. RDF graph size by representation. Counts reflect storage structure, not runtime or scientific accuracy.'),
 '### 3.2 Preservation of identity, provenance, and context': ('Figure1_Representation_Fidelity.png','Figure 1. Source-assertion field recoverability for frozen V3 RDF projections.'),
 '### 3.4 Clinical context variation and need for expert assessment': ('Figure4_Clinical_Context_Candidates.png','Figure 4. Clinical review candidates; different annotations do not establish contradiction.'),
 '### 3.5 Qualifier ablation and development competency queries': ('Figure3_Qualifier_Ablation.png','Figure 3. Controlled deletion of M3 evidence qualifiers. The outcome is by-design information loss.'),
}
# Insert figures after section paragraphs, before next numbered section, only once.
position_to_fig={'### 3.2 Preservation of identity, provenance, and context':'Figure2_Graph_Size.png',
'### 3.3 Loss of source-level uniqueness under naive SPO encoding':'Figure1_Representation_Fidelity.png',
'### 3.5 Qualifier ablation and development competency queries':'Figure4_Clinical_Context_Candidates.png',
'### 3.6 Authentic SHACL Core validation':'Figure3_Qualifier_Ablation.png'}
fig_captions={v[0]:v[1] for v in figs.values()}

lines=MD.splitlines();i=0;lastsection=None
while i<len(lines):
    line=lines[i].rstrip();s=line.strip()
    if not s:i+=1;continue
    if s.startswith('|'):
        batch=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            batch.append(lines[i]);i+=1
        table(batch);continue
    if s.startswith('##') and s in position_to_fig:
        name=position_to_fig[s];add_fig(name,fig_captions[name])
    if s.startswith('# '):
        p=D.add_paragraph(style='Title');inline(s[2:],p)
    elif s.startswith('## '):
        p=D.add_paragraph(style='Heading 1');inline(s[3:],p)
        lastsection=s
    elif s.startswith('### '):
        p=D.add_paragraph(style='Heading 2');inline(s[4:],p)
    elif s.startswith('**Figure'):
        # Captions already placed alongside corresponding figures.
        pass
    elif s.startswith('*Note.*') or s.startswith('*Note. '):
        p=D.add_paragraph();inline(s,p);p.paragraph_format.space_after=Pt(8)
        for r in p.runs:r.font.size=Pt(8.2)
    elif s.startswith('- '):
        p=D.add_paragraph(style='List Bullet');inline(s[2:],p)
    elif s.startswith('**') and s.endswith('**') and len(s)<130:
        p=D.add_paragraph();inline(s,p)
    elif s.startswith('---'):
        pass
    else:
        p=D.add_paragraph();inline(s,p)
        if lastsection and 'References' in lastsection:
            p.paragraph_format.left_indent=Inches(.21);p.paragraph_format.first_line_indent=Inches(-.21)
    i+=1

D.core_properties.title='Evidence-Centric RDF Knowledge Graph for Thai Herbal Medicine: Representation Fidelity, Provenance, SHACL'
D.core_properties.subject='Paper 3 author-review methods manuscript'
D.core_properties.keywords='RDF, SHACL, provenance, herbal medicine, EvidenceKG'
D.core_properties.author='Research team (author review pending)'
D.save(OUT)
print('Created',OUT,OUT.stat().st_size)
