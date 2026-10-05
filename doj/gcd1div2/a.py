import sys
input=sys.stdin.readline

def solve():
    n,m,k=map(int,input().split())
    a=[*map(int,input().split())]
    
    ans=[[None]*m for _ in range(n)]
    
    nowc,nowr=0,0
    for i in range(k):
        ai=a[i]
        while ai:
            ans[nowc][nowr]=i+1
            #print(nowc,nowr,i+1)
            if nowc%2==0:
                if nowr==m-1:
                    nowc+=1
                else:
                    nowr+=1
                
            else:
                if nowr==0:
                    nowc+=1
                else:
                    nowr-=1
                
            
            ai-=1
            
    for x in ans:
        print(" ".join(map(str,x)))
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()