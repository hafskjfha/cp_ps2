import sys
from math import *

input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    print(max(a[n//2:]))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()