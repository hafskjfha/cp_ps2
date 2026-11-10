import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[tuple(map(int,input().split()))for i in range(n)]
    
    costCou=min(arr,key=lambda x:x[0])[0]
    s=sum(b for a,b in arr)
    cost=sorted(a-b for a,b in arr)
    p=0
    ans=s+n*costCou
    
    for k in range(1,n//2+n%2+1):
        p+=cost[k-1]
        ans=min(ans,s+p+costCou*max(0,n-2*k))
        
    
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()