import sys,math
from itertools import permutations

with open(sys.argv[1], "r") as f:
    test_input = iter(f.read().splitlines()).__next__
with open(sys.argv[2], "r") as f:
    code_output = iter(f.read().splitlines()).__next__
    
n=int(test_input())
s=code_output().strip()
if len(s)>10000:
    print("! len")
    exit(1)
for x in permutations(range(1,n+1),n):
    y="".join(map(str,x))
    if y not in s:
        print("!",y)
        exit(1)