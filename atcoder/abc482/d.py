import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    for i in range(n):
        if i==0:
            print((a[-1]-a[i])//2)
        elif i==n-1:
            print((a[-1]-a[0])//2)
        else:
            print(min(
                (a[i]-a[i-1])//2+max((a[i-1]-a[0])//2,(a[-1]-a[i])//2),
                (a[i+1]-a[i])//2+max((a[-1]-a[i+1])//2,(a[i]-a[0])//2)
            ))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()