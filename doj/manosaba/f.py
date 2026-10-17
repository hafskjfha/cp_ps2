import sys
from bisect import *
input=sys.stdin.readline

def lis_reconstruct(a):
    n = len(a)
    tails = []
    tails_idx = []
    prev = [-1] * n

    for i, x in enumerate(a):
        # strict lis, non-decreasing -> bisect_right
        k = bisect_left(tails, x)
        
        if k == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[k] = x
            tails_idx[k] = i
        if k > 0:
            prev[i] = tails_idx[k - 1]

    cur = tails_idx[-1]
    seq = []
    while cur != -1:
        seq.append(a[cur])
        cur = prev[cur]
    seq.reverse()
    return len(tails), seq

def solve():
    n=int(input())
    c=[*map(int,input().split())]
    tempc=[-x for x in c]
    
    cl,lisc=lis_reconstruct(c)
    print(cl,lisc)
    tcl,ldsc=lis_reconstruct(tempc)
    print(tcl,ldsc)
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()