def main():
    from collections import deque
    I=open(0).readline
    n,k=map(int,I().split())
    b=[I()for _ in range(2)]
    v=[[0]*n for _ in range(2)]
    q=deque([(0,0,0)])
    v[0][0]=1
    while q:
        x,y,t=q.popleft()
        if x>0 and b[y][x-1]=='1' and v[y][x-1]==0 and x-1>t:
            v[y][x-1]=1
            q.append((x-1,y,t+1))
        if x+1>=n or x+k>=n:exit(print(1))
        if b[y][x+1]=='1' and v[y][x+1]==0:
            v[y][x+1]=1
            q.append((x+1,y,t+1))
        ny=y==0
        if b[ny][x+k]=='1' and v[ny][x+k]==0:
            v[ny][x+k]=1
            q.append((x+k,ny,t+1))
    print(0)
main()