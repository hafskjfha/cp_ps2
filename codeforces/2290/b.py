import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    pen="RB"
    now=0
    ans=0
    for c in s:
        #print(c,pen[now])
        if pen[now]!=c:
            ans+=1
        else:
            now=(now+1)%2
    
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()