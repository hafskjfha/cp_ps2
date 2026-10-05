import sys

def main():
    input=sys.stdin.readline
    for _ in range(int(input())):
        n=int(input())
        a=[*map(int,input().split())]
        ans=1
        dadas=a[0]
        for i in range(1,n):
            if dadas>a[i]:
                ans+=1
            else:
                break
        print(ans)
    
main()