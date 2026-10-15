import sys
input=sys.stdin.readline

def solve():
    s=input().strip()
    ans=1
    temp=1
    last=s[0]
    for i in range(1,len(s)):
        if last==s[i]:
            temp+=1
        else:
            #print(last,temp)
            if temp>2:
                ans+=1
            temp=1
            last=s[i]
    if temp>2:ans+=1
    #print(last,temp)
    print(1+("111" in s or "000" in s)+("010" in s or "101" in s))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()