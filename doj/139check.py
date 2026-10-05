import sys

with open(sys.argv[1], "r") as f:
    test_input = f.read()
with open(sys.argv[2], "r") as f:
    code_output = f.read()
    
n,k=map(int,test_input.split())
a=[*map(int,code_output.split())]

def mex(s):
    for i in range(len(s)+2):
        if i not in s:
            return i

s=set()
for i in range(n):
    for j in range(i,n):
        s.add(mex(a[i:j+1]))
        print(a[i:j+1])

if mex(s)==k:
    print(s)
    print(mex(s))
    print("OK")
else:
    print(s)
    print(mex(s))
    print("NO")
    exit(1)