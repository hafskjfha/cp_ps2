import sys

def solve(s,check,n,m):
    res=[]
    ccc="ad"
    
    sq=[]
    for i in range(n):
        for j in range(m):
            if s[i][j]=='s':
                sq.append((i,j))
                
    for x,y in sq:
        temp=[(x,y)]
        state=0
        count=0
        flg=False
        
        for i in range(x-1,-1,-1):
            if check[i][y]: break
            
            if s[i][y]==ccc[state]:
                if state==1:
                    temp.append((i+1,y))
                    temp.append((i,y))
                    count+=2
                state=(state+1)%2
            else:break
        
        if count!=0 and count%2==0:
            flg=True
            for a,b in temp:
                check[a][b]=True
            res.append((temp[-1][0]+1,temp[-1][1]+1,temp[0][0]+1,temp[0][1]+1))
                
        
        if not flg:
            temp=[(x,y)]
            state=0
            count=0
            flg=False
            
            for j in range(y-1,-1,-1):
                if check[x][j]: break
                
                if s[x][j]==ccc[state]:
                    if state==1:
                        temp.append((x,j+1))
                        temp.append((x,j))
                        count+=2
                    state=(state+1)%2
                    
                else: break
            #print(state,count)
            if count!=0 and count%2==0:
                for a,b in temp:
                    check[a][b]=True
                res.append((temp[-1][0]+1,temp[-1][1]+1,temp[0][0]+1,temp[0][1]+1))
                    
    for i in range(n):
        for j in range(m):
            if check[i][j]==False:
                # print(res)
                # print(check)
                print("NO")
                break
        else:
            continue
        break
    else:
        print("YES")
        print(len(res))
        for a in res:
            print(*a)

def main():
    input=sys.stdin.readline
    for _ in range(int(input())):
        n,m=map(int,input().split())
        s=[input().strip()for _ in range(n)]
        check=[[False]*m for _ in range(n)]
        
        solve(s,check,n,m)

                
    
main()