import sys,math

with open(sys.argv[1], "r") as f:
    test_input = iter(f.read().splitlines()).__next__
with open(sys.argv[2], "r") as f:
    code_output = iter(f.read().splitlines()).__next__
    
n=int(test_input())
arr=[[*range(n+1)]+[*range(n+1)],[-1]*(2*n)]

m=int(code_output())
for _ in range(m):
    r,c,d=code_output().split()
    r,c=int(r),int(c)
    if d=="U":
        ...
    elif d=="D":
        ...
    elif d=="L":
        ...
    elif d=="R":
        ...
    else:
        print("Not ok d")
        exit(1)
        
target=[[-1]*(2*n+1),[-1]*(2*n+1)]
print(target)
for i in range(n):
    target[0][2*i+1]=i+1
    target[0][2*i+2]=i+1

assert arr==target