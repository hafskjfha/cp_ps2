from collections import Counter
n,k=map(int,input().split())
counter=Counter(map(int,input().split()))
for i in range(4):counter[i]=counter.get(i,0)
INF=float('inf')
dp=[INF]*(k+1)
dp[0]=0
for w in range(1,4):
    c=counter[w]
    t=1
    while c>0:
        take=min(t,c)
        c-=take
        
        tw=take*w
        tv=take
        for j in range(k,tw-1,-1):
            dp[j]=min(dp[j],dp[j-tw]+tv)
        
        t*=2
print(dp[k] if dp[k]!=INF else -1)