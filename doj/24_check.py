import sys

with open(sys.argv[1], "r") as f:
    test_input = f.read()
with open(sys.argv[2], "r") as f:
    code_output = f.read()
    
n=int(test_input)
a=[*map(int,code_output.split())]

if len(a)!=n:
    print("! LEN")
    exit(1)

if sorted(a)!=[*range(1,n+1)]:
    print("! PERMUTATION")
    exit(1)

for i in range(1,n+1):
    x=a[i-1]
    k=x+i
    if (k & (k - 1)) != 0:
        print("! 2^k",i-1)
        exit(1)