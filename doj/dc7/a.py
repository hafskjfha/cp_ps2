import sys
from math import *

input=sys.stdin.readline

def solve():
    a,b=map(int,input().split())
    print(lcm(a,b)*gcd(a,b))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()