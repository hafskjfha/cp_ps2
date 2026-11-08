import sys
input=sys.stdin.readline

def solve():
    a,b,c=map(int,input().split())
    ans=[]
    for x in range(91):
        if b==90-abs(x-a):
            #print(x)
            for y in range(-90,91):
                if c==90-abs(x-y):
                    ans.append(y)
    
    print(" ".join(map(str,sorted(set(ans))))or-1)
            

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()