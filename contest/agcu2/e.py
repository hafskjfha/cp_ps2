import sys

def main():
    input=sys.stdin.readline
    n,m=map(int,input().split())
    print("YNEOS"[sum(map(int,input().split()))<=sum(map(int,input().split()))::2])
    
main()