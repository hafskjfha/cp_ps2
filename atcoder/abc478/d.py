import sys
from collections import defaultdict
input=sys.stdin.readline

def solve():
    n,q=map(int,input().split())
    updates=defaultdict(list)
    
    for _ in range(q):
        l,r,x=map(int,input().split())
        updates[x].append((l,r))
    
    imos=[0]*(n+3)
    for xl in updates.values():
        xl.sort()
        #print(xl)
        nowl,nowr=xl[0]
        for i in range(1,len(xl)):
            if nowr<xl[i][0]:
                imos[nowl]+=1
                imos[nowr+1]-=1
                nowl,nowr=xl[i]
            else:
                nowr=max(nowr,xl[i][1])
        imos[nowl]+=1
        imos[nowr+1]-=1
        
        # print(imos)
        # print()
    
    cur=0
    for i in range(1,n+1):
        cur+=imos[i]
        print(cur,end=' ')

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()