import sys
from collections import deque

input=sys.stdin.readline

def solve():
    N,K=map(int,input().split())
    K%=64
    
    res=['0']*64
    for i in range(64):
        k=(1<<i)
        count0=min(N,k-1+max(0,(N-k+1)//(k<<1)*k)+max(0,(N-k+1)%(k<<1)-k))
        count1=N-count0
        #print(count0,count1)
        if count0 % 2 == 0:
            res[i]='1'
    
    #print(res)
    dq=deque(res[::-1])
    for _ in range(K):
        dq.append(dq.popleft())
    
    print(int("".join(map(str,dq)),2))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()