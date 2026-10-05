import sys

def main():
    input=sys.stdin.readline
    [print(*x) for x in sorted([[*map(int,input().split())] for _ in range(int(input()))],key=lambda x:(x[0],-x[1]))]
    
main()