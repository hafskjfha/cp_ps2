import sys
sys.setrecursionlimit(200_005)
input=sys.stdin.readline

def dfs(gr,u,vi):
    for v in gr[u]:
        if vi[v]==-1:
            vi[v]=vi[u]+1
            dfs(gr,v,vi)

def solve():
    n=int(input())
    gr=[[]for _ in range(n+1)]
    for _ in range(n-1):
        u,v=map(int,input().split())
        gr[u].append(v)
        gr[v].append(u)
    color=[-1]+[*map(int,input().split())]
    dist1=[-1]*(n+1)
    dist1[1]=0
    dfs(gr,1,dist1)
    temp=(1,0)
    for i in range(2,n+1):
        if temp[1]<dist1[i]:
            temp=(i,dist1[i])
    dist2=[-1]*(n+1)
    dist2[temp[0]]=0
    dfs(gr,temp[0],dist2)
    
    diameter=0
    for i in range(1,n+1):
        diameter=max(diameter,dist2[i])
    
    print(dist1)
    print(dist2)
    print(diameter)
    
    count=0
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            print(i,j,color[i],color[j],dist1[i],dist1[j])
            if color[i]==color[j] and dist1[i]+dist1[j]==diameter:
                print('!',i,j)
                count+=1
    
    print(count)
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()