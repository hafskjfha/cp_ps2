import sys

def main():
    input=sys.stdin.readline
    n,m=map(int,input().split())
    san=[[*map(int,input().split())]for _ in range(n)]
    mul=[[*map(int,input().split())]for _ in range(m)]
    
    ans=float('inf')
    
    for x1,y1 in san:
        for x2,y2 in mul:
            ans=min(ans,((x1-x2)**2+(y1-y2)**2)**0.5)
            
    print(ans)
    
main()