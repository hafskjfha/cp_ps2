n=int(input())
arr=[tuple(map(int,input().split()))for i in range(n)]

def short(n,arr):
    arr2=sorted(arr,key=lambda x:(x[1]-x[0],x[0],x[1]))
    
    ans=0
    res=[]
    
    for l,r in arr2:
        for li,ri in res:
            if l<=li<=r or l<=ri<=r:break
        else:
            ans+=1
            res.append((l,r))
    
    return ans,res
    
def opti(n,arr):
    arr2=sorted(arr,key=lambda x:x[1])
    
    ans=0
    res=[]
    
    now=-1
    for l,r in arr2:
        if now<l:
            ans+=1
            res.append((l,r))
            now=r
    
    return ans,res

print(short(n,arr))
print(opti(n,arr))