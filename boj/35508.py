import bisect

def solve(n,d,w):
    w2=sorted(w,key=lambda x:x[1])
    ww2=[0]*n
    for i in range(n):
        if i==0:
            ww2[i]=w2[i][3]
        else:
            ww2[i]=max(ww2[i-1],w2[i][3])
    ts=[x[1]for x in w2]
    
    ans=0
    for i,t,a,b in w:
        ans=max(ans,a+b)
        index=bisect.bisect_right(ts,d-t)
        if index!=0:
            ans=max(ans,a+ww2[index-1])
        else:
            ans=max(ans,a+b)
    return ans

def main():
    input=open(0).readline
    n,d=map(int,input().split())
    w=[[i,*map(int,input().split())]for i in range(n)]
    print(solve(n,d,w))
            
main()