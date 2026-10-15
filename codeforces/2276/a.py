import sys
input=sys.stdin.readline

def solve():
    a,b=map(int,input().split())
    for x in range(b,0,-1):
        y,z=divmod(b,x)
        #print(x,y,z,(y+1)*x,(y+2)*z)
        if a>=((y+1)*x+z):
            
            print(x)
            return
    print(-1)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()