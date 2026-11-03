import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    ma,mb=0,0
    arr=[]
    for _ in range(n):
        a,b,c,d=map(int,input().split())
        ma=max(ma,a)
        mb=max(mb,b)
        arr.append((c,d))
    
    ans=0
    for c,d in arr:
        if c>=ma and d>=mb:
            ans+=1
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()