NUMS="abcdefghijklmnopqrstuvwxzy"
BASE=len(NUMS)
t=int(input())

if t==1:
    n=sum(map(int,input().split()))

    temp=[]
    
    while n>0:
        temp.append(NUMS[n%BASE])
        n//=BASE

    p="".join(temp[::-1])
    print("a"*(13-len(p))+p)
else:
    s=input()
    ans=0
    for c in s:
        idx=NUMS.index(c)
        ans=ans*BASE+idx
    
    print(ans)