n=4

target=[[-1]*(2*n+1),[-1]*(2*n+1)]
print(target)
for i in range(n):
    target[0][2*i+1]=i+1
    target[0][2*i+2]=i+1
print(target)