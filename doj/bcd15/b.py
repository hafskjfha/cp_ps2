import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    ans=0
    for _ in range(n):
        x1,y1,x2,y2=map(int,input().split())
        if (y1<0 and y2>0) or (y1>0 and y2<0):
            ans+=1
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()