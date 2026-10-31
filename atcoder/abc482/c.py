import sys
from bisect import *
input=sys.stdin.readline

def solve():
    h,w,n,q=map(int,input().split())
    col=[]
    row=[]
    for _ in range(n):
        i,j=map(int,input().split())
        row.append(i)
        col.append(j)
    col.sort()
    row.sort()
    
    for _ in range(q):
        t,l,r=map(int,input().split())
        if t==1:
            i,j=bisect_left(row,l),bisect_right(row,r)
            print(j-i)
        else:
            i,j=bisect_left(col,l),bisect_right(col,r)
            print(j-i)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()