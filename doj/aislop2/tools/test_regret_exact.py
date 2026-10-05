import importlib.util,itertools,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate,match_count
spec=importlib.util.spec_from_file_location('regret',ROOT/'solvers/experiments/regret_exact.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
rng=random.Random(141855)
for n,d in ((3,2),(3,3),(4,3)):
 for k in (1,2,3):
  for _ in range(2):
   c=3;grid=[rng.randrange(c) for _ in range(n*n)];target=[rng.randrange(c) for _ in range(n*n)];stamp=[rng.randrange(c) for _ in range(d*d)]
   ins=Instance(n,d,c,k,grid,target,stamp);idx,_,ops,_,_=s.build(n,d,target)
   optimum=match_count(ins,grid)
   for length in range(1,k+1):
    for word in itertools.product(ops,repeat=length):optimum=max(optimum,match_count(ins,simulate(ins,word)[0]))
   answer=s.regret_exact_tail(n,d,c,k,grid,target,stamp)
   got=match_count(ins,simulate(ins,answer)[0]);assert got==optimum,(n,d,k,got,optimum)
   assert answer==s.regret_exact_tail(n,d,c,k,grid,target,stamp)
print('PASS 18 exact-three canonical exhaustive optima, K, and determinism cases')
