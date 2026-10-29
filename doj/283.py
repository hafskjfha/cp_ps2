import sys
input=sys.stdin.readline

def fprint(*agv):
    print(*agv,flush=True)

def solve():
    s=input().strip()
    t=int(input())
    for _ in range(t):
        n,m=map(int,input().split())
        count=[0]*n
        for _ in range(m):
            u,v=map(int,input().split())
            count[u-1]+=1
            count[v-1]+=1
        #fprint(count)
            
        if s=="dadas08":
            fprint("".join(map(str,[c%2 for c in count])))
        else:
            k=input().strip()
            res=[]
            for i in range(n):
                if count[i]%2!=int(k[i]):
                    res.append(i+1)
            fprint(*res)

def main():
    solve()
main()