n=int(input())
a=[*map(int,input().split())]
for i in range(n-1):
    tempmin,ind=a[i],i
    for j in range(i+1,n):
        if tempmin>a[j]:
            tempmin=a[j]
            ind=j
    a[i],a[ind]=a[ind],a[i]
    print(*a)