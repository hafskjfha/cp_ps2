import sys
input=sys.stdin.readline

def hanoi(n, start, end, via):
    if n==0:
        return

    hanoi(n - 1, start, via, end)
    print(start, end)
    hanoi(n - 1, via, end, start)

def solve():
    n=int(input())
    print(2**n-1)
    hanoi(n,1,3,2)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()