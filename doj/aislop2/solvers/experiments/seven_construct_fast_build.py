"""Build and audit the self-contained exact cluster-state speed variant."""
import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
source_path=ROOT/'solvers/experiments/seven_construct_combined_readable.py'
bytearray_mode='--bytearray' in sys.argv
fragment_path=ROOT/('solvers/experiments/seven_construct_fast_state_bytearray.py'if bytearray_mode else 'solvers/experiments/seven_construct_fast_state.py')
output_path=ROOT/('solvers/experiments/seven_construct_fast_bytearray_readable.py'if bytearray_mode else 'solvers/experiments/seven_construct_fast_readable.py')
source=source_path.read_text()
tree=ast.parse(source)
function=next(node for node in tree.body if isinstance(node,ast.FunctionDef)and node.name=='cluster_improve')
lines=source.splitlines(keepends=True)
body=''.join(lines[function.lineno-1:function.end_lineno])
assert body.count('initial=State(')==1 and body.count('child=clone_state(state)')==1
replacement=body.replace('initial=State(','initial=ClusterState(').replace('child=clone_state(state)','child=clone_cluster_state(state)')
result=''.join(lines[:function.lineno-1])+fragment_path.read_text()+'\n\n'+replacement+''.join(lines[function.end_lineno:])
compile(result,str(output_path),'exec')
output_path.write_text(result)
output_tree=ast.parse(result)
output_functions={node.name:node for node in output_tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
unchanged=[]
for node in tree.body:
    if isinstance(node,(ast.FunctionDef,ast.ClassDef))and node.name!='cluster_improve':
        # Duplicate definitions are intentional: compare against any same-name
        # output node instead of only the latest global binding.
        assert any(type(other)is type(node)and getattr(other,'name',None)==node.name and
                   ast.dump(other,include_attributes=False)==ast.dump(node,include_attributes=False)
                   for other in output_tree.body)
        unchanged.append(node.name)
expected=ast.parse(replacement).body[0]
assert ast.dump(expected,include_attributes=False)==ast.dump(output_functions['cluster_improve'],include_attributes=False)
review=dict(parent=str(source_path.relative_to(ROOT)),parent_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
            output=str(output_path.relative_to(ROOT)),output_sha256=hashlib.sha256(output_path.read_bytes()).hexdigest(),
            bytes=output_path.stat().st_size,only_replaced_calls=['State -> ClusterState in cluster_improve','clone_state -> clone_cluster_state in cluster_improve'],
            unchanged_definitions=len(unchanged),heuristic_logic_unchanged=True)
(ROOT/('results/seven_construct_fast_bytearray_static.json'if bytearray_mode else 'results/seven_construct_fast_static.json')).write_text(json.dumps(review,indent=2))
print(review)
