import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    s1=input().strip()
    s2=input().strip()
    count=[0]*27
    for c in s1:
        count[ord(c)-ord('a')]+=1
    for c in s2:
        count[ord(c)-ord('a')]-=1
    
    for i in range(27):
        if i in [18,8,23]:
            if count[i]!=1:
                return print("NO")
        else:
            if count[i]!=0:
                return print("NO")
    print("YES")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()