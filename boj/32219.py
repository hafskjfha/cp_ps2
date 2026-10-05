input=open(0).readline
for _ in range(int(input())):
    r,c=map(int,input().split())
    if r==c:print('dohoon')
    else:
        print('jinseo')
        print(min(r,c),min(r,c))