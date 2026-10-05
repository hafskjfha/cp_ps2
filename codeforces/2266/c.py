import sys
input=sys.stdin.readline
INF=float('inf')

def solve():
    n=int(input())
    s=input().strip()
    c0=[0]*(n+1)
    c1=[0]*(n+1)
    for i in range(1,n+1):
        if s[i-1]=='0':
            c0[i]=c0[i-1]+1
            c1[i]=c1[i-1]
        else:
            c1[i]=c1[i-1]+1
            c0[i]=c0[i-1]
    
    # print(c0)
    # print(c1)
    
    ans=INF
    if s[0]=='0':ans=c1[n]
    else:ans=c0[n]
    
    for i in range(n-1):
        if s[0]=='0' and s[i]=='0' and s[i+1]=='1':
            ans=min(ans, c1[i+1]+c0[-1]-c0[i+2])
            
    
            
    print(ans)
    #print('----')

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()