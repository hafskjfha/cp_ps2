import sys
from collections import deque
input=sys.stdin.readline

def solve():
    dex=[1,-1,0,0]
    dey=[0,0,1,-1]
    dem=['^','v','<','>']
    h,w=map(int,input().split())
    board=[input().strip()for _ in range(h)]
    
    ans=[[None]*w for _ in range(h)]
    q=deque()
    
    for i in range(h):
        for j in range(w):
            if board[i][j]=='#': ans[i][j]='#'
            elif board[i][j]=='E':
                ans[i][j]='E'
                q.append((i,j))

    while q:
        x,y=q.popleft()
        
        for i in range(4):
            dx,dy,dm=dex[i],dey[i],dem[i]
            nx,ny=x+dx,y+dy
            
            if 0<=nx<h and 0<=ny<w and ans[nx][ny] is None:
                ans[nx][ny]=dm
                q.append((nx,ny))
    
    for k in ans:
        print(''.join(k))
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()