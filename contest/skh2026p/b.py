import sys
input=sys.stdin.readline
for _ in range(int(input())):
    x=[*map(int,input().strip().split('.')[1])]
    for i in range(len(x)-1,-1,-1):
        if i==0:
            print("Yes"if x[i]>=5 else "No")
        else:
            if x[i]>=5:x[i-1]+=1