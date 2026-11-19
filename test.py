from math import floor

k=1
prev=0

#c=set([x**2 for x in range(1,100)])
c=set()

for i in range(1,1000):
    if i%floor(i**0.5)==0:
        print(i)
        c.add(i)

print(sorted(c))

ceil = lambda a, b: (a + b - 1) // b