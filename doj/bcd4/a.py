import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    a=sorted(map(int,input().split()))
    b=sorted(map(int,input().split()))
    
    print(max(
        a[0]*b[0],
        a[-1]*b[0],
        a[0]*b[-1],
        a[-1]*b[-1]
    ))
    
    
main()