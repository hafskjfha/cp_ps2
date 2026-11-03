import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    print(2**n.bit_length()-1)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()