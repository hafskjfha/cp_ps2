s=input()
n=len(s)
ps=[0]*(n+1)
for i in range(n):ps[i+1]=ps[i]+[-1,1][s[i]=='B']
i=j=-1
mi,ma=float('inf'),float('-inf')
for x in range(n+1):
    if ps[x]>ma:
        ma=ps[x]
        i=x
    if ps[x]<mi:
        mi=ps[x]
        j=x
if i>j:i,j=j,i
i+=1
print(i,j)