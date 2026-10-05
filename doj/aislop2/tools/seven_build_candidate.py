"""Assemble reverse-construction candidate from readable standard-library sources."""
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parent=(ROOT/'solvers/experiments/million_safe_readable.py').read_text()
tree=ast.parse((ROOT/'solvers/experiments/seven_fastback.py').read_text())
class Inline(ast.NodeTransformer):
    def visit_Attribute(self,node):
        self.generic_visit(node)
        if isinstance(node.value,ast.Name)and node.value.id=='m':return ast.copy_location(ast.Name(node.attr,node.ctx),node)
        return node
for node in tree.body:
    if isinstance(node,ast.FunctionDef)and node.name=='construct':
        node.name='seven_backward_construct';node.args.args.pop(0)
tree=Inline().visit(tree);ast.fix_missing_locations(tree)
fragment=ast.unparse(tree)
hook='''
_seven_original_retained=solve_retained_iterated
def solve_retained_iterated(n,d,c,k,grid,target,stamp):
    if n<10 or k<12:
        return _seven_original_retained(n,d,c,k,grid,target,stamp)
    base=sum(a==b for a,b in zip(grid,target))
    if 100*base>=88*color_bound(grid+stamp,target):
        return _seven_original_retained(n,d,c,k,grid,target,stamp)
    patterns=set()
    for x in range(n-d+1):
        for y in range(n-d+1):
            patterns.add(tuple(target[(x+i)*n+y+j]for i in range(d)for j in range(d)))
            if len(patterns)>4*c:
                return _seven_original_retained(n,d,c,k,grid,target,stamp)
    return seven_backward_construct(n,d,c,k,grid,target,stamp,width=48)
'''
pos=parent.rindex('def main():')
source=parent[:pos]+fragment+'\n'+hook+'\n'+parent[pos:]
out=ROOT/'solvers/experiments/seven_reverse_integrated_readable.py'
out.write_text(source,encoding='utf8',newline='\n')
compile(source,str(out),'exec')
print(out,len(source.encode()))
