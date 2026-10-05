import sys
from collections import deque

def main():
    input=sys.stdin.readline
    n,m=map(int,input().split())
    board=[]
    start,end=None,None
    for i in range(n):
        s=input().strip()
        for j in range(m):
            if s[j]=='S':start=(i,j)
            elif s[j]=='T':end=(i,j)
        board.append(s)
    
    print(bfs(n,m,board,start,end))
    
    
def bfs(n,m,board,start,end):
    INF=float('inf')
    v=[[[INF]*4 for _ in range(m)] for _ in range(n)]
    delta=((0,1),(0,-1),(1,0),(-1,0))
    q=deque()
    
    for k,(dx,dy) in enumerate(delta):
        nx,ny=start[0]+dx,start[1]+dy
        if board[nx][ny]!='#':
            q.append((nx,ny,k))
            v[nx][ny][k]=1
    
    while q:
        x,y,d=q.popleft()
        
        if (x,y)==end: return v[x][y][d]
        
        for k, (dx,dy) in enumerate(delta):
            nx,ny=x+dx,y+dy
            
            if board[nx][ny]=='#': continue
            
            cost=v[x][y][d]+(d!=k)
            
            if cost < v[nx][ny][k]:
                v[nx][ny][k]=cost
                
                if d==k:
                    q.appendleft((nx,ny,k))
                else:
                    q.append((nx,ny,k))
                    
    
    return -1
    
main()