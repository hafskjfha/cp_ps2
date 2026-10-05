a,b=map(int,input().split())
for x in [range(a,b+1),range(a,b-1,-1)][a>b]:
    for i in range(1,10):
        print(f"{x} * {i} = {x*i}")
    print()