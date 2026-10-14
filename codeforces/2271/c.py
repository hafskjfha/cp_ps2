import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    prefixXor=[]
    m=1
    while 2*m<=n:m*=2
    
    for i in range(m):
        prefixXor.append(i) 
    for i in range(2*m-1,m-1,-1):
        prefixXor.append(i)
    
    for i in range(len(prefixXor)):
        prefixXor.append(prefixXor[i])
        
    #print(prefixXor)
    ans=[prefixXor[i]^prefixXor[i-1] for i in range(1,len(prefixXor))]
    print(len(ans))
    print(*ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()