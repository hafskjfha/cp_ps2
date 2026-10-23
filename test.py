s="0011"
k=3
print(s,s.count("1"))

for _ in range(k):
    arr=[]
    arr.append(s[0])
    for i in range(1,len(s)):
        if arr[-1]=="1" or s[i]=="1":
            arr.append("1")
        else:
            arr.append("0")
        arr.append(s[i])
    
    s="".join(arr)
    print(s,s.count("1"))