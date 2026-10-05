import sys

input=sys.stdin.readline

dr='NESW'
now=0
for _ in range(10):
    t=int(input())
    if t==1:
        now=(now+1)%4
    elif t==2:
        now=(now+2)%4
    else:
        now=(now-1)%4

print(dr[now])