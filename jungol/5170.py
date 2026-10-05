input=open(0).readline
def sol(K,A,M):
    s=0
    for i in A:
        s+=0 if i-K<0 else i-K
    return 0 if s<M else 1

def main():
    N,M=map(int,input().split())
    A=sorted([*map(int,input().split())])
    start,end=0,A[-1]
    while start<=end:
        mid=(start+end)//2
        if sol(mid,A,M):
            ans=mid
            start=mid+1
        else:
            end=mid-1
    print(ans)
main()