import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    gr=[[]for _ in range(n+1)]
    
    flg=True
    for i in range(n-1):
        u,v=map(int,input().split())
        if u!=i+1 or v!=i+2: flg=False
    
    if n==3:
        print(-1)
        return
    
    if flg:
        if n%2:
            print(-1)
            return
        for i in range(2,n+1,2):
            if i+2<=n:
                print(i,i+2)
        print(n-(n%2),1)
        for i in range(1,n+1,2):
            if i+2<=n:
                print(i,i+2)
        
    else:
        print(-1)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()