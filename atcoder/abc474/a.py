import sys
input=sys.stdin.readline

def solve():
    x=int(input())
    if x==1:print(2)
    else:print(1)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()