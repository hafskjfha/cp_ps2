input()
a=set(input().split())
print(" ".join(x for x in input().split() if x not in a)or -1)