import sys
from collections import deque

def main():
    input=sys.stdin.readline
    
    q=deque()
    n=int(input())
    for _ in range(n):
        cmd,*i=input().split()
        if cmd=='i':
            q.append(i[0])
        elif cmd=='o':
            if q:
                print(q.popleft())
            else:
                print('empty')
        else:
            print(len(q))
    
main()