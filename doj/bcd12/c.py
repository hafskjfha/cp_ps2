import sys
input=sys.stdin.readline
delta=[(-1,0),(1,0),(0,1),(0,-1),(-1,1),(-1,-1),(1,1),(1,-1)]

def solve():
    n,m,k=map(int,input().split())
    board=[input().strip()for _ in range(n)]
    count=[[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if board[i][j]=='#':
                for di,dj in delta:
                    ni,nj=i+di,j+dj
                    if 0<=ni<n and 0<=nj<m and board[ni][nj]=='.':
                        count[ni][nj]+=1
    
    ans=now=0
    cc=[]
    for i in range(n):cc.extend([x for x in count[i] if x>0])
    cc.sort(reverse=True)
    
    for p in cc:
        if now>=k:break
        ans+=1
        now+=p
        
    #print(cc)
    print(ans if now>=k else -1)
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()