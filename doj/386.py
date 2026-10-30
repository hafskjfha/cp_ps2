import sys
from collections import Counter
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    c=Counter(a)
    
    ans=0
    t=0
    
    for k,v in sorted(c.items(),reverse=True):
        b=k+v-1
        ans+=max(0,b-t)
        t=max(0,b-v)
        
        print(ans,t)
    
    print(ans)
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()