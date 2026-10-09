def query(a,b):
    print(a,b,flush=True)

x1=int(input())
a1=1+(x1==13)
query(a1,0)
x2=int(input())
query(12,1)
int(input())
query(1,0)

while 1:
    x=int(input())
    if x==-1:break
    query(14-x,0)