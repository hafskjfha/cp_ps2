import sys

def main():
    input=sys.stdin.readline
    s=input().strip()
    for i in range(len(s)):
        if i in [0,1,4]:
            print(s[i]+'!',end='')
        else:print(s[i],end='')
    if len(s)!=5:print('!')

main()