import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    i=0
    print(n)
    for _ in range(n):
        print(i%n+1,(i-1)%n+1,(i+1)%n+1)
        i=(i+2)%n

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()