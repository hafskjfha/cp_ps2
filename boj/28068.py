import sys
input=sys.stdin.readline
n=int(input())
a,b=[],[]
for _ in range(n):
    x,y=map(int,input().split())
    if y-x<0:b.append((x,y))
    else:a.append((x,y))
a.sort()
b.sort(key=lambda x:(-x[1],-x[0]))
c=0
#print(a)
for x,y in a:
    if x<=c:c+=y-x
    else:exit(print(0))
#print(c,b)
for x,y in b:
    if x<=c:c+=y-x
    else:exit(print(0))
print(1)