import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    b=[*map(int,input().split())]
    
    res=[]
    flg=False
    for i in range(n):
        if a[i]>b[i]:
            res.append(10**18)
            flg=True
        else:
            res.append(1)
            
    if flg:
        print("Yes")
        print(*res)
    else:
        print("No")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()