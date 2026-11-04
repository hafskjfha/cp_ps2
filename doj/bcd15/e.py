import sys
input=sys.stdin.readline

def solve():
    n,r,c=map(int,input().split())
    ans=[[-1]*(n+1) for _ in range(n+1)]
    
    if n==1:
        print("0")
        return
    elif n==2:
        if (r,c)==(1,1):
            print("0 1")
            print("1 1")
        elif (r,c)==(1,2):
            print("1 0")
            print("1 1")
        elif (r,c)==(2,1):
            print("1 1")
            print("0 1")
        elif (r,c)==(2,2):
            print("1 1")
            print("1 0")
        return
    elif n==3:
        if (r,c)==(2,2):
            print("1 1 2")
            print("1 0 2")
            print("2 2 2")
        elif (r,c)==(1,1):
            print("0 1 2")
            print("1 1 2")
            print("2 2 2")
        elif (r,c)==(3,1):
            print("2 1 0")
            print("2 1 1")
            print("2 2 2")
    elif n==4:
        ...
    
    
    if r==c==1:
        ans[r][c]=0
        for i in range(2,n+1):
                ans[i][i]=i-1
                for k in range(1,i):
                    ans[i-k][i]=i-1
                    ans[i][i-k]=i-1
    
    for x in ans[1:]:
        print(*x[1:])

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()