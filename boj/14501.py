I=open(0).readline
n=int(I())
w={}
for i in range(n):
    t,p=map(int,I().split())
    w.setdefault(i+t-1,[]).append((t,p))
dp=[0]*n
dp[0]=w.get(0,[[0,0]])[0][1]
for i in range(1,n):
    x=dp[i-1]
    for t,p in w.get(i,[]):x=max(x,dp[i-t]+p)
    dp[i]=x
print(dp[-1])