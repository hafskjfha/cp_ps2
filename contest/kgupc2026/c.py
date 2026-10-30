h,m=map(int,input().split(":"))
n=int(input())
arr=[*map(int,input().split())]
m+=60*h
limit=720
for t in arr:
    if m+t>limit:
        break
    m+=t

print(f"{m//60:02d}:{m%60:02d}")