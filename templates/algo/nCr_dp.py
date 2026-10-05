# all C(n, r), O(N^2) time / memory
N = 100
C = [[0] * (N + 1) for _ in range(N + 1)]
for n in range(N + 1):
    C[n][0] = C[n][n] = 1
    for r in range(1, n):
        C[n][r] = C[n-1][r-1] + C[n-1][r]

# answer: C[n][r]

######

# 메모리 O(R)
def nCr_dp(n, r, mod=10**9+7):
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    dp = [0] * (r + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, r), 0, -1):
            dp[j] += dp[j - 1]
            if mod is not None:
                dp[j] %= mod
    return dp[r]