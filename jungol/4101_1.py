import sys
from collections import Counter

def main():
    input=sys.stdin.readline
    n=int(input())
    s=input().strip()
    m=int(input())
    t=input().strip()
    cs=Counter(s)
    ct=Counter(t)
    
    if cs.get('I',0)+ct.get('I',0)>0 and cs.get('C',0)+ct.get('C',0)>1 and cs.get('P',0)+ct.get('P',0)>0:
        print("m4us happy")
    else:
        print("m4us sad ")
    
main()
    