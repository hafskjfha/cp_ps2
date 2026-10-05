import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    
    count=0
    flg=False
    for c in s:
        if c=='(':
            count+=1
        else:
            count-=1
    print(count)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()