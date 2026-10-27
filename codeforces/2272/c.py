import sys
input=sys.stdin.readline

ceil = lambda a, b: (a + b - 1) // b

RMAX=10**18

def solve():
    n,x=map(int,input().split())
    a=[*map(int,input().split())]
    left,right=1,RMAX
    ans=RMAX
    while left<=right:
        mid=(left+right)//2
        temp=0
        temp2=[]
        for i in range(n-1):
            if a[i+1]-a[i]>mid:
                if i>0:
                    if a[i]-a[i-1]>mid:
                        temp+=ceil(min(a[i]-a[i-1],a[i+1]-a[i]),mid)-1
                else:
                    ...
        
        print(mid,temp)
        if temp<=x:
            ans=mid
            right=mid-1
        else:
            left=mid+1
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()