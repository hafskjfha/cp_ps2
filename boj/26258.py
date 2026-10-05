import bisect as b
I=open(0).readline
m={}
d=[]
for i in range(int(I())):
    x,y=map(int,I().split())
    d.append(x)
    if i:m[i]=(y>p)-(y<p)
    p=y
for _ in range(int(I())):print(m[b.bisect_left(d,float(I()))])