import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    temp0=[]
    temp1=[]
    for i in range(n):
        if a[i]:temp1.append(i+1)
        else:temp0.append(i+1)
    
    res=[]
    if not temp0:
        print(*temp1)
    elif not temp1:
        print(*temp0[::-1])
    elif temp1[-1]<temp0[-1]:
        print(*temp1,*temp0[::-1])
    elif temp0[0]>temp1[0]:
        print(*temp0[::-1],*temp1)
    else:
        print(-1)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()