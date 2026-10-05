import sys
from collections import defaultdict
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    a=[*map(int,input().split())]
    soa=sorted(a[::])
    
    nx=0
    check=defaultdict(lambda :[-1,-1])
    for i in range(n):
        if nx<=a[i]:
            check[a[i]][0]=i
        check[soa[i]][1]=i

        nx=max(nx,a[i])
        check[nx][0]=i
        #print('??',a[i],check[a[i]])
    
    #print(check)
    
    ans=0
    
    for i in range(n):
        x=soa[i]
        if check[x][0]==-1:
            check[x][0]=-1 if i==0 else check[soa[i-1]][0]
        
        #print('?',x,check[x])
        if check[x][0]<check[x][1]:
            if i!=n-1:
                ans+=soa[i+1]-x
            else:
                ans+=nx-x
    
    # for x in range(1,m+1):
    #     if x not in check:
    #         check[x]=check[x-1]
    #     elif check[x][0]==-1:
    #         check[x][0]=check[x-1][0]
            
    #     if check[x][0]<check[x][1]:
    #         ans+=1
    #     #print('?',x,check[x])
    
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()