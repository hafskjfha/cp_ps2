import sys
input=sys.stdin.readline

ceil = lambda a, b: (a + b - 1) // b

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    ans=0
    
    for i in range(1,n):
        if arr[i]>=arr[i-1]:continue
        ans+=ceil(arr[i-1]-arr[i],2)
        arr[i]+=2*ceil(arr[i-1]-arr[i],2)
    
    #print(arr)
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()