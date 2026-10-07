import sys

input=sys.stdin.readline

RIGHTN=3*10**18
INF=float('inf')

def solve():
    n,k=map(int,input().split())
    lab=[]
    
    for _ in range(n): lab.append(tuple(map(int,input().split())))
    
    ans=min(sum(x)for x in lab)
    left,right=ans,RIGHTN
    
    
    while left<=right:
        mid=(left+right)//2
        
        used=0
        
        for a,b,c in lab:
            score=sum([a,b,c])
            if score>=mid:continue
            
            if a>b or a>c or b>c:
                used+=mid-score
            else:
                temp=INF
                if a!=c and b+1-a<temp:temp=b+1-a
                if a!=b and c+1-b<temp:temp=c+1-b
                
                used+=2*temp+mid-score
                #print(mid,temp,used)
    
        #print(mid,used,debug)
        if used<=k:
            ans=mid
            left=mid+1
        else:
            right=mid-1
    
    print(ans)
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()