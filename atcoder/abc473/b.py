import sys
from collections import Counter

def main():
    input=sys.stdin.readline
    n=int(input())
    count=Counter([*map(int,input().split())])
    
    print(sum(x for x,v in count.items() if v%2))
    
main()