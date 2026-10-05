"""Thirteen fixed small-board holdouts and independent deeper-beam probes.

Official timings execute the frozen candidate unchanged. A separate diagnostic
run counts beam layers without changing their results and must reproduce the
official output after newline normalization.
"""
import argparse
import hashlib
import heapq
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time

if __package__:
    from . import check_submission, anneal_late_holdout
    from .simulate import Instance, format_instance, parse_instance, simulate
else:
    import check_submission
    import anneal_late_holdout
    from simulate import Instance, format_instance, parse_instance, simulate


def probe(path, instance):
    spec=importlib.util.spec_from_file_location('pool_deeper_candidate',path)
    solver=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    evidence={'reference':None,'calls':[]}
    original_reference=solver.solve_without_deeper_beam
    original_finish=solver.deeper_beam_finish

    def reference(n,d,c,k,grid,target,stamp):
        operations=original_reference(n,d,c,k,grid,target,stamp)
        board,_=simulate(Instance(n,d,c,k,grid[:],target,stamp[:]),operations)
        missing=sum(a!=b for a,b in zip(board,target))
        evidence['reference']={'operations':len(operations),'missing':missing,
                               'spare_operations':k-len(operations),
                               'eligible':5<=n<=9 and d==3 and
                                          k-len(operations)>=3 and 1<=missing<=8}
        return operations

    def finish(n,grid,target,stamp,k):
        before=sum(a==b for a,b in zip(grid,target))
        row={'remaining_operations':k,'initial_matches':before,
             'missing':n*n-before,'color_bound':solver.color_bound(grid+stamp,target),
             'completed_layers':0,'max_depth_reached':0,'expanded_states':0,
             'retained_frontier_sizes':[]}
        original_expand_factory=solver.packed3_transitions
        original_nlargest=heapq.nlargest

        def expand_factory(size):
            expand=original_expand_factory(size)
            def counted_expand(state):
                row['expanded_states']+=1
                row['max_depth_reached']=max(row['max_depth_reached'],
                                             row['completed_layers']+1)
                return expand(state)
            return counted_expand

        def retained(*args,**kwargs):
            selected=original_nlargest(*args,**kwargs)
            row['completed_layers']+=1
            row['retained_frontier_sizes'].append(len(selected))
            return selected

        solver.packed3_transitions=expand_factory
        heapq.nlargest=retained
        started=time.perf_counter()
        try:
            tail=original_finish(n,grid,target,stamp,k)
        finally:
            solver.packed3_transitions=original_expand_factory
            heapq.nlargest=original_nlargest
        row['diagnostic_runtime_sec']=time.perf_counter()-started
        row['returned_operations']=None if tail is None else len(tail)
        row['successful_repair']=tail is not None
        if tail is not None:
            width=n-2
            operations=[(aid//4//width,aid//4%width,aid%4) for aid in tail]
            final,_=simulate(Instance(n,3,instance.c,k,grid[:],target,stamp[:]),operations)
            row['final_matches']=sum(a==b for a,b in zip(final,target))
            assert row['final_matches']>before
            assert len(tail)<=min(8,k)
        evidence['calls'].append(row)
        return tail

    solver.solve_without_deeper_beam=reference
    solver.deeper_beam_finish=finish
    operations=solver.solve(instance.n,instance.d,instance.c,instance.k,
                            instance.a[:],instance.t,instance.s[:])
    simulate(instance,operations)
    output=str(len(operations))+'\n'+''.join(f'{x} {y} {r}\n' for x,y,r in operations)
    evidence.update(normalized_output_sha256=hashlib.sha256(output.encode('ascii')).hexdigest(),
                    attempted_calls=len(evidence['calls']),
                    actual_search_calls=sum(row['expanded_states']>0 for row in evidence['calls']),
                    successful_repairs=sum(row['successful_repair'] for row in evidence['calls']),
                    depth8_calls=sum(row['max_depth_reached']>=8 for row in evidence['calls']))
    return evidence


def run(path,output_path,timeout):
    source=path.resolve().read_bytes()
    recipes=anneal_late_holdout.configurations()
    assert len(recipes)==13
    report={'kind':'deeper_beam_fixed13_small_board_holdout','version':1,
            'solver':str(path.resolve()),'solver_sha256':hashlib.sha256(source).hexdigest(),
            'python':sys.version,'jobs':1,'timeout_sec':timeout,
            'timing_scope':'Unchanged fresh subprocesses, shared machine load; not isolated stress.',
            'recipes_source':str(Path(anneal_late_holdout.__file__).resolve()),
            'recipes_source_sha256':hashlib.sha256(Path(anneal_late_holdout.__file__).read_bytes()).hexdigest(),
            'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seed':anneal_late_holdout.SEED,'all_reserve_recipes_run':True,'cases':[]}
    with tempfile.TemporaryDirectory(prefix='pool-deeper-holdout-') as directory:
        snapshot=Path(directory)/path.name
        snapshot.write_bytes(source)
        report['static']=check_submission.inspect_source(snapshot)
        assert report['static']['valid'],report['static']
        for recipe in recipes:
            case=anneal_late_holdout.make_case(recipe)
            text=format_instance(case)
            row,output=check_submission.run_solver(snapshot,case,timeout,directory)
            row.update(recipe,input=text,input_sha256=hashlib.sha256(text.encode('ascii')).hexdigest(),
                       canonical_valid=row['valid'],output_sha256=hashlib.sha256(output).hexdigest(),
                       normalized_output_sha256=hashlib.sha256(output.replace(b'\r\n',b'\n')).hexdigest())
            try:
                diagnostic=subprocess.run([sys.executable,str(Path(__file__).resolve()),
                                           str(snapshot),'--probe'],input=text.encode('ascii'),
                                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                          cwd=directory,timeout=max(12,3*timeout),check=True)
                assert not diagnostic.stderr,diagnostic.stderr
                evidence=json.loads(diagnostic.stdout)
                row['diagnostic']=evidence
                row['diagnostic_output_parity']=evidence['normalized_output_sha256']==row['normalized_output_sha256']
                if not row['diagnostic_output_parity']:
                    row.update(valid=False,error='Diagnostic wrapper changed normalized solver output.')
            except (subprocess.SubprocessError,ValueError,AssertionError) as exc:
                row.update(valid=False,diagnostic_error=str(exc))
            report['cases'].append(row)
            output_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
            evidence=row.get('diagnostic',{})
            print(f"{recipe['id']}: valid={row['valid']} time={row['runtime_sec']:.3f}s "
                  f"searches={evidence.get('actual_search_calls','?')} "
                  f"depth8={evidence.get('depth8_calls','?')} "
                  f"repairs={evidence.get('successful_repairs','?')}",flush=True)
    rows=report['cases']
    report.update(passed=all(row['valid'] for row in rows),cases_total=len(rows),
                  cases_passed=sum(row['valid'] for row in rows),
                  max_runtime_sec=max(row['runtime_sec'] for row in rows),
                  avg_runtime_sec=statistics.mean(row['runtime_sec'] for row in rows),
                  branch_executed_cases=sum(row.get('diagnostic',{}).get('attempted_calls',0)>0 for row in rows),
                  actual_search_cases=sum(row.get('diagnostic',{}).get('actual_search_calls',0)>0 for row in rows),
                  depth8_cases=sum(row.get('diagnostic',{}).get('depth8_calls',0)>0 for row in rows),
                  successful_repair_cases=sum(row.get('diagnostic',{}).get('successful_repairs',0)>0 for row in rows),
                  total_score=sum(row.get('score',0) for row in rows),
                  source_unchanged=hashlib.sha256(path.resolve().read_bytes()).hexdigest()==report['solver_sha256'])
    output_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:report[key] for key in ('passed','cases_total','cases_passed',
          'max_runtime_sec','avg_runtime_sec','branch_executed_cases','actual_search_cases',
          'depth8_cases','successful_repair_cases','source_unchanged')}),flush=True)
    return report['passed']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--timeout',type=float,default=5)
    parser.add_argument('--probe',action='store_true')
    args=parser.parse_args()
    if args.probe:
        print(json.dumps(probe(args.solver,parse_instance(sys.stdin.read()))))
        return 0
    if args.output is None:parser.error('--output is required')
    return 0 if run(args.solver,args.output,args.timeout) else 1


if __name__=='__main__':
    raise SystemExit(main())
