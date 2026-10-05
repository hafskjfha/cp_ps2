import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    a=[*map(int,input().split())]
    
    r=0
    for i in range(1,n):
        if abs(a[i]-a[i-1])!=1:
            if abs(a[i]-a[i-1])==0:r+=1
            else:r+=abs(a[i]-a[i-1])-1
    
    print(r)
    
main()