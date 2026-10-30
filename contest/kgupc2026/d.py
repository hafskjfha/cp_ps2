import sys
from collections import defaultdict
input=sys.stdin.readline
n=int(input())
count=defaultdict(int)
for _ in range(n):
    m,_,c,a=input().split()
    count[c]+=int(a)

print(m,"Highest Spending:",*max(count.items(),key=lambda x:x[1]))
print(m,"Lowest Spending:",*min(count.items(),key=lambda x:x[1]))