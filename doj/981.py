import sys
from itertools import permutations

input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    arr=[tuple(map(int,input().split()))for _ in range(k)]
    
    ans=0
    for x in permutations(range(1,n+1),n):
        for a,b in arr:
            if x[a-1]==b:break
        else:
            ans+=1
            
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()