from itertools import combinations
n,m=map(int,input().split())
arr=[input()for _ in range(n)]
ans=0 if n!=1 else arr[0].count('1')
for i,j in combinations(range(n),2):
    temp=0
    for k in range(m):
        if arr[i][k]=='1' or arr[j][k]=='1':
            temp+=1
    ans=max(temp,ans)
print(ans)