import sys
from collections import Counter
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=sorted(map(int,input().split()))
    count=Counter(arr)
    
    #print(arr[-1],arr[0]+n-arr.count(arr[0]))
    #print(min(arr[-1],arr[0]+n-arr.count(arr[0])))
    ans=float('inf')
    
    for i in range(n):
        x=arr[i]
        count[x]-=1
        ans=min(ans,x+(n-i-1)-(count.get(x,0)))
        #print(i,x,x+(n-i-1)-(count.get(x,0)))
        #print(count)
        
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()