from itertools import permutations

ans=set()
for x in permutations([1,1,1,4],4):
    if x!=(1,1,1,4):ans.add(x)
    
print(len(ans))
