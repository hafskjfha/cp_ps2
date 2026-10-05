import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    bm,cm,bc=0,0,0
    
    for _ in range(n):
        s=input().strip()
        if s=="good-chinese":
            cm+=1
        elif s=="bad-chinese":
            bm+=1
            cm+=1
            bc+=1
        elif s=="bad-foreigner":
            bm+=1
    
    print("gboaodd"[(bm!=cm and bc!=0)::2]+"-kolorvxl")
    
main()