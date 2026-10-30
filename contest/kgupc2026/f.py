n=int(input())
diff=[0]*10001
for _ in range(n):
    s,e=map(int,input().split())
    diff[s]+=1
    diff[e]-=1

cur=0
ans=0
for i in range(10001):
    cur+=diff[i]
    ans=max(ans,cur)
print(ans)