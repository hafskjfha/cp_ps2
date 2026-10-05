import sys

def main():
    input=sys.stdin.readline
    n,k=map(int,input().split())
    s=input().strip()
    b=[0]*n
    for i in range(n):
        b[i] = s[i]=='H'
        
    ans=0
    
    for i in range(n):
        if s[i]=='P':
            flg=True
            for j in range(k,0,-1):
                if i-j<0: continue
                
                if b[i-j]:
                    b[i-j]=0
                    ans+=1
                    flg=False
                    break
            
            if flg:
                for j in range(k):
                    if i+j+1>=n:break
                    
                    if b[i+j+1]:
                        b[i+j+1]=0
                        ans+=1
                        break
                    
    print(ans)
    
main()

# k
# i-k i+1