p=5
arr=[p,1,1,1,1]+[0,0,0,0,0,0]
x=2*10**9

t=3

for k in range(6,11):
    si=0
    for i in range(p):
        temp=0
        for j in range(k-i-1):
            #print(i,j)
            temp+=arr[j]
        si+=temp**(p-i)
        #print(temp**(p-i))
    #print(f'! a{k}=',si)
    arr[k]=si

print(arr)