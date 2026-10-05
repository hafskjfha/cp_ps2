import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip()
    print("AI slop"if "ai" in s else "Human made")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()