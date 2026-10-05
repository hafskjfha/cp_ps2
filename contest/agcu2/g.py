import sys

def main():
    input=sys.stdin.readline
    n,q=map(int,input().split())
    s=sum(map(int,input().split()))
    for _ in range(q):
        c,*k=map(int,input().split())
        if c==2:
            print(s)
        else:
            s+=(k[1]-k[0]+1)*k[2]
    
main()