import sys
with open(sys.argv[1], "r") as f:
    test_input = f.read().splitlines()
with open(sys.argv[2], "r") as f:
    code_output = f.read().splitlines()
    
n,q=map(int, test_input[0].split())    

k=code_output[0]


if k=="No":
    exit(0)

a=[*map(int,code_output[1].split())]

if len(a)!=n:
    print("len")
    exit(1)

for i in range(1,q+1):
    t,u,v=map(int,test_input[i].split())
    if t==0:
        if a[u-1]>a[v-1]:
            print("Not good",t,u,v,a[u-1],a[v-1])
            exit(1)
    else:
        if a[u-1]>=a[v-1]:
            print("Not good",t,u,v,a[u-1],a[v-1])
            exit(1)
            
if all(1<=a[i]<=n for i in range(n)):
    exit(0)
else:
    exit(1)