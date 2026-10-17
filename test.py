def log(x):
    r=1
    t=0
    while r*2<=x:
        r*=2
        t+=1
    return t+1
print(log(7),log(8))