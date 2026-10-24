import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    a=[*map(int,input().split())]
    ans=0
    for i in range(n-1):
        if a[i]<k<a[i+1] or a[i+1]<k<a[i]:
            ans+=1
        if a[i]==k:ans+=1
    print(ans+(a[-1]==k))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()