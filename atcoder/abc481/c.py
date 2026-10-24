import sys
input=sys.stdin.readline

def solve():
    q=int(input())
    id=1
    mapping=dict()
    for _ in range(q):
        s=input().strip()
        if s not in mapping:
            mapping[s]=id
            id+=1
        print(mapping[s])

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()