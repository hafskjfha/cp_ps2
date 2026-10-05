import sys

def main():
    input=sys.stdin.readline
    t=int(input())
    
    for _ in range(t):
        n=int(input())
        a=[*map(int,input().split())]
        
        for i in range(n-1):
            if a[i]-i-1<0:
                print("NO")
                break
            k=a[i]-i-1
            a[i]=i+1
            a[i+1]+=k
        else:
            if n==1 or a[-2]<a[-1]:
                print("YES")
            else:
                print("NO")
        
    
    
main()