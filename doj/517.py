import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    print((n+2)*(n-1))
    res=[]
    for i in range(2,n+1):
        res.append(f"1 {i} D")
    for i in range(n+1,2,-1):
        res.append(f"1 {i} L")
    
    for i in range(2,n+1):
        for j in range(i+n,2*i,-1):
            res.append(f"1 {j} L")
    
    for i in range(n,1,-1):
        for j in range(i,2*i-1):
            res.append(f"2 {j} R")
        res.append(f"2 {2*i-1} U")
        
    print("\n".join(res))
    assert len(res)==(n+2)*(n-1)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()