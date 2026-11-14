import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    for _ in range(n):
        if input().strip()=="UNICON":
            print("ACCEPTED")
        else:
            print("WRONG ANSWER")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()