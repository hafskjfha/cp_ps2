import sys
input=sys.stdin.readline

def solve():
    INF=float('inf')
    n=int(input())
    a=[*map(int,input().split())]
    pfmax=[0]*n
    sfmin=[INF]*n
    for i in range(n-1):pfmax[i+1]=max(pfmax[i],a[i])
    for i in range(n-1,0,-1):sfmin[i-1]=min(sfmin[i],a[i])
    
    #print(pfmax)
    #print(sfmin)
    
    ans=0
    for i in range(n):
        if pfmax[i]<=a[i] and a[i]<=sfmin[i]:
            ans+=1
    print(ans)
    
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()