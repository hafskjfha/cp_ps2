import sys
input=sys.stdin.readline

def solve():
    n,q=map(int,input().split())
    lv=[0]+[*map(int,input().split())]
    rv=[*map(int,input().split())]+[0]
    
    INF=float('inf')
    tempr=[INF]*n
    templ=[INF]*n
    for i in range(n-1):
        tempr[i+1]=min(tempr[i],rv[i])
    for i in range(n-1,0,-1):
        templ[i-1]=min(templ[i],lv[i])
    
    #print(tempr)
    #print(templ)
    
    for _ in range(q):
        s,t=map(int,input().split())
        if s<t:
            print(min(rv[s-1],lv[s-1]+tempr[s-1]))
        else:
            print(min(lv[s-1],rv[s-1]+templ[s-1]))
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()