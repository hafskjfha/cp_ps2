def main():
    I=open(0).readline
    c=lambda:exit(print(0))
    n=int(I())
    if n*(n+1)//2 % 3:c()
    a=[I().strip()for _ in range(n)]
    e=[[1]*(_+1) for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            if e[i][j]==0:continue
            if i==n-1:c()
            if a[i][j]=='R':
                if e[i+1][j] and e[i+1][j+1] and a[i+1][j]==a[i+1][j+1]=='R':
                    e[i][j]=e[i+1][j]=e[i+1][j+1]=0
                else:
                    c()
            else:
                if j==i or e[i][j]==0 or a[i][j+1]!='B':c()
                if  e[i+1][j+1] and a[i+1][j+1]=='B':
                    e[i][j]=e[i+1][j+1]=e[i][j+1]=0
                else:c()
    print(1)
main()