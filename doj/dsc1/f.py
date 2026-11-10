import sys
from collections import Counter
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[input().strip()for _ in range(n)]
    
    print(*sorted(arr,key=lambda x:(sum(v**2 for v in Counter(x).values()), len(x), x)),sep='\n')

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()