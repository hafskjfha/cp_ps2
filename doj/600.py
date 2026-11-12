import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    a=[*map(int,input().split())]
    b=[*map(int,input().split())]
    
    dp=[[0]*(m+1)for _ in range(n+1)]
    for i in range(1,n+1):
        for j in range(1,m+1):
            if a[i-1]==b[j-1]:
                dp[i][j]=dp[i-1][j-1]+1
            else:
                dp[i][j]=max(dp[i-1][j],dp[i][j-1])
    
    print(dp[n][m])
    
    if dp[n][m]==0:return
    
    res=[]
    # a.reverse()
    # b.reverse()
    
    i,j=1,1
    while i<=n and j<=m:
        if a[i-1]==b[j-1]:
            res.append(a[i-1])
            i+=1
            j+=1
        else:
            if dp[i-1][j]>dp[i][j-1]:
                i+=1
            else:
                j+=1
    print(*res)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()