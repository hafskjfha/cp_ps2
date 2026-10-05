n=int(input())
if n < 0 or n > 50 or n%2==0:
    print('INPUT ERROR!')
    exit(0)
    

for i in range(n):
    for j in range(n-i if n//2+1<=i else i+1):
        print(j+1,end=' ')
    print()