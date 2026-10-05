import sys

input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    odd,two,four=0,0,0
    
    for x in a:
        if x%2==1:
            odd+=1
        else:
            if x%4==0: four+=1
            else: two+=1
    
    print(max(odd,two,four))
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
    
    
main()