import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    b=[*map(int,input().split())]
    
    ans=sum([2 if a[i]==b[i] else 1 for i in range(n)])
    prefixSum=[0]
    for i in range(n-1):
        temp=0
        temp+=2 if a[i]==b[i+1] else 1
        temp+=2 if a[i+1]==b[i] else 1
        prefixSum.append(prefixSum[-1]+temp)
        ans+=(2 if b[i]==a[i+1]else 1)

    #print(prefixSum)
    
    temp=0
    for i in range(n-1):
        ans=max(ans,temp+prefixSum[-1]-prefixSum[i]+(2 if a[-1]==b[-1] else 1))
        #print(temp+prefixSum[-1]-prefixSum[i]+(2 if a[-1]==b[-1] else 1))
        temp+=(2 if a[i]==b[i] else 1)+(2 if b[i]==a[i+1] else 1)
    print(ans)
    #print("-----")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()