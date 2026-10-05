def check(n,s):
    c=[set()for _ in range(n**2)]
    r=[set()for _ in range(n**2)]
    for i in range(n**2):
        for j in range(n**2):
            k=s[i][j]
            if k in r[j] or k<1 or k>n**2:
                return True
            r[j].add(s[i][j])
            k=s[j][i]
            if k in c[j] or k<1 or k>n**2:
                return True
            c[j].add(s[j][i])
    for a in range(n):
        for b in range(n):
            x,y=a*n,b*n
            p=set()
            for i in range(n):
                for j in range(n):
                    k=s[y+i][x+j]
                    if k in p or k<1 or k>n**2:
                        return True
                    p.add(k)
    return False
    

def main():
    input=open(0).readline
    for t in range(int(input())):
        n=int(input())
        s=[[*map(int,input().split())]for _ in range(n**2)]
        print(f'Case #{t+1}:','YNeos'[check(n,s)::2])

main()