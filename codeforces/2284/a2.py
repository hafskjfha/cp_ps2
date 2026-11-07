import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=sorted([*map(int,input().split())])
    a,b=0,0
    for i in range(n):
        if a<=b:
            a+=2**arr[i]
        else:
            b+=2**arr[i]
    print(a,b)
    print(a*b)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()