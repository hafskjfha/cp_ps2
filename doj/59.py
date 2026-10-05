import sys

def main():
    MOD=998244353
    input=sys.stdin.readline
    n,p,q=map(int,input().split())
    
    if p<0:
        y=pow(pow(n,-1,MOD),-p,MOD)
    else:
        y=pow(n,p,MOD)
        
    
    print(pow(y,pow(q,-1,MOD-1),MOD))
    
    
main()