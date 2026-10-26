import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    c=0
    k=n
    for i in range(n):
        if s[i]=='0':
            k=i
            break
    else:
        return print(0)
    
    ans=0
    i=k
    while i<n-1:
        if s[i]==s[i+1]=='1':
            ans+=i-k
            k+=2
            i+=2
        elif s[i]=='1' and s[i+1]=='0':
            return print(-1)
        else:
            i+=1
    #print(i)
    print(ans if i>=n or s[i]!='1' else -1)
            

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()