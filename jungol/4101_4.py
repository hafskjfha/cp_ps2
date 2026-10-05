import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    s=input().strip()
    
    ans=[]
    temp,count=s[0],1
    for i in range(1,n):
        c=s[i]
        if c!=temp:
            if count>1:
                if temp>c:
                    ans.append(temp)
                else:
                    for _ in range(count):
                        ans.append(temp)
                temp=c
                count=1
            else:
                ans.append(temp)
                temp=c
        else:
            count+=1
    
    ans.append(temp)
    
    print("".join(ans))

main()