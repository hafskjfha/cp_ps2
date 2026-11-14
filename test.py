import random
def temp():
    check=[0]*64

    N=random.randint(1,10000)

    for i in range(1,N+1):
        t=bin(i)[2:].zfill(64)[::-1]
        #print(*t)
        for j in range(len(t)):
            if t[j]=='0':
                check[j]+=1

    for i in range(64):
        k=(1<<i)
        assert check[i]==min(N,k-1+max(0,(N-k+1)//(k<<1)*k)+max(0,(N-k+1)%(k<<1)-k))

for i in range(100):
    temp()