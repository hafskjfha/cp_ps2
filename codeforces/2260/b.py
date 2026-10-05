import sys
input=sys.stdin.readline

def solve():
    x,y,k=map(int,input().split())
    ans,last=0,-1
    flg=False
    temp=y-x
    while k:
        ans+=y%x
        if y%x==temp: break
        
        x+=1
        y+=1
        k-=1
    
    if k:
        ans+=temp*(k-1)
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()