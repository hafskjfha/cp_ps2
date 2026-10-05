from itertools import combinations
print(len(set(float('inf')if a[0]==b[0]else(b[1]-a[1])/(b[0]-a[0]) for a,b in combinations([[*map(int,i.split())]for i in [*open(0)][1:]],2))))