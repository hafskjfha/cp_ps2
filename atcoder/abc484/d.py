import sys
from collections import defaultdict
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    
    count=defaultdict(int)
    ans=1
    count[arr[0]]+=1
    for i in range(1,n):
        if arr[i]!=arr[i-1]:
            ans+=i-count.get(arr[i],0)
        count[arr[i]]+=1
        #print(count)
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()