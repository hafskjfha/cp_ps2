import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=sorted([2**x for x in map(int,input().split())])
    s=sum(arr)
    a,b=0,s
    #print(s,s//2)
    for i in range(n-1,-1,-1):
        if a+arr[i]>s//2:continue
        a+=arr[i]
        b-=arr[i]
    
        #print(a,b)
    print(a*b)

def main():
    t=int(input())
    for _ in range(t):
        solve()
        #print("======")
main()