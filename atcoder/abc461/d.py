import sys

def main():
    input=sys.stdin.readline
    h,w,k=map(int,input().split())
    grid=[[*map(int,input().strip())]for _ in range(h)]
    ps=prefix_sum_2d(grid,h,w)
    
    ans=0
    
    for i in range(h):
        for j in range(i,h):
            pss=[ps[j+1][k]-ps[i][k] for k in range(w+1)]
            
            a,b=0,0
            for l in range(w+1):
                a=max(a,l+1)
                b=max(b,l+1)
                while a<=w and pss[a]-pss[l]<k:a+=1
                while b<=w and pss[b]-pss[l]<=k:b+=1
                
                ans+=b-a
    
    print(ans)
    
def prefix_sum_2d(mat,n,m):
    psum=[[0]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1):
        for j in range(1,m+1):
                psum[i][j] = mat[i-1][j-1]+psum[i-1][j]+psum[i][j-1]-psum[i-1][j-1]
    return psum
    
main()