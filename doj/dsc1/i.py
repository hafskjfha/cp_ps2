import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    arr=[*map(int,input().split())]
    
    soarr=sorted(enumerate(arr),key=lambda x:x[1])
    #print(soarr)
    
    res=[]
    for i in range(n):
        if arr[i]==soarr[i][1]:continue
        for j in range(i,0,-1):
            if k==0:break
            res.append(j)
            arr[j],arr[j-1]=arr[j-1],arr[j]
            k-=1
            if arr[j-1]==soarr[i][1]:break
            
        
        if k==0:break
    ans=0
    for i in range(n):
        for j in range(i+1,n):
            if arr[i]<arr[j]:ans+=1
    
    if k==0:
        print(ans)
        print(*res,sep='\n')
    else:
        print(ans-k%2)
        print(*res+[1]*k,sep='\n')
        
    
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()