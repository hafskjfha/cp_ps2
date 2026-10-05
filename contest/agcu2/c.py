import sys
from itertools import combinations

def main():
    input=sys.stdin.readline
    n=int(input())
    k=[1,2,4,8]
    d={1:'A',2:'G',4:'C',8:'U'}
    if n==15:
        return print('AGCU')
    for x in combinations(k,1):
        if n==x[0]:
            return print(d[x[0]]*4)
    
    for x in combinations(k,2):
        if n==sum(x):
            return print(d[x[0]]*2+d[x[1]]*2)
    
    for x in combinations(k,3):
        if n==sum(x):
            return print(d[x[0]]*2+d[x[1]]+d[x[2]])
    
main()