import sys

def main():
    input=sys.stdin.readline
    x,y=map(int,input().split())
    l1,l2=map(int,input().split())
    t=sorted([(x**2+y**2)**0.5,l1,l2])
    #print(t,t[:2])
    print("YNEOS"[t[2]>sum(t[:2])::2])
    
main()