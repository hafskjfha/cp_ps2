"""Generalized three-cycle repair by conjugation BFS."""
import collections


def small_cycle_repair(n,d,k,grid,target,stamp,actions,minimum_gain=1):
    nn=n*n;dd=d*d;width=n-d+1;size=nn+dd
    def canonical(a,b,c):
        if a<b and a<c:return(a,b,c)
        if b<c:return(b,c,a)
        return(c,a,b)
    direct={}
    for x in range(width):
        for y in range(width):
            for dx,dy in ((d-1,d-1),(d-1,1-d)):
                if not(0<=x+dx<width and 0<=y+dy<width):continue
                for r in range(4):
                    a=(x*width+y)*4+r
                    b=((x+dx)*width+y+dy)*4+r
                    pa=(a,b)*3+((a//4)*4+(r+2)%4,(b//4)*4+(r+2)%4)*3
                    state=list(range(size))
                    for aid in pa:
                        for j,p in enumerate(actions[aid]):state[p],state[nn+j]=state[nn+j],state[p]
                    changed=[p for p,q in enumerate(state) if p!=q]
                    assert len(changed)==3
                    p=changed[0];q=state[p];r2=state[q]
                    triple=canonical(p,q,r2)
                    direct[triple]=pa
                    direct[canonical(p,r2,q)]=pa[::-1]
    renames=[]
    for pos in actions:
        mapping=list(range(size))
        for j,p in enumerate(pos):mapping[p]=nn+j;mapping[nn+j]=p
        renames.append(mapping)
    def score(state,triple):
        a,b,c=triple
        gain=0
        for p,q in ((a,b),(b,c),(c,a)):
            if p<nn:gain+=(state[q]==target[p])-(state[p]==target[p])
        return gain
    state=grid+stamp
    initial=nn-sum(a!=b for a,b in zip(grid,target))
    parents={trip:None for trip in direct}
    front=list(direct)
    for depth in range(12,min(k,24)+1,2):
        for triple in front:
            gain=score(state,triple)
            if gain>=minimum_gain:
                word=[];tr=triple
                while parents[tr] is not None:
                    tr,aid=parents[tr];word.append(aid)
                path=word+list(direct[tr])+word[::-1]
                return path,initial+gain,len(parents),depth
        if depth+2>k:break
        nextfront=[]
        for triple in front:
            a,b,c=triple
            for aid,rename in enumerate(renames):
                child=canonical(rename[a],rename[b],rename[c])
                if child not in parents:
                    parents[child]=(triple,aid);nextfront.append(child)
                    gain=score(state,child)
                    if gain>=minimum_gain:
                        word=[];tr=child
                        while parents[tr] is not None:
                            tr,step=parents[tr];word.append(step)
                        path=word+list(direct[tr])+word[::-1]
                        return path,initial+gain,len(parents),depth+2
        front=nextfront
        if not front:break
    return [],initial,len(parents),0

if __name__=='__main__':
    import sys,json,importlib.util,time
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
    from tools.simulate import parse_instance,simulate,match_count
    spec=importlib.util.spec_from_file_location('parent',ROOT/'solvers/experiments/seven_construct_fast_bytearray_readable.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    ids=sys.argv[1].split(',') if len(sys.argv)>1 else ['case_168','case_152','case_056']
    baseline={r['id']:r for r in json.load(open(ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json'))['results']}
    cache={r['id']:r for r in json.load(open(ROOT/'results/m2_parent_cache.json'))['results']}
    manifest=json.load(open(ROOT/'cases/manifest.json'))['cases'];results=[]
    for meta in manifest:
        if meta['id'] not in ids:continue
        inst=parse_instance((ROOT/meta['path']).read_text());start=time.perf_counter()
        inds,_,ops,_,_=parent.build(inst.n,inst.d,inst.t)
        basepath=cache[meta['id']]['operations'];best=baseline[meta['id']]['matches'];path=basepath
        cuts=list(range(min(len(basepath),inst.k-12),-1,-1))
        for cut in cuts:
            if inst.k-cut<12:continue
            board,stamp=simulate(inst,basepath[:cut])
            if match_count(inst,board)+3<=best:continue
            aids,value,states,depth=small_cycle_repair(inst.n,inst.d,inst.k-cut,board,inst.t,stamp,inds,minimum_gain=best-match_count(inst,board)+1)
            can=basepath[:cut]+[ops[a] for a in aids]
            actual=match_count(inst,simulate(inst,can)[0]);assert actual==value,(actual,value)
            if value>best:best=value;path=can
        row=dict(id=meta['id'],matches=best,base=baseline[meta['id']]['matches'],delta=1000000*best//inst.n**2-baseline[meta['id']]['score'],runtime=time.perf_counter()-start,operations=path)
        results.append(row);print({k:v for k,v in row.items() if k!='operations'},flush=True)
    (ROOT/'results/m2_gap_cyclebfs.json').write_text(json.dumps(dict(results=results),indent=2))
