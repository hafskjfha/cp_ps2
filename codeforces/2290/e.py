import sys
from collections import deque

input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    arr=[*map(int,input().split())]
    s=sum(arr)%2
    
    temp=0
    dq=deque()
    for i in range(n-1,-1,-1):
        arr[i]^=temp
        #print(s,temp,min(k,i)*arr[i])
        s^=min(k,i)*arr[i]
        temp^=arr[i]
        dq.append(arr[i])
        if len(dq)>k:
            temp^=dq.popleft()
        #print(dq)
    
    #print(s)
    print("Alice" if s%2 else "Bob")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()