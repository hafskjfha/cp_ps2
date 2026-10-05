import sys
from bisect import bisect_left,bisect_right
input=sys.stdin.readline
sys.setrecursionlimit(1000000)
INF=float('inf')

n,a,b=map(int,input().split())

tag=[set()for _ in range(1001)]
cs=dict()
ans=INF
for _ in range(n):
    t,d,e=map(int,input().split())
    tag[t].add(d)
    cs[(t,d)]=min(cs.get((t,d),INF),e)
    
keys=[i for i in range(1,1001) if tag[i]]
for k in keys:tag[k]=sorted(tag[k])
#print(keys)

# print(tag[:10])
# print(cs)

def dfs(ds,es,i):
    global ans
    if i==len(keys)-1:
        ans=min(ans,es)
        return
    
    for x in tag[keys[i]]:
        arr=tag[keys[i+1]]
        idx1=bisect_left(arr,a-ds-x)
        idx2=bisect_right(arr,b-ds-x)
        print(x,ds)
        print(idx1,idx2,arr[idx1:idx2])
        print(arr)
        for y in arr[idx1:idx2]:
            dfs(ds+x+y,es+cs[(keys[i],x)]+cs[(keys[i+1],y)],i+1)

dfs(0,0,0)

print(ans if ans!=INF else -1)