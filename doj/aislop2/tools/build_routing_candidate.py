"""Reproducible assembly of compact routing experiments from immutable source."""
import argparse
import ast
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.compact_submission import compact_source,pack_source,decode_literal_wrapper,dense_source

parser=argparse.ArgumentParser()
parser.add_argument('--parent',type=int,default=27)
parser.add_argument('--rounds',type=int,default=3)
parser.add_argument('--temporal',type=int,default=0)
parser.add_argument('--removals',type=int,default=0)
parser.add_argument('--repeat',type=int,nargs='+',default=[3])
parser.add_argument('--tail',type=int,nargs='*',default=[])
parser.add_argument('--bits',action='store_true')
parser.add_argument('--plain',action='store_true')
parser.add_argument('--uncapped',action='store_true')
parser.add_argument('--name',required=True)
args=parser.parse_args()
source=next((ROOT/'submissions').glob('best_%03d_*.py'%args.parent)).read_text()
source=source.replace('def solve(n,d,c,k,grid,target,stamp):','def solve_route_parent(n,d,c,k,grid,target,stamp):')
route=(ROOT/'solvers/experiments/route_sparse_fragment.py').read_text()
if args.bits:
    tree=ast.parse(route)
    route='\n\n'.join(ast.unparse(node) for node in tree.body if getattr(node,'name','')=='route_patterns')
    route+='\n\n'+(ROOT/'solvers/experiments/route_bits_fragment.py').read_text().replace('def route_tail_bits(', 'def route_tail(')
temporal=ast.parse((ROOT/'solvers/experiments/temporal_fragment.py').read_text())
keep={'cancel_inverse_pairs'}
if args.temporal:keep|={'best_insertion','deletion_deltas','temporal_repair'}
fragment='\n\n'.join(ast.unparse(node) for node in temporal.body if getattr(node,'name','') in keep)
wrapper=f'''
def solve(n,d,c,k,grid,target,stamp):
    reference=solve_route_parent(n,d,c,k,grid[:],target,stamp[:])
    if k<=2:return reference
    indices,_,ops,_,_=build(n,d,target)
    side=n-d+1
    sequence=cancel_inverse_pairs([(x*side+y)*4+r for x,y,r in reference])
    initial=grid+stamp
'''
if args.temporal:
    wrapper+=f'    sequence=temporal_repair(n,d,k,initial,target,list(zip(indices,ops)),sequence,{args.temporal},{args.removals})\n'
wrapper+=f'''
    final=initial[:]
    for aid in sequence:seq_transition(final,n*n,indices[aid])
    candidate=[ops[aid] for aid in sequence]
    if sum(a==b for a,b in zip(final,target))>=color_bound(initial,target):return candidate
    rounds={str(args.rounds) if args.uncapped else f'min({args.rounds},max(3,3000//(n*n)))'}
'''
if args.tail:
    wrapper+=f'''    for powers,cap in [({tuple(args.repeat)!r},rounds)]+[(tuple([power]),1) for power in {args.tail!r}]:
        if k-len(candidate)<2*min(powers):continue
        tail=route_tail(n,d,final[:n*n],target,final[n*n:],k-len(candidate),powers,cap)
        candidate.extend(tail)
        for x,y,r in tail:seq_transition(final,n*n,indices[(x*side+y)*4+r])
    return candidate
'''
else:
    wrapper+=f'    return candidate+route_tail(n,d,final[:n*n],target,final[n*n:],k-len(candidate),{tuple(args.repeat)!r},rounds)\n'
source=source.replace('def main():',route+'\n\n'+fragment+'\n\n'+wrapper+'\n\ndef main():')
plain=ROOT/'solvers/experiments'/f'{args.name}_source.py'
output=ROOT/'solvers/experiments'/f'{args.name}.py'
plain.write_text(source,encoding='utf8')
if args.plain:
    original=ast.unparse(ast.parse(source))
    dense=dense_source(original)
    assert ast.dump(ast.parse(dense),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False)
    output.write_text(dense,encoding='utf8',newline='\n')
else:
    dense=compact_source(source)
    packed=pack_source(dense,'latin1')
    assert decode_literal_wrapper(packed)==dense
    output.write_bytes(packed.encode('latin1'))
print(output.name,len(output.read_bytes()),'bytes')
