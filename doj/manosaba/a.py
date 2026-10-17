import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    a=sorted(zip([*map(int,input().split())],range(1,n+1)))
    last=a[-1]
    ans=[]
    for i in range(n-1,-1,-1):
        if last==a[i][0]:
            ans.append(a[i][1])
            k-=1
            continue
        
        if k>=0:
            last=a[i][0]
            ans.append(a[i][1])
            k-=1
        else:
            break
    print(len(ans))
    print(*ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()