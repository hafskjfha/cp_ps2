import sys

def main():
    input = sys.stdin.readline

    for _ in range(int(input())):
        n=int(input())
        a=[*map(int,input().split())]
        
        if sovle(n,a):
            print("Yes")
        else:
            print("No")
        

def sovle(n,a):
    for x in range(1000000):
        for i in range(n-1):
            if a[i]>x: break
            a[i+1]+=x-a[i]
            a[i]=x
        else:
            if a[n-1]==x:
                return True
    
    return False

main()