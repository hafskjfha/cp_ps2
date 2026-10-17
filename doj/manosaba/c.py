import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[]
    for _ in range(n):
        s,x=input().split()
        a.append((s,int(x)))
    
    q=int(input())
    for _ in range(q):
        s=input().strip()
       # print(s)
        ans=-1
        for s2,x in a:
            if len(s)!=len(s2):continue
            flg=True
            count=0
            for c1,c2 in zip(s,s2):
                if c1=='_' or c2=='_':
                    if c1!=c2:
                        flg=False
                        break
                    else:continue
                else:
                    if c1!=c2:count+=1
            if flg and count<=1:
                ans=max(ans,x)
                
        print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()