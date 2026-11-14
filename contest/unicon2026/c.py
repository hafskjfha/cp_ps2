import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    temp=n-(n//10//2*10*2)
    t2=n//10//2*10
    #print(n//10//2*10,temp)
    count=0
    for i in range(10):
        for j in range(10):
            a,b=t2+i,t2+j
            if a+b==n and a>0 and b>0 and len(str(a))==len(str(b))==len(str(n)):
                count+=1
    print("bass" if count==0 else count)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()