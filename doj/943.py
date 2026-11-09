import sys
input=sys.stdin.readline

def solve():
    hl,hh=map(int,input().split())
    sl,sh=map(int,input().split())
    vl,vh=map(int,input().split())
    r,g,b=map(int,input().split())
    
    ma,mi=max(r,g,b),min(r,g,b)
    v=ma
    s=255*(v-mi)/v
    
    if v==r:
        h=60*(g-b)/(v-mi)
    elif v==g:
        h=120+60*abs(b-r)/(v-mi)
    else:
        h=240+60*abs(r-g)/(v-mi)
    h%=360
    
    if hl<=h<=hh and sl<=s<=sh and vl<=v<=vh:
        print("Lumi will like it.")
    else:
        print("Lumi will not like it.")
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()