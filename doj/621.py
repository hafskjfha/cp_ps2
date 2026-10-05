import sys
from collections import defaultdict
input=sys.stdin.readline

def shash(s):
    idx=[-1]*26
    now=0
    temp=[]
    for c in s:
        if idx[ord(c)-65]==-1:
            idx[ord(c)-65]=now
            now+=1
        temp.append(idx[ord(c)-65])
    return tuple(temp)

def solve():
    n=int(input())
    arr=input().split()
    s=input().strip()
    
    sh=shash(s)
    
    count=defaultdict(int)
    for x in arr:count[x]+=1
    
    ans="-1"
    maxv=0
    for k,v in count.items():
        if len(k)!=len(s) or sh!=shash(k): continue
        if maxv==0:
            ans=k
            maxv=v
            continue
        
        if maxv==v:
            ans = ans if ans<k else k
        elif maxv<v:
            ans=k
            maxv=v
            
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()