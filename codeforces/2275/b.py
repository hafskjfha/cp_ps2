import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    
    stack=[]
    res1=[]
    for i in range(n):
        if s[i]=='1':
            stack.append(i+1)
        elif s[i]=='2':
            if stack:
                stack.pop()
                res1.append(i+1)
    
    print(len(stack)+len(res1))
    print(*sorted(stack+res1))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()