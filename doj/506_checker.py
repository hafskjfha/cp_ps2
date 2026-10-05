from math import *




def check(arr):
    n=len(arr)
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            a,b=arr[i],arr[j]
            if (a+b)%gcd(a,b)==0 and abs(a-b)%gcd(a,b)==0:
                pass
            else:
                print("no")
                exit(1)
                
    if sum(arr)>=n*(n+1)//2:
        print("ok")
    else:
        print("no")
        exit(1)

def main():
    arr=[1]
    for i in range(100_000-1):
        arr.append(i*2+2)
        print(i,check(arr))
        
main()