def main():
    for a,s,b in map(str.split,[*open(0)][:-1]):
        print(convert(int(s,int(a)),int(b)))
        
def convert(n,b):
    if n==0:return 0
    
    NUMS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res=[]
    
    while n>0:
        res.append(NUMS[n%b])
        n=n//b
    
    return "".join(res[::-1])
main()