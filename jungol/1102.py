import sys

def main():
    input=sys.stdin.readline
    
    stack=[]
    n=int(input())
    for _ in range(n):
        cmd,*i=input().split()
        if cmd=='i':
            stack.append(i[0])
        elif cmd=='o':
            if stack:
                print(stack.pop())
            else:
                print('empty')
        else:
            print(len(stack))
    
main()