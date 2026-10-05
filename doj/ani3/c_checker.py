import sys

MO="AEIOU"
JA="BCDFGHJKLMNPQRSTVWXYZ"

with open(sys.argv[1], "r") as f:
    test_input = f.read()
with open(sys.argv[2], "r") as f:
    code_output = f.read()
    
n,m=map(int,test_input.split())
r,*d=code_output.split()
if (m==1 and n>26) or n>10:
    if r!='NO': 
        print('a')
        exit(1)
    exit(0)

if any([len(x)!=m for x in d]):
    print('b')
    exit(1)

for j in range(m):
    s=set()
    for i in range(n):
        if d[i][j] in s:
            print('c')
            exit(1)
        s.add(d[i][j])
        
        if j==0 or ((d[i][j] in MO and d[i][j-1] in JA) or (d[i][j] in JA and d[i][j-1] in MO)):
            pass
        else:
            print('d')
            print(d[i][j-1],d[i][j],j)
            exit(1)
