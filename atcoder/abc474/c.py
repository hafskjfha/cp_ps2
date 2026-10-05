import sys
input=sys.stdin.readline

def solve():
    n,q=map(int,input().split())
    a=[*map(int,input().split())]
    idxs={}
    k=n
    for i in range(n):
        idxs[a[i]]=i
    
    for _ in range(q):
        y=int(input())
        idxs[y]=k
        k+=1
    
    d=[x[0] for x in sorted(idxs.items(),key=lambda x:x[1])]
    print(*d)
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()