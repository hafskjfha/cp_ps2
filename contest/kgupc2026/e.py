n,q=map(int,input().split())
queue=[-1]*(n+1)
ans=0
for _ in range(q):
    s,*i=input().split()
    if s=="SAVEALL":
        for i in range(1,n+1):
            if queue[i]!=-1:
                ans+=1
                queue[i]=-1
    elif s=="EDIT":
        i=int(i[0])
        queue[i]=1
    else:
        i=int(i[0])
        if queue[i]!=-1:
            ans+=1
            queue[i]=-1
print(ans)