import ast,importlib.util,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate
from tools.compact_submission import decode_literal_wrapper

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);return s
new=load('solvers/experiments/regret_wildcard_source.py','new')
packed=load('solvers/experiments/regret_wildcard.py','packed')
old=load('submissions/best_027_251280679.py','old')
source_ast=ast.parse((ROOT/'solvers/experiments/regret_wildcard_source.py').read_text())
dense_ast=ast.parse((ROOT/'solvers/experiments/regret_wildcard_plain.py').read_text())
renaming=dict(zip([n.name for n in source_ast.body if isinstance(n,ast.FunctionDef)],[n.name for n in dense_ast.body if isinstance(n,ast.FunctionDef)]))
packed_finish=getattr(packed,renaming['wildcard_finish'])
rng=random.Random(817244)
transition_checks=0
expand=new.packed_transitions()
for c in (2,6):
 for _ in range(12):
  grid=[rng.randrange(c) for _ in range(16)];stamp=[rng.randrange(c) for _ in range(9)]
  ins=Instance(4,3,c,1,grid,grid,stamp);state=sum(v<<(3*p) for p,v in enumerate(grid+stamp))
  for aid,child in expand(state):
   board,buffer=simulate(ins,[(aid//8,(aid//4)%2,aid%4)])
   assert child==sum(v<<(3*p) for p,v in enumerate(board+buffer))
   assert dict(expand(child))[aid]==state
   transition_checks+=1
binary=0
for k in range(1,6):
 for _ in range(6):
  grid=[rng.randrange(2) for _ in range(16)];stamp=[rng.randrange(2) for _ in range(9)]
  ins=Instance(4,3,2,k,grid,grid,stamp)
  if _<3:
   target=simulate(ins,[(rng.randrange(2),rng.randrange(2),rng.randrange(4)) for _ in range(k)])[0]
  else:target=[rng.randrange(2) for _ in range(16)]
  reference=old.binary_bfs(grid,target,stamp,k)
  candidate=new.wildcard_finish(grid,target,stamp,k,depth=5)
  assert (reference is None)==(candidate is None),(k,reference,candidate)
  if candidate is not None:
   assert len(candidate)<=k
   assert simulate(ins,[(a//8,(a//4)%2,a%4) for a in candidate])[0]==target
  binary+=1
reachable=0
for depth in range(1,9):
 c=rng.randrange(2,7);grid=[rng.randrange(c) for _ in range(16)];stamp=[rng.randrange(c) for _ in range(9)]
 ins=Instance(4,3,c,depth,grid,grid,stamp)
 target=simulate(ins,[(rng.randrange(2),rng.randrange(2),rng.randrange(4)) for _ in range(depth)])[0]
 candidate=new.wildcard_finish(grid,target,stamp,depth)
 assert candidate is not None and len(candidate)<=depth
 assert simulate(ins,[(a//8,(a//4)%2,a%4) for a in candidate])[0]==target
 assert candidate==packed_finish(grid,target,stamp,depth)
 reachable+=1
escapes=0
for n,d in ((3,2),(4,3),(8,2),(9,3)):
 for _ in range(4):
  c=4;grid=[rng.randrange(c) for _ in range(n*n)];stamp=[rng.randrange(c) for _ in range(d*d)];target=[rng.randrange(c) for _ in range(n*n)]
  for typ in ('State','ProductiveState'):
   a=getattr(old,typ)(n,d,c,grid[:],target,stamp[:]);b=new.State(n,d,c,grid[:],target,stamp[:])
   kwargs=dict(width=12)
   if typ=='ProductiveState':kwargs['min_gain']=rng.choice((-2,0,1))
   assert a.escape(random.Random(121),**kwargs)==b.escape(random.Random(121),**kwargs)
   assert a.grid==b.grid and a.stamp==b.stamp
   escapes+=1
payload=(ROOT/'solvers/experiments/regret_wildcard.py').read_bytes();assert len(payload)<=10000
assert decode_literal_wrapper(payload.decode('latin1'))==(ROOT/'solvers/experiments/regret_wildcard_plain.py').read_text()
report=dict(transitions=transition_checks,binary_replacement_parity=binary,reachable_and_packed_parity=reachable,escape_dedup_parity=escapes,bytes=len(payload))
(ROOT/'results/regret_wildcard_verification.json').write_text(json.dumps(report,indent=2));print('PASS',report)
