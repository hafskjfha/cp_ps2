"""Bidirectional approximate matching search; standalone research helper."""
import heapq
import random
import time


def mitm(n,d,c,k,grid,target,stamp,expand,width=768,branch_budget=700000,seed=733,mode=0):
    nn=n*n; dd=d*d; size=nn+dd
    mask=sum(1<<(3*i) for i in range(size))
    boardmask=sum(1<<(3*i) for i in range(nn))
    pack=lambda a:sum(v<<(3*i) for i,v in enumerate(a))
    initial=pack(grid+stamp); wanted=pack(target+[6]*dd)
    upper=sum(min((grid+stamp).count(v),target.count(v)) for v in range(c))
    rng=random.Random(seed)
    tie_mask=sum(1<<(3*i) for i in range(size) if rng.randrange(4)==0)
    used=0
    def beam(first,goal,depth,budget,back=False):
        nonlocal used
        front=[(first,())]; seen={first}
        best=[]; bestscore=-1
        for level in range(depth):
            records={}
            for state,path in front:
                for aid,child in expand(state):
                    used+=1
                    if path and aid==path[-1] or child in seen or child in records:continue
                    diff=child^goal
                    wrong=(diff|diff>>1|diff>>2)&mask
                    score=size-wrong.bit_count()
                    if mode==0:rank=score*8-(wrong&tie_mask).bit_count()
                    elif mode==1:rank=score*8-rng.randrange(16)
                    elif mode==2:rank=score*8-(wrong&tie_mask).bit_count()*3
                    else:rank=score*8
                    records[child]=(rank,rng.getrandbits(32),path+(aid,))
            selected=heapq.nlargest(width,records,key=records.get)
            front=[(s,records[s][2]) for s in selected]
            seen.update(selected)
            if not front:break
        return front
    leftdepth=k//2;rightdepth=k-leftdepth
    left=beam(initial,wanted,leftdepth,branch_budget//2)
    right=beam(wanted,initial,rightdepth,branch_budget//2,True)
    # Index each exact physical state by each cell's color.
    bytecount=(len(left)+7)//8
    buffers=[[bytearray(bytecount) for _ in range(c)] for _ in range(size)]
    for i,(state,path) in enumerate(left):
        by=i>>3;bit=1<<(i&7)
        for pos in range(size):
            buffers[pos][state&7][by]|=bit;state>>=3
    indexes=[[int.from_bytes(b,'little') for b in row] for row in buffers]
    allbits=(1<<len(left))-1
    best=sum(a==b for a,b in zip(grid,target));answer=[]
    for wishes,suffix in right:
        planes=[0]*nn.bit_length()
        for row in indexes:
            color=wishes&7;wishes>>=3
            if color==6:continue
            carry=row[color];p=0
            while carry:
                planes[p],carry=planes[p]^carry,planes[p]&carry;p+=1
        candidates=allbits;value=0
        for p in range(len(planes)-1,-1,-1):
            hits=candidates&planes[p]
            if hits:candidates=hits;value|=1<<p
        if value>best:
            pick=(candidates&-candidates).bit_length()-1
            answer=list(left[pick][1])+list(suffix[::-1]);best=value
            if best==upper:break
    return answer,best,used

if __name__=='__main__':
    import sys,json,importlib.util
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(ROOT))
    from tools.simulate import parse_instance,simulate,match_count
    from tools.validate_output import validate_output
    spec=importlib.util.spec_from_file_location('parent',ROOT/'solvers/experiments/seven_construct_fast_bytearray_readable.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    ids=sys.argv[1].split(',') if len(sys.argv)>1 else ['case_308','case_145','case_225','case_037','case_276']
    width=int(sys.argv[2]) if len(sys.argv)>2 else 768
    mode=int(sys.argv[3]) if len(sys.argv)>3 else 0
    baseline={r['id']:r for r in json.load(open(ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json'))['results']}
    manifest=json.load(open(ROOT/'cases/manifest.json'))['cases'];results=[]
    for meta in manifest:
        if meta['id'] not in ids:continue
        inst=parse_instance((ROOT/meta['path']).read_text());start=time.perf_counter()
        aids,value,used=mitm(inst.n,inst.d,inst.c,inst.k,inst.a,inst.t,inst.s,parent.i1_packed_expand(inst.n,inst.d),width=width,mode=mode)
        ops=parent.build(inst.n,inst.d,inst.t)[2];path=[ops[a] for a in aids]
        out=str(len(path))+'\n'+'\n'.join(' '.join(map(str,a)) for a in path)+'\n'
        valid=validate_output(inst,out.encode());grid,_=simulate(inst,valid);actual=match_count(inst,grid)
        assert actual==value,(actual,value)
        row=dict(id=meta['id'],matches=value,base=baseline[meta['id']]['matches'],delta=(1000000*value//inst.n**2-baseline[meta['id']]['score']),runtime=time.perf_counter()-start,used=used,operations=path)
        results.append(row);print({k:v for k,v in row.items() if k!='operations'},flush=True)
    report=dict(width=width,mode=mode,results=results)
    (ROOT/f'results/m2_gap_mitm_w{width}_m{mode}.json').write_text(json.dumps(report,indent=2))
