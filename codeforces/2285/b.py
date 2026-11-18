import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    s=input().strip()
    c0=s.count('0')
    c1=n-c0
    dx=abs(c0-c1)
    p=dx+2*min((n-dx)//2,k)
    #print(dx,p)

    delat=0
    temp=n-1
    #print(n-p)
    for i in range(n,-1,-2):
        if i==p:break
        delat+=temp
        temp-=2
    print(n*(n+1)//2+1-delat)

def main():
    t=int(input())
    for _ in range(t):
        solve()
        #print("====")
main()