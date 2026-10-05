a,b,c=map(int,open(0))
n=a*b*c

count=[0]*10

while n>0:
    count[n%10]+=1
    n//=10

print(*count,sep='\n')
