def s(b,n,m,pr,pc,sd):
    delta=(0,-1),(1,0),(0,1),(-1,0)
    sl=1,0,3,2
    bs=3,2,1,0
    v=[[[0]*4 for _ in range(m)]for _ in range(n)]
    c=1
    v[pr][pc][sd]=1
    while 1:
        dx,dy=delta[sd]
        pr,pc=pr+dy,pc+dx
        if 0<=pc<m and 0<=pr<n and b[pr][pc]!='C':
            if v[pr][pc][sd]:return "Voyager"
            c+=1
            v[pr][pc][sd]=1
            if b[pr][pc]=='/':
                sd=sl[sd]
            elif b[pr][pc]=='\\':
                sd=bs[sd]
        else:
            return c
        
def main():
    I=open(0).readline
    n,m=map(int,I().split())
    b=[I().strip()for _ in range(n)]
    pr,pc=map(int,I().split())
    ansd=0
    ansc=0
    for sd in range(4):
        v=s(b,n,m,pr-1,pc-1,sd)
        if v=="Voyager":return print(f"{'URDL'[sd]}\n{v}")
        if v>ansc:
            ansc=v
            ansd=sd
    print("URDL"[ansd])
    print(ansc)
main()