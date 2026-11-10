import sys
from decimal import *
input=sys.stdin.readline

def solve():
    temp=["N", 
    "NNE", 
    "NE", 
    "ENE", 
    "E", 
    "ESE", 
    "SE", 
    "SSE", 
    "S", 
    "SSW", 
    "SW", 
    "WSW", 
    "W", 
    "WNW", 
    "NW", 
    "NNW",
    "N"
    ]
    deg=[0,112.5,337.5,562.5,787.5,1012.5,1237.5,1462.5,1687.5,1912.5,2137.5,2362.5,2587.5,2812.5,3037.5,3262.5,3487.5]
    fu=[0,3,16,34,55,80,108,139,172,208,245,285,327,9999999999999999999999999999999]
    
    dg,ds=input().strip().split()
    
    dg=int(dg)
    kkkkk="N"
    for i in range(len(temp)-1):
        if deg[i]<=dg<deg[i+1]:
            kkkkk=temp[i]
            break
    #print(kkkkk)
    
    ds=Decimal(ds)/Decimal("60")
    
    ds=ds.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)*10
    #print(ds)
    for i in range(len(fu)-1):
        #print(i,fu[i],ds,fu[i+1])
        if fu[i]<=ds<fu[i+1]:
            return print(kkkkk if i!=0 else "C",i)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()