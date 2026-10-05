"""Short algebraic macro composition for isolated repairs."""
import time


def macros(n,d,actions):
    nn=n*n;dd=d*d;width=n-d+1
    found={}
    for a,ia in enumerate(actions):
        x,y=divmod(a//4,width)
        for dx,dy in ((d-1,d-1),(d-1,1-d)):
            if not(0<=x+dx<width and 0<=y+dy<width):continue
            for r in range(4):
                b=((x+dx)*width+y+dy)*4+r
                state=list(range(nn+dd))
                path=(a,b)*3
                for aid in path:
                    for j,p in enumerate(actions[aid]):state[p],state[nn+j]=state[nn+j],state[p]
                changed=tuple(p for p,v in enumerate(state) if p!=v)
                if len(changed)!=5:continue
                mapping=tuple((p,state[p]) for p in changed)
                found[mapping]=path
                inverse=tuple(sorted((q,p) for p,q in mapping))
                found[inverse]=path[::-1]
    return [(dict(m),set(p for p,q in m),path) for m,path in found.items()]

def simplify(path):
    answer=[]
    for aid in path:
        if answer and answer[-1]==aid:answer.pop()
        else:answer.append(aid)
    return tuple(answer)


_CACHE={}

def repair(n,d,c,k,grid,target,stamp,actions,rounds=8):
    nn=n*n;dd=d*d;initial=grid+stamp;wanted=target+[6]*dd
    if (n,d) not in _CACHE:
        found=macros(n,d,actions)
        # Products of two 5-cycles can cancel to a 3-cycle in twelve moves.
        direct={}
        for ma,sa,pa in found:
            for mb,sb,pb in found:
                if len(sa&sb)<3:continue
                state={p:ma.get(mb.get(p,p),mb.get(p,p)) for p in sa|sb}
                changed=tuple(sorted((p,q) for p,q in state.items() if p!=q))
                if len(changed)==3:direct[changed]=simplify(pa+pb)
        # Find commutators whose support collapses to exactly 3 locations.
        bypos={}
        for i,(m,s,path) in enumerate(found):
            for p in s:bypos.setdefault(p,[]).append(i)
        candidates=direct
        for a,(ma,sa,pa) in enumerate(found):
            for common in sa:
                for b in bypos[common]:
                    if b<=a:continue
                    mb,sb,pb=found[b]
                    if len(sa&sb)!=1:continue
                    support=sa|sb
                    state={p:p for p in support}
                    ima={v:k for k,v in ma.items()};imb={v:k for k,v in mb.items()}
                    for mapping in (ma,mb,ima,imb):
                        old=state.copy()
                        for p,q in mapping.items():state[p]=old[q]
                    nonzero=tuple(sorted((p,q) for p,q in state.items() if p!=q))
                    assert len(nonzero)==3
                    # Focus repair words that move a stamp color into the grid.
                    word=simplify(pa+pb+pa[::-1]+pb[::-1])
                    if nonzero not in candidates or len(word)<len(candidates[nonzero]):candidates[nonzero]=word
                    inverse=tuple(sorted((q,p) for p,q in nonzero))
                    candidates[inverse]=candidates[nonzero][::-1]
        # Add a single-operation conjugation; permutation support remains three.
        original=list(candidates.items())
        for aid,positions in enumerate(actions):
            rename={p:nn+j for j,p in enumerate(positions)}
            rename.update({nn+j:p for j,p in enumerate(positions)})
            for mapping,path in original:
                transformed=tuple(sorted((rename.get(p,p),rename.get(q,q)) for p,q in mapping))
                word=simplify((aid,)+path+(aid,))
                if transformed not in candidates or len(word)<len(candidates[transformed]):candidates[transformed]=word
        _CACHE[n,d]=(candidates,len(found))
    candidates,found_count=_CACHE[n,d]
    answer=[];state=initial[:]
    for _ in range(rounds):
        best=0;chosen=None
        for mapping,path in candidates.items():
            if len(answer)+len(path)>k:continue
            gain=sum((state[q]==wanted[p])-(state[p]==wanted[p]) for p,q in mapping if p<nn)
            if gain>best:best=gain;chosen=(mapping,path)
        if chosen is None:break
        mapping,path=chosen;old=state[:]
        for p,q in mapping:state[p]=old[q]
        answer.extend(path)
    return answer,sum(a==b for a,b in zip(state,target)),found_count,len(candidates)

if __name__=='__main__':
    import sys,json,importlib.util
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
    from tools.simulate import parse_instance,simulate,match_count
    from tools.validate_output import validate_output
    spec=importlib.util.spec_from_file_location('parent',ROOT/'solvers/experiments/seven_construct_fast_bytearray_readable.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    ids=sys.argv[1].split(',') if len(sys.argv)>1 else ['case_168']
    baseline={r['id']:r for r in json.load(open(ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json'))['results']}
    cache={r['id']:r for r in json.load(open(ROOT/'results/m2_parent_cache.json'))['results']}
    manifest=json.load(open(ROOT/'cases/manifest.json'))['cases'];results=[]
    for meta in manifest:
        if meta['id'] not in ids:continue
        inst=parse_instance((ROOT/meta['path']).read_text());start=time.perf_counter()
        inds,_,ops,_,_=parent.build(inst.n,inst.d,inst.t)
        basepath=cache[meta['id']]['operations']
        best_value=baseline[meta['id']]['matches'];path=basepath
        for cut in range(min(len(basepath),max(0,inst.k-12))+1):
            board,stamp=simulate(inst,basepath[:cut])
            aids,value,mc,cc=repair(inst.n,inst.d,inst.c,inst.k-cut,board,inst.t,stamp,inds)
            if value>best_value:best_value=value;path=basepath[:cut]+[ops[a] for a in aids]
        value=best_value
        out=str(len(path))+'\n'+'\n'.join(' '.join(map(str,a)) for a in path)+'\n'
        valid=validate_output(inst,out.encode());grid,_=simulate(inst,valid);actual=match_count(inst,grid)
        assert actual==value,(actual,value)
        row=dict(id=meta['id'],matches=value,base=baseline[meta['id']]['matches'],delta=(1000000*value//inst.n**2-baseline[meta['id']]['score']),runtime=time.perf_counter()-start,macros=mc,commutators=cc,operations=path)
        results.append(row);print({k:v for k,v in row.items() if k!='operations'},flush=True)
    (ROOT/f'results/m2_gap_commute.json').write_text(json.dumps(dict(results=results),indent=2))
