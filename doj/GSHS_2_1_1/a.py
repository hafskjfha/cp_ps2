import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    print(n//2)
    if n%2:
        print(*[2 for _ in range(n//2-1)],3)
    else:print(*[2 for _ in range(n//2)])
    
main()