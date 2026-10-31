from itertools import permutations

count=0
for arr in permutations(range(1,6),5):
    if max(arr[1:3])==3:
        print(arr)
        count+=1
import math
print((math.perm(2,1))*math.factorial(3))
print(count)