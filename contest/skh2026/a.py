n=int(input())
s=input()
if 'O' in s:
    ss=set(s)
    #print(ss)
    if len(ss)!=1:
        print("bye")
        #print(len())
    else:
        print("hi")
else:
    print("hi"if len(s)==4 else "bye")