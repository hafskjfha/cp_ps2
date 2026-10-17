import sys
input=sys.stdin.readline

def log(x):
    r=1
    t=0
    while r*2<=x:
        r*=2
        t+=1
    return t+1

def solve():
    n=int(input())
    k=log(n)
    temp=[[0]*(k+1)for _ in range(n+1)]
    
    po=1
    x,y=None,None
    for i in range(1,k+1):
        po*=2
        for j in range(1,min(po,n+1)):
            temp[j][i]=po-j
            if po-j==n:
                x,y=j,i
    
    rs=set()
    res=[None]*n
    t=n
    while t:
        if temp[x][y]==t and x not in rs:
            res[t-1]=x
            rs.add(x)
            t-=1
        x+=1
        if x==n+1:
            x=1
            y-=1
    
    print(*res)
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()