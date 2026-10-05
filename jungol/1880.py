key=input()
for c in input():
    code=ord(c)
    print((key[code-65].upper() if code<97 else key[code-97])if c!=' ' else ' ',end="")