def main():
    INF=float('inf')
    n=int(input())
    dp=[INF]*(n+1)
    dp[0]=0
    a=[i**2 for i in range(1,int(n**0.5)+1)]
    for i in range(1,n+1):
        for x in a:
            if x>i:break
            dp[i]=min(dp[i],dp[i-x]+1)
    print(dp[-1])
main()