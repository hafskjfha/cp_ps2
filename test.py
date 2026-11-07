import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=sorted(map(int,input().split()))
    a,b=sum(2**x for x in arr),0
    ans=0
    for i in range(n-1,-1,-1):
        a-=2**arr[i]
        b+=2**arr[i]
        ans=max(ans,a*b)
        print(a,b)
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()