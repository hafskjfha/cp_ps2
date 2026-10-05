import sys
from itertools import combinations

input=sys.stdin.readline

def solve():
    n,v=map(int,input().split())
    w=[*map(int,input().split())]
    
    ans=0
    for x in combinations(range(n),3):
        if sum(x)+3<=v:
            ans=max(ans,w[x[0]]+w[x[1]]+w[x[2]])
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()