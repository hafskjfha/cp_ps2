def main():
    input=open(0).readline
    n,k=map(int,input().split())
    a=[*map(int,input().split())]
    r=0
    
    if k>0:
        for i in range(1,n):
            t=max(0,(a[i-1]-a[i]+1)//k+(((a[i-1]-a[i]+1)%k)!=0))
            r+=t
            a[i]+=k*t
            
            
    else:
        tk=-k
        for i in range(n-2,-1,-1):
            t=max(0,(a[i]-a[i+1]+1)//tk+(((a[i]-a[i+1]+1)%tk)!=0))
            #print(i,a,t,(a[i]-a[i+1]-1),((a[i]-a[i+1]-1)%tk)!=0)
            r+=t
            a[i]+=k*t

            
    print(r)
        
        

main()