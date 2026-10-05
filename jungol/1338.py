n=int(input())
nx=0
for i in range(n):
    vv=[chr(65+(nx+sum(range(n-1,n-1-j,-1)))%26)for j in range(i+1)]
    print(' '*(2*(n-i-1))+' '.join(vv))
    nx=(nx+1)%26