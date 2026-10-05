import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    even=odd=0
    
    for x in map(int,input().split()):
        if x&1:odd+=1
        else:even+=1
    
    if even>=odd: print("hambak")
    else:
        if (odd-even)&1==1:print("myongjin")
        else:print("hambak")
    
main()