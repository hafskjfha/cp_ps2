import sys
from collections import defaultdict
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    arr=[input().strip()for _ in range(n)]
    counter=defaultdict(int)
    
    for i in range(n-k+1):
        counter[tuple(arr[i:i+k])]+=1
    print(*max(counter.items(),key=lambda x:x[1])[0],sep='\n')

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()