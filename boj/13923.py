input=open(0).readline
while 1:
    x=input()
    if not x:break
    n=int(x)
    b=[input().strip()for _ in range(n)]
    r=[[0]*26 for _ in range(n)]
    c=[[0]*26 for _ in range(n)]

    for i in range(n):
        for j in range(n):
            r[i][ord(b[i][j])-65]+=1
            c[i][ord(b[j][i])-65]+=1

    d1={}
    d2={}
    for i in range(n):
        d1.setdefault(tuple(r[i]),[]).append(i+1)
        d2.setdefault(tuple(c[i]),[]).append(i+1)

    r=c=None
    mr=mc=None
    for k,v in d1.items():
        if len(v)==1:
            r=k,v[0]
        else:
            mr=k
    for k,v in d2.items():
        if len(v)==1:c=v[0]
    ansc=None
    for i in range(26):
        if int(r[0][i])<int(mr[i]):
            ansc=chr(65+i)
    print(r[1],c,ansc)