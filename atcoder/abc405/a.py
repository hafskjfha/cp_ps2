import sys
input=sys.stdin.readline

def solve():
    r,x=map(int,input().split())
    if x==1:
        print("Yes"if 1600<=r<=2999 else "No")
    else:
        print("Yes"if 1200<=r<=2399 else "No")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()