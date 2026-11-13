import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=sorted(map(int,input().split()))
    
    res=[None]*n
    idx=(n-1)//2
    for j in range(n):
        #print(idx)
        res[idx]=arr.pop()
        if j%2==0:
            idx+=j+1
        else:
            idx-=j+1
            
        #print(*res)
    
    check=[0]*n
    check[0]=check[n-1]=1
    for i in range(1,n):
        if res[i-1]<res[i] and check[i]==0:
            check[i]=1
    
    for i in range(n-2,-1,-1):
        if res[i+1]<res[i] and check[i]==0:
            check[i]=1
    
    #print(check)
    print(sum(check))
    print(*res)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()