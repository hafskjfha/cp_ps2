import sys,string

def main():
    MO="AEIOU"
    JA="BCDFGHJKLMNPQRSTVWXYZ"
    input=sys.stdin.readline
    n,m=map(int,input().split())
    
    if m==1:
        if n>26:return print("NO")
        else:
            print("YES")
            return print(*string.ascii_uppercase[:n],sep='\n')
    
    if n>10:return print("NO")
    
    print("YES")
    for i in range(n):
        r=[]
        for j in range(m):
            if i%2:
                if j%2:
                    r.append(MO[(i//2)%5])
                else:
                    r.append(JA[(i//2)%21])
            else:
                if j%2==0:
                    r.append(MO[(i//2)%5])
                else:
                    r.append(JA[(i//2)%21])
        print("".join(r))
    
    
main()