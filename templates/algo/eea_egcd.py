# ax+by=gcd(a,b)를 만족시키는 gcd(a,b),x,y 반환
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1