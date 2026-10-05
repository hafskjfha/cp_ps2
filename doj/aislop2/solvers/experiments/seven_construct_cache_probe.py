"""Isolated stamp-plane cache ablation and exact-output diagnostic."""
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
from tools.simulate import parse_instance,format_instance,simulate,match_count
from tools.validate_output import validate_output
from tools.check_submission import readiness_cases

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    names=['parent','uncached','cached']
    filenames=['seven_construct_fast_bytearray_readable.py','seven_construct_uncached_readable.py','seven_construct_cached_readable.py']
    paths=[ROOT/'solvers/experiments'/name for name in filenames]
    modules=[load(name,path)for name,path in zip(names,paths)]
    rng=random.Random(931047);checks=0;clears=0
    parent,cached=modules[0],modules[2]
    for n in (3,8,30):
        for d in (2,3):
            c=6;grid=[rng.randrange(c)for _ in range(n*n)];target=[rng.randrange(c)for _ in grid];stamp=[rng.randrange(c)for _ in range(d*d)]
            base=parent.ClusterState(n,d,c,grid[:],target,stamp[:])
            cached.CachedClusterState.cache_limit=2
            fast=cached.CachedClusterState(n,d,c,grid[:],target,stamp[:])
            pool=[(base,fast)]
            for step in range(80):
                a,b=rng.choice(pool);x=parent.clone_cluster_state(a);y=cached.clone_cached_cluster_state(b)
                assert y._stamp_score_cache is b._stamp_score_cache
                aid=rng.randrange(len(x.actions)//4)*4+step%4;x.apply(aid);y.apply(aid)
                assert x.grid==y.grid and x.stamp==y.stamp and x.old_planes==y.old_planes and x.matches==y.matches
                assert x.best_candidates()==y.best_candidates()
                seed=rng.randrange(10**9);ra=random.Random(seed);rb=random.Random(seed)
                assert parent.million_choices(x,ra,8)==cached.cached_cluster_choices(y,rb,8)
                assert ra.getstate()==rb.getstate()
                assert len(y._stamp_score_cache)<=2
                assert all(isinstance(value,tuple)for value in y._stamp_score_cache.values())
                pool.append((x,y));pool=pool[-8:];checks+=1
    cached.CachedClusterState.cache_limit=8192
    print('exact cache/forced-eviction/choice/RNG checks',checks,flush=True)
    cases=[('case_001',parse_instance((ROOT/'cases/generated/case_001.in').read_text()))]
    cases.extend((name,ins)for name,ins in readiness_cases(0)if ins.n==30 and ins.d==3)
    rows=[]
    for case_name,ins in cases:
        expected=None
        for name,path in zip(names,paths):
            start=time.perf_counter()
            p=subprocess.run([sys.executable,'-I','-B',str(path)],input=format_instance(ins).encode(),capture_output=True,timeout=8)
            elapsed=time.perf_counter()-start
            assert p.returncode==0 and not p.stderr,(name,case_name,p.stderr)
            operations=validate_output(ins,p.stdout);matches=match_count(ins,simulate(ins,operations)[0])
            if expected is None:expected=p.stdout
            assert p.stdout==expected,(name,case_name)
            row=dict(case=case_name,variant=name,runtime_sec=elapsed,matches=matches,output_sha256=hashlib.sha256(p.stdout).hexdigest(),exact_output=True)
            rows.append(row);print(row,flush=True)
    helper=[];ins=cases[-1][1];expected=None
    for repeat in range(2):
        for name,m in zip(names,modules):
            start=time.perf_counter();operations=m.cluster_improve(ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,[],width=16)
            elapsed=time.perf_counter()-start
            if expected is None:expected=operations
            assert operations==expected
            helper.append(dict(variant=name,repeat=repeat,runtime_sec=elapsed));print('helper',name,repeat,round(elapsed,4),flush=True)
    stats=dict(gets=0,hits=0,misses=0,clears=0,max_entries=0)
    class CountingCache(dict):
        def get(self,key,default=None):
            stats['gets']+=1;value=super().get(key,default)
            stats['hits'if value is not None else 'misses']+=1
            return value
        def clear(self):stats['clears']+=1;super().clear()
        def __setitem__(self,key,value):
            super().__setitem__(key,value);stats['max_entries']=max(stats['max_entries'],len(self))
    old_init=cached.CachedClusterState.__init__
    def counted_init(self,*args):old_init(self,*args);self._stamp_score_cache=CountingCache()
    cached.CachedClusterState.__init__=counted_init
    assert cached.cluster_improve(ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,[],width=16)==expected
    stats['hit_rate']=stats['hits']/stats['gets']
    report=dict(source_sha256={name:hashlib.sha256(path.read_bytes()).hexdigest()for name,path in zip(names,paths)},
                exact_state_choice_rng_checks=checks,forced_cache_limit=2,standalone=rows,helper=helper,cache_profile=stats,all_outputs_identical=True)
    (ROOT/'results/seven_construct_cache_probe.json').write_text(json.dumps(report,indent=2));print(stats,flush=True)

if __name__=='__main__':main()
