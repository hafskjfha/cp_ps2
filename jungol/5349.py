s=input().split()
print(*[s[i] for i in range(len(s))if i%2][::-1])