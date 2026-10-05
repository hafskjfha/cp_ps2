import sys
from collections import defaultdict
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    a=[*map(int,input().split())]
    
    count=defaultdict(int)
    for x in a:
        count[x]+=1
    
    ans=0
    while 1:
        for i in range(1,m+1):
            if count[i]==0:
                break
        else:
            count[a.pop()]-=1
            ans+=1
            continue
        break
    
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()