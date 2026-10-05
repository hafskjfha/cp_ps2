import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    for i in range(n//10):
        k=[*range(i*10+1,(i+1)*10+1)]
        sub=sorted(a[i*10:(i+1)*10])
        if sub!=k:
            print("No")
            return
    print("Yes")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()