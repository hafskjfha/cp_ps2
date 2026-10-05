import sys
from math import *

input=sys.stdin.readline

def dis(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

dr=[(0,0,2),(3,3,1)]

for i in range(len(dr)):
    x1,y1,r1=dr[i]
    for j in range(i+1,len(dr)):
        x2,y2,r2=dr[j]
        d=sqrt(dis(x1,y1,x2,y2)**2-(abs(r1-r2)**2))
        rr=abs(r1-r2)
        print(4*(sqrt(d**2+rr**2)))