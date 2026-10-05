import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    r={'^':'v','v':'^','9':'6','6':'9','(':')',')':'(','u':'n','n':'u'}
    s=input().strip()
    c1=s.count("^9(u")
    c2="".join([r[c]for c in s][::-1]).count("^9(u")
    #print("".join([r[c]for c in s][::-1]),c1,c2)
    if c1==c2:
        print("SAME")
    else:
        print("YNEOS"[c1>c2::2])
    
main()