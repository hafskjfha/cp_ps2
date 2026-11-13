import sys
input=sys.stdin.readline

def solve():
    a,b,c=map(int,input().split())
    if c-b==1==b-a:
        print("YES")
    else:
        print("NO")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()