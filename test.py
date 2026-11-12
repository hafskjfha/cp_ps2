import math


for a in range(3,10):
    print(a)
    b=c=1
    while 1:
        k=a**2+b**2
        if int(math.sqrt(k)) ** 2 == k:
            print(b,math.sqrt(k))
        
        
        b+=1
        
        if b>1000:break
    