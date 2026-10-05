import sys
input=sys.stdin.readline

mode=-1

def solve():
    if mode==0:
        n=int(input())
        s=input().strip()
        print(s,s,sep='')
    else:
        n,l=map(int,input().split())
        p=input().strip()
        
        t11,t12=p[:l//2],p[l//2:]
        t21,t22=p[:l//2+1],p[l//2+1:]
        print(t11,t12)
        print(t21,t22)
        
        f1=False
        i,j=0,0
        while j<l//2:
            #print('?',t11[j],t12[i])
            if t11[j]!=t12[i]:
                if f1:
                    break
                else:
                    f1=True
                    j+=1
            else:
                i+=1
                j+=1
        else:
            #print(t11)
            return
        
        #print('----')
        
        f1=False
        i,j=0,0
        while j<l//2:
            #print('?',t21[i],t22[j])
            if t21[i]!=t22[j]:
                if f1:
                    break
                else:
                    f1=True
                    j+=1
            else:
                i+=1
                j+=1
        else:
            print(t22)
        
        #print('??')

def main():
    global mode
    mode=int(input())
    t=int(input())
    for _ in range(t):
        solve()
main()