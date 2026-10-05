def mat_mul(A, B, mod=None):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            if A[i][k] == 0:
                continue
            for j in range(p):
                C[i][j] += A[i][k] * B[k][j]
                if mod:
                    C[i][j] %= mod
    return C

def mat_pow(A, e, mod=None):
    n = len(A)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1:
            R = mat_mul(R, A, mod)
        A = mat_mul(A, A, mod)
        e >>= 1
    return R