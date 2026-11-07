"""Small, dependency-free KG analysis helpers; never overwrite primary evidence."""
import csv, hashlib, itertools, json, math, statistics
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pair_rolling(formulas,herbs):
    n=len(formulas)
    assert n>1
    sets={h:{x['id'] for x in formulas if h in x['herbs']} for h in herbs}
    result={}
    for a,b in itertools.combinations(herbs,2):
        na,nb=len(sets[a]),len(sets[b]); support=len(sets[a]&sets[b])
        p_ab=support/n
        if support==0 or support==n or not na or not nb:
            npmi=0.0
        else:
            npmi=math.log(p_ab/((na/n)*(nb/n)))/-math.log(p_ab)
        result[(a,b)]={'support':support,'npmi':max(0.0,npmi),'raw_npmi':npmi}
    return result

def weights(formulas,herbs,k=2.0):
    pairs=pair_rolling(formulas,herbs)
    deg={h:sum(row['npmi']>0 for (a,b),row in pairs.items() if h in (a,b)) for h in herbs}
    out={}
    for (a,b),row in pairs.items():
        n=row['support']; base=row['npmi']; sd=base*n/(n+k) if n else 0.0
        # Degree correction is used ONLY for walks/ranking, never evidence quality.
        correction=(deg[a]*deg[b])**-0.25 if deg[a] and deg[b] else 0.0
        out[(a,b)]={'support':n,'npmi':base,'support_weight':sd,
                    'degree_weight':base*correction,'combined_weight':sd*correction,
                    'degree_a':deg[a],'degree_b':deg[b]}
    return out

def ranks(rows,field):
    # Deterministic rank with zeros last, tie-break stable pair IDs.
    return [key for key,val in sorted(rows.items(),key=lambda kv:(-kv[1][field],kv[0])) if val[field]>0]

def correlation(xs,ys):
    # Spearman with average tie ranks; None if one vector is constant.
    if len(xs)!=len(ys) or len(xs)<2: return None
    def rank(v):
        idx=sorted(range(len(v)),key=lambda i:v[i]); out=[0.0]*len(v); pos=0
        while pos<len(idx):
            end=pos+1
            while end<len(idx) and v[idx[end]]==v[idx[pos]]:end+=1
            rr=(pos+1+end)/2
            for j in range(pos,end):out[idx[j]]=rr
            pos=end
        return out
    a,b=rank(xs),rank(ys); am=statistics.mean(a);bm=statistics.mean(b)
    num=sum((x-am)*(y-bm) for x,y in zip(a,b))
    den=math.sqrt(sum((x-am)**2 for x in a)*sum((y-bm)**2 for y in b))
    return num/den if den else None

def write_csv(path,rows):
    path=Path(path)
    if not rows: return
    with path.open('w',encoding='utf-8-sig',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
