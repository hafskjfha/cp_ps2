from bisect import *
import sys
input=sys.stdin.readline
YO=["MON","TUE","WED","THU","FRI","SAT","SUN"]
n,q=map(int,input().split())
plan=[[]for k in range(7)]
check=[[]for k in range(7)]
for _ in range(n):
    d,s,e,k=input().split()
    d=YO.index(d)
    sm,ss=map(int,s.split(":"))
    em,es=map(int,e.split(":"))
    check[d].append((em*60+es,len(plan[d])))
    plan[d].append((sm*60+ss,em*60+es,k))

for _ in range(q):
    d,t=input().split()
    m,s=map(int,t.split(':'))
    d=YO.index(d)
    idx=bisect_left(check[d],(m*60+s,-1))
    #print(m*60+s,idx,len(check[d]),plan[d])
    if idx==len(check[d]) or m*60+s<plan[d][idx][0]:
        print("Kiryong is free!!!")
    else:
        print(plan[d][idx][2])