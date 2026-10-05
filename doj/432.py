n=int(input())

c=[*range(1,n+1)]

while len(c)>9:
    a,b=c[:len(c)//2],c[len(c)//2:]
    print('?',len(a),*a)
    res=input()
    if res=="YES":c=b
    else:c=a

for x in c:
    print('?',len(c)-1,*[i for i in c if i!=x])
    res=input()
    if res=="YES":
        print('!',x)
        exit(0)