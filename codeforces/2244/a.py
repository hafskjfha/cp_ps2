import sys

def main():
    input=sys.stdin.readline
    t=int(input())
    
    for _ in range(t):
        n=int(input())
        s=len(max(input().strip().split('*'),key=len))
        print(s//2+s%2)
        
    
main()