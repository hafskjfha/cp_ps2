import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    p=[input().strip()for _ in range(n)]
    count=[0]*n
    for _ in range(m):
        s=input().strip()
        flg1,flg2=-1,[]
        for i in range(n):
            x=p[i]
            if s==x:flg1=i
            else:
                if len(s)!=len(x):continue
                temp=True
                for c1,c2 in zip(s,x):
                    if c1!=c2:
                        if temp:temp=False
                        else:
                            break
                else:
                    flg2.append(i)
        
        if flg1!=-1:
            count[flg1]+=1
        else:
            if len(flg2)==1:
                count[flg2[0]]+=1
    print(*count,sep='\n')

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()