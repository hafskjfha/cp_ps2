"""Canonical full-suite exact-output parity check for runtime-only candidates."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

path=ROOT/'solvers/experiments/m2_sequence_runtime_csa.py'
source_hash=hashlib.sha256(path.read_bytes()).hexdigest()
cache=json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']
results=[]
for parent in cache:
    data=(ROOT/'cases/generated'/(parent['id']+'.in')).read_bytes()
    instance=parse_instance(data.decode())
    start=time.perf_counter()
    process=subprocess.run([sys.executable,'-I','-B',str(path)],input=data,capture_output=True,timeout=20)
    elapsed=time.perf_counter()-start
    assert not process.returncode and not process.stderr,(parent['id'],process.stderr)
    digest=hashlib.sha256(process.stdout).hexdigest()
    assert digest==parent['output_sha256'],(parent['id'],digest,parent['output_sha256'])
    operations=validate_output(instance,process.stdout)
    matches=match_count(instance,simulate(instance,operations)[0])
    assert matches==parent['matches']
    results.append(dict(id=parent['id'],matches=matches,score=1000000*matches//instance.n**2,
                        output_sha256=digest,runtime_sec=elapsed))
    if len(results)%20==0:print(len(results),'exact',round(sum(r['runtime_sec'] for r in results),3),flush=True)
assert source_hash==hashlib.sha256(path.read_bytes()).hexdigest()
result=dict(solver=str(path),solver_sha256=source_hash,diagnostic_only=True,cases=len(results),
            total_score=sum(r['score'] for r in results),max_runtime_sec=max(r['runtime_sec'] for r in results),
            total_runtime_sec=sum(r['runtime_sec'] for r in results),results=results)
(ROOT/'results/m2_sequence_runtime_parity320.json').write_text(json.dumps(result,indent=2))
print({k:v for k,v in result.items() if k!='results'},flush=True)
