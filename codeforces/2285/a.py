import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    if n<=3:
        return print(-1)

    print(*[*range(1,5)][::-1],*[*range(5,n+1)])
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()