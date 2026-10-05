import sys
input=sys.stdin.readline

def divcon(mat,n,col,row,fun):
    if n==0:
        return (mat[col][row],mat[col][row])
    
    s1,m1=divcon(mat,n-1,col,row,fun)
    s2,m2=divcon(mat,n-1,col,row+2**(n-1),fun)
    s3,m3=divcon(mat,n-1,col+2**(n-1),row,fun)
    s4,m4=divcon(mat,n-1,col+2**(n-1),row+2**(n-1),fun)
    
    k=fun(m1+s2+s3+s4, s1+m2+s3+s4, s1+s2+m3+s4, s1+s2+s3+m4)
    return (k,fun(m1,m2,m3,m4))

def solve():
    n=int(input())
    a=[]
    for _ in range(2**n):
        a.append([*map(int,input().split())])
    #print(a)
    
    print(divcon(a,n,0,0,min)[0],divcon(a,n,0,0,max)[0])

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()