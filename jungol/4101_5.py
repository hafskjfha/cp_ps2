import sys

def main():
    input=sys.stdin.readline
    n=int(input())
    s=input().strip()
    
    t0,t1=[],[]
    for i in range(n):
        if i%2==0:
            t0.append(+('0'!=s[i]))
            t1.append(+('1'!=s[i]))
        else:
            t0.append(+('1'!=s[i]))
            t1.append(+('0'!=s[i]))
    
    print(min(len([x for x in "".join(map(str,t0)).split("0")if x]),len([x for x in "".join(map(str,t1)).split("0")if x])))
        
    
main()