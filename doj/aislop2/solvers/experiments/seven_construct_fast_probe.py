"""Exact-output and isolated runtime diagnostics for private cluster state."""
import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,parse_instance,format_instance,simulate,match_count
from tools.validate_output import validate_output
from tools.check_submission import readiness_cases

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def main():
    paths=[ROOT/'solvers/experiments'/name for name in
           ('seven_construct_combined_readable.py','seven_construct_fast_readable.py','seven_construct_fast_bytearray_readable.py')]
    names=['parent','planes','bytearray']
    modules=[load(name,path)for name,path in zip(names,paths)]
    rng=random.Random(741931);checks=0
    m=modules[2]
    for n in (3,5,16,30):
        for d in (2,3):
            for c in (2,6):
                target=[rng.randrange(c)for _ in range(n*n)]
                grid=[rng.randrange(c)for _ in target];stamp=[rng.randrange(c)for _ in range(d*d)]
                normal=m.State(n,d,c,grid[:],target,stamp[:])
                quick=m.ClusterState(n,d,c,grid[:],target,stamp[:])
                fixed_counts=quick.counts[:];fixed_mask=quick.stampmask
                pool=[(normal,quick)]
                for step in range(60):
                    normal,quick=rng.choice(pool)
                    child=m.clone_state(normal);fast=m.clone_cluster_state(quick)
                    assert fast.counts is quick.counts and fast._runtime_cover_bits is quick._runtime_cover_bits
                    original=(bytes(quick.grid),bytes(quick.stamp),quick.old_planes[:])
                    aid=rng.randrange(len(child.actions)//4)*4+step%4
                    child.apply(aid);fast.apply(aid)
                    assert child.grid==list(fast.grid) and child.stamp==list(fast.stamp)
                    assert child.matches==fast.matches and child.old_planes==fast.old_planes
                    assert fast.counts==fixed_counts and fast.stampmask==fixed_mask
                    assert (bytes(quick.grid),bytes(quick.stamp),quick.old_planes)==original
                    ins=Instance(n,d,c,1,normal.grid[:],target,normal.stamp[:])
                    cg,cs=simulate(ins,[child.actions[aid][1]])
                    assert (list(fast.grid),list(fast.stamp))==(cg,cs) and fast.matches==match_count(ins,cg)
                    assert child.best()==fast.best()
                    seed=rng.randrange(10**9)
                    assert m.million_choices(child,random.Random(seed),8)==m.million_choices(fast,random.Random(seed),8)
                    pool.append((child,fast));pool=pool[-8:];checks+=1
    print('bytearray canonical transition/best/choice checks',checks,flush=True)
    cases=[('case_001',parse_instance((ROOT/'cases/generated/case_001.in').read_text()))]
    cases.extend((name,ins)for name,ins in readiness_cases(0)if ins.n==30 and ins.d==3)
    rows=[]
    for case_name,ins in cases:
        expected=None
        for name,path in zip(names,paths):
            start=time.perf_counter()
            process=subprocess.run([sys.executable,'-I','-B',str(path)],input=format_instance(ins).encode(),capture_output=True,timeout=8)
            elapsed=time.perf_counter()-start
            assert process.returncode==0 and not process.stderr,(name,case_name,process.stderr)
            operations=validate_output(ins,process.stdout)
            matches=match_count(ins,simulate(ins,operations)[0])
            if expected is None:expected=process.stdout
            assert process.stdout==expected,(name,case_name,'different output')
            row=dict(case=case_name,variant=name,runtime_sec=elapsed,matches=matches,
                     output_sha256=hashlib.sha256(process.stdout).hexdigest(),exact_output=True)
            rows.append(row);print(row,flush=True)
    helper_rows=[]
    ins=cases[-1][1]
    expected=None
    for repeat in range(2):
        for name,module in zip(names,modules):
            start=time.perf_counter()
            operations=module.cluster_improve(ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,[],width=16)
            elapsed=time.perf_counter()-start
            if expected is None:expected=operations
            assert operations==expected,(name,'helper different operations')
            helper_rows.append(dict(variant=name,repeat=repeat,runtime_sec=elapsed,exact_operations=True))
            print('helper',name,repeat,round(elapsed,4),flush=True)
    report=dict(canonical_bytearray_checks=checks,source_sha256={name:hashlib.sha256(path.read_bytes()).hexdigest()for name,path in zip(names,paths)},
                standalone=rows,helper=helper_rows,all_outputs_identical=True)
    (ROOT/'results/seven_construct_fast_boundary_probe.json').write_text(json.dumps(report,indent=2))
    print('saved isolated boundary and helper profile',flush=True)

if __name__=='__main__':main()
