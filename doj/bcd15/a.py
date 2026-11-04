import sys
input=sys.stdin.readline

def solve():
    int(input())
    print(sum(map(int,input().split())))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()