import sys,math

with open(sys.argv[1], "r") as f:
    test_input = iter(f.read().splitlines()).__next__
with open(sys.argv[2], "r") as f:
    code_output = iter(f.read().splitlines()).__next__

for _ in range(int(test_input())):
    n,x=test_input().split()
    n,x=int(n),float(x)
    
    arr=[*map(int,code_output().split())]
    
    if arr[0]==-1:continue
    
    math.trunc(sum(arr)/n*100)/ 100
    
    if len(arr)==n and math.trunc(sum(arr)/n*100)/ 100 == x and all([1<=k<=5 for k in arr]):
        print(_,'ok')
    else:
        print(_,'no')
        print(math.trunc(sum(arr)/n*100)/ 100)
        exit(1)
    
