import sys
from collections import Counter
input=sys.stdin.readline

def solve():
    n=int(input())
    arra=[*map(int,input().split())]
    arrb=[*map(int,input().split())]
    if Counter(arra)!=Counter(arrb):
        return print("No")

    l,r=-1,-1
    for i in range(n):
        if arra[i]!=arrb[i]:
            if l==-1:l=i
            else:r=i
    
    #print(l,r)
    print("Yes" if arra[l+1:r+1]==arrb[l:r] or arra[l:r]==arrb[l+1:r+1] else "No")
    #print()

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()