n=int(input())
t="OIZEASGTBQ"
t2={"O":"0","I":"1","Z":"2","E":"3","A":"4","S":"5","G":"6","T":"7","B":"8","Q":"9"}
for _ in range(n):
    s=input()
    ans=[]
    for c in s:
        if c.isalpha():
            if c in t2:
                ans.append(t2[c])
            else:
                ans.append(c)
        else:
            ans.append(t[int(c)])
    print("".join(ans))