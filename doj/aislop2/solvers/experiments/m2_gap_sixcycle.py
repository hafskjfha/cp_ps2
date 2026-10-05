"""Exact six-operation three-cycles from almost-identical conjugated stamps."""
_SIX_TEMPLATES=None
_SIX_GEOMETRY=None

def six_templates():
 global _SIX_TEMPLATES
 if _SIX_TEMPLATES is not None:return _SIX_TEMPLATES
 n=5;d=3;nn=25;size=34;indices=[];ops=[]
 for x in range(3):
  for y in range(3):
   for r in range(4):
    patch=[]
    for u in range(3):
     for v in range(3):
      p,q=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r];patch.append((x+p)*5+y+q)
    indices.append(patch);ops.append((x,y,r))
 groups={};found={}
 for a in range(len(indices)):
  for b in range(len(indices)):
   if a==b:continue
   st=list(range(size))
   for aid in(a,b,a):
    for j,p in enumerate(indices[aid]):st[p],st[nn+j]=st[nn+j],st[p]
   pairs=tuple((p,q)for p,q in enumerate(st)if p<q)
   for j,pair in enumerate(pairs):
    key=pairs[:j]+pairs[j+1:]
    for old,word in groups.get(key,[]):
     if len(set(old+pair))!=3:continue
     path=word+(a,b,a);state=list(range(size))
     for aid in path:
      for j,p in enumerate(indices[aid]):state[p],state[nn+j]=state[nn+j],state[p]
     changed=[p for p,q in enumerate(state)if p!=q];assert len(changed)==3
     grids=[p for p in changed if p<nn]
     if len(grids)!=1:continue
     p=grids[0];q=state[p];r=state[q];assert q>=nn and r>=nn and state[r]==p
     found[p,q-nn,r-nn]=tuple(ops[a]for a in path)
    groups.setdefault(key,[]).append((pair,(a,b,a)))
 _SIX_TEMPLATES=[(p//5,p%5,q,r,path)for(p,q,r),path in found.items()]
 return _SIX_TEMPLATES

def six_geometry(n):
 global _SIX_GEOMETRY
 if _SIX_GEOMETRY is not None and _SIX_GEOMETRY[0]==n:return _SIX_GEOMETRY[1]
 nn=n*n;found={}
 for u,v,q,r,word in six_templates():
  minx=min(p[0]for p in word);miny=min(p[1]for p in word);maxx=max(p[0]for p in word);maxy=max(p[1]for p in word)
  for x in range(-minx,n-2-maxx):
   for y in range(-miny,n-2-maxy):
    p=(x+u)*n+y+v;key=(p,nn+q,nn+r)
    if key not in found:found[key]=tuple((x+a,y+b,c)for a,b,c in word)
 _SIX_GEOMETRY=n,found
 return found

def six_choose(n,state,wanted,minimum_gain=1):
 best=minimum_gain-1;word=None
 for(p,q,r),path in six_geometry(n).items():
  gain=(state[q]==wanted[p])+(state[r]==wanted[q])+(state[p]==wanted[r])-(state[p]==wanted[p])-(state[q]==wanted[q])-(state[r]==wanted[r])
  if gain>best:best=gain;word=path
 return word,best

if __name__=='__main__':
 import sys,json,importlib.util,time
 from pathlib import Path
 ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
 from tools.simulate import parse_instance,simulate,match_count
 s=importlib.util.spec_from_file_location('m',ROOT/'solvers/experiments/m2_combined_readable.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 cache={r['id']:r for r in json.load(open(ROOT/'results/m2_gap_combined_cache.json'))['results']};base={r['id']:r for r in json.load(open(ROOT/'results/m2_combined_stable.json'))['results']};rows=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases']:
  if meta['d']!=3 or meta['n']<5 or meta['k']<6:continue
  i=parse_instance((ROOT/meta['path']).read_text());reference=cache[meta['id']]['operations'];old=base[meta['id']];upper=m.color_bound(i.a+i.s,i.t)
  if old['matches']==upper:continue
  start=time.perf_counter();answer=reference;best=old['matches'];wanted=i.t+[6]*9
  for cut in range(min(len(reference),i.k-6),-1,-1):
   grid,stamp=simulate(i,reference[:cut]);value=match_count(i,grid)
   if value+(i.k-cut)//6<=best:continue
   path=reference[:cut]
   while i.k-len(path)>=6:
    word,gain=six_choose(i.n,grid+stamp,wanted)
    if word is None:break
    path=path+list(word);grid,stamp=simulate(i,path);actual=match_count(i,grid);assert actual==value+gain;value=actual
    if value>best:answer=path;best=value
    if best==upper:break
   if best==upper:break
  if best>old['matches']:
   row=dict(id=meta['id'],gain=1000000*best//i.n**2-old['score'],matches=best,base=old['matches'],runtime=time.perf_counter()-start,operations=answer);rows.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/'results/m2_gap_sixcycle.json').write_text(json.dumps(dict(results=rows),indent=2))
