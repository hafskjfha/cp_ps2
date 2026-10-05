import sys

input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    openone=False
    
    res=[]
    for x in a:
        if x!=-1:
            res.append(x)
            if x==1:
                openone=True
        else:
            if not openone:
                res.append(1)
                openone=True
            else:
                res.append(x)
    
    flg=False
    for i in range(n-1,-1,-1):
        if res[i]==1: flg=True
        
        if res[i]==-1:
            if flg: res[i]=0
            else:
                res[i]=1
                flg=True
                
    print(*res)

def main():
    t=int(input())
    for _ in range(t):
        solve()
    
    
main()