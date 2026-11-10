import sys
from collections import deque

input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    dq=deque(arr)
    
    sarr=sorted(arr)
    for i in range(n):
        if sarr==[*dq]:
            return print("YES")
        dq.append(dq.popleft())
    
    print("NO")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()