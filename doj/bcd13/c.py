import sys
import heapq
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[]
    ans=0
    for _ in range(n):
        u,a=map(int,input().split())
        if u*(a+1)-1<=0:
            ans+=1
        else:
            arr.append((u*a,u*(a+1)-1))
    
    #print(arr)
    
    if not arr:
        return print(n)        
    
    arr.sort()
    res=0
    temp=1
    pq=[]
    for i in range(len(arr)):
        while pq and pq[0]<arr[i][0]:
            heapq.heappop(pq)
        
        heapq.heappush(pq,arr[i][1])
        res=max(res,len(pq))
        
    res=max(res,temp)    
    
    # print(arr)
    # print(res,temp)
    print(n-res)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()