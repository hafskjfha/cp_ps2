import sys

def main():
    input=sys.stdin.readline
    for _ in range(int(input())):
        n,m,k=map(int,input().split())
        a=[input().strip()for _ in range(m-1)]
        b=[input().strip()for _ in range(k)]
        r=[]
        for s in b:
            if m==1:
                r.append(s)
            elif n==1:
                if s<a[0]:r.append(s)
            elif n==m:
                if a[-1]<s:r.append(s)
            else:
                if a[n-2]<s<a[n-1]:
                    r.append(s)
        print(len(r))
        print("\n".join(r))
    
main()