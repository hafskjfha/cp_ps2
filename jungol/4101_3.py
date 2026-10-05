import sys

def main():
    input=sys.stdin.readline
    input()
    scons=input().strip().split('S')
    
    cj=jc=0
    
    for s in scons:
        temp=[]
        for c in s:
            if temp:
                if temp[-1]!=c:temp.append(c)
            else:temp.append(c)
        
        if len(temp)==2:
            if temp==['C','J']:cj+=1
            else:jc+=1
    
    print(cj,jc,sep='\n')
    
main()