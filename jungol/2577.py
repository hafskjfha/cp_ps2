def main():
    input=open(0).readline
    n,d,k,c=map(int,input().split())
    a=[int(input())for _ in range(n)]
    eat={c:0}
    count=ans=0
    for i in range(k):
        if eat.get(a[i],0)==0:
            count+=1
            eat[a[i]]=0
        eat[a[i]]+=1
        ans=count + (eat[c]==0)
    
    
    for i in range(k,n+k):
        eat[a[(i-k)%n]]-=1
        if eat[a[(i-k)%n]]==0:count-=1
        
        if eat.get(a[i%n],0)==0:
            count+=1
            eat[a[i%n]]=0
        eat[a[i%n]]+=1
        
        ans=max(ans,count + (eat[c]==0))
            
            
    print(ans)
main()