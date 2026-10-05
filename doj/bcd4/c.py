import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    INF=float('inf')
    
    minx,maxx=INF,-INF
    miny,maxy=INF,-INF
    for _ in range(n):
        x,y=map(int,input().split())
        minx=min(minx,x)
        maxx=max(maxx,x)
        miny=min(miny,y)
        maxy=max(maxy,y)
    
    h,w=-1,-1
    if (minx>=0 and maxx>=0):
        h=maxx-minx
    elif (minx<0 and maxx<0):
        h=maxx-minx
    else:
        h=maxx-minx
    
    
    if (miny>=0 and maxy>=0):
        w=maxy-miny
    elif (miny<0 and maxy<0):
        w=maxy-miny
    else:
        w=maxy-miny
    
    print(h*2+w*2)
    
main()