import sys

with open(sys.argv[1], "r") as f:
    test_input = f.read()
with open(sys.argv[2], "r") as f:
    code_output = f.read()
    
n,m=map(int,test_input.split())
a=[*map(int,code_output.split())]

if len(a)!=m:
    print("len miss")
    exit(1)

sum=0
for i in range(m-1):
    sum+=a[i]^a[i+1]
    
sum+=a[0]^a[-1]

if sum!=n:
    print("sum miss")
    exit(1)