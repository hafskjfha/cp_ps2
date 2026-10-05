import sys

def main():
    input=sys.stdin.readline
    n,p,q=map(int,input().split())
    a=[*map(int,input().split())]
    
    mina=min(a)
    w=[]
    for x in a:
        w.append(1<<(x-mina))
    w.sort(reverse=1)
    sw=sum(w)
    temp=0
    count=0
    for x in w:
        temp+=x
        count+=1
        if temp*q>=sw*p:break
    
    print(count)
    
main()