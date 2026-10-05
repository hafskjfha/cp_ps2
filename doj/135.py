import sys

def main():
    input=sys.stdin.readline
    a,b=map(int,input().split())
    x=f(a,b)
    
    if f(6,30)<=x<=f(9,0) or f(9,50)<=x<=f(10,0) or f(10,50)<=x<=f(11,0) or f(11,50)<=x<=f(12,0) or f(12,50)<=x<=f(13,50) or f(14,40)<=x<=f(14,50) or f(15,40)<=x<=f(15,50) or f(16,40)<=x<=f(22,50):
        print('Yes')
    else:
        print('No')

def f(a,b):
    return a*60+b

main()