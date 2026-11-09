import sys,math
input=sys.stdin.readline

def solve():
    x1,y1,x2,y2=map(int,input().split())
    print(math.gcd(abs(x1-x2),abs(y1-y2))-1)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()