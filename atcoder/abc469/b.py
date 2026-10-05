import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    
    if n==1:
        if s=='x':print(1)
        else:print(0)
        return
    
    ans=0
    for i in range(n):
        if s[i:i+3]=="xxx":ans+=1
        
    if s[0]==s[1]=='x':ans+=1
    if s[-2]==s[-1]=='x':ans+=1
    
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()