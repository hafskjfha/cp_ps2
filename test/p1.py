def fpow1(a,b,mod):
    res=1
    while b:
        if b&1:
            res=(res*a)%mod
        a=(a*a)%mod
        b>>=1
    return res

def fpow2(a,b:int,mod):
    res=1
    for i in range(b.bit_length()-1,-1,-1):
        res=(res*res)%mod
        if (b>>i)&1:
            res=(res*a)%mod
    return res

print(pow(2,10000,int(1e9+7)),fpow1(2,10000,int(1e9+7)),fpow2(2,10000,int(1e9+7)))

def naiv_pow(a,b,mod):
    res=1
    for _ in range(b):
        res=(res*a)%mod

import time

a=3
b=100_000
mod=int(1e9)+7
start1=time.perf_counter()
r1=naiv_pow(a,b,mod)
end1=time.perf_counter()
print(end1-start1)

start1=time.perf_counter()
r1=fpow1(a,b,mod)
end1=time.perf_counter()
print(f"{end1-start1:.15f}")

start1=time.perf_counter()
r1=fpow2(a,b,mod)
end1=time.perf_counter()
print(f"{end1-start1:.15f}")

start1=time.perf_counter()
r1=pow(a,b,mod)
end1=time.perf_counter()
print(f"{end1-start1:.15f}")