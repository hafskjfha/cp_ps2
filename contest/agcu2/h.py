import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    s=input().strip()
    r=[s[0]]
    prv=s[0]
    for i in range(1,n):
        if prv=='G' and s[i]=='G':continue
        if prv=='S' and s[i]=='S':continue
        r.append(s[i])
        prv=s[i]
    
    j=-1
    for i in range(len(r)):
        if r[i]=='G':
            j=i
    
    print(j+1)
    
main()