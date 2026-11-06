n=7
arr=[*range(1,n+1)]

k=0
for x in arr:
    k|=x

arr2=[1,2,3,4,5*2,6,7]
m=0
for x in arr2:
    m^=x

print(k,m)