import sys
input=sys.stdin.readline
n,k=map(int,input().split())
s=input()


count=0
for i in range(n):
    if s[i]=='1':count+=1

#print(count)



print(count)