import heapq
I=open(0).readline
pq=[]
n,t,k=map(int,I().split())
ans=0
for _ in range(n):
    c,a,*b=map(int,I().split())
    if c==1:heapq.heappush(pq,(-b[0],a))
    else:
        c=0
        while c<k:
            if not pq:break
            v,m=heapq.heappop(pq)
            if a-m>t:continue
            ans+=-v
            c+=1
print(ans)