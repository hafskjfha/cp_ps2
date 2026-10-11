arr=[*map(int,"1 2 3 3 2 1 3".split())] #[1,1,1]
print(arr)
n=len(arr)

temp=0
for i in range(n):
    t=arr[i]
    if t==0:
        temp+=1
        print(i,i)
    for j in range(i+1,n):
        t^=arr[j]
        if t==0:
            temp+=1
            print(i,j)

print(temp)