import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    a=sorted([*map(int,input().split())])
    
    nextNum=0
    ac,bc=0,0
    turn=True
    
    for x in a:
        if x!=nextNum:
            if ac<k:
                print("NO")
                return
            else:
                if ac!=bc:
                    print("YES")
                    return
            nextNum+=1
            if x!=nextNum:
                print("NO")
                return
            ac=1
            bc=0
        else:
            if turn:
                if ac==k:
                    continue
                ac+=1
            else:
                bc+=1
        turn=not turn
    
        #print(x,ac,bc)
    if ac==k and ac!=bc:
        print("YES")
    else:
        print("NO")
    
    #print("======")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()