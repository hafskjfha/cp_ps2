import sys
input=sys.stdin.readline

n,q=map(int,input().split())
p=0
for _ in range(q):
    c,x=map(int,input().split())
    if c==1:
        p=(p+x)%n
    elif c==2:
        p=(p-x)%n
    else:
        pp=(n-p+x-1)
        print(pp%n+1)