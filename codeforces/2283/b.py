import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    temp=[1]*n
    
    for i in range(n):
        for j in range(n):
            if i==j:continue
            if arr[j]%arr[i]==0:
                temp[i]+=1
    #print(temp)
    print(n-max(temp))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()