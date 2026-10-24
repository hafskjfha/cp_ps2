import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[input().split() for _ in range(n)]
    x=int(input())
    for i in range(n):
        if int(arr[i][1])>x:
            print(arr[i-1][0],x-int(arr[i-1][1])+1)
            break
    else:
        print(arr[-1][0],x-int(arr[-1][1])+1)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()