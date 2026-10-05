n=int(input())
a=sorted([[*map(int,input().split())]for _ in range(n)],key=lambda x:x[1])
ans=0
temp=-271
for x,y in a:
    if x<=temp<=y:continue
    temp=y
    ans+=1

print(ans)

# 난이도 함정 문제?

# y_1, y_2, 