n=int(input())
a=sorted(map(int,input().split()),reverse=1)

print(sum(a[i]-a[i-1]for i in range(0,n,2)))