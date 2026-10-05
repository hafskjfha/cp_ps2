import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    a=[*map(int,input().split())]
    r=0
    for i in range(n-1,0,-1):
        if a[i]<a[i-1]:
            r+=1
            a[i-1]=a[i]
    print(r)
    print(*a)
    
main()