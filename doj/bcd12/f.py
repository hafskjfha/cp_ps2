import sys
input=sys.stdin.readline

ceil = lambda a, b: (a + b - 1) // b

def solve():
    n=int(input())
    a=[0]+[*map(int,input().split())]
    
    count=0
    for i in range(1,2*n+1):
        if a[i]==i:continue
        
        for j in range(i+1,2*n+1):
            if a[j]==i:
                a[i],a[j]=a[j],a[i]
                count+=1
                break
    
    print(ceil(count*2,n),count*2)
    print(a)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()