import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    flg=None
    
    for i in range(1,n+1,2):
        if n%2==0 and i==n-1:break
        if flg:
            print('?',i,min(i-1,n>>1<<1),flush=True)
            x=int(input())
            if x==0:
                print('!',flg,flush=True)
                return
            else:
                print('!',flg+1,flush=True)
                return
        else:
            print('?',i,min(i+1,n>>1<<1),flush=True)
            x=int(input())
            if x==1:
                flg=i
    
    if n%2==0:
        if flg:
            print('?',flg,n,flush=True)
            x=int(input())
            if x==0:print('!',flg+1,flush=True)
            else:print('!',flg,flush=True)
        else:
            print('?',1,n,flush=True)
            x=int(input())
            if x==0:
                print('!',n-1,flush=True)
            else:
                print('!',n,flush=True)
    else:
        print('!',n,flush=True)
        

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()
