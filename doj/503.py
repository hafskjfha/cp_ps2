import sys
input=sys.stdin.readline

def solve():
    a=int(input())
    if a%2:
        print((a**2+1)//2-1,(a**2+1)//2)
    else:
        print((a**2+4)//4-2, (a**2+4)//4)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()