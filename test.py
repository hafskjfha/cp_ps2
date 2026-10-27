import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[input().strip()for _ in range(2)]
    if n%2:
        print(arr[0][-1]==arr[1][-1]=='f')
    else:
        print(0)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()