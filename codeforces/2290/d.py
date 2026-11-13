import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[ord(c)-ord('a') for c in input().strip()]
    
    check=[0]*26
    for i in range(n//2):
        if arr[i]>arr[n-i-1]:arr[i],arr[n-i-1]=arr[n-i-1],arr[i]
        
        for j in range(arr[i]+1,arr[n-i-1]+1):
            check[j]=1
    print(sum(check))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()