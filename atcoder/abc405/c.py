import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    prefixSum=[0]
    for x in a:
        prefixSum.append(prefixSum[-1]+x)
    
    #print(prefixSum)
    
    ans=0
    for i in range(n-1):
        ans+=a[i]*(prefixSum[n]-prefixSum[i+1])
    
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()