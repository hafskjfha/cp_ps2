import sys

input=sys.stdin.readline

n,k=map(int,input().split())
ans=[]

def back(arr,x,d):
    if d==1:
        arr[0]=x
        ans.append(tuple(arr))
        #print(arr,0,d)
        arr[0]=0
        return
    
    #print(arr,x,d)
    if x==0:
        ans.append(tuple(arr))
        return
    
    
    for i in range(1+x//d):
        arr[d-1]=i
        back(arr,x-d*i,d-1)
        
    arr[d-1]=0
    
    
    

back([0]*n,k,n)
ans.sort()
print("\n".join(" ".join(map(str,x)) for x in ans))