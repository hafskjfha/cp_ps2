import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[input().strip()for _ in range(2)]
    #print([1 for i in range(n) if arr[0][i]!=arr[0][i]])
    print(1 if sum([1 for i in range(n) if arr[0][i]!=arr[1][i]])%2 else 0)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()