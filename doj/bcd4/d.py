import sys

def main():
    INF=float('inf')
    input=sys.stdin.readline
    n,m=map(int,input().split())
    a=[*map(int,input().split())]
    b=[*map(int,input().split())]
    
    submina,submaxa=subf(a,n,'m'),subf(a,n,'M')
    subminb,submaxb=subf(b,m,'m'),subf(b,m,'M')
    
    print(max(
        submaxa*submaxb,
        submina*subminb,
        submina*submaxb,
        submaxa*subminb
    ))


def subf(arr,n,k):
    fun=min if k=='m' else max
    res=arr[0]
    temp=arr[0]
    
    for i in range(1,n):
        x=arr[i]
        temp=fun(x,temp+x)
        
        if k=='M':
            if temp > res:res=temp
        else:
            if temp < res:res=temp
    
    return res

    # 카데인 알고리즘
    # dp[i] = i번을 포함하여 만들수 있는 부분합의 최댓/최솟값
    # dp[i] = max(dp[i-1]+arr[i],arr[i])
    # 이전값에 i번 요소를 더하거나(바로 이어붙이거나) i번 요소에서 새로 시작
        
    
main()