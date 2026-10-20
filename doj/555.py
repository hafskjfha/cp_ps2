import sys
input=sys.stdin.readline

def solve():
    s=input().strip()
    n=len(s)
    e,y=-1,-1
    hard=[]
    easy1=[]
    easy2=[[],[]]
    easy3=[[],[]]
    easy4=[[],[]]
    for i in range(n):
        if s[i:i+4]=="HARD":
            hard.append(i)
        if s[i]=="E":
            if e==-1:e=i
            easy4[0].append(i)
        if s[i]=="Y":
            y=i
            easy2[1].append(i)
        if s[i:i+4]=="EASY":
            easy1.append(i)
        if s[i:i+3]=="EAS":
            easy2[0].append(i)
        if s[i:i+2]=="EA":
            easy3[0].append(i)
        if s[i:i+2]=="SY":
            easy3[1].append(i)
        if s[i:i+3]=="ASY":
            easy4[1].append(i)
    
    #print(hard,easy1)
    if e==-1 or y==-1:
        print("No")
        return  

    #print(easy1,easy2,easy3,easy4)
    for i in easy1:
        #print(i,hard[0],hard[-1])
        if not hard or hard[0]>i:
            return print("Yes")
        if not hard or  hard[-1]<i:
            return print("Yes")    
    
    for arr in [easy2,easy3,easy4]:
        if not arr[0] or not arr[1]: continue
        i,j=arr[0][0],arr[1][-1]
        #print(i,j,hard)
        if i<j and (not hard or (i<hard[0] and hard[-1]<j)):
            return print("Yes")
    print("No")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()