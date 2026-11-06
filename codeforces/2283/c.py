import sys
input=sys.stdin.readline

def solve():
    m=0
    n=int(input())
    arr=[*range(1,n+1)]
    for i in range(n):
        if (arr[i]&(arr[i]-1))==0:
            arr[i]<<=1
    for x in arr:
        m^=x
    print(arr)
    print(2**n.bit_length()-1,m)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()