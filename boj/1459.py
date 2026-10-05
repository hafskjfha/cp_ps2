x,y,w,s=map(int,input().split())
if s<w*2:
    if y>x:
        print(x*s+(y-x)*s+(y-x)%2*w)
    else:
        print(y*s+(x-y)*s+(x-y)%2*w)
else:
    print((x+y)*w)