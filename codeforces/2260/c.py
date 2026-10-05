import sys
input=sys.stdin.readline

def solve():
    x,y=map(int,input().split())
    if x&y==0:
        print(x+y,0)
    else:
        temp=x+y
        
        for i in range(temp.bit_length()-1,-1,-1):
            if ((temp>>i)&1)==1 and ((x>>i)&1==0):
                temp&=~(1<<i)
                if temp<=x:
                    break
        
        #print(temp,bin(temp))
        print(x+y,x-temp)
    
    #print('---')

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()