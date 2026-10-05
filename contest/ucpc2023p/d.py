import sys

def main():
    input=sys.stdin.readline
    n,m,k=map(int,input().split())
    board=[[*input().strip()]for _ in range(n)]
    
    INF=float('inf')
    ans_count=0
    ans_board=[[None]*k for _ in range(k)]
    
    
    for i in range(k):
        for j in range(k):
            tempmin,tempchar=INF,None
            
            for c in range(26):
                char=chr(65+c)
                count=0
                for x in range(n//k):
                    for y in range(m//k):
                        if board[x*k+i][y*k+j]!=char:
                            count+=1
                
                if count < tempmin:
                    tempmin=count
                    tempchar=char
            
            ans_count+=tempmin
            ans_board[i][j]=tempchar
    
    print(ans_count)
    for i in range(k):
        for j in range(k):
            for x in range(n//k):
                for y in range(m//k):
                    board[x*k+i][y*k+j]=ans_board[i][j]
    
    for xx in board:
        print(*xx,sep='')
    
main()