import sys

def main():
    input=sys.stdin.readline
    n=int(input())-1
    a=[0]
    
    for i in range(n):
        if i%2==0:
            a.append(i//2+1)
        else:
            a.append(-(i//2+1))
    
    print(*a)
    
main()