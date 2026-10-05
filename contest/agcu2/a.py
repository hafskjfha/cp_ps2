import sys

def main():
    input=sys.stdin.readline
    s=set(input().strip())
    c={'A':1,'G':2,'C':4,'U':8}
    print(sum(c[cc] for cc in s))
    
main()