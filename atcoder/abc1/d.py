import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    
    arr=[]
    for i in range(n):
        s,e=input().strip().split('-')
        st=int(s[:2])*60+int(s[2:])
        et=int(e[:2])*60+int(e[2:])
        
        #print(st,et)
        s5=st%5
        e5=et%5
        st-=s5
        et+=5-e5 if e5!=0 else 0
            
            
        #print(st,et,min(5-st%5,st%5),min(5-et%5,et%5))
        
        arr.append((st,et))
    
    arr.sort()
    
    ans=[]
    start,last=-1,-1
    for st,et in arr:
        if last<st:
            if last!=-1:
                ans.append((start,last))
            last=et
            start=st
        else:
            last=max(last,et)
    
    ans.append((start,last))
    
    for s,e in ans:
        #print(s,e)
        print(str(s//60).zfill(2),str(s%60).zfill(2),'-',str(e//60).zfill(2),str(e%60).zfill(2),sep='')
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()