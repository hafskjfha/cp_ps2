import sys
input=sys.stdin.readline

def solve():
    n,t,x,y=map(int,input().split())
    p={"Y":set("RG"),"C":set("GB"),"M":set("RB"),"W":set("RGB")}
    temp=set()
    for _ in range(n):
        i,j,c=input().strip().split()
        if c!='K':
            i,j=int(i),int(j)
            k=max(abs(x-i),abs(y-j))
            #print(k)
            if k<=t:
                if c in p:
                    temp|=p[c]
                else:
                    temp.add(c)
    ans="K"
    if "R" in temp:ans="R"
    if "G" in temp:ans="G"
    if "B" in temp:ans="B"
    if set("RG")==temp:ans="Y"
    if set("GB")==temp:ans="C"
    if set("RB")==temp:ans="M"
    if set("RGB")==temp:ans="W"
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()