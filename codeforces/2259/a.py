import sys

input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    s=input().strip()
    
    ans=0
    for i in range(0,n,k):
        if "0" not in s[i:i+k]:
            ans+=1
    
    print(ans)
    
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
    
    
main()