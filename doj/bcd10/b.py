import sys
from math import *

input=sys.stdin.readline

def solve():
    m,k=map(int,input().split())
    a=100*m/(100+k)
    b=(100*m+99)/(100+k)
    n=100*m//(100+k)
    while n<=b:
        if a<=n<=b:
            print("YES")
            return
        n+=1
    print("NO")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()