import sys
from collections import deque
from itertools import permutations


input=sys.stdin.readline

def check(gr,u,v):
    q=deque([u])
    vi=[False]*(len(gr)+1)
    
    while q:
        x=q.popleft()
        if x==v:
            return True
        
        for dx in gr[x]:
            if vi[dx]==False:
                q.append(dx)
                vi[dx]=True
    return False

def solve():
    n,m=map(int,input().split())
    w=[0]+[*map(int,input().split())]
    gr=[set()for _ in range(n+1)]
    edge=dict()
    edger=[None]*(m+1)
    
    for i in range(m):
        u,v=map(int,input().split())
        gr[u].add(v)
        gr[v].add(u)
        edge[(u,v)]=i+1
        edger[i+1]=(u,v)
    
    ans=float('inf')
    res=[]
    
    for kk in permutations(range(1,m+1),m):
        temp=0
        for k in kk:
            u,v=edger[k]
            gr[u].remove(v)
            gr[v].remove(u)
            if check(gr,u,v):
                temp+=min(w[u],w[v])
            else:
                temp+=max(w[u],w[v])
        if ans>temp:
            ans=temp
            res=kk
        
        for k in kk:
            u,v=edger[k]
            gr[u].add(v)
            gr[v].add(u)
    
    print(ans)
    print(*res)
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()