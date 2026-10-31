import sys
input=sys.stdin.readline

def solve():
    board=[input().strip()for _ in range(5)]
    ans=100
    for i in range(5):
        ans=min(ans,board[i].count('.'))
    for i in range(5):
        temp=0
        for j in range(5):
            if board[j][i]=='.':
                temp+=1
        ans=min(temp,ans)
    temp=0
    for i in range(5):
        if board[i][i]=='.':temp+=1
    ans=min(ans,temp)
    temp=0
    for i in range(4,-1,-1):
        if board[i][i]=='.':temp+=1
    print(min(ans,temp))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()