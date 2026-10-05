"""Build a standalone, retained-parent i1 experiment from its reviewed fragment."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='solvers/experiments/i1_block_beam.py')
    parser.add_argument('--rounds', type=int, default=8)
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--nodes', type=int, default=160000)
    parser.add_argument('--internal-first', action='store_true')
    args = parser.parse_args()
    source = (ROOT/'submissions/runtime_049_252862932.py').read_text(encoding='utf-8')
    fragment = (ROOT/'solvers/experiments/i1_block_fragment.py').read_text(encoding='utf-8')
    if args.internal_first:
        old = 'left=len(best)-span if trial%4 in (0,3) else rng.randrange(len(best)-span+1)'
        new = 'left=len(best)-span if trial%4==3 else rng.randrange(len(best)-span+1)'
        if fragment.count(old) != 1:
            raise ValueError('internal-first build expected one trial-position expression')
        fragment = fragment.replace(old, new)
    wrapper = '''
_i1_parent = solve

def solve(n,d,c,k,grid,target,stamp):
    reference = _i1_parent(n,d,c,k,grid[:],target,stamp[:])
    if k < 4:
        return reference
    indices,_,ops,_,_ = build(n,d,target)
    span = n-d+1
    sequence = [(x*span+y)*4+r for x,y,r in reference]
    candidate = i1_block_repair(n,d,c,k,grid+stamp,target,list(zip(indices,ops)),sequence,
                              rounds=%d,width=%d,node_budget=%d)
    return [ops[aid] for aid in candidate]

''' % (args.rounds, args.width, args.nodes)
    prefix, entry = source.rsplit('def main():', 1)
    candidate = prefix+fragment+'\n'+wrapper+'def main():'+entry
    data = candidate.encode('utf-8')
    if len(data) > 100000:
        raise ValueError('source exceeds contest 100000-byte limit: '+str(len(data)))
    compile(candidate, args.output, 'exec')
    (ROOT/args.output).write_bytes(data)
    print(args.output, len(data), 'bytes')


if __name__ == '__main__':
    main()
