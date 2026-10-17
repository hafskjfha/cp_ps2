import sys
from bisect import *
input=sys.stdin.readline

def solve():
    n,q=map(int,input().split())
    a=[*map(int,input().split())]
    psum=[0]
    for x in a:psum.append(psum[-1]+x)
    sz=[0]
    for k in range(1,n+1):sz.append(sz[-1]+k)
    pt=[0]
    for i in range(1,n):pt.append(pt[-1]+psum[i])
    #print(pt)
    
    for _ in range(q):
        l,r=map(int,input().split())
        bl,br=bisect_left(sz,l)-1,bisect_left(sz,r)-1
        #print(bl,br,sz[bl],sz[br])
        l2,r2=l-sz[bl],r-sz[br]
        #print(l2,r2)
        
        if bl==br:
            print(psum[r2]-psum[l2-1])
        else:
            print(psum[bl+1]-psum[l2-1]+psum[r2]+pt[br]-pt[bl+1])
        #print("======")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()