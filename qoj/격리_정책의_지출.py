import sys
input=sys.stdin.readline

def solve():
    MOD=1000000007
    delta=[[(-1,0),(1,0),(0,-1),(0,1)],[(-1,-1),(-1,1),(1,-1),(1,1)]]
    n,m,d0,d1,d2=map(int,input().split())
    board=[input().strip()for _ in range(n)]
    
    ans=0
    INV2=500000004
    for x in range(n):
        for y in range(m):
            if board[x][y]=='V':
                ans=(ans+d0)%MOD
                continue
            
            flg=[False,False]
            count=[0,0]
            for i in range(2):
                for dx,dy in delta[i]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<n and 0<=ny<m:
                        if board[nx][ny]=='V':
                            flg[i]=True
                        elif board[nx][ny]=='?':
                            count[i]+=1
            
            p=INV2 if board[x][y]=='?' else 1
            if board[x][y]=='?':
                ans+=d0*INV2
                
            a,b=(0 if flg[0] else pow(INV2,count[0],MOD)),(0 if flg[1] else pow(INV2,count[1],MOD))
            ans+=p*((1-a)*d1+a*(1-b)*d2)
            ans%=MOD
    print(ans%MOD)
    
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()

# 468750012