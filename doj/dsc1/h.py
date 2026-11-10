import sys,math
input=sys.stdin.readline

# N=100000
# fact=[1]*(N+1)
# for i in range(2,N+1):fact[i]=(fact[i-1]*i)

def solve():
    n=int(input())
    arr=sorted(map(int,input().split()))
    
    ans=math.factorial(n)
    r=1
    
    temp=0
    prev=None
    for x in arr:
        if x==prev:
            temp+=1
        else:
            r*=math.factorial(temp)
            temp=1
            prev=x
    r*=math.factorial(temp)
    #print(r)
    
    print((ans-r)//r)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()