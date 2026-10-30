dp=[0]*91
dp[0]=dp[1]=1
for i in range(2,91):
    dp[i]=dp[i-1]+dp[i-2]
#print(dp)

n=int(input())
prev=None
ans=1
temp=1
for _ in range(n):
    s=input()
    if prev==s:
        temp+=1
    else:
        ans*=dp[temp]
        temp=1
    prev=s
    #print(ans,prev,temp)
print(ans*dp[temp])