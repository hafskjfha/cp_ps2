import sys
input=sys.stdin.readline

FIR="first"
SEC="second"
temp=0

def query(i,s):
    global temp
    print(f"? {s} {i}",flush=True)
    temp+=1
    return int(input())

n=int(input())
vi=set()

check=dict()

a=1
b=2
while b<=2*n:
    x1=query(a,FIR)
    x2=query(b,SEC)
    check.setdefault(x1,set()).add(a)
    check.setdefault(x2,set()).add(b)
    #print(x1,x2)
    
    if x1!=x2 and len(check[x1])==2:
        query(list(check[x1])[0],FIR)
        query(list(check[x1])[1],SEC)
        vi.add(list(check[x1])[0])
        vi.add(list(check[x1])[1])
        
    if x1!=x2 and len(check[x2])==2:
        query(list(check[x2][0]),FIR)
        query(list(check[x2][1]),SEC)
        vi.add(list(check[x2])[0])
        vi.add(list(check[x2])[1])
    
    if x1==x2:
        #print('!',a,b,)
        for i in range(a+1,2*n):
            if i not in vi:
                a=i
    
    b=max(a,b)+1

# for i in range(1,n+1):
#     x=check.get(i,[])
#     if len(x)==2:
#         query(x[0],FIR)
#         query(x[1],SEC)
#     elif len(x)==0:
#         query(2*n-1,FIR)
#         query(2*n,SEC)

print(check)
print("qc",temp)
print("mqc",4*n-2)