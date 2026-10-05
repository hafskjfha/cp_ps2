import sys

def main():
    a,b=open(0).read().split()
    
    af,bf=False,False
    for i in range(len(a)):
        if a[i] in "aeiou":af=True
        else:
            if af:break
    
    for j in range(len(b)):
        if b[j] in "aeiou":bf=True
        else:
            if bf:break

    if not af or not bf or a[i] in "aeiou" or b[j] in "aeiou":
        return print('no such exercise')

    print(a[:i]+b[:j])

main()