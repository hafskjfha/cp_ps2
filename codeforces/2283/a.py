import sys
input=sys.stdin.readline

def solve():
    l,r=map(int,input().split())
    if l==r:
        print(0)
    elif l==0 or r==0:
        print(r-l-1)
    elif (l<0 and r<0) or (l>0 and r>0):
        print(r-l)
    else:
        print(max(0,(r-l+1)-(min(-l,r)*2+2)))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()