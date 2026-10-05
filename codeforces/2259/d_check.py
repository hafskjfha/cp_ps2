import sys

with open(sys.argv[1], "r") as f:
    test_input = f.read()
with open(sys.argv[2], "r") as f:
    code_output = f.read()

inputt=iter(test_input.splitlines()).__next__
inputc=iter(code_output.splitlines()).__next__

def mex(data):
    i=0
    while 1:
        if i not in data:
            return i
        i+=1
        
flgg=False

for _ in range(int(inputt())):
    n=int(inputt())
    a=[*map(int,inputt().split())]
    
    flg=inputc()
    if flg=="NO":
        continue
    else:
        ss=inputc()
        seta,setb,setc=set(),set(),set()
        for j in range(n):
            if ss[j]=='A':
                seta.add(a[j])
            elif ss[j]=='B':
                setb.add(a[j])
            else:
                setc.add(a[j])
    
    mexa,mexb,mexc=mex(seta),mex(setb),mex(setc)
    print(mexa,mexb,mexc,2*max(mexa,mexb,mexc))
    if mexa+mexb+mexc<2*max(mexa,mexb,mexc):
        flgg=True
        print("w")
        
if flgg: exit(1)