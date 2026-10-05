import sys

def main():
    n=int(input())
    s=input().strip()
    
    if "OO" in s or "XXX" in s: return print(-1)
    
    INF=float('-inf')
    dp=[[INF]*3 for _ in range(n)]
    
    if s[0]=='O':dp[0][0]=1
    elif s[0]=='X':dp[0][1]=0
    else:
        dp[0][0]=1
        dp[0][1]=0
    
    for i in range(1,n):
        c=s[i]
        if c=='O':
            dp[i][0]=max(dp[i-1][1],dp[i-1][2])+1
        elif c=='X':
            dp[i][1]=dp[i-1][0]
            dp[i][2]=dp[i-1][1]
        else:
            dp[i][0]=max(dp[i-1][1],dp[i-1][2])+1
            dp[i][1]=dp[i-1][0]
            dp[i][2]=dp[i-1][1]
    
    ans=max(dp[n-1])
    print(-1 if ans==INF else ans)

    
main()