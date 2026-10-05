import sys
input=sys.stdin.readline
sys.setrecursionlimit(1000000)

n,a,b=map(int,input().split())
arr=[*map(int,input().split())]
ans=0

#temp=[]

def dfs(ds,i):
    global ans
    #print(ds,i)
    if a<=ds<=b:
        ans+=1
        #temp.append((ds,i))
        
    
    for j in range(i+1,n):
        #print(i,ds+arr[j])
        dfs(ds+arr[j],j)
            #print(ds)

for i in range(n):
    dfs(arr[i],i)            

print(ans)

#for k in temp:print(k)