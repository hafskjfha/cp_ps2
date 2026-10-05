import sys
from itertools import permutations

input=sys.stdin.readline


def solve():
    n,l=map(int,input().split())
    aa=sorted([tuple(map(int,input().split()))for _ in range(n)],key=lambda x:x[1])
    
    ans=0
    for a in permutations(aa,n):
        templ=l
        for x,y in a:
            if y<=templ: templ+=y
            elif x<templ<y: templ+=templ
        ans=max(templ,ans)
        # print(a)
        # print(ans)
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()