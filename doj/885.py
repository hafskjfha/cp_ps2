import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    a=[*map(int,input().split())]
    b=[*map(int,input().split())]
    
    c=[]
    for x,y in zip(a,b):
        c.append((y-x,x,y))
    c.sort()
    ans=0
    for _,x,y in c:
        if k:
            ans+=x
            k-=1
        else:
            ans+=y
    print(ans)
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()