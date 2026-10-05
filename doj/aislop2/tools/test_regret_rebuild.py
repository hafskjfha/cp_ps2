import importlib.util
import json
import random
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate
spec=importlib.util.spec_from_file_location('regret',ROOT/(sys.argv[1] if len(sys.argv)>1 else 'solvers/experiments/regret_rebuild.py'))
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
s.regret_rebuild=getattr(s,'regret_rebuild',getattr(s,'regret_causal_rebuild',getattr(s,'regret_lookahead',None)))
rng=random.Random(771310)
checks=0
for d in (2,3):
 for n in (3,4,7,12):
  c=4;k=28;nn=n*n
  for trial in range(4):
   initial=[rng.randrange(c) for _ in range(nn+d*d)]
   target=[rng.randrange(c) for _ in range(nn)]
   idx,_,ops,_,_=s.build(n,d,target);actions=list(zip(idx,ops))
   path=[rng.randrange(len(ops)) for _ in range(rng.randrange(4,24))]
   inst=Instance(n,d,c,k,initial[:nn],target,initial[nn:])
   goal=target+[6]*(d*d)
   left=rng.randrange(len(path));right=rng.randrange(left+1,len(path)+1)
   actual=list(sum(simulate(inst,[ops[i] for i in path[:left]]),[]))
   wishes=goal[:]
   for aid in reversed(path[right:]):s.seq_transition(wishes,nn,idx[aid])
   order=list(range(len(actions)));rng.shuffle(order)
   state=s.regret_state(n,d,actual,wishes,actions,order)
   before=sum(a==b for a,b in zip(actual,wishes))
   chosen,gain=state.best()
   oracle=[0]
   for aid in order:
    changed=actual[:];s.seq_transition(changed,nn,idx[aid])
    oracle.append(sum(a==b for a,b in zip(changed,wishes))-before)
   assert gain==max(oracle),(n,d,gain,max(oracle))
   if chosen>=0:
    actual2=actual[:];s.seq_transition(actual2,nn,idx[chosen])
    state.apply(chosen)
    assert state.grid+state.stamp==actual2
    assert sum(a==b for a,b in zip(actual2,wishes))-before==gain
   cut=path[:left]+path[right:]
   canonical=simulate(inst,[ops[i] for i in cut])[0]
   assert before==sum(a==b for a,b in zip(canonical,target))
   base=simulate(inst,[ops[i] for i in path])[0]
   candidate=s.regret_rebuild(n,d,k,initial,target,actions,path,rounds=15)
   result=simulate(inst,[ops[i] for i in candidate])[0]
   assert len(candidate)<=k
   assert sum(a==b for a,b in zip(result,target))>=sum(a==b for a,b in zip(base,target))
   assert candidate==s.regret_rebuild(n,d,k,initial,target,actions,path,rounds=15)
   checks+=1
print('PASS',checks,'canonical suffix-boundary, exhaustive delta, floor, determinism cases')
