import sys

with open(sys.argv[1], "r") as f:
    test_input = f.read()
with open(sys.argv[2], "r") as f:
    code_output = f.read()
    
n=int(test_input)
code_output=[*map(int,code_output.split())]

if len(code_output)!=n:
    print('wrong len')
    exit(1)

for i in range(n-1):
    if int(str(code_output[i])+str(code_output[i+1]))%39!=0:
        print(str(code_output[i])+str(code_output[i+1]),"39 배수 이님")
        exit(1)