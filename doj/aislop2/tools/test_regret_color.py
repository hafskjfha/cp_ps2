import importlib.util,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate
spec=importlib.util.spec_from_file_location('regret',ROOT/'solvers/experiments/regret_color.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
rng=random.Random(4116)
for trial in range(30):
 n=rng.randrange(3,10);d=rng.choice((2,3));c=rng.randrange(2,7);k=24;nn=n*n
 initial=[rng.randrange(c) for _ in range(nn+d*d)];target=[rng.randrange(c) for _ in range(nn)]
 idx,_,ops,_,_=s.build(n,d,target);actions=list(zip(idx,ops))
 path=[rng.randrange(len(ops)) for _ in range(rng.randrange(4,24))]
 instance=Instance(n,d,c,k,initial[:nn],target,initial[nn:])
 old=simulate(instance,[ops[i] for i in path])[0]
 candidate=s.regret_color_repair(n,d,c,k,initial,target,actions,path)
 new=simulate(instance,[ops[i] for i in candidate])[0]
 assert len(candidate)<=k
 assert sum(a==b for a,b in zip(new,target))>=sum(a==b for a,b in zip(old,target))
 assert candidate==s.regret_color_repair(n,d,c,k,initial,target,actions,path)
print('PASS 30 color-priority canonical floor, K, and determinism cases')
