import sys, heapq

def main():
    input=sys.stdin.readline
    n,b=map(int,input().split())
    a=[*map(int,input().split())]
    
    left,right=0,10**18
    ans=-1
    
    while left<=right:
        mid=(left+right)//2
        
        pq=[]
        credit=0
        cost=0
        
        for x in a:
            if x>=mid:
                credit+=1
            else:
                if credit==0:
                    if not pq or x>-pq[0]:
                        cost+=mid-x
                        credit+=1
                    else:
                        k=-heapq.heappop(pq)
                        cost+=mid-k
                        credit+=1
                        heapq.heappush(pq,-x)
                        
                else:
                    heapq.heappush(pq,-x)
                    credit-=1
        
        #print(mid,credit,cost,)
        if cost<=b and 0<=credit:
            ans=mid
            left=mid+1
        else:
            right=mid-1
    
    print(ans)
                    
    
    
main()