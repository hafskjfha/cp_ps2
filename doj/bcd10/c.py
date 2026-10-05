import sys
from collections import deque

input=sys.stdin.readline

def solve():
    n=int(input())
    gr=[[]for _ in range(n)]
    j=0
    for i in range(n):
        for _ in range(int(input())):
            x,y,r=map(int,input().split())
            gr[i].append((x,y,r,j))
            j+=1
    
    q=deque()
    vi=[False]*j
    for x,y,r,j in gr[0]:
        q.append((x,y,r,0,j))
        vi[j]=True
        
    while q:
        x,y,r,i,j=q.popleft()
        #print(j)
        if i==n-1:
            print("NO")
            return
        
        
        if i!=0:t=[i-1,i,i+1]
        else:t=[i,i+1]
        
        for k in t:
            for x2,y2,r2,j2 in gr[k]:
                if ((x2-x)**2+(y2-y)**2)<=(r+r2)**2 and vi[j2]==False:
                    q.append((x2,y2,r2,k,j2))
                    vi[j2]=True
                    #print(j,j2)
                else:
                    pass
                    #print(j,j2)
    
    print("YES")


def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()