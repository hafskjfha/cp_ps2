import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    if n%2:return print("NO")

    s=input().strip()
    inx=[[0,0]for _ in range(4)]
    
    for i in range(n):
        if s[i] in "PAUL":
            inx["PAUL".index(s[i])][i%2]=1
    
    
        
    
    
    
main()