import sys
from itertools import permutations

def main():
    input=sys.stdin.readline
    p=permutations(map(int,input().split()),3)
    h=int(input())
    
    ans=float('inf')
    
    for y in p:
        temp=0
        hh=h
        for x in y:
            if hh>x//2:
                hh-=x//2
                temp+=x//2
            else:
                temp+=x
        ans=min(ans,temp)
    print(ans)
    
main()