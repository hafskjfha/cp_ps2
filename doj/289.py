import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    arr=sorted(tuple(map(int,input().split()))for _ in range(n))
    ans=0
    count=0
    s1,e1=arr[0]
    for i in range(1,n):
        s2,e2=arr[i]
        if e1<s2:
            ans+=(e1-s1)*m
            count+=1
            s1,e1=s2,e2
        elif e1>s2:
            ans+=max(s2-s1,0)*m
            count+=1
            s1,e1=e1,e2
        else:
            s1,e1=s2+1,max(e1,e2)
    ans+=(e1-s1)*m
    print(ans+count)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()