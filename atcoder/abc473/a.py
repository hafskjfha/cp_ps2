import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    a=[*map(int,input().split())]
    print(sum(a[n//2:]))
    
main()