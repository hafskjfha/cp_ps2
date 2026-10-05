import math
input=open(0).readline

for _ in range(int(input())):
    n,x=input().split()
    n,x=int(n),float(x)

    sum=n
    arr=[1]*n
    idx=0
    while sum<=5*n:
        if sum/n == x:
            print(*arr)
            break
        sum+=1
        arr[idx]+=1
        idx=(idx+1)%n
    else:
        print(-1)
