import sys
input=sys.stdin.readline

def solve():
    board=[input().strip()for _ in range(2)]
    a=d=None
    for i in range(2):
        for j in range(2):
            if board[i][j]=='A':
                a=(i,j)
            elif board[i][j]=='D':
                d=(i,j)
    print("Yes"if abs(a[0]-d[0])+abs(a[1]-d[1])!=2 else "No")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()