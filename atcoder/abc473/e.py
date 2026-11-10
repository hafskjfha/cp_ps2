import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    arr=[*map(int,input().split())]
    
    ans=0
    pfixSum=[0]
    for x in arr:pfixSum.append((pfixSum[-1]+x)%k)
    #print(pfixSum)
    
    check=set([0])
    for i in range(1,len(pfixSum)):
        if pfixSum[i] in check:
            #print(i,pfixSum[i],check)
            ans+=1
            check.clear()
        check.add(pfixSum[i])
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()