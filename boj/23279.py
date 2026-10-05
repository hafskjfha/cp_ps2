input=open(0).readline
n,k=map(int,input().split())
for _ in range(k):print(*map(lambda x:x[0]+x[1]+1,enumerate(sorted(map(int,input().split()[1:])))))