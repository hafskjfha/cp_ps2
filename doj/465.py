import sys
input=sys.stdin.readline

n,p,q=map(int,input().split())
a=[*map(int,input().split())]
b=[*map(int,input().split())]

pc,qc=0,0
ans=0
for x in b:
    if x==p:pc+=1
    else: qc+=1

ok=[False]*n

c=[x%p for x in a]
d=[]

for i in range(n):
    x=c[i]
    d.append((a[i]%q-x,i))

#print(sorted(d)[:qc],sorted(d)[qc:])
#print(d)

for _,i in sorted(d)[:qc]:
    ans+=a[i]%q
    
for _,i in sorted(d)[qc:]:
    ans+=a[i]%p
        
print(ans)

