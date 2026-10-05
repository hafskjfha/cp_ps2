import sys
from collections import deque


input=sys.stdin.readline

def solve():
    n,l=map(int,input().split())
    a=[]
    for i in range(n):
        x,y=map(int,input().split())
        a.append((y,x,i,0))
    a.sort()
    
    temp=deque(a)
    #print(temp)
    
    while temp:
        y,x,i,c=temp.popleft()
        if y<=l: l+=y
        elif x<l<y: l+=l
        else:
            
            if c==2:
                #print('??',x,y)
                continue
            temp.append((y,x,i,c+1))
        #print('?',x,y,l,c,x<l)
    
    print(l)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()