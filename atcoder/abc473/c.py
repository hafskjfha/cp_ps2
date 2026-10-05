import sys

def main():
    input=sys.stdin.readline
    n,k=map(int,input().split())
    a=[*map(int,input().split())]
    
    count={}
    for x in a:
        count[x]=count.get(x,0)+1
    
    mav=max(count.values())
    
    ans=0
    
    for v in count.values():
        if v==mav or v==mav-1:
            ans+=1
            
    print(ans)
    
    
    
main()