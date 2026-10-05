import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    a=sorted(map(int,input().split()))
    
    now=-1
    for t in a:
        now=max(t+1,now+1)
    
    print(now)

    
main()