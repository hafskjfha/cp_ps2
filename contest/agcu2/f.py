import sys

def main():
    input=sys.stdin.readline
    for _ in range(int(input())):
        n,m,k=map(int,input().split())
        print(m)
    
main()