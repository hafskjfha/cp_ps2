import sys

input=sys.stdin.readline

def solve():
    a,b=map(int,input().split())
    if b>a+1:
        print(-1)
        return
    
    if (a+b)%2==0:print(a)
    else:print(a+1)
                    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()