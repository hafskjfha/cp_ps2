import sys
from itertools import permutations

input=sys.stdin.readline

def com(ss):
    temp=[]
    l=ss[0]
    for i in range(1,len(ss)):
        if ss[i]!=l:
            temp.append(l)
            l=ss[i]
    temp.append(l)
    return "".join(temp)

def solve():
    s=input().strip()
    
    sl=list(s)
    tt=set([com(sl)])
    for i in range(1,len(s)-1):
        if sl[i]=='1':
            sl[i]='0'
            tt.add(com(sl))
            sl[i]='1'
        else:
            sl[i]='1'
            tt.add(com(sl))
            sl[i]='0'
    #print(tt)
    print(len(tt))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()