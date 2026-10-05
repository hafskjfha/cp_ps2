import sys

def fprint(*v):
    print(*v,flush=1)

def main():
    input=sys.stdin.readline
    n=int(input())
    a,b=1,n if n%2 else n-1
    l1=False
    for _ in range(n//2+1):
        fprint(f"? {a} {b}")
        r=int(input())
        if l1:
            if r:
                fprint("!",a)
            else:
                fprint("!",b+1)
            return
        else:
            if r:
                l1=True
                b-=1
            else:
                a+=1
                b-=1
        if a==b:break
                
        
    fprint("!",n//2+1 if n%2 else n)
    
main()