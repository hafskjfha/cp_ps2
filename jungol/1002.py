def gcd(a, b):
    while b > 0:
        a, b = b, a%b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

n = int(input())
ans_gcd, ans_lcm = None, None   
a = map(int, input().split())
for x in a:
    if ans_gcd is None:
        ans_gcd = x
        ans_lcm = x
    else:
        ans_gcd, ans_lcm = gcd(ans_gcd, x), lcm(ans_lcm, x)

print(ans_gcd, ans_lcm)

