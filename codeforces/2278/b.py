import sys
input=sys.stdin.readline

def solve():
    x,y,z=map(int,input().split())
    t=max(x,y,z)
    if t==x:
        print("P"*sum([x,y,z]))
    elif t==y:
        print("R"*sum([x,y,z]))
    else:
        print("S"*sum([x,y,z]))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()