"""Compose cache/no-cache ablation variants without editing measured sources."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
parent_path=ROOT/'solvers/experiments/seven_construct_fast_bytearray_readable.py'
source=parent_path.read_text()
tree=ast.parse(source);lines=source.splitlines(keepends=True)
choices=next(node for node in tree.body if isinstance(node,ast.FunctionDef)and node.name=='million_choices')
choice_text=''.join(lines[choices.lineno-1:choices.end_lineno])
position=choice_text.index('    remaining = state.all_actions')
choice_text='def cached_cluster_choices(state,rng,branch=6):\n    planes=state._combined_score_planes()\n'+choice_text[position:]
state_text=(ROOT/'solvers/experiments/seven_construct_cache_state.py').read_text()
cluster=next(node for node in tree.body if isinstance(node,ast.FunctionDef)and node.name=='cluster_improve')
cluster_text=''.join(lines[cluster.lineno-1:cluster.end_lineno])
changed=cluster_text.replace('initial=ClusterState(','initial=CachedClusterState(')
changed=changed.replace('child=clone_cluster_state(state)','child=clone_cached_cluster_state(state)')
changed=changed.replace('million_choices(state,rng,8)','cached_cluster_choices(state,rng,8)')
assert changed!=cluster_text
reports=[]
for limit,suffix in ((8192,'cached'),(0,'uncached')):
    fragment=state_text.replace('cache_limit=8192','cache_limit='+str(limit))+'\n\n'+choice_text+'\n\n'
    text=''.join(lines[:cluster.lineno-1])+fragment+changed+''.join(lines[cluster.end_lineno:])
    output=ROOT/('solvers/experiments/seven_construct_'+suffix+'_readable.py')
    compile(text,str(output),'exec');output.write_text(text)
    result_tree=ast.parse(text)
    old=[ast.dump(node,include_attributes=False)for node in tree.body if node is not cluster]
    new=[ast.dump(node,include_attributes=False)for node in result_tree.body]
    assert all(item in new for item in old)
    # The random tie selection and all other action selection statements must
    # remain verbatim apart from the source of their combined score planes.
    fresh_choices=next(node for node in result_tree.body if isinstance(node,ast.FunctionDef)and node.name=='cached_cluster_choices')
    tail_start=next(i for i,node in enumerate(choices.body)if isinstance(node,ast.Assign)and
                    isinstance(node.targets[0],ast.Name)and node.targets[0].id=='remaining')
    assert [ast.dump(node,include_attributes=False)for node in choices.body[tail_start:]]==[ast.dump(node,include_attributes=False)for node in fresh_choices.body[1:]]
    reports.append(dict(cache_limit=limit,path=str(output.relative_to(ROOT)),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                        original_ast_nodes_preserved=True,action_selection_tail_identical=True))
report=dict(parent=str(parent_path.relative_to(ROOT)),parent_sha256=hashlib.sha256(parent_path.read_bytes()).hexdigest(),variants=reports)
(ROOT/'results/seven_construct_cache_static.json').write_text(json.dumps(report,indent=2));print(report)
