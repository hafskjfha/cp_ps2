import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    count=[0]*14
    for x in a:count[x]+=1
    
    maxv,maxi=-1,-1
    for i in range(1,14):
        if maxv<=count[i]:
            maxv=count[i]
            maxi=i
    
    if maxi==1:
        print(-1)
    else:
        print(maxi)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()