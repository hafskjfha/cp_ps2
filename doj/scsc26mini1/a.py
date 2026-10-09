import sys
input=sys.stdin.readline

def solve():
    n,q=map(int,input().split())
    a=[*map(int,input().split())]
    comp={v:idx for idx,v in enumerate(sorted(a))}
    pfixSum=[0]+[1]*n
    for _ in range(q):
        x,y=map(int,input().split())
        a[x-1],a[y-1]=a[y-1],a[x-1]
        b=a[:]
        temp=pfixSum[:]
        ans=0
        left,right=n//2-(n%1),n//2
        m=n
        
        while m:
            ...
        
    
        print(ans)
        #print("======")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()