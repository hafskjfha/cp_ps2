d,n=input().split()
n=int(n)
d=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].index(d)
tsum=0
for ip in input().split():
    m,s=map(int,ip.split(":"))
    tsum+=m*60+s

#print(tsum)
ans=tsum//24300*7
tsum%=24300
for i in range(7):
    #print(tsum)
    if tsum<=0:break
    ans+=1
    tsum-=2700 if d<=4 else 5400
    d=(d+1)%7

    
print(ans)