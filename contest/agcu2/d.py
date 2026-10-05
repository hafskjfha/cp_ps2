import sys
from collections import Counter

def main():
    input=sys.stdin.readline
    n=int(input())
    x=Counter([int(input())%7 for _ in range(n)])
    p,_=max(x.items(),key=lambda x:x[1])
    print(7 if p==0 else p)
    
main()