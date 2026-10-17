import sys
from collections import deque

input=sys.stdin.readline

def bfs(board,vi,q,n,m,x,y,p,t):
    while q:
        c,r=q.popleft()
        
        for nc,nr in [(c+1,r),(c-1,r),(c,r+1),(c,r-1)]:
            if (nc,nr)==(x,y):
                return vi[c][r]+1
            
            if 0<=nc<n and 0<=nr<m and vi[nc][nr]==0 and board[nc][nr]!='x' and board[nc][nr]!='#' and (p==1 or (board[nc][nr]!='!' or vi[c][r]<t-1)):
                vi[nc][nr]=vi[c][r]+1
                q.append((nc,nr))
    
    return -1

def solve():
    n,m,t=map(int,input().split())
    board=[]
    
    sc,sr=-1,-1
    tc,tr=-1,-1
    for i in range(n):
        s=input().strip()
        for j in range(m):
            if s[j]=='S':
                sc,sr=i,j
            elif s[j]=='E':
                tc,tr=i,j
        board.append(s)
    
    vi=[[0]*m for _ in range(n)]
    
    print("Miria")
    
    k=bfs(board,vi,deque([(sc,sr)]),n,m,tc,tr,0,t)
    # for x in vi:
    #     print(*x)
    if k!=-1:
        return print(k)
    vi=[[0]*m for _ in range(n)]
    print(bfs(board,vi,deque([(sc,sr)]),n,m,tc,tr,1,t))
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()