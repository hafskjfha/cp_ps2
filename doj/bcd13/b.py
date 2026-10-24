import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    a=[*map(int,input().split())]
    
    left,right=1,10**9
    ans=right
    while left<=right:
        mid=(left+right)//2
        
        count=1
        temp=0
        for x in a:
            if temp+x>mid:
                count+=1
                temp=0
            
            if temp==0:
                if mid<x:
                    count=float('inf')
                    break
            
            temp+=x
        
        #print(mid,count,temp)
        
        if count<=m:
            ans=mid
            right=mid-1
        else:
            left=mid+1
    
    print(ans)
        
        

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()