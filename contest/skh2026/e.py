## wtf? ac

import sys
from heapq import heappush,heappop

input=sys.stdin.readline
n,m,d=map(int,input().split())
arr=sorted([tuple(map(int,input().split()))for _ in range(n)])
#print(arr)

pq=[]
for i in range(m):
    heappush(pq,0)
    
ans=0

for s,e in arr:
    t=heappop(pq)
    if s<=t:
        heappush(pq,max(e,t))
    else:
        ans+=s-t
        #print(ans)
        heappush(pq,e)
        
while pq:
    t=heappop(pq)
    #print(t)
    ans+=d-t
        
print(ans)