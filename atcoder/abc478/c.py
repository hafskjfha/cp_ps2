import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    a=[*map(int,input().split())]
    
    soa=sorted(a)
    
    for i in range(n):
        if a[i]!=soa[i]:
            break
    
    for j in range(n-1,-1,-1):
        if a[j]!=soa[j]:
            break

    if j-i+1<=k:
        print("Yes")
    else:
        print("No")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()