n=int(input())

arr=[1]
for i in range(n-1):
    arr.append(i*2+2)
print(*arr)