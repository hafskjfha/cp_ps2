import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    count={"MUPC":0,"MJUPC":0,"MPC":0,"MJPC":0}
    for _ in range(n):
        s=input().strip()
        if s in count:
            count[s]+=1
        else:
            count["MUPC"]+=1
    
    name,v=max(count.items(),key=lambda x:x[1])
    print("REVOTE"if [*count.values()].count(v)>1 else name)
    
    
main()