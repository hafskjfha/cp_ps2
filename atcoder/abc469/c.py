import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    
    o,x=0,0
    cc=0
    
    for i in range(n):
        if s[i]=='o':
            o+=1
        else:
            x+=1
            print(o+x)
            cc+=1     
    
    for _ in range(n-cc):print(n)
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()