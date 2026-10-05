import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    ss=set()
    for i in range(m):
        x,y=map(int,input().split())
        if i==0:
            ss.add((x,y))
        elif i==1:
            xx,yy=ss.pop()
            ss.add((xx,x))
            ss.add((xx,y))
            ss.add((yy,x))
            ss.add((yy,y))
        else:
            temp=[]
            for v in ss:
                if x not in v and y not in v:
                    temp.append(v)
            for v in temp:ss.remove(v)
        #print(ss)
        
    print(len(ss))
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()