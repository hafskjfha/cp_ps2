I=open(0).readline
n,m=10,2000
dp=[[0]*(m) for _ in range(n)]
dp[0]=[1]*(m)
for i in range(1,n):
    for j in range(m):
        dp[i][j]=sum(dp[i-1][:(j+1)//2])
for _ in range(int(I())):
    n,m=map(int,I().split())
    print(sum(dp[n-1][:m]))