import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    arr=[*map(int,input().split())]
    
    res=[]
    for i in range(n):
        if k==0:break
        tempv,tempidx=arr[i],i
        for j in range(i+1,n):
            if arr[j]<tempv:
                tempv=arr[j]
                tempidx=j
        if tempidx==i: continue
        
        for j in range(tempidx,i,-1):
            k-=1
            res.append(j)
            arr[j],arr[j-1]=arr[j-1],arr[j]
            
            if k==0:break
    ans=0
    for i in range(n):
        for j in range(i+1,n):
            if arr[i]<arr[j]:ans+=1
    
    #print(arr)
    if k==0:
        print(ans)
        print(*res,sep='\n')
    else:
        temp=-1
        
        for i in range(n-1):
            if arr[i]==arr[i+1]:
                temp=i+1
                break
        
        if k%2 and temp!=-1:
            res.append(temp)
            k-=1
        elif k%2:
            ans-=1
        print(ans)
        print(*res+[1]*k,sep='\n')
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()