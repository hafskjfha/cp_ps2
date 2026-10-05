import sys

def main():
    input=sys.stdin.readline
    t=int(input())
    for _ in range(t):
        s=input().split()
        
        for ss in s:
            print(ss[0],end="")
        print()
    
main()